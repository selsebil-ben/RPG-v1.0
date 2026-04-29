from pycozo.client import Client
import json
import os

client = Client('rocksdb', 'snbsf01.db')

# #relationn creation 
# res = client.run('{:create node {id_n: Int}} {:create edge {id_e: Int, ns: Int, nd: Int}} {:create label {ln: String}} {:create prop {key: String}} {:create node_label {id_n: Int, ln: String}} {:create edge_label {id_e: Int, ln: String}} {:create node_prop {id_n: Int, key: String, value}} {:create edge_prop {id_e: Int, key: String, value}}')
# print(res)

#health check of rel creation
# res = client.run('::relations')
# print(res)

# #index cteation

# res = client.run('{::index create node:id_idx {id_n}} {::index create edge:id_idx {id_e,ns, nd}} {::index create node_label:id_idx {id_n, ln}} {::index create edge_label:id_idx {id_e, ln}} {::index create node_prop:id_idx {id_n, key}} {::index create edge_prop:id_idx {id_e, key}}')    
# print(res)

#index remove

# res = client.run('{::index drop edge:id_idx}{::index drop node_label:id_idx}{::index drop edge_label:id_idx}{::index drop node_prop:id_idx}{::index drop edge_prop:id_idx}')
# print(res)
# exited with code=0 in 1228.314 seconds

# #new index cteation

# res = client.run(""" 
# {::index create edge:e_idx {id_e}}
# {::index create edge:ns_idx {ns}} 
# {::index create edge:nd_idx {nd}} 
# {::index create node_label:n_idx {id_n}} 
# {::index create node_label:l_idx {ln}}
# {::index create edge_label:e_idx {id_e}} 
# {::index create edge_label:l_idx {ln}} 
# {::index create node_prop:n_idx {id_n}} 
# {::index create node_prop:k_idx {key}} 
# {::index create edge_prop:e_idx {id_e}}
# {::index create edge_prop:k_idx {key}}                

# """)    
# print(res)

# exited with code=0 in 77446.087 seconds = 21h , 30 min, 49 s


# res = client.run('?[nd] := *node[ nd]')
# print(res)


# ça pour l'impooooort


INPUT_DIR = "../output_json"

for file in sorted(os.listdir(INPUT_DIR)):
    if not file.endswith(".json"):
        continue

    path = os.path.join(INPUT_DIR, file)
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    print(f"Importing {file} ...")
    res = client.import_relations(data)
    print(res)

