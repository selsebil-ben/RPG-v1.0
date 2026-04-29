# chunk_util.py
import os, json

def safe_int(val):
    if val is None: return None
    s = str(val).strip()
    if s == '' or s.lower() in ('null','nan','none'): return None
    try:
        # keep integer if it's a pure integer string
        if '.' in s:
            # don't cast floats to int — keep as string
            return int(float(s)) if float(s).is_integer() else s
        return int(s)
    except:
        return s

def write_chunk_json(out_path, data):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
