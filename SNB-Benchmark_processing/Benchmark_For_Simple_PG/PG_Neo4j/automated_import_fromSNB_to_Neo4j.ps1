# ===============================
# LDBC-SNB CSV Importer (Neo4j)
# ===============================

# --- 1. CONFIGURATION ---
# u hafta change the below paths
#How to find import folder path ? go to neo4j, click on ⋮ , choose open folder , choose Import, it open the import folder in his location :) 
#How to find cypher-shell.bat path ? when you reach import folder , go to previous folder, open bin folder, and your bat file is there ^^
$neo4j_user = "neo4j"
$neo4j_pass = "yourpassword"  
$neo4j_import_dir = "C:\Users\Selsebil\.Neo4jDesktop\relate-data\dbmss\dbms-73a0a32c-4a50-4ef4-86a5-01f6e855ac48\import"
$cypher_shell = "C:\Users\Selsebil\.Neo4jDesktop\relate-data\dbmss\dbms-73a0a32c-4a50-4ef4-86a5-01f6e855ac48\bin\cypher-shell.bat"
$PSScriptRoot="C:\Users\Selsebil\Desktop\EXPv2" #here where u put this script file
# --- 2. PATH OF SNB CSV FILES ---
#change this path for every SF (Sf01, 03 and 1)
$dataset_path = "C:\Users\Selsebil\Desktop\EXPv2\social_network-sf0.1-CsvBasic-LongDateFormatter"

# --- 3. COPY ALL CSV FILES ---
Write-Host "Copying CSV files into the import folder of  Neo4j..."
Get-ChildItem -Path "$dataset_path\static" -Recurse -Filter *.csv | Copy-Item -Destination $neo4j_import_dir -Force
Get-ChildItem -Path "$dataset_path\dynamic" -Recurse -Filter *.csv | Copy-Item -Destination $neo4j_import_dir -Force

Write-Host "All csv files are cpoied in $neo4j_import_dir"

# --- 4. CONSTRAINT CREATION + INDEX ---
$constraints = @"
CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT forum_id IF NOT EXISTS FOR (f:Forum) REQUIRE f.id IS UNIQUE;
CREATE CONSTRAINT post_id IF NOT EXISTS FOR (p:Post) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT comment_id IF NOT EXISTS FOR (c:Comment) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT tag_id IF NOT EXISTS FOR (t:Tag) REQUIRE t.id IS UNIQUE;
CREATE CONSTRAINT place_id IF NOT EXISTS FOR (pl:Place) REQUIRE pl.id IS UNIQUE;
CREATE CONSTRAINT organisation_id IF NOT EXISTS FOR (o:Organisation) REQUIRE o.id IS UNIQUE;
CREATE CONSTRAINT tagclass_id IF NOT EXISTS FOR (tc:TagClass) REQUIRE tc.id IS UNIQUE;
"@
Write-Host "creating constraints and indexes..."
$constraints | & $cypher_shell -u $neo4j_user -p $neo4j_pass

# --- IMPORT NODES ---
Write-Host "Importing nodes..."
& $cypher_shell -u $neo4j_user -p $neo4j_pass -f "$PSScriptRoot\cypher_nodes.cypher"

# --- IMPORT RELATIONSHIPS ---
Write-Host "Importing relationships..."
& $cypher_shell -u $neo4j_user -p $neo4j_pass -f "$PSScriptRoot\cypher_rels.cypher"

Write-Host "Import completed successfully!"