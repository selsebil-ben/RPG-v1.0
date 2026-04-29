@echo off
echo === Step 1: Activate venv and install dependencies ===
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt

echo === Step 2: Convert CSVs to JSON ===
cd scripts
python csv_to_json_nodes.py
python csv_to_json_props.py
python csv_to_json_edges.py

echo === Step 3: Import into Cozo (embedded RocksDB mode) ===
python import_to_cozo.py
cd ..

echo === DONE! Data successfully imported into snbsf1.db ===
pause
