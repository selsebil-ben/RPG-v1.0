
# csv_to_json_edges.py 
import csv
import os
import sys
from chunk_util import safe_int, write_chunk_json

if __name__ == "__main__":
    # usage: python csv_to_json_edges.py
    BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
    INPUT_DIR = os.path.join(BASE_DIR, "data")
    OUTPUT_DIR = os.path.join(BASE_DIR, "output_json")
    STATE_DIR = os.path.join(BASE_DIR, "state")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(STATE_DIR, exist_ok=True)

    counter_file = os.path.join(STATE_DIR, "edge_counter.txt")

    # read persisted counter if exists
    if os.path.exists(counter_file):
        with open(counter_file, 'r', encoding='utf-8') as f:
            try:
                edge_counter = int(f.read().strip())
            except:
                edge_counter = 1
    else:
        edge_counter = 1

    chunk_size = 50000

    # special property CSVs to skip (handled elsewhere)
    special_prop_files = {
        "person_speaks_language_0_0.csv",
        "person_email_emailaddress_0_0.csv"
    }

    # list all CSV files sorted
    all_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".csv")])

    for fname in all_files:
        # skip special prop files
        if fname in special_prop_files:
            continue

        base = os.path.splitext(fname)[0]
        parts = base.split('_')

        # skip node files like "person_0_0.csv"
        if len(parts) >= 2 and parts[1].isdigit():
            continue

        

        # use relation name as label
        label = parts[1]
        path = os.path.join(INPUT_DIR, fname)
        print(f"[Processing] {fname} -> edge label '{label}'")

        edges, edge_labels, edge_props = [], [], []
        chunk_index, row_count = 1, 0

        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            try:
                headers = next(reader)
            except StopIteration:
                print(f"  empty file: {fname}")
                continue

            for r in reader:
                if not r or len(r) < 2:
                    continue

                ns = safe_int(r[0])
                nd = safe_int(r[1])
                if ns is None or nd is None:
                    continue

                eid = edge_counter
                edges.append([eid, ns, nd])
                edge_labels.append([eid, label])

                # collect edge properties if any
                for idx in range(2, len(r)):
                    key = headers[idx] if idx < len(headers) else f"col{idx}"
                    val = safe_int(r[idx])
                    if val is None or (isinstance(val, str) and val == ""):
                        continue
                    edge_props.append([eid, key, val])

                edge_counter += 1
                row_count += 1

                # write chunk
                if row_count >= chunk_size:
                    data = {
                        "edge": {"headers": ["id_e", "ns", "nd"], "rows": edges},
                        "edge_label": {"headers": ["id_e", "ln"], "rows": edge_labels}
                    }
                    if edge_props:
                        data["edge_prop"] = {"headers": ["id_e", "key", "value"], "rows": edge_props}

                    out_path = os.path.join(OUTPUT_DIR, f"{base}_chunk{chunk_index}.json")
                    write_chunk_json(out_path, data)
                    print(f"  wrote {out_path} ({row_count} rows)")
                    chunk_index += 1
                    edges, edge_labels, edge_props, row_count = [], [], [], 0

            # write last chunk
            if row_count > 0:
                data = {
                    "edge": {"headers": ["id_e", "ns", "nd"], "rows": edges},
                    "edge_label": {"headers": ["id_e", "ln"], "rows": edge_labels}
                }
                if edge_props:
                    data["edge_prop"] = {"headers": ["id_e", "key", "value"], "rows": edge_props}

                out_path = os.path.join(OUTPUT_DIR, f"{base}_chunk{chunk_index}.json")
                write_chunk_json(out_path, data)
                print(f"  wrote {out_path} (final {row_count} rows)")

    # save counter for next run in status folder
    with open(counter_file, 'w', encoding='utf-8') as f:
        f.write(str(edge_counter))

    print(f"\n All edges processed. Edge counter saved: {edge_counter}")
