from invoke.tasks import task

REQUIREMENTS_FILE = "/home/westerd/_/research_projects/tedla-hypertension/src/nlp_method/requirements.txt"
CONSTRAINTS_FILE = "/home/westerd/_/research_projects/tedla-hypertension/src/nlp_method/pip_constraints.txt"


def chain_cmds(c, cmds):
    c.run(" && ".join(cmds))


@task
def lsync(c):
    cmds = [
        "ssh lambda-server bash -c 'cd /home/westerd/_/research_projects/tedla-hypertension; git checkout master'",
        'git pull lambda sync && (git add . --all && git diff --cached --quiet || (git commit -m "wip" && git push lambda sync))',
        "ssh lambda-server bash -c 'cd /home/westerd/_/research_projects/tedla-hypertension; git checkout sync'",
    ]
    chain_cmds(c, cmds)


@task
def install(c, package):
    c.run(f"python -m pip install {package}")
    freeze(c)


@task
def freeze(c):
    """Write current pinned dependencies to requirements.txt, but only if git is clean."""
    res = c.run("git status --porcelain", hide=True, warn=True)
    if res.stdout.strip():
        print(
            "There are uncommitted changes in the working tree. "
            "Please commit or stash them before freezing requirements."
        )
        raise SystemExit(1)
    c.run(f"python -m pip freeze > {REQUIREMENTS_FILE}")


@task
def install_packages(c):
    """Install Python dependencies from requirements.txt with constraints."""
    cmds = [
        f"python -m pip install -r {REQUIREMENTS_FILE} -c {CONSTRAINTS_FILE}",
        f"python -m pip freeze > {REQUIREMENTS_FILE}",
    ]
    chain_cmds(c, cmds)


@task
def help(c):
    """Show available tasks."""
    print("Available tasks:")
    print(
        "  install  - Install Python dependencies from requirements.txt with constraints"
    )
    print("  help     - Show this help message")


@task(aliases=["note_row_count"])
def get_note_data_row_count(c):
    import glob
    import polars as pl
    from concurrent.futures import ThreadPoolExecutor

    parquet_files = glob.glob(
        "/var/nfs_share/workspaces/ciphi/westerd/tedla/tedla/note_data_*_parquet/*.parquet"
    )

    def get_row_count(f):
        try:
            import pyarrow.parquet as pq

            return pq.ParquetFile(f).metadata.num_rows
        except Exception as e:
            print(f"Error reading {f}: {e}")
            return 0

    with ThreadPoolExecutor() as executor:
        total_rows = sum(executor.map(get_row_count, parquet_files))

    print(f"Total rows in note data: {total_rows}")


@task
def create_data_dictionary_pdf(c):
    from pathlib import Path

    src: Path = Path(
        "/home/westerd/_/research_projects/tedla-hypertension/data-dictionary.md"
    )
    dest_html: Path = src.parent / "data-dictionary.html"
    dest_pdf: Path = src.parent / "data-dictionary.pdf"
    if dest_pdf.exists():
        dest_pdf.unlink()
    if dest_html.exists():
        dest_html.unlink()
    with open(src, "r") as fh:
        text = fh.read()

    import markdown

    html_output = markdown.markdown(text, extensions=["tables"])
    with open(dest_html, "w") as fh:
        fh.write(html_output)

    from weasyprint import HTML

    HTML(string=html_output).write_pdf(dest_pdf)
