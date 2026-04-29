# A. Installing and Running HO-GDB with Python 3.11

This guide explains how to install **HO-GDB** using a clean **Python 3.11** environment with **Anaconda**, and how to run the data import notebook that loads the dataset into **Neo4j** so you will be able to query the HO-GBD graph.

---

# 1 Install Anaconda and Prepare the Environment

First install **Anaconda** if it is not already installed:

🔗 https://www.anaconda.com/download

Then open **Anaconda Prompt**.

---

# 2 Create and Activate a Clean Python 3.11 Environment

Creating a dedicated environment avoids dependency conflicts with other Python installations.

```bash
# Create a new conda environment with Python 3.11
conda create -n hogdb311 python=3.11 -y

# Activate the environment
conda activate hogdb311
```

---

# 3️ Install Jupyter Notebook and Useful Tools

```bash
# Install Jupyter Notebook
conda install -y notebook

# (Optional) Install JupyterLab instead of Notebook
# conda install -y jupyterlab

# Install IPython kernel support
pip install ipykernel
```



# 4️ Clone the Official HO-GDB Repository

Clone the original repository from GitHub:

```bash
git clone https://github.com/spcl/HO-GDB.git
```

Repository link:  
🔗 https://github.com/spcl/HO-GDB



# 5️ Fix the Configuration File (Important)

Replace the file:

```
HO-GDB/pyproject.toml
```

with the **custom `pyproject.toml`** provided in the current project directory:

```
HOGDB_Neo4j/pyproject.toml
```

### /!\ Why this step is necessary

The original configuration file may contain **dependency version conflicts** between:

- **Python 3.11**
- some **HO-GDB dependencies**

Using the corrected file ensures a **clean and compatible installation**.



# 6️ Move to the Cloned Repository

```bash
cd your\path\HO-GDB
```

Example:

```bash
cd C:\Users\yourname\Documents\HO-GDB
```



# 7️ Install HO-GDB and Its Dependencies

```bash
# Standard installation (pip resolves declared dependencies)
pip install .
```



# 8️ Add the Environment as a Jupyter Kernel (Recommended)

This allows Jupyter to run notebooks with the **HO-GDB Python environment**.

```bash
python -m ipykernel install --user --name hogdb311 --display-name "Python 3.11 (HO-GDB)"
```

After this step, **Python 3.11 (HO-GDB)** will appear in the list of available kernels in Jupyter.


# B. Importing SNB CSVs into HO-GDB

This guide explains how to import **LDBC SNB CSV** data into **HO-GDB**.



# 1. Download the SNB data

1. Go to:  
   [https://ldbcouncil.org/data-sets-surf-repository/snb-interactive-v1-datagen-v100](https://ldbcouncil.org/data-sets-surf-repository/snb-interactive-v1-datagen-v100)

2. Download the file:  
   `social_network-sfX-CsvBasic-LongDateFormatter.tar.zst`  
   *(X = 0.1 | 0.3 | 1)*

3. Extract the archive. You will find two folders:

## static/
Contains **static entities** (data that does not change) such as:  
Tag, Place, Organisation, etc.

## dynamic/
Contains **dynamic entities and relationships** (graph events), such as:  
- knows (friendship relations)  
- messages  
- comments  
- hasCreator, replyOf, etc.

---

# 2. Prepare CSV files

1. Select **only CSV files** from both `static/` and `dynamic/` folders.
2. In the static/ and dynamic/ folders, rename the first two columns in these files:

   person_knows_person.csv

   comment_replyOf_comment.csv

   place_isPartOf_place.csv

   tagclass_isSubclassOf_tagclass.csv

   The first column must be LabelName1.id and the second column must be LabelName2.id.


3. Place all  node CSV files into `data/` folder in the same directory of the script to run
4. Place all  edge CSV files into `data/edges_without_id` folder

Example structure:

```
HOGDB_Neo4j
│
├── data
│   ├── nodes
│   │   ├── person.csv
│   │   ├── comment.csv
│   │   ├── place.csv
│   │   └── ...
    ├── edges_without_id
    └── edges

```
---
# 3. Prepare Neo4j:  
   Before running the import notebook:
1. Open **Neo4j Desktop**.
2. **Create a new Graph Database**.
3. **Start the database server**.

/!\ The database **must be running**, otherwise the import script will not be able to connect.

---

# 4. Create constraints / indexes (mandatory before import)

Example:


CREATE CONSTRAINT person_id IF NOT EXISTS
FOR (p:Person)
REQUIRE p.id IS UNIQUE;

# 5. Import nodes and relationships
run the script importDataViaHOGDB.ipynb



# What the Notebook Does

The notebook:

- Connects to the **active Neo4j database**
- Uses **HO-GDB APIs**
- Imports the **CSV dataset**
- Builds the **higher-order graph structures**

/!\ **Important:**  
The import script **automatically loads the data into the currently running Neo4j database**.



After completing these steps, you should be able to run queries available in each workload







