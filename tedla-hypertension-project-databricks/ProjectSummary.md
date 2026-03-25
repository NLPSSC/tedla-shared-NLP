# Project Summary: Tedla Hypertension Project - Databricks

## Project Overview

The Tedla Hypertension Project is a sophisticated clinical Natural Language Processing (NLP) research system designed to extract and analyze hypertension-related medical information from clinical notes. This project implements a scalable, multi-threaded NLP pipeline specifically tailored for processing large volumes of Electronic Health Record (EHR) notes from a cohort of patients, using advanced clinical NLP techniques to identify and extract relevant medical entities and contextual information.

The system addresses the critical challenge of converting unstructured clinical text into structured, analyzable data for hypertension research. It employs medspaCy, a specialized clinical NLP framework built on top of spaCy, to perform targeted entity extraction with clinical context detection (such as negation, family history, and hypothetical statements). The project was originally implemented on Azure Databricks for large-scale processing but has been transcribed to support local database environments including MSSQL, PostgreSQL, and MySQL.

This solution targets medical researchers, clinical informaticists, and data scientists working on hypertension epidemiology studies who need to process vast amounts of clinical documentation efficiently. The system processes patient notes in batches, categorizes them by note types (admissions, discharge summaries, ECG impressions, etc.), and extracts hypertension-related terms with their surrounding context windows for detailed analysis.

**Project Entry Point:** `src/nlp_method/__main__.py`

## Main Goals

1. **Large-Scale Clinical NLP Processing**: Enable parallel, multi-process extraction of hypertension-related medical entities from thousands of clinical notes with configurable worker processes and queue management for optimal throughput.

2. **Clinical Context-Aware Entity Extraction**: Implement sophisticated clinical NLP pipelines using medspaCy to not only identify hypertension-related terms but also understand their clinical context (negation, family history, hypothetical scenarios) to ensure accurate data extraction.

3. **Note Categorization and Classification**: Automatically classify and process clinical notes across eight distinct categories (problem lists, outpatient, inpatient, emergency department, ECG impressions, discharge summaries, communication encounters, and admissions) to enable category-specific analysis.

4. **Flexible Data Infrastructure**: Support multiple data storage backends (originally Databricks, now local databases) with configurable paths for source tables, results storage, and data exports, making the solution adaptable to various research environments.

5. **Performance Monitoring and Metrics**: Track processing performance through detailed metrics collection, including cycle times per worker, batch processing statistics, and comprehensive logging for quality assurance and optimization.

6. **Scalable Batch Processing Architecture**: Implement a robust batch processing system that can handle large cohorts of patients with monotonically increasing batch groups, allowing for resumable processing and efficient resource utilization.

7. **Context Window Extraction**: Extract not just the matched entities but also configurable context windows around each match, preserving the clinical narrative necessary for accurate interpretation and downstream analysis.

## Primary Technologies and Their Applications

### Core NLP and Clinical Processing Technologies

1. **spaCy (3.7.5)**
   - **Primary Use**: Foundation NLP framework providing tokenization, linguistic annotations, and pipeline architecture
   - **Application**: Serves as the base engine for all text processing, loaded with the `en_core_web_sm` English model and extended with clinical components
   - **Key Components**: `src/nlp_method/nlp/method.py`, `src/nlp_method/nlp/spacy_model.py`, `src/nlp_method/nlp/worker.py`

2. **medspaCy (1.3.1) with Extensions**
   - **Primary Use**: Clinical NLP specialized library for medical text processing with context detection
   - **Application**: Implements `medspacy_target_matcher` for entity extraction and `medspacy_context` for clinical context analysis (negation, family history, hypotheticals)
   - **Key Components**: `src/nlp_method/nlp/method.py` (NLPProcessor class), custom TargetRule implementations
   - **Plugins**: medspacy_quickumls (3.2), medspacy_unqlite (0.9.8) for medical concept linking

### Data Processing and Analytics

3. **Pandas (latest from conda-forge)**
   - **Primary Use**: Primary data manipulation framework for note batches and results aggregation
   - **Application**: Manages DataFrames for note batches, search term mappings, and result records throughout the processing pipeline
   - **Key Components**: `src/nlp_method/notes/notes.py`, `src/nlp_method/data/map_search_term_to_note_group.py`

4. **PyArrow (22.0.0)**
   - **Primary Use**: High-performance columnar data format for efficient data I/O and filtering
   - **Application**: Parquet dataset reading/writing for source tables and results, enabling efficient column-based filtering and batch retrieval
   - **Key Components**: `src/nlp_method/notes/notes.py` (dataset operations), result storage and retrieval

5. **PySpark (from conda-forge)**
   - **Primary Use**: Distributed computing framework for Databricks compatibility and large-scale data operations
   - **Application**: Originally used for Databricks implementation, maintained for compatibility with cluster-based processing
   - **Key Components**: Data extract utilities, exfiltration manager

### Database and Storage Technologies

6. **SQLite with Custom File Locking**
   - **Primary Use**: Local results database storage with concurrent write protection
   - **Application**: Stores extracted NLP results in structured tables with multi-process safe writes via custom file locking mechanism
   - **Key Components**: `src/nlp_method/results/data_store.py`, `src/nlp_method/results/FileLock.py`

7. **pyodbc (via dependencies)**
   - **Primary Use**: Database connectivity abstraction supporting multiple SQL database backends
   - **Application**: Enables flexible database connections to MSSQL, PostgreSQL, or MySQL for source data retrieval
   - **Key Components**: Environment configuration (.env), source table access layer

### Development and Infrastructure Tools

8. **Poetry (1.3.2)**
   - **Primary Use**: Python dependency management and packaging
   - **Application**: Manages project dependencies, virtual environments, and package versions with lock files
   - **Key Components**: `requirements.txt`, `pip_constraints.txt`, poetry-related dependencies

9. **Loguru (0.7.3)**
   - **Primary Use**: Advanced logging framework with structured logging support
   - **Application**: Comprehensive logging across all modules with rotation, retention, and severity levels
   - **Key Components**: `src/common/logr.py`, `src/common/instance_logr_mixin.py`

10. **Databricks Asset Bundles**
    - **Primary Use**: Databricks workspace synchronization and deployment
    - **Application**: Manages workspace configuration, paths, and sync settings for Azure Databricks deployment
    - **Key Components**: `databricks.yml`

### Supporting NLP and Text Processing Libraries

11. **NLTK (3.9.2)**
    - **Primary Use**: Additional natural language processing utilities
    - **Application**: Supplementary text processing and linguistic analysis tools
    - **Key Components**: Integrated within NLP method processing pipeline

12. **PyRuSH (1.0.12) and pysbd (0.3.4)**
    - **Primary Use**: Sentence segmentation and boundary detection
    - **Application**: Clinical text sentence splitting with rule-based sentence boundary detection
    - **Key Components**: Text preprocessing in NLP pipeline

### Testing and Quality Assurance

13. **pytest (9.0.1)**
    - **Primary Use**: Python testing framework
    - **Application**: Unit testing infrastructure for validating NLP processing logic
    - **Key Components**: `src/nlp_method/test_note_iterator.py`

### Data Serialization and Configuration

14. **python-dotenv (1.2.1)**
    - **Primary Use**: Environment variable management from .env files
    - **Application**: Loads configuration for database paths, API keys, worker settings, and file paths
    - **Key Components**: `src/nlp_method/.env`, `src/data_extract/.env`

15. **Invoke (tasks.py integration)**
    - **Primary Use**: Task automation and command execution
    - **Application**: Provides task commands for dependency installation, environment setup, and synchronization
    - **Key Components**: `tasks.py`

## Novel Approaches and Methodologies

### 1. Multi-Process Clinical NLP Pipeline with Queue-Based Load Balancing

The project implements a sophisticated parallel processing architecture specifically designed for clinical NLP at scale. Rather than using simple thread pools, it employs a multi-process architecture with a bounded queue system that balances memory usage with throughput. Each worker process maintains its own spaCy/medspaCy NLP pipeline instance (which are notoriously memory-intensive), preventing memory bloat while achieving true parallelism by bypassing Python's Global Interpreter Lock (GIL).

```python
# From src/nlp_method/__main__.py
def main(num_workers: int, max_queue_size: int, num_test_iterations: int | None = None):
    import multiprocessing as mp
    
    # Create a queue with configurable max size for backpressure
    queue = mp.Queue(maxsize=max_queue_size)
    
    # Create worker processes with individual spaCy model instances
    processes = []
    ready_events = [mp.Event() for _ in range(num_workers)]
    for id in range(num_workers):
        p = mp.Process(target=worker, args=(queue, (id + 1), ready_events[id]))
        p.start()
        processes.append(p)
    
    # Load dataframes into the queue with automatic backpressure
    for notes_df in NotesIterator(num_test_iterations):
        queue.put(notes_df)  # Blocks when queue is full
```

This design elegantly handles backpressure: when workers are slower than the data producer, the queue fills up and automatically throttles the data loading, preventing out-of-memory errors. The recommendation in the configuration comments (`NUM_WORKER_PROCESSES * 2 <= MAX_WORKER_QUEUE_SIZE <= NUM_WORKER_PROCESSES * 3`) shows thoughtful tuning for optimal performance.

### 2. Clinical Context-Aware Entity Extraction with Note Group Mapping

Unlike generic NLP entity extraction, this system implements a sophisticated mapping between clinical search terms and note categories. The `MapSearchTermToNoteGroup` class creates a dynamic relationship between what to search for and where to search for it, enabling context-specific sensitivity and specificity.

```python
# From src/nlp_method/data/map_search_term_to_note_group.py
class MapSearchTermToNoteGroup:
    JOIN_COLS: List[str] = [
        "notes_admissions",
        "notes_communication_encounter",
        "notes_discharge_summary",
        "notes_ecg_impression",
        "notes_emergency_department",
        "notes_inpatient",
        "notes_outpatient",
        "notes_problem_lists",
    ]
```

This approach acknowledges that clinical terms may have different significance in different note types. For instance, a hypertension mention in a problem list carries different weight than one in an ECG impression. The bitmap-based note group relationships enable efficient filtering and category-specific analysis without duplicating data.

### 3. Resumable Batch Processing with PyArrow Dataset Filtering

The project uses PyArrow's dataset API to implement highly efficient resumable batch processing. Rather than loading all notes into memory, it leverages PyArrow's predicate pushdown to filter at the storage layer:

```python
# From src/nlp_method/notes/notes.py
def _get_notes_for_batch_group(self, batch_group_num: int) -> pd.DataFrame:
    # Efficient filtering at the parquet level
    ds_cohort = pds.dataset(COHORT_NOTE_DATA_TABLE, format="parquet")
    table_cohort = ds_cohort.to_table(
        filter=(pc.field("batch_group") == batch_group_num),
    )
```

Combined with batch group tracking in the ResultsDataStore, the system can identify which batches have already been processed and resume from the next unprocessed batch, making it resilient to interruptions and enabling incremental processing of very large cohorts.

### 4. Custom File-Based Locking for Multi-Process Database Writes

To handle concurrent writes from multiple worker processes to a SQLite database (which has limited concurrent write support), the project implements a custom file-based locking mechanism using the `FileLock` class. This is a sophisticated solution that provides mutual exclusion across processes without requiring external locking services:

```python
# From src/nlp_method/results/FileLock.py (conceptual structure)
class FileLock:
    # Implements file-system based locking for cross-process synchronization
    # Ensures only one worker writes to SQLite at a time
```

This approach is particularly clever because it uses the file system's atomic operations to coordinate access, making it portable across different operating systems while avoiding the complexity of multiprocessing locks or external lock servers.

### 5. Context Window Extraction for Clinical Narrative Preservation

The system doesn't just extract matched entities; it preserves clinical context by extracting configurable token windows around each match. This is crucial for clinical NLP because isolated terms often lack diagnostic value without surrounding context:

```python
# From src/nlp_method/notes/note_batch_processor.py
def _get_window_end_char_offset(ent, doc):
    return doc[min(len(doc), ent.end + 1 + WINDOW_SIZE) - 1].idx

def _get_window_start_char_offset(ent, doc):
    return doc[max(0, ent.start - WINDOW_size)].idx
```

The use of character offsets rather than just token positions allows for precise text extraction while the configurable `WINDOW_SIZE` parameter enables researchers to balance between context richness and data volume based on their specific analytical needs.

### 6. Performance Metrics Collection Per Worker

Each worker process maintains its own metrics file, tracking cycle times for each batch processed. This distributed metrics collection approach avoids the overhead of centralized metrics aggregation while providing detailed performance insights:

```python
# From src/nlp_method/nlp/worker.py
class MetricsTracking:
    def __init__(self, file_name: str):
        self._metrics_file: Path = metrics_path / f"{file_name}.csv"
        
    @contextmanager
    def start_cycle_clock(self, number_notes: int):
        self._start_time = time()
        yield
        total_time = time() - self._start_time
        self._fh.write(f"{number_notes},{total_time}\n")
```

This enables post-hoc analysis of processing rates, identification of bottlenecks, and optimization opportunities without adding runtime overhead for metrics aggregation.

### 7. Flexible Database Backend Abstraction

The project implements a clean abstraction layer that supports migration from Databricks to local database systems while maintaining the same processing logic. The use of environment variables for all database connections and table paths makes the system highly configurable:

```python
# Environment-driven configuration supports multiple backends
# MSSQL, PostgreSQL, MySQL, or file-based storage
PYODBC_CONN = os.getenv("PYODBC_CONN")  # Flexible connection string
NOTE_ID_TO_NOTE_GROUPS_TABLE = os.getenv("NOTE_ID_TO_NOTE_GROUPS_TABLE")  # Path-based
```

This architectural decision demonstrates forward-thinking design, enabling the research to be portable across different institutional environments with varying infrastructure constraints.

### 8. Instance-Level Logging Mixin Pattern

The project employs a mixin pattern for logging that automatically provides logger instances to classes, reducing boilerplate while maintaining clear logging contexts:

```python
# From src/common/instance_logr_mixin.py (conceptual)
class InstanceLogrMixin:
    # Provides self.logger to any class that inherits from it
    # Automatically configures logger with class name context
```

This pattern is used extensively across `NLPProcessor`, `NoteBatchProcessor`, and other core classes, providing consistent, contextual logging without coupling classes to specific logging implementations.

## Code Quality and Complexity Analysis

### Qualitative Assessment

**Strengths:**

1. **Sophisticated Architecture for Scale**: The multi-process architecture with bounded queues demonstrates expert-level understanding of Python's concurrency limitations and clinical NLP's memory requirements. The design effectively addresses the GIL limitation while managing memory-intensive spaCy models.

2. **Comprehensive Documentation**: Functions include detailed docstrings following NumPy/SciPy documentation standards, with complete parameter descriptions, return types, exception documentation, and usage examples. The `NoteBatchProcessor.__call__` method, for instance, includes extensive documentation of behavior, side effects, and potential exceptions.

3. **Production-Ready Error Handling**: The code implements robust validation with clear error messages (e.g., `ValueError` when environment variables are missing), making debugging straightforward. The use of assertions and type hints enhances reliability.

4. **Clean Separation of Concerns**: The project exhibits excellent modular organization with distinct layers: data access (`data_extract`), NLP processing (`nlp_method/nlp`), note management (`nlp_method/notes`), and results handling (`nlp_method/results`). Each module has clear responsibilities.

5. **Environment-Driven Configuration**: Extensive use of environment variables through `.env` files makes the system highly configurable without code changes, supporting multiple deployment environments (local development, Databricks, various database backends).

6. **Performance Awareness**: The implementation shows careful attention to performance through PyArrow's efficient columnar operations, streaming data processing via generators, and batch processing to minimize memory footprint.

7. **Research-Oriented Design**: The system is purpose-built for clinical research with features like resumable processing, comprehensive metrics collection, and flexible categorization schemes that align with clinical research workflows.

8. **Type Hints and Modern Python**: Consistent use of type hints (e.g., `int | None`, `List[str]`, `pd.DataFrame`) improves code clarity and enables static analysis tools to catch errors early.

**Areas of Complexity:**

1. **Multi-Process Coordination**: The interaction between the main process, worker processes, ready events, and the shared queue introduces complexity that requires careful reasoning to understand the full lifecycle and potential race conditions.

2. **Cross-Module Dependencies**: The NLP pipeline depends on multiple data sources (note groups, search term mappings, cohort data) and configuration settings spread across different files, making the initialization sequence non-trivial.

3. **Clinical Domain Knowledge Requirements**: Understanding the code fully requires familiarity with clinical note types, medical terminology, and the clinical context detection capabilities of medspaCy, creating a steeper learning curve for general software engineers.

4. **Database Abstraction Layer**: Supporting multiple database backends (Databricks, MSSQL, PostgreSQL, MySQL, SQLite) through environment configuration adds conditional logic and potential edge cases across different storage systems.

5. **File Path Management**: The system uses absolute paths in environment variables and configuration files, which are environment-specific and require careful setup to run in different environments (as evidenced by `/home/westerd/_/` paths in `.env` files).

**Improvement Opportunities:**

1. **Hardcoded Configuration in Main**: The `__main__.py` file contains hardcoded values (`num_workers=64`, `max_queue_size=128`) that override environment variable settings, which could lead to confusion and should be removed or made conditional for testing.

2. **Path Portability**: The extensive use of absolute paths specific to a development environment (e.g., `/home/westerd/_/research_projects/`) in both code and documentation reduces portability. Consider relative paths or more generic examples.

3. **Test Coverage**: While a pytest infrastructure exists, there's only one visible test file (`test_note_iterator.py`), suggesting limited test coverage for a system of this complexity. More comprehensive testing would improve confidence.

4. **Lock File Dependency Management**: The project uses both `requirements.txt` and `pip_constraints.txt` along with Poetry configuration, creating multiple sources of truth for dependencies. Consolidating to Poetry would simplify dependency management.

5. **Error Recovery and Retry Logic**: While the system has resumable batch processing, there's no visible retry logic for transient failures (network issues, temporary database locks). Adding exponential backoff for retryable operations would improve robustness.

### Quantitative Metrics

**Codebase Statistics:**
- **Total Python Files**: 36 files
- **Total Jupyter Notebooks**: 8 notebooks
- **Total Lines of Python Code**: ~6,038 lines
- **Largest Files**:
  - `src/data_extract/exfiltration_manager.py`: 509 lines
  - `src/nlp_method/notes/notes.py`: 294 lines
  - `src/nlp_method/results/data_store.py`: 243 lines
  - `src/nlp_method/notes/note_batch_processor.py`: 225 lines
  - `src/data_extract/fs/TableDef.py`: 145 lines

**Code Organization:**
- **Number of Modules**: 7 primary modules (data_extract, nlp_method, common, plus submodules)
- **Number of Classes**: Approximately 25-30 classes across the codebase
- **Design Patterns Used**: 
  - Mixin pattern (InstanceLogrMixin)
  - Factory pattern (NLP processor initialization)
  - Iterator pattern (NotesIterator)
  - Worker pattern (multi-process workers)
  - Context manager pattern (MetricsTracking)
- **Configuration Files**: 3 main configuration files (.env files, databricks.yml, pyrightconfig.json)

**Complexity Indicators:**
- **Abstraction Layers**: 4-5 layers (presentation/entry → orchestration → processing → data access → storage)
- **External Dependencies**: 98 package dependencies in requirements.txt
- **Database Backends Supported**: 5 (Databricks/Spark, MSSQL, PostgreSQL, MySQL, SQLite)
- **Note Categories Processed**: 8 distinct clinical note types
- **Parallel Worker Processes**: Configurable, commonly 10-64 workers
- **Integration Points**: 
  - Databricks workspace sync
  - Multiple database systems via pyodbc
  - File system (Parquet, CSV, SQLite)
  - External NLP models (spaCy, medspaCy)

### Developer Expertise Evaluation

**Estimated Level**: **Senior to Expert** (5-8+ years equivalent experience)

**Evidence:**

1. **Advanced Python Concurrency**: Demonstrates mastery of multiprocessing, including proper use of queues, events, and process management. Understanding of GIL implications and when to use processes vs threads indicates deep Python expertise.

2. **Clinical NLP Domain Knowledge**: The implementation shows sophisticated understanding of clinical NLP challenges including the need for context detection (negation, family history), note type categorization, and medical entity linking - expertise that typically requires both NLP and clinical informatics experience.

3. **Performance Engineering**: The choice of PyArrow for efficient I/O, use of generators for memory efficiency, batch processing strategies, and custom file locking all indicate strong systems programming and performance optimization skills.

4. **Research Software Engineering**: The code balances research flexibility (configurable parameters, comprehensive metrics) with production engineering practices (logging, error handling, documentation), a balance typically achieved by experienced research software engineers.

5. **Architecture and Design**: The clean separation of concerns, use of appropriate design patterns (mixins, context managers, iterators), and extensible architecture demonstrate senior-level software design capabilities.

6. **Data Engineering Competence**: Proficiency with multiple data technologies (PySpark, PyArrow, Pandas, multiple SQL databases) and understanding of data formats (Parquet, CSV) indicates strong data engineering background.

7. **Production Mindset**: The inclusion of comprehensive logging, metrics collection, resumable processing, and environment-based configuration shows thinking beyond proof-of-concept toward production-ready research systems.

**Complexity Handling:**

The codebase handles significant complexity across multiple dimensions: clinical NLP challenges, high-volume data processing, multi-process coordination, cross-platform database support, and Databricks integration. The developer demonstrates capability through layered abstractions that isolate complexity within modules while maintaining clean interfaces. For example, the `NotesIterator` hides the complexity of batch management and resumption, presenting a simple iterator interface to consumers. Similarly, the `NLPProcessor` encapsulates the intricacies of medspaCy configuration while exposing a straightforward processing method.

The use of environment-driven configuration throughout shows architectural maturity - enabling the same code to run in development, Databricks, or various institutional environments without modification. The careful documentation and clear error messages suggest an awareness that this code will be maintained and extended by others, demonstrating senior-level professional practices.

**Assessment**: 

This project represents high-quality research software engineering that successfully bridges clinical informatics, natural language processing, and distributed systems. The code quality, architecture, and technical decisions reflect a developer (or team) with substantial experience in both software engineering and the clinical NLP domain. The system is production-grade research software - robust enough for large-scale clinical studies while remaining flexible for research iterations. The attention to performance, comprehensive documentation, and thoughtful error handling elevate this beyond typical academic research code to professional-grade scientific software engineering.

## Keywords

### Clinical NLP & Medical Informatics
- Clinical Natural Language Processing
- Medical Entity Extraction
- Clinical Context Detection
- Negation Detection
- Family History Detection
- Hypothetical Statement Detection
- Electronic Health Records (EHR)
- Clinical Note Processing
- Medical Text Mining
- Hypertension Research
- Clinical Documentation
- Medical Terminology Extraction
- Clinical Informatics
- Biomedical NLP
- Healthcare Analytics

### NLP Technologies & Frameworks
- spaCy
- medspaCy
- Named Entity Recognition (NER)
- Target Matching
- Context Analysis
- Entity Linking
- Medical Concept Linking
- QuickUMLS
- Sentence Segmentation
- Tokenization
- Linguistic Annotations
- NLP Pipeline
- Text Processing
- Rule-Based NLP
- Clinical Language Models

### Note Types & Clinical Categories
- Problem Lists
- Discharge Summaries
- Admission Notes
- ECG Impressions
- Emergency Department Notes
- Inpatient Documentation
- Outpatient Documentation
- Communication Encounters
- Clinical Note Classification
- Note Categorization
- Document Type Classification

### Data Processing & Analytics
- Pandas
- PyArrow
- Parquet Format
- Columnar Storage
- Batch Processing
- Data Pipelines
- ETL (Extract Transform Load)
- Data Streaming
- Large-Scale Data Processing
- DataFrame Operations
- Data Aggregation
- Statistical Analysis

### Distributed Computing & Parallelism
- Multi-Processing
- Parallel Processing
- Worker Processes
- Process Pools
- Queue-Based Processing
- Load Balancing
- Distributed NLP
- Concurrent Processing
- Multiprocessing Queues
- Process Synchronization
- Backpressure Management
- Global Interpreter Lock (GIL)

### Cloud & Database Technologies
- Azure Databricks
- PySpark
- Databricks Asset Bundles
- Workspace Synchronization
- SQLite
- MSSQL (Microsoft SQL Server)
- PostgreSQL
- MySQL
- pyodbc
- Database Abstraction
- Multi-Database Support
- ODBC Connectivity

### Software Engineering Practices
- Type Hints
- Design Patterns
- Mixin Pattern
- Iterator Pattern
- Factory Pattern
- Context Managers
- Modular Architecture
- Separation of Concerns
- Environment-Based Configuration
- Logging and Monitoring
- Error Handling
- Exception Management
- Code Documentation
- Docstring Standards

### Performance & Optimization
- Performance Metrics
- Cycle Time Tracking
- Memory Optimization
- Streaming Processing
- Generator Functions
- Lazy Evaluation
- Efficient I/O
- Predicate Pushdown
- Query Optimization
- Resource Management
- Throughput Optimization

### Research & Scientific Computing
- Cohort Studies
- Patient Data Analysis
- Research Data Processing
- Reproducible Research
- Scientific Workflows
- Research Software Engineering
- Clinical Research
- Epidemiology
- Data Quality Assurance
- Resumable Processing

### Python Ecosystem & Tools
- Poetry
- Dependency Management
- Virtual Environments
- pip
- requirements.txt
- Constraints Files
- pytest
- Unit Testing
- Invoke
- Task Automation
- python-dotenv
- Environment Variables

### Logging & Monitoring
- Loguru
- Structured Logging
- Log Rotation
- Log Retention
- Metrics Collection
- Performance Monitoring
- Worker Metrics
- Diagnostic Logging
- Debug Logging
- Application Monitoring

### Data Structures & Algorithms
- Queue Data Structures
- Bounded Queues
- Event Synchronization
- File-Based Locking
- Mutual Exclusion
- Concurrent Data Access
- Batch Grouping
- Bitmap Indexing
- Hash Maps
- Data Filtering

### Text Analysis & Extraction
- Context Window Extraction
- Character Offset Tracking
- Token Offsets
- Text Span Extraction
- Clinical Narrative Analysis
- Semantic Search
- Search Term Mapping
- Pattern Matching
- Regular Expressions

### Development & Deployment
- Configuration Management
- Environment Files (.env)
- Path Management
- Workspace Management
- Version Control
- Git
- Continuous Integration
- Development Workflows
- Local Development
- Cloud Deployment

### Data Formats & Serialization
- Parquet
- CSV
- JSON
- SQL
- PyArrow Tables
- DataFrames
- Tabular Data
- Columnar Data Formats

---

**Generated**: 2026-01-11  
**Repository**: NLPSSC/tedla-hypertension-project-databricks
