# Importing SNB CSVs into Neo4j

This guide explains how to import **LDBC SNB CSV** data into **Neo4j**.



# 1. Download the data

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

# NOTES

- All the steps below can be automated by running:  
  `automated_import_fromSNB_to_Neo4j.ps1`
- Make sure to read the **IMPORTANT** section before running the script.

---

# 4. Prepare CSV files

1. Select **only CSV files** from both `static/` and `dynamic/` folders.

2. Prepare Neo4j:  
   - Create a new database  
   - Place all CSV files into the `import/` folder of your Neo4j database

---

# 5. Create constraints / indexes (mandatory before import)

Example:


CREATE CONSTRAINT person_id IF NOT EXISTS
FOR (p:Person)
REQUIRE p.id IS UNIQUE;

# 6. Import nodes
# 7. Import relationships

# /!\ Important Notes before running the script

Before executing the automation script:

1. Read carefully the comments in the script file that guide you to change the paths of each used file.

2. Install the APOC plugin in your Neo4j DBMS.

3. In the static/ and dynamic/ folders, rename the first two columns in these files:

person_knows_person.csv

comment_replyOf_comment.csv

place_isPartOf_place.csv

tagclass_isSubclassOf_tagclass.csv

The first column must be LabelName1.id and the second column must be LabelName2.id.
