import pandas as pd
import json
import os

INPUT_DIR = "../data"
OUTPUT_DIR = "../output_json"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FILES = [
    "person_speaks_language_0_0.csv",
    "person_email_emailaddress_0_0.csv"
]

for file in FILES:
    path = os.path.join(INPUT_DIR, file)
    df = pd.read_csv(path, sep='|')
    df.fillna("", inplace=True)

    key = file.split("_")[1]  # speaks or email
    rows = []

    for _, r in df.iterrows():
        id_n = int(r["Person.id"])
        value = r[df.columns[1]]
        rows.append([id_n, key, value])

    data = {"node_prop": {"headers": ["id_n","key","value"], "rows": rows}}
    out_path = os.path.join(OUTPUT_DIR, f"props_{file.replace('.csv','.json')}")
    json.dump(data, open(out_path, "w"), indent=2)
    print(f"[OK] {file} → {out_path}")
