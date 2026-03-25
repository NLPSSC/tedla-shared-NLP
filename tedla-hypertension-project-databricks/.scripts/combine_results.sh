#!/usr/bin/bash

# Trap errors and print a message before exiting
trap 'echo "[combine_results] Error occurred on line $LINENO. Exiting."; exit 1' ERR
set -o errexit



###############################################################################
# Functions
###############################################################################

# initial space
echo "" >&2

function log_success() {
    local section="$(echo "$1" | tr '[:lower:]' '[:upper:]')"
    local message="$2"
    echo -e "\033[0;32m \u2705 \033[1m($section)\033[0m - $message" >&2
}

log_info() {
    local section="$(echo "$1" | tr '[:lower:]' '[:upper:]')"
    local message="$2"
    echo -e "\033[0;34m \u2139\ufe0f \033[1m($section)\033[0m - $message" >&2
}

function log_error() {
    local section="$(echo "$1" | tr '[:lower:]' '[:upper:]')"
    local message="$2"
    echo -e "\033[0;31m \u274C \033[1m($section)\033[0m - $message" >&2
}

function log_warning() {
    local section="$(echo "$1" | tr '[:lower:]' '[:upper:]')"
    local message="$2"
    echo -e "\033[0;33m \u26A0\ufe0f \033[1m($section)\033[0m - $message" >&2
}

function exec_sqlite() {
    if [ -z "$1" ]; then
        echo "Error: No SQL command provided to exec_sqlite function."
        return 1
    fi
    # echo -e "Executing SQL command:\n$1" >&2
    local cmd_result="$(echo "$1" | sqlite3 "${WORKING_ALL_DB_PATH}")"
    echo "$cmd_result"
}

###############################################################################
# Global variables
###############################################################################

RESULTS_PATH=""
ACCEPT_ALL_PROMPTS=false
COMPILE_ONLY=false
ARCHIVE_DBS=false

if [ "$#" -eq 0 ]; then
    log_error "param check" "No arguments provided. Usage: $0 [RESULTS_PATH] [-y]"
    exit 1
fi


for arg in "$@"; do
    case "$arg" in
        -y)
            ACCEPT_ALL_PROMPTS=true
            log_info "param check" "Found switch: -y"
            ;;
        --compile-only|-c)
            COMPILE_ONLY=true
            log_info "param check" "Found switch: --compile-only/-c"
            ;;
        *)
            if [ -z "$RESULTS_PATH" ]; then
                RESULTS_PATH="$arg"
                log_info "param check" "Found RESULTS_PATH: $RESULTS_PATH"
            else
                log_warning "param check" "Unexpected argument: $arg"
            fi
            ;;
    esac
done

echo "ACCEPT_ALL_PROMPTS: $ACCEPT_ALL_PROMPTS"

ALL_DB_NAME=all_results.db
SOURCE_RESULTS_TABLE_NAME=results
PATH_TO_SCRIPT=$(dirname "$(realpath "$0")")
ROOT_DB_PATH="/home/westerd/_/project_data/tedla-hypertension/results/db"
ALL_RESULTS_PATH="${ROOT_DB_PATH}/${ALL_DB_NAME}"
WORKING_DIR="${ROOT_DB_PATH}/working"
WORKING_ALL_DB_PATH="${WORKING_DIR}/${ALL_DB_NAME}"
WORKING_ARCHIVE_PATH="${WORKING_DIR}/results_dbs.7z"

unset ALL_DB_NAME

mkdir -p "$WORKING_DIR"

###############################################################################
# Validate parameters
###############################################################################

if [ -z "$RESULTS_PATH" ]; then
    RESULTS_PATH="."
    log_warning "param check" "No RESULTS_PATH provided.  Using RESULTS_PATH: $RESULTS_PATH"
fi

# Always resolve to absolute path so it remains valid after cd
RESULTS_PATH="$(realpath "$RESULTS_PATH")"
log_info "param check" "Resolved RESULTS_PATH: $RESULTS_PATH"

if [ ! -d "$RESULTS_PATH" ]; then
    log_error "param check" "Error: $RESULTS_PATH is not a directory."
    exit 1
fi

if [ "$PATH_TO_SCRIPT" != "/home/westerd/_/research_projects/tedla-hypertension/.scripts" ]; then
    log_error "param check" "Error: PATH_TO_SCRIPT is not /home/westerd/_/research_projects/tedla-hypertension/.scripts"
fi

###############################################################################
# Work
###############################################################################

cd "$RESULTS_PATH"

###############################################################################
# Step 1: Combine results from all source databases into a single database
###############################################################################

#------------------------------------------------------------------------------
#   Step 1.1: Check to make sure the target db doesn't exist
#------------------------------------------------------------------------------
echo $WORKING_ALL_DB_PATH
if [ -f "${WORKING_ALL_DB_PATH}" ]; then
    if [ "$ACCEPT_ALL_PROMPTS" = true ]; then
        rm -f "${WORKING_ALL_DB_PATH}"
        log_success "combining results" "Removed existing ${WORKING_ALL_DB_PATH} due to -y flag."
    else
        log_warning "combining results" "${WORKING_ALL_DB_PATH} already exists."
        echo -e "\n\033[1;97mDo you want to remove ${WORKING_ALL_DB_PATH} and continue? [y/N]: \033[0m"
        read confirm
        if [[ "$confirm" =~ ^[Yy]$ ]]; then
            rm -f "${WORKING_ALL_DB_PATH}"
            log_success "combining results" "Removed existing ${WORKING_ALL_DB_PATH}."
        else
            log_error "combining results" "Aborted by user. ${WORKING_ALL_DB_PATH} was not removed."
            exit 1
        fi
    fi
fi

#------------------------------------------------------------------------------
#   Step 1.2: Gather the schema for the target schema
#------------------------------------------------------------------------------

# Assuming at least one result db
create_table_cmd="$(sqlite3 "$RESULTS_PATH/results_0.db" ".schema ${SOURCE_RESULTS_TABLE_NAME}")"
# Drop the primary key
create_table_cmd=$(echo "$create_table_cmd" | sed 's/ PRIMARY KEY AUTOINCREMENT//g')
create_table_cmd="drop table if exists ${SOURCE_RESULTS_TABLE_NAME}; $create_table_cmd;"
log_success "combining results" "Gathered schema for '${SOURCE_RESULTS_TABLE_NAME}' from results_0.db and removed primary key constraint."
exec_sqlite "$create_table_cmd" > /dev/null 2>&1 && log_success "combining results" "Created '${WORKING_ALL_DB_PATH}' with table '${SOURCE_RESULTS_TABLE_NAME}'."

#------------------------------------------------------------------------------
#   Step 1.3: Gather the schema for the target schema
#------------------------------------------------------------------------------

log_info "combining results" "Starting integrity check for all source DBs..."
for db in results_*.db; do
    sqlite3 "$db" "PRAGMA journal_mode; PRAGMA integrity_check;" >/dev/null 2>&1 || \
        { log_error "combining results" "Integrity check failed for '$db'. Aborting."; exit 1; }
done
log_success "combining results" "Integrity check complete for all source DBs."

#------------------------------------------------------------------------------
#   Step 1.4: Insert data from each source database
#------------------------------------------------------------------------------

for db in results_*.db; do
    log_success "combining results" "Inserting data from $db into ${WORKING_ALL_DB_PATH}..."
    exec_sqlite "ATTACH DATABASE '$db' AS src; INSERT INTO ${SOURCE_RESULTS_TABLE_NAME} SELECT * FROM src.${SOURCE_RESULTS_TABLE_NAME}; DETACH DATABASE src;"  > /dev/null 2>&1 || exit 1
done
log_success "combining results" "Data insertion complete."

exec_sqlite "PRAGMA integrity_check;" >/dev/null 2>&1 && log_success "combining results" "Integrity check passed for combined database." || { log_error "combining results" "Integrity check failed for combined database. Aborting."; exit 1; }

all_count=$(exec_sqlite "SELECT COUNT(1) FROM ${SOURCE_RESULTS_TABLE_NAME};")
log_success "combining results" "Counted ${all_count} rows in combined database." || { log_error "combining results" "Failed to count rows in combined database. Aborting."; exit 1; }

#------------------------------------------------------------------------------
#   Step 1.5: Insert data from each source database
#------------------------------------------------------------------------------

if [ "$ARCHIVE_DBS" = true ]; then

    log_info "combining results" "Archiving contributor DBs ..."

    rm -rf "${WORKING_ARCHIVE_PATH}" && \
        7z a -t7z -mx=9 -sdel "${WORKING_ARCHIVE_PATH}" "${RESULTS_PATH}/results_*.db" > /dev/null 2>&1 && \
        log_success "combining results" "Archived and removed source DBs: ${RESULTS_PATH}/results_*.db." || \
        { log_error "combining results" "Failed to archive source DBs. Source DBs not removed." ; exit 1; }
else
    log_info "combining results" "Skipping archiving of contributor DBs."
fi

# Optimize combined database
exec_sqlite "VACUUM;"
log_success "combining results" "Ran VACUUM on '${WORKING_ALL_DB_PATH}'."
verify_count=$(exec_sqlite "SELECT COUNT(1) FROM ${SOURCE_RESULTS_TABLE_NAME};")
if [ "$verify_count" -eq "$all_count" ]; then
    log_success "combining results" "Row count verified: $verify_count rows in combined database after VACUUM."
else
    log_error "combining results" "Row count mismatch after VACUUM: expected $all_count, found $verify_count."
    exit 1
fi

if [ "$COMPILE_ONLY" = true ]; then
    log_info "combining results" "COMPILE_ONLY flag is set. Exiting after compilation steps."
    exit 0
fi

#------------------------------------------------------------------------------
#   Step 1.6: Check for duplicates
#------------------------------------------------------------------------------

# Are results unique?

note_batch_index="${SOURCE_RESULTS_TABLE_NAME}__note_id__batch_group__IDX"
exec_sqlite "CREATE INDEX ${note_batch_index} ON ${SOURCE_RESULTS_TABLE_NAME} (batch_group, result_id);"
log_success "combining results" "Created index ${note_batch_index} on note_id."
duplicate_result_ids=$(exec_sqlite "SELECT result_id FROM ${SOURCE_RESULTS_TABLE_NAME} group by batch_group, result_id having count(result_id) > 1;")
echo $duplicate_result_ids
if [ -n "$duplicate_result_ids" ]; then
    log_error "combining results" "Found duplicate result_id values in ${WORKING_ALL_DB_PATH}:"
    log_error "combining results" "$duplicate_result_ids"
else
    log_success "combining results" "No duplicate result_id values found in ${WORKING_ALL_DB_PATH}."
fi
exec_sqlite "DROP INDEX IF EXISTS ${note_batch_index};"

# Are notes unique to batch groups?

note_id_index="${SOURCE_RESULTS_TABLE_NAME}__note_id__batch_group__IDX"
drop_index_cmd="DROP INDEX IF EXISTS ${note_id_index}"
log_info "combining results" "Creating index on note_id and batch_group to check for duplicate note_id values within batch_groups..."
exec_sqlite "${drop_index_cmd}; CREATE INDEX ${note_id_index} ON ${SOURCE_RESULTS_TABLE_NAME} (note_id, batch_group);"
check_duplicate_note_ids_in_batch_groups=$(sqlite3 "${WORKING_ALL_DB_PATH}" "SELECT note_id FROM ${SOURCE_RESULTS_TABLE_NAME} GROUP BY note_id HAVING COUNT(DISTINCT batch_group) > 1;")
if [ -n "$check_duplicate_note_ids_in_batch_groups" ]; then
    log_error "combining results" "Found duplicate note_id values within batch_groups in ${WORKING_ALL_DB_PATH}:"
    log_error "combining results" "$check_duplicate_note_ids_in_batch_groups"
else
    log_success "combining results" "No duplicate note_id values found within batch_groups in ${WORKING_ALL_DB_PATH}."
fi

exec_sqlite "${drop_index_cmd};"

# Were all search terms used?

# Read search terms from .scripts/search_terms.txt into an array
mapfile -t search_term_entries < "${PATH_TO_SCRIPT}/search_terms.txt"
log_success "combining results" "Loaded ${#search_term_entries[@]} search terms from .scripts/search_terms.txt."

log_info "combining results" "Checking that all expected search_term values are present in ${WORKING_ALL_DB_PATH}..."
insert_terms=$(printf "('%s')," "${search_term_entries[@]}")
insert_terms=${insert_terms%,}
search_term_check_table_cmd=$(cat <<SQL
drop table if exists search_term_check;
CREATE TEMP TABLE search_term_check (
    search_term VARCHAR(128)
);
INSERT INTO search_term_check (search_term) VALUES
${insert_terms};
select c.search_term
from search_term_check c 
where c.search_term not in (
    select distinct search_term from ${SOURCE_RESULTS_TABLE_NAME} order by search_term
);
SQL
)
missing_search_terms=$(exec_sqlite "$search_term_check_table_cmd")
if [ -n "$missing_search_terms" ]; then
    # Define a list of 5 contrasting ANSI color codes
    colors=("\033[1;31m" "\033[1;32m" "\033[1;33m" "\033[1;34m" "\033[1;35m")
    missing_search_terms_list=""
    i=0
    while IFS= read -r term; do
        color="${colors[$((i % 5))]}"
        missing_search_terms_list+="${color}'${term}'\033[0m, "
        i=$(( i + 1 ))
    done <<< "$missing_search_terms"
    # Remove trailing comma and space
    missing_search_terms_list="${missing_search_terms_list%, }"
    log_error "combining results" "Error: Found missing search_term values in ${WORKING_ALL_DB_PATH}:\n\n${missing_search_terms_list}"
else
    log_success "combining results" "All expected search_term values are present in ${SOURCE_RESULTS_TABLE_NAME}."
fi

# Validate that all search terms found are present in the window text

log_info "combining results" "Validating that all search_term values found in ${WORKING_ALL_DB_PATH} are present in the window_text entries..."

function check_search_term() {
    local search_term="$1"
    drop_table_cmd="DROP TABLE IF EXISTS ${SOURCE_RESULTS_TABLE_NAME}_fts"
    exec_sqlite "${drop_table_cmd}; CREATE VIRTUAL TABLE ${SOURCE_RESULTS_TABLE_NAME}_fts USING fts5(window_text);" > /dev/null 2>&1
    exec_sqlite "INSERT INTO ${SOURCE_RESULTS_TABLE_NAME}_fts(window_text) \
    SELECT window_text FROM ${SOURCE_RESULTS_TABLE_NAME} \
    where search_term = '$search_term';" > /dev/null 2>&1
    count_total=$(exec_sqlite "SELECT count(1) FROM ${SOURCE_RESULTS_TABLE_NAME}_fts;")
    count_match=$(exec_sqlite "SELECT count(1) FROM ${SOURCE_RESULTS_TABLE_NAME}_fts \
    WHERE window_text MATCH '\"${search_term}\"';")
    exec_sqlite "${drop_table_cmd};" > /dev/null 2>&1
    if [ "$count_total" -ne "$count_match" ]; then
        return 1
    else
        return 0
    fi
}

errored_search_terms=()
for search_term_to_check in "${search_term_entries[@]}"; do
    if ! check_search_term "$search_term_to_check"; then
        errored_search_terms+=("$search_term_to_check")
    fi
done

if [ "${#errored_search_terms[@]}" -ne 0 ]; then
    errored_terms=("${errored_search_terms[@]}")
    colors=("\033[1;31m" "\033[1;32m" "\033[1;33m" "\033[1;34m" "\033[1;35m")
    errored_terms_list=""
    i=0
    for term in "${errored_terms[@]}"; do
        color="${colors[$((i % 5))]}"
        errored_terms_list+="${color}'${term}'\033[0m, "
        i=$((i + 1))
    done
    errored_terms_list="${errored_terms_list%, }"
    log_error "combining results" "The following search_term values were found in ${WORKING_ALL_DB_PATH} but did not match any window_text entries:\n${errored_terms_list}"
else
    log_success "combining results" "All search_term values found in ${WORKING_ALL_DB_PATH} matched at least one window_text entry."
fi

# Check for each search term that for found terms the term exists in the window text



# sqlite3 all_results.db "CREATE INDEX results_search_term_IDX ON results (search_term);"
# echo "[combine_results] Created index on search_term."



# sqlite3 all_results.db "drop index if exists results__search_term_batch_group__IDX;"
# echo "[combine_results] Dropped old index on search_term and batch_group if it existed."



# Step 8: Move combined database to parent directory
# mv all_results.db ../
# parent_dir=$(dirname "$(pwd)")
# echo "[combine_results] Moved ${WORKING_ALL_DB_PATH} to parent directory (${parent_dir})."


