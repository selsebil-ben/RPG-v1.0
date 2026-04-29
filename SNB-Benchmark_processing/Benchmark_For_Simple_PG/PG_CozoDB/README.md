# Importing SNB CSVs into CozoDB

This guide explains how to import **LDBC SNB CSV** data into **CozoDB**.



## 1. Download SNB Data

1. Go to:  
   **https://ldbcouncil.org/data-sets-surf-repository/snb-interactive-v1-datagen-v100**

2. Download the file:  
   **social_network-sfX-CsvBasic-LongDateFormatter.tar.zst**  
   where `X ∈ {0.1, 0.3, 1}`.

3. Unzip the archive. You will find two folders:

### `static/`
Contains stable data that does not change (static entities) — such as **Tag**, **Place**, **Organisation**, etc.

### `dynamic/`
Contains graph events / evolving relationships — **knows**, **messages**, **comments**, **hasCreator**, **replyOf**, etc.



## 2. Project Structure to Reproduce

Create the following folder structure in your project root:

project-root/
├── data/
├── scripts/
├── output_json/
├── state/
├── venv/
├── requirements.txt
└── run.bat


### `data/`
Select all CSV files from both `static/` and `dynamic/` and place them here.

### `scripts/`
Contains all scripts used to transform CSV data into **JSON objects** ready for import into CozoDB.  
Reference documentation: https://docs.cozodb.org/en/latest/nonscript.html

### `output_json/`
Directory where chunks produced by the CSV-to-JSON Python scripts are stored.  
This folder also contains the **query_cozo file**, which must be located in the **same directory as the `DB/` folder** (see *Important* section below).

### `state/`
Stores the state of the last edge ID for each CSV file.  
(We must generate edge IDs manually because SNB CSV edges do not include IDs.)


### `requirements.txt`
Dependency list (for embedded CozoDB use).

### `run.bat`
Batch file used to run the full import pipeline.

---

## IMPORTANT: Before Running the Batch File

For every SNB scale factor:

### 1. Initialize the CozoDB schema
- Open: `scripts/import_to_cozo.py`
- Temporarily **uncomment** the schema-creation code (creates a simple property graph schema + indexes).
- Once you run the script, a new `DB` folder will be created in the same directory (`scripts/`).
- Then **comment the schema code again**, leaving only the import code active.

### 2. Reset edge counters
- Open: `state/edge-counter.txt`
- Ensure the file is **empty** before starting the import process.


