# csv_to_json_nodes.py
import os
import sys
import pandas as pd
from chunk_util import write_chunk_json

# ------------------------------------------------------------
#  Configuration des chemins
# ------------------------------------------------------------
BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
INPUT_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_json")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ------------------------------------------------------------
#  Liste des fichiers node et leurs colonnes
# ------------------------------------------------------------
NODE_FILES = {
    "person": ["id", "firstName", "lastName", "gender", "birthday", "creationDate", "locationIP", "browserUsed"],
    "forum": ["id", "title", "creationDate"],
    "post": ["id", "imageFile", "creationDate", "locationIP", "browserUsed", "language", "content", "length"],
    "comment": ["id", "creationDate", "locationIP", "browserUsed", "content", "length"],
    "tag": ["id", "name", "url"],
    "place": ["id", "name", "url", "type"],
    "organisation": ["id", "type", "name", "url"],
    "tagclass": ["id", "name", "url"]
}

# ------------------------------------------------------------
#  Taille du chunk que je peux modifier
# ------------------------------------------------------------
chunk_size = 50000

# ------------------------------------------------------------
#  Boucle principale : conversion CSV → JSON chunké
# ------------------------------------------------------------
for label, headers in NODE_FILES.items():
    file_path = os.path.join(INPUT_DIR, f"{label}_0_0.csv")
    if not os.path.exists(file_path):
        print(f"[WARN] File not found: {file_path}")
        continue

    print(f"[Processing] {label} ...")

    # lire le fichier CSV par morceaux (streaming)
    reader = pd.read_csv(file_path, sep='|', chunksize=chunk_size)
    chunk_index = 1
    total_rows = 0

    for chunk in reader:
        chunk.fillna("", inplace=True)

        node_rows = [[int(x)] for x in chunk["id"]]
        label_rows = [[int(x), label] for x in chunk["id"]]
        prop_rows = []

        for _, row in chunk.iterrows():
            id_n = int(row["id"])
            for k in headers[1:]:
                value = row[k]
                if "Date" in k or "birthday" in k:
                    try:
                        value = int(value)
                    except:
                        value = 0
                prop_rows.append([id_n, k, value])

        data = {
            "node": {"headers": ["id_n"], "rows": node_rows},
            "node_label": {"headers": ["id_n", "ln"], "rows": label_rows},
            "node_prop": {"headers": ["id_n", "key", "value"], "rows": prop_rows}
        }

        # chemin du chunk
        out_path = os.path.join(OUTPUT_DIR, f"node_{label}_chunk{chunk_index}.json")
        write_chunk_json(out_path, data)
        print(f"  wrote {out_path} ({len(node_rows)} rows)")
        chunk_index += 1
        total_rows += len(node_rows)

    print(f"[OK] {label} exported ({total_rows} total rows)\n")

print("\n All nodes processed successfully!")
