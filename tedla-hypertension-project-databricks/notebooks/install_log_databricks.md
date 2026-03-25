## Installs

python -m pip install "medspacy==1.3.1" "loguru==0.7.3" "threadpoolctl==3.6" "nlp_preprocessor==0.0.1"
python -m pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_sm-0.5.4.tar.gz


## Log from databricks

```plaintext
Collecting medspacy
  Downloading medspacy-1.3.1.tar.gz (244 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/244.6 kB ? eta -:--:--
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸━ 235.5/244.6 kB 12.5 MB/s eta 0:00:01
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 244.6/244.6 kB 6.6 MB/s eta 0:00:00
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Getting requirements to build wheel: started
  Getting requirements to build wheel: finished with status 'done'
  Preparing metadata (pyproject.toml): started
  Preparing metadata (pyproject.toml): finished with status 'done'
Collecting PyRuSH>=1.0.8 (from medspacy)
  Downloading pyrush-1.0.12-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (4.6 kB)
Collecting pysbd==0.3.4 (from medspacy)
  Downloading pysbd-0.3.4-py3-none-any.whl.metadata (6.1 kB)
Collecting jsonschema (from medspacy)
  Downloading jsonschema-4.25.1-py3-none-any.whl.metadata (7.6 kB)
Collecting medspacy-quickumls==3.2 (from medspacy)
  Downloading medspacy_quickumls-3.2.tar.gz (69 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/69.9 kB ? eta -:--:--
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 69.9/69.9 kB 4.2 MB/s eta 0:00:00
  Preparing metadata (setup.py): started
  Preparing metadata (setup.py): finished with status 'done'
Collecting spacy<4.0,>=3.8 (from medspacy)
  Downloading spacy-3.8.11-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (27 kB)
Requirement already satisfied: numpy>=1.8.2 in /databricks/python3/lib/python3.12/site-packages (from medspacy-quickumls==3.2->medspacy) (1.26.4)
Collecting unidecode>=0.4.19 (from medspacy-quickumls==3.2->medspacy)
  Downloading Unidecode-1.4.0-py3-none-any.whl.metadata (13 kB)
Collecting nltk>=3.3 (from medspacy-quickumls==3.2->medspacy)
  Downloading nltk-3.9.2-py3-none-any.whl.metadata (3.2 kB)
Collecting pysimstring (from medspacy-quickumls==3.2->medspacy)
  Downloading pysimstring-1.3.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (931 bytes)
Collecting medspacy_unqlite>=0.8.1 (from medspacy-quickumls==3.2->medspacy)
  Downloading medspacy_unqlite-0.9.8-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (9.3 kB)
Collecting pytest>=6 (from medspacy-quickumls==3.2->medspacy)
  Downloading pytest-9.0.1-py3-none-any.whl.metadata (7.6 kB)
Requirement already satisfied: six in /usr/lib/python3/dist-packages (from medspacy-quickumls==3.2->medspacy) (1.16.0)
Requirement already satisfied: Cython in /databricks/python3/lib/python3.12/site-packages (from PyRuSH>=1.0.8->medspacy) (3.0.11)
Requirement already satisfied: setuptools in /usr/local/lib/python3.12/dist-packages (from PyRuSH>=1.0.8->medspacy) (74.0.0)
Collecting PyFastNER>=1.0.8 (from PyRuSH>=1.0.8->medspacy)
  Downloading PyFastNER-1.0.10-py3-none-any.whl.metadata (15 kB)
Collecting quicksectx>=0.3.5 (from PyRuSH>=1.0.8->medspacy)
  Downloading quicksectx-0.4.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.7 kB)
Collecting loguru (from PyRuSH>=1.0.8->medspacy)
  Downloading loguru-0.7.3-py3-none-any.whl.metadata (22 kB)
Collecting spacy-legacy<3.1.0,>=3.0.11 (from spacy<4.0,>=3.8->medspacy)
  Downloading spacy_legacy-3.0.12-py2.py3-none-any.whl.metadata (2.8 kB)
Collecting spacy-loggers<2.0.0,>=1.0.0 (from spacy<4.0,>=3.8->medspacy)
  Downloading spacy_loggers-1.0.5-py3-none-any.whl.metadata (23 kB)
Collecting murmurhash<1.1.0,>=0.28.0 (from spacy<4.0,>=3.8->medspacy)
  Downloading murmurhash-1.0.15-cp312-cp312-manylinux1_x86_64.manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_5_x86_64.whl.metadata (2.3 kB)
Collecting cymem<2.1.0,>=2.0.2 (from spacy<4.0,>=3.8->medspacy)
  Downloading cymem-2.0.13-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (9.7 kB)
Collecting preshed<3.1.0,>=3.0.2 (from spacy<4.0,>=3.8->medspacy)
  Downloading preshed-3.0.12-cp312-cp312-manylinux1_x86_64.manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_5_x86_64.whl.metadata (2.5 kB)
Collecting thinc<8.4.0,>=8.3.4 (from spacy<4.0,>=3.8->medspacy)
  Downloading thinc-8.3.10-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (15 kB)
Collecting wasabi<1.2.0,>=0.9.1 (from spacy<4.0,>=3.8->medspacy)
  Downloading wasabi-1.1.3-py3-none-any.whl.metadata (28 kB)
Collecting srsly<3.0.0,>=2.4.3 (from spacy<4.0,>=3.8->medspacy)
  Downloading srsly-2.5.2-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (19 kB)
Collecting catalogue<2.1.0,>=2.0.6 (from spacy<4.0,>=3.8->medspacy)
  Downloading catalogue-2.0.10-py3-none-any.whl.metadata (14 kB)
Collecting weasel<0.5.0,>=0.4.2 (from spacy<4.0,>=3.8->medspacy)
  Downloading weasel-0.4.3-py3-none-any.whl.metadata (4.6 kB)
Collecting typer-slim<1.0.0,>=0.3.0 (from spacy<4.0,>=3.8->medspacy)
  Downloading typer_slim-0.20.0-py3-none-any.whl.metadata (16 kB)
Collecting tqdm<5.0.0,>=4.38.0 (from spacy<4.0,>=3.8->medspacy)
  Downloading tqdm-4.67.1-py3-none-any.whl.metadata (57 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/57.7 kB ? eta -:--:--
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 57.7/57.7 kB 4.9 MB/s eta 0:00:00
Requirement already satisfied: requests<3.0.0,>=2.13.0 in /databricks/python3/lib/python3.12/site-packages (from spacy<4.0,>=3.8->medspacy) (2.32.2)
Requirement already satisfied: pydantic!=1.8,!=1.8.1,<3.0.0,>=1.7.4 in /databricks/python3/lib/python3.12/site-packages (from spacy<4.0,>=3.8->medspacy) (2.8.2)
Collecting jinja2 (from spacy<4.0,>=3.8->medspacy)
  Downloading jinja2-3.1.6-py3-none-any.whl.metadata (2.9 kB)
Requirement already satisfied: packaging>=20.0 in /databricks/python3/lib/python3.12/site-packages (from spacy<4.0,>=3.8->medspacy) (24.1)
Collecting attrs>=22.2.0 (from jsonschema->medspacy)
  Downloading attrs-25.4.0-py3-none-any.whl.metadata (10 kB)
Collecting jsonschema-specifications>=2023.03.6 (from jsonschema->medspacy)
  Downloading jsonschema_specifications-2025.9.1-py3-none-any.whl.metadata (2.9 kB)
Collecting referencing>=0.28.4 (from jsonschema->medspacy)
  Downloading referencing-0.37.0-py3-none-any.whl.metadata (2.8 kB)
Collecting rpds-py>=0.7.1 (from jsonschema->medspacy)
  Downloading rpds_py-0.29.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.1 kB)
Requirement already satisfied: click in /databricks/python3/lib/python3.12/site-packages (from nltk>=3.3->medspacy-quickumls==3.2->medspacy) (8.1.7)
Requirement already satisfied: joblib in /databricks/python3/lib/python3.12/site-packages (from nltk>=3.3->medspacy-quickumls==3.2->medspacy) (1.4.2)
Collecting regex>=2021.8.3 (from nltk>=3.3->medspacy-quickumls==3.2->medspacy)
  Downloading regex-2025.11.3-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (40 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/40.5 kB ? eta -:--:--
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 40.5/40.5 kB 2.9 MB/s eta 0:00:00
Requirement already satisfied: annotated-types>=0.4.0 in /databricks/python3/lib/python3.12/site-packages (from pydantic!=1.8,!=1.8.1,<3.0.0,>=1.7.4->spacy<4.0,>=3.8->medspacy) (0.7.0)
Requirement already satisfied: pydantic-core==2.20.1 in /databricks/python3/lib/python3.12/site-packages (from pydantic!=1.8,!=1.8.1,<3.0.0,>=1.7.4->spacy<4.0,>=3.8->medspacy) (2.20.1)
Requirement already satisfied: typing-extensions>=4.6.1 in /databricks/python3/lib/python3.12/site-packages (from pydantic!=1.8,!=1.8.1,<3.0.0,>=1.7.4->spacy<4.0,>=3.8->medspacy) (4.11.0)
Collecting iniconfig>=1.0.1 (from pytest>=6->medspacy-quickumls==3.2->medspacy)
  Downloading iniconfig-2.3.0-py3-none-any.whl.metadata (2.5 kB)
Collecting pluggy<2,>=1.5 (from pytest>=6->medspacy-quickumls==3.2->medspacy)
  Downloading pluggy-1.6.0-py3-none-any.whl.metadata (4.8 kB)
Requirement already satisfied: pygments>=2.7.2 in /databricks/python3/lib/python3.12/site-packages (from pytest>=6->medspacy-quickumls==3.2->medspacy) (2.15.1)
Requirement already satisfied: charset-normalizer<4,>=2 in /databricks/python3/lib/python3.12/site-packages (from requests<3.0.0,>=2.13.0->spacy<4.0,>=3.8->medspacy) (2.0.4)
Requirement already satisfied: idna<4,>=2.5 in /databricks/python3/lib/python3.12/site-packages (from requests<3.0.0,>=2.13.0->spacy<4.0,>=3.8->medspacy) (3.7)
Requirement already satisfied: urllib3<3,>=1.21.1 in /databricks/python3/lib/python3.12/site-packages (from requests<3.0.0,>=2.13.0->spacy<4.0,>=3.8->medspacy) (1.26.16)
Requirement already satisfied: certifi>=2017.4.17 in /databricks/python3/lib/python3.12/site-packages (from requests<3.0.0,>=2.13.0->spacy<4.0,>=3.8->medspacy) (2024.6.2)
Collecting blis<1.4.0,>=1.3.0 (from thinc<8.4.0,>=8.3.4->spacy<4.0,>=3.8->medspacy)
  Downloading blis-1.3.3-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (7.5 kB)
Collecting confection<1.0.0,>=0.0.1 (from thinc<8.4.0,>=8.3.4->spacy<4.0,>=3.8->medspacy)
  Downloading confection-0.1.5-py3-none-any.whl.metadata (19 kB)
Collecting cloudpathlib<1.0.0,>=0.7.0 (from weasel<0.5.0,>=0.4.2->spacy<4.0,>=3.8->medspacy)
  Downloading cloudpathlib-0.23.0-py3-none-any.whl.metadata (16 kB)
Collecting smart-open<8.0.0,>=5.2.1 (from weasel<0.5.0,>=0.4.2->spacy<4.0,>=3.8->medspacy)
  Downloading smart_open-7.5.0-py3-none-any.whl.metadata (24 kB)
Collecting MarkupSafe>=2.0 (from jinja2->spacy<4.0,>=3.8->medspacy)
  Downloading markupsafe-3.0.3-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.7 kB)
Requirement already satisfied: wrapt in /databricks/python3/lib/python3.12/site-packages (from smart-open<8.0.0,>=5.2.1->weasel<0.5.0,>=0.4.2->spacy<4.0,>=3.8->medspacy) (1.14.1)
Downloading pysbd-0.3.4-py3-none-any.whl (71 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/71.1 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 71.1/71.1 kB 6.4 MB/s eta 0:00:00
Downloading pyrush-1.0.12-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (547 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/547.9 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 547.9/547.9 kB 20.7 MB/s eta 0:00:00
Downloading spacy-3.8.11-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (33.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/33.2 MB ? eta -:--:--
   ━━╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.3/33.2 MB 67.8 MB/s eta 0:00:01
   ━━━━━━━╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.6/33.2 MB 96.4 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━ 13.4/33.2 MB 169.5 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━╸━━━━━━━━━━━━━━━ 20.7/33.2 MB 203.4 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╺━━━━━━━ 26.8/33.2 MB 191.0 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╺━━━━ 29.3/33.2 MB 131.3 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 33.2/33.2 MB 125.4 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 33.2/33.2 MB 125.4 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 33.2/33.2 MB 125.4 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 33.2/33.2 MB 125.4 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 33.2/33.2 MB 125.4 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 33.2/33.2 MB 125.4 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 33.2/33.2 MB 125.4 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 33.2/33.2 MB 125.4 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 33.2/33.2 MB 125.4 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 33.2/33.2 MB 125.4 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 33.2/33.2 MB 23.5 MB/s eta 0:00:00
Downloading jsonschema-4.25.1-py3-none-any.whl (90 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/90.0 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 90.0/90.0 kB 8.0 MB/s eta 0:00:00
Downloading attrs-25.4.0-py3-none-any.whl (67 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/67.6 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 67.6/67.6 kB 5.9 MB/s eta 0:00:00
Downloading catalogue-2.0.10-py3-none-any.whl (17 kB)
Downloading cymem-2.0.13-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (260 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/260.8 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 260.8/260.8 kB 20.1 MB/s eta 0:00:00
Downloading jsonschema_specifications-2025.9.1-py3-none-any.whl (18 kB)
Downloading medspacy_unqlite-0.9.8-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (408 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/408.5 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 408.5/408.5 kB 30.5 MB/s eta 0:00:00
Downloading murmurhash-1.0.15-cp312-cp312-manylinux1_x86_64.manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_5_x86_64.whl (134 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/134.1 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 134.1/134.1 kB 8.4 MB/s eta 0:00:00
Downloading nltk-3.9.2-py3-none-any.whl (1.5 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/1.5 MB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.5/1.5 MB 63.5 MB/s eta 0:00:00
Downloading preshed-3.0.12-cp312-cp312-manylinux1_x86_64.manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_5_x86_64.whl (874 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/875.0 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 875.0/875.0 kB 33.4 MB/s eta 0:00:00
Downloading PyFastNER-1.0.10-py3-none-any.whl (22 kB)
Downloading pytest-9.0.1-py3-none-any.whl (373 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/373.7 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 373.7/373.7 kB 29.0 MB/s eta 0:00:00
Downloading quicksectx-0.4.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/1.1 MB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.1/1.1 MB 44.1 MB/s eta 0:00:00
Downloading referencing-0.37.0-py3-none-any.whl (26 kB)
Downloading rpds_py-0.29.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (395 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/395.3 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 395.3/395.3 kB 29.0 MB/s eta 0:00:00
Downloading spacy_legacy-3.0.12-py2.py3-none-any.whl (29 kB)
Downloading spacy_loggers-1.0.5-py3-none-any.whl (22 kB)
Downloading srsly-2.5.2-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (1.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/1.2 MB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 51.1 MB/s eta 0:00:00
Downloading thinc-8.3.10-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (3.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/3.9 MB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 3.9/3.9 MB 176.7 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.9/3.9 MB 92.2 MB/s eta 0:00:00
Downloading tqdm-4.67.1-py3-none-any.whl (78 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/78.5 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 78.5/78.5 kB 6.8 MB/s eta 0:00:00
Downloading typer_slim-0.20.0-py3-none-any.whl (47 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/47.1 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 47.1/47.1 kB 4.1 MB/s eta 0:00:00
Downloading Unidecode-1.4.0-py3-none-any.whl (235 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/235.8 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 235.8/235.8 kB 17.7 MB/s eta 0:00:00
Downloading wasabi-1.1.3-py3-none-any.whl (27 kB)
Downloading weasel-0.4.3-py3-none-any.whl (50 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/50.8 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 50.8/50.8 kB 4.2 MB/s eta 0:00:00
Downloading jinja2-3.1.6-py3-none-any.whl (134 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/134.9 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 134.9/134.9 kB 7.5 MB/s eta 0:00:00
Downloading loguru-0.7.3-py3-none-any.whl (61 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/61.6 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 61.6/61.6 kB 5.1 MB/s eta 0:00:00
Downloading pysimstring-1.3.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.5 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/1.5 MB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.5/1.5 MB 51.1 MB/s eta 0:00:00
Downloading blis-1.3.3-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (11.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/11.4 MB ? eta -:--:--
   ━━━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━ 4.1/11.4 MB 123.0 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸━━━━━━━━━━━ 8.1/11.4 MB 120.6 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 11.4/11.4 MB 109.6 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 11.4/11.4 MB 109.6 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 11.4/11.4 MB 109.6 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 11.4/11.4 MB 109.6 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 11.4/11.4 MB 48.7 MB/s eta 0:00:00
Downloading cloudpathlib-0.23.0-py3-none-any.whl (62 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/62.8 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 62.8/62.8 kB 4.9 MB/s eta 0:00:00
Downloading confection-0.1.5-py3-none-any.whl (35 kB)
Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)
Downloading markupsafe-3.0.3-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (22 kB)
Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)
Downloading regex-2025.11.3-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (803 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/803.5 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 803.5/803.5 kB 52.1 MB/s eta 0:00:00
Downloading smart_open-7.5.0-py3-none-any.whl (63 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/63.9 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 63.9/63.9 kB 3.7 MB/s eta 0:00:00
Building wheels for collected packages: medspacy, medspacy-quickumls
  Building wheel for medspacy (pyproject.toml): started
  Building wheel for medspacy (pyproject.toml): finished with status 'done'
  Created wheel for medspacy: filename=medspacy-1.3.1-py3-none-any.whl size=313647 sha256=3dff60c935a441b80dc4375ba4bf84834eabebc04f6302e3484bd0373a11bcc6
  Stored in directory: /home/spark-8e5edb0d-ecd9-4242-bd9c-97/.cache/pip/wheels/54/ad/fd/49994aa138989a814164fed5afc6d8c7c3f1329d0aa0f327da
  Building wheel for medspacy-quickumls (setup.py): started
  Building wheel for medspacy-quickumls (setup.py): finished with status 'done'
  Created wheel for medspacy-quickumls: filename=medspacy_quickumls-3.2-py3-none-any.whl size=98385 sha256=e981313fe682c41e1115984dc62d2ab39af624b6ff10c15757e912ea5b73ad13
  Stored in directory: /home/spark-8e5edb0d-ecd9-4242-bd9c-97/.cache/pip/wheels/5b/b8/96/ba72adae50099aa20ee8b11952fff415c8b82d86ca44528c92
Successfully built medspacy medspacy-quickumls
Installing collected packages: pysimstring, medspacy_unqlite, wasabi, unidecode, typer-slim, tqdm, spacy-loggers, spacy-legacy, smart-open, rpds-py, regex, quicksectx, pysbd, pluggy, murmurhash, MarkupSafe, loguru, iniconfig, cymem, cloudpathlib, catalogue, blis, attrs, srsly, referencing, pytest, PyFastNER, preshed, nltk, jinja2, jsonschema-specifications, confection, weasel, thinc, jsonschema, spacy, PyRuSH, medspacy-quickumls, medspacy
  Attempting uninstall: pluggy
    Found existing installation: pluggy 1.0.0
    Not uninstalling pluggy at /databricks/python3/lib/python3.12/site-packages, outside environment /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858
    Can't uninstall 'pluggy'. No files were found to uninstall.
Successfully installed MarkupSafe-3.0.3 PyFastNER-1.0.10 PyRuSH-1.0.12 attrs-25.4.0 blis-1.3.3 catalogue-2.0.10 cloudpathlib-0.23.0 confection-0.1.5 cymem-2.0.13 iniconfig-2.3.0 jinja2-3.1.6 jsonschema-4.25.1 jsonschema-specifications-2025.9.1 loguru-0.7.3 medspacy-1.3.1 medspacy-quickumls-3.2 medspacy_unqlite-0.9.8 murmurhash-1.0.15 nltk-3.9.2 pluggy-1.6.0 preshed-3.0.12 pysbd-0.3.4 pysimstring-1.3.0 pytest-9.0.1 quicksectx-0.4.1 referencing-0.37.0 regex-2025.11.3 rpds-py-0.29.0 smart-open-7.5.0 spacy-3.8.11 spacy-legacy-3.0.12 spacy-loggers-1.0.5 srsly-2.5.2 thinc-8.3.10 tqdm-4.67.1 typer-slim-0.20.0 unidecode-1.4.0 wasabi-1.1.3 weasel-0.4.3
Note: you may need to restart the kernel using %restart_python or dbutils.library.restartPython() to use updated packages.
Requirement already satisfied: loguru in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (0.7.3)
Note: you may need to restart the kernel using %restart_python or dbutils.library.restartPython() to use updated packages.
Requirement already satisfied: threadpoolctl in /databricks/python3/lib/python3.12/site-packages (2.2.0)
Collecting threadpoolctl
  Downloading threadpoolctl-3.6.

*** WARNING: max output size exceeded, skipping output. ***

ed: murmurhash<1.1.0,>=0.28.0 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy>=2.2.2->nlp_preprocessor) (1.0.15)
Requirement already satisfied: cymem<2.1.0,>=2.0.2 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy>=2.2.2->nlp_preprocessor) (2.0.13)
Requirement already satisfied: preshed<3.1.0,>=3.0.2 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy>=2.2.2->nlp_preprocessor) (3.0.12)
Requirement already satisfied: thinc<8.4.0,>=8.3.4 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy>=2.2.2->nlp_preprocessor) (8.3.10)
Requirement already satisfied: wasabi<1.2.0,>=0.9.1 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy>=2.2.2->nlp_preprocessor) (1.1.3)
Requirement already satisfied: srsly<3.0.0,>=2.4.3 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy>=2.2.2->nlp_preprocessor) (2.5.2)
Requirement already satisfied: catalogue<2.1.0,>=2.0.6 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy>=2.2.2->nlp_preprocessor) (2.0.10)
Requirement already satisfied: weasel<0.5.0,>=0.4.2 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy>=2.2.2->nlp_preprocessor) (0.4.3)
Requirement already satisfied: typer-slim<1.0.0,>=0.3.0 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy>=2.2.2->nlp_preprocessor) (0.20.0)
Requirement already satisfied: tqdm<5.0.0,>=4.38.0 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy>=2.2.2->nlp_preprocessor) (4.67.1)
Requirement already satisfied: numpy>=1.19.0 in /databricks/python3/lib/python3.12/site-packages (from spacy>=2.2.2->nlp_preprocessor) (1.26.4)
Requirement already satisfied: requests<3.0.0,>=2.13.0 in /databricks/python3/lib/python3.12/site-packages (from spacy>=2.2.2->nlp_preprocessor) (2.32.2)
Requirement already satisfied: pydantic!=1.8,!=1.8.1,<3.0.0,>=1.7.4 in /databricks/python3/lib/python3.12/site-packages (from spacy>=2.2.2->nlp_preprocessor) (2.8.2)
Requirement already satisfied: jinja2 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy>=2.2.2->nlp_preprocessor) (3.1.6)
Requirement already satisfied: setuptools in /usr/local/lib/python3.12/dist-packages (from spacy>=2.2.2->nlp_preprocessor) (74.0.0)
Requirement already satisfied: packaging>=20.0 in /databricks/python3/lib/python3.12/site-packages (from spacy>=2.2.2->nlp_preprocessor) (24.1)
Requirement already satisfied: annotated-types>=0.4.0 in /databricks/python3/lib/python3.12/site-packages (from pydantic!=1.8,!=1.8.1,<3.0.0,>=1.7.4->spacy>=2.2.2->nlp_preprocessor) (0.7.0)
Requirement already satisfied: pydantic-core==2.20.1 in /databricks/python3/lib/python3.12/site-packages (from pydantic!=1.8,!=1.8.1,<3.0.0,>=1.7.4->spacy>=2.2.2->nlp_preprocessor) (2.20.1)
Requirement already satisfied: typing-extensions>=4.6.1 in /databricks/python3/lib/python3.12/site-packages (from pydantic!=1.8,!=1.8.1,<3.0.0,>=1.7.4->spacy>=2.2.2->nlp_preprocessor) (4.11.0)
Requirement already satisfied: charset-normalizer<4,>=2 in /databricks/python3/lib/python3.12/site-packages (from requests<3.0.0,>=2.13.0->spacy>=2.2.2->nlp_preprocessor) (2.0.4)
Requirement already satisfied: idna<4,>=2.5 in /databricks/python3/lib/python3.12/site-packages (from requests<3.0.0,>=2.13.0->spacy>=2.2.2->nlp_preprocessor) (3.7)
Requirement already satisfied: urllib3<3,>=1.21.1 in /databricks/python3/lib/python3.12/site-packages (from requests<3.0.0,>=2.13.0->spacy>=2.2.2->nlp_preprocessor) (1.26.16)
Requirement already satisfied: certifi>=2017.4.17 in /databricks/python3/lib/python3.12/site-packages (from requests<3.0.0,>=2.13.0->spacy>=2.2.2->nlp_preprocessor) (2024.6.2)
Requirement already satisfied: blis<1.4.0,>=1.3.0 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from thinc<8.4.0,>=8.3.4->spacy>=2.2.2->nlp_preprocessor) (1.3.3)
Requirement already satisfied: confection<1.0.0,>=0.0.1 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from thinc<8.4.0,>=8.3.4->spacy>=2.2.2->nlp_preprocessor) (0.1.5)
Requirement already satisfied: click>=8.0.0 in /databricks/python3/lib/python3.12/site-packages (from typer-slim<1.0.0,>=0.3.0->spacy>=2.2.2->nlp_preprocessor) (8.1.7)
Requirement already satisfied: cloudpathlib<1.0.0,>=0.7.0 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from weasel<0.5.0,>=0.4.2->spacy>=2.2.2->nlp_preprocessor) (0.23.0)
Requirement already satisfied: smart-open<8.0.0,>=5.2.1 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from weasel<0.5.0,>=0.4.2->spacy>=2.2.2->nlp_preprocessor) (7.5.0)
Requirement already satisfied: MarkupSafe>=2.0 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from jinja2->spacy>=2.2.2->nlp_preprocessor) (3.0.3)
Requirement already satisfied: wrapt in /databricks/python3/lib/python3.12/site-packages (from smart-open<8.0.0,>=5.2.1->weasel<0.5.0,>=0.4.2->spacy>=2.2.2->nlp_preprocessor) (1.14.1)
Building wheels for collected packages: nlp_preprocessor
  Building wheel for nlp_preprocessor (setup.py): started
  Building wheel for nlp_preprocessor (setup.py): finished with status 'done'
  Created wheel for nlp_preprocessor: filename=nlp_preprocessor-0.0.1-py3-none-any.whl size=2308 sha256=35ce96e2bac4b5caa7d59057a5f26c070c04202500a1ca666d3f1ded65119d77
  Stored in directory: /home/spark-8e5edb0d-ecd9-4242-bd9c-97/.cache/pip/wheels/6d/09/96/92c2f4750d49a063f75756d48281f618cab5802e0d5e132da4
Successfully built nlp_preprocessor
Installing collected packages: nlp_preprocessor
Successfully installed nlp_preprocessor-0.0.1
Note: you may need to restart the kernel using %restart_python or dbutils.library.restartPython() to use updated packages.
Collecting https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_sm-0.5.4.tar.gz
  Downloading https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_sm-0.5.4.tar.gz (14.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/14.8 MB ? eta -:--:--
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/14.8 MB ? eta -:--:--
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/14.8 MB ? eta -:--:--
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.1/14.8 MB 623.4 kB/s eta 0:00:24
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.1/14.8 MB 623.4 kB/s eta 0:00:24
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.1/14.8 MB 812.0 kB/s eta 0:00:19
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.1/14.8 MB 812.0 kB/s eta 0:00:19
     ╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.2/14.8 MB 967.9 kB/s eta 0:00:16
     ╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.3/14.8 MB 1.3 MB/s eta 0:00:11
     ╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.3/14.8 MB 1.3 MB/s eta 0:00:11
     ━╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.7/14.8 MB 2.2 MB/s eta 0:00:07
     ━╸━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.7/14.8 MB 2.2 MB/s eta 0:00:07
     ━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.5/14.8 MB 3.6 MB/s eta 0:00:04
     ━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.5/14.8 MB 3.6 MB/s eta 0:00:04
     ━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.5/14.8 MB 3.1 MB/s eta 0:00:05
     ━━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.0/14.8 MB 6.0 MB/s eta 0:00:02
     ━━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.0/14.8 MB 6.0 MB/s eta 0:00:02
     ━━━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━ 5.3/14.8 MB 9.1 MB/s eta 0:00:02
     ━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━ 6.1/14.8 MB 9.7 MB/s eta 0:00:01
     ━━━━━━━━━━━━━━━━━━━╸━━━━━━━━━━━━━━━━━━━━ 7.3/14.8 MB 11.0 MB/s eta 0:00:01
     ━━━━━━━━━━━━━━━━━━━╸━━━━━━━━━━━━━━━━━━━━ 7.3/14.8 MB 11.0 MB/s eta 0:00:01
     ━━━━━━━━━━━━━━━━━━━━━━━╸━━━━━━━━━━━━━━━━ 8.7/14.8 MB 12.3 MB/s eta 0:00:01
     ━━━━━━━━━━━━━━━━━━━━━━━━━━╸━━━━━━━━━━━━━ 9.9/14.8 MB 13.4 MB/s eta 0:00:01
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╺━━━━━━━━━━ 10.9/14.8 MB 22.4 MB/s eta 0:00:01
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸━━━━━━ 12.5/14.8 MB 31.1 MB/s eta 0:00:01
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸━━━ 13.7/14.8 MB 34.6 MB/s eta 0:00:01
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 14.8/14.8 MB 31.5 MB/s eta 0:00:01
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 14.8/14.8 MB 31.5 MB/s eta 0:00:01
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 14.8/14.8 MB 31.5 MB/s eta 0:00:01
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 14.8/14.8 MB 24.1 MB/s eta 0:00:00
  Preparing metadata (setup.py): started
  Preparing metadata (setup.py): finished with status 'done'
Collecting spacy<3.8.0,>=3.7.4 (from en_core_sci_sm==0.5.4)
  Downloading spacy-3.7.5-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (27 kB)
Requirement already satisfied: spacy-legacy<3.1.0,>=3.0.11 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (3.0.12)
Requirement already satisfied: spacy-loggers<2.0.0,>=1.0.0 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (1.0.5)
Requirement already satisfied: murmurhash<1.1.0,>=0.28.0 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (1.0.15)
Requirement already satisfied: cymem<2.1.0,>=2.0.2 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (2.0.13)
Requirement already satisfied: preshed<3.1.0,>=3.0.2 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (3.0.12)
Collecting thinc<8.3.0,>=8.2.2 (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4)
  Downloading thinc-8.2.5-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (15 kB)
Requirement already satisfied: wasabi<1.2.0,>=0.9.1 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (1.1.3)
Requirement already satisfied: srsly<3.0.0,>=2.4.3 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (2.5.2)
Requirement already satisfied: catalogue<2.1.0,>=2.0.6 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (2.0.10)
Requirement already satisfied: weasel<0.5.0,>=0.1.0 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (0.4.3)
Collecting typer<1.0.0,>=0.3.0 (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4)
  Downloading typer-0.20.0-py3-none-any.whl.metadata (16 kB)
Requirement already satisfied: tqdm<5.0.0,>=4.38.0 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (4.67.1)
Requirement already satisfied: requests<3.0.0,>=2.13.0 in /databricks/python3/lib/python3.12/site-packages (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (2.32.2)
Requirement already satisfied: pydantic!=1.8,!=1.8.1,<3.0.0,>=1.7.4 in /databricks/python3/lib/python3.12/site-packages (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (2.8.2)
Requirement already satisfied: jinja2 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (3.1.6)
Requirement already satisfied: setuptools in /usr/local/lib/python3.12/dist-packages (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (74.0.0)
Requirement already satisfied: packaging>=20.0 in /databricks/python3/lib/python3.12/site-packages (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (24.1)
Collecting langcodes<4.0.0,>=3.2.0 (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4)
  Downloading langcodes-3.5.0-py3-none-any.whl.metadata (29 kB)
Requirement already satisfied: numpy>=1.19.0 in /databricks/python3/lib/python3.12/site-packages (from spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (1.26.4)
Collecting language-data>=1.2 (from langcodes<4.0.0,>=3.2.0->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4)
  Downloading language_data-1.3.0-py3-none-any.whl.metadata (4.3 kB)
Requirement already satisfied: annotated-types>=0.4.0 in /databricks/python3/lib/python3.12/site-packages (from pydantic!=1.8,!=1.8.1,<3.0.0,>=1.7.4->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (0.7.0)
Requirement already satisfied: pydantic-core==2.20.1 in /databricks/python3/lib/python3.12/site-packages (from pydantic!=1.8,!=1.8.1,<3.0.0,>=1.7.4->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (2.20.1)
Requirement already satisfied: typing-extensions>=4.6.1 in /databricks/python3/lib/python3.12/site-packages (from pydantic!=1.8,!=1.8.1,<3.0.0,>=1.7.4->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (4.11.0)
Requirement already satisfied: charset-normalizer<4,>=2 in /databricks/python3/lib/python3.12/site-packages (from requests<3.0.0,>=2.13.0->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (2.0.4)
Requirement already satisfied: idna<4,>=2.5 in /databricks/python3/lib/python3.12/site-packages (from requests<3.0.0,>=2.13.0->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (3.7)
Requirement already satisfied: urllib3<3,>=1.21.1 in /databricks/python3/lib/python3.12/site-packages (from requests<3.0.0,>=2.13.0->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (1.26.16)
Requirement already satisfied: certifi>=2017.4.17 in /databricks/python3/lib/python3.12/site-packages (from requests<3.0.0,>=2.13.0->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (2024.6.2)
Collecting blis<0.8.0,>=0.7.8 (from thinc<8.3.0,>=8.2.2->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4)
  Downloading blis-0.7.11-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (7.4 kB)
Requirement already satisfied: confection<1.0.0,>=0.0.1 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from thinc<8.3.0,>=8.2.2->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (0.1.5)
Requirement already satisfied: click>=8.0.0 in /databricks/python3/lib/python3.12/site-packages (from typer<1.0.0,>=0.3.0->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (8.1.7)
Collecting shellingham>=1.3.0 (from typer<1.0.0,>=0.3.0->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4)
  Downloading shellingham-1.5.4-py2.py3-none-any.whl.metadata (3.5 kB)
Collecting rich>=10.11.0 (from typer<1.0.0,>=0.3.0->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4)
  Downloading rich-14.2.0-py3-none-any.whl.metadata (18 kB)
Requirement already satisfied: typer-slim<1.0.0,>=0.3.0 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from weasel<0.5.0,>=0.1.0->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (0.20.0)
Requirement already satisfied: cloudpathlib<1.0.0,>=0.7.0 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from weasel<0.5.0,>=0.1.0->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (0.23.0)
Requirement already satisfied: smart-open<8.0.0,>=5.2.1 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from weasel<0.5.0,>=0.1.0->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (7.5.0)
Requirement already satisfied: MarkupSafe>=2.0 in /local_disk0/.ephemeral_nfs/envs/pythonEnv-8e5edb0d-ecd9-4242-bd9c-97197433c858/lib/python3.12/site-packages (from jinja2->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (3.0.3)
Collecting marisa-trie>=1.1.0 (from language-data>=1.2->langcodes<4.0.0,>=3.2.0->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4)
  Downloading marisa_trie-1.3.1-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.metadata (10 kB)
Collecting markdown-it-py>=2.2.0 (from rich>=10.11.0->typer<1.0.0,>=0.3.0->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4)
  Downloading markdown_it_py-4.0.0-py3-none-any.whl.metadata (7.3 kB)
Requirement already satisfied: pygments<3.0.0,>=2.13.0 in /databricks/python3/lib/python3.12/site-packages (from rich>=10.11.0->typer<1.0.0,>=0.3.0->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (2.15.1)
Requirement already satisfied: wrapt in /databricks/python3/lib/python3.12/site-packages (from smart-open<8.0.0,>=5.2.1->weasel<0.5.0,>=0.1.0->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4) (1.14.1)
Collecting mdurl~=0.1 (from markdown-it-py>=2.2.0->rich>=10.11.0->typer<1.0.0,>=0.3.0->spacy<3.8.0,>=3.7.4->en_core_sci_sm==0.5.4)
  Downloading mdurl-0.1.2-py3-none-any.whl.metadata (1.6 kB)
Downloading spacy-3.7.5-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (6.5 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/6.5 MB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 6.5/6.5 MB 211.5 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.5/6.5 MB 105.7 MB/s eta 0:00:00
Downloading langcodes-3.5.0-py3-none-any.whl (182 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/183.0 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 183.0/183.0 kB 14.4 MB/s eta 0:00:00
Downloading thinc-8.2.5-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (865 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/865.0 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 865.0/865.0 kB 42.6 MB/s eta 0:00:00
Downloading typer-0.20.0-py3-none-any.whl (47 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/47.0 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 47.0/47.0 kB 3.2 MB/s eta 0:00:00
Downloading blis-0.7.11-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (10.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/10.2 MB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━ 5.7/10.2 MB 170.3 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸━━ 9.5/10.2 MB 139.5 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 10.2/10.2 MB 139.0 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 10.2/10.2 MB 139.0 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 10.2/10.2 MB 139.0 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 10.2/10.2 MB 53.5 MB/s eta 0:00:00
Downloading language_data-1.3.0-py3-none-any.whl (5.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/5.4 MB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━━ 3.4/5.4 MB 102.1 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 5.4/5.4 MB 122.5 MB/s eta 0:00:01
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.4/5.4 MB 77.1 MB/s eta 0:00:00
Downloading rich-14.2.0-py3-none-any.whl (243 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/243.4 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 243.4/243.4 kB 19.4 MB/s eta 0:00:00
Downloading shellingham-1.5.4-py2.py3-none-any.whl (9.8 kB)
Downloading marisa_trie-1.3.1-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (1.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/1.3 MB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.3/1.3 MB 59.4 MB/s eta 0:00:00
Downloading markdown_it_py-4.0.0-py3-none-any.whl (87 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0.0/87.3 kB ? eta -:--:--
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 87.3/87.3 kB 7.3 MB/s eta 0:00:00
Downloading mdurl-0.1.2-py3-none-any.whl (10.0 kB)
Building wheels for collected packages: en_core_sci_sm
  Building wheel for en_core_sci_sm (setup.py): started
  Building wheel for en_core_sci_sm (setup.py): finished with status 'done'
  Created wheel for en_core_sci_sm: filename=en_core_sci_sm-0.5.4-py3-none-any.whl size=14778483 sha256=c1f9597062ed0b621731637098aaf88da2c3476ab625c7b15e5a8728b6eb3759
  Stored in directory: /home/spark-8e5edb0d-ecd9-4242-bd9c-97/.cache/pip/wheels/49/7f/0f/ec0fc3a935bfe55e6ef2ca04b7a31e33cbd533a6d7cbd9e11e
Successfully built en_core_sci_sm
Installing collected packages: shellingham, mdurl, marisa-trie, blis, markdown-it-py, language-data, rich, langcodes, typer, thinc, spacy, en_core_sci_sm
  Attempting uninstall: blis
    Found existing installation: blis 1.3.3
    Uninstalling blis-1.3.3:
      Successfully uninstalled blis-1.3.3
  Attempting uninstall: thinc
    Found existing installation: thinc 8.3.10
    Uninstalling thinc-8.3.10:
      Successfully uninstalled thinc-8.3.10
  Attempting uninstall: spacy
    Found existing installation: spacy 3.8.11
    Uninstalling spacy-3.8.11:
      Successfully uninstalled spacy-3.8.11
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
medspacy 1.3.1 requires spacy<4.0,>=3.8; python_version >= "3.12", but you have spacy 3.7.5 which is incompatible.
pyrush 1.0.12 requires spacy>=3.8; python_version >= "3.12", but you have spacy 3.7.5 which is incompatible.
Successfully installed blis-0.7.11 en_core_sci_sm-0.5.4 langcodes-3.5.0 language-data-1.3.0 marisa-trie-1.3.1 markdown-it-py-4.0.0 mdurl-0.1.2 rich-14.2.0 shellingham-1.5.4 spacy-3.7.5 thinc-8.2.5 typer-0.20.0
Note: you may need to restart the kernel using %restart_python or dbutils.library.restartPython() to use updated packages.
```