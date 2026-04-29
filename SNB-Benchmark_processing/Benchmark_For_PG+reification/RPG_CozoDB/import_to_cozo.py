from pycozo.client import Client
import json
import os

client = Client('rocksdb', 'snbsf1.db')

# #reified_node & reified-edge relations creation 
query="""
{:create reified_node {
    id_rn: Int 
}}

{:create reified_edge {
    id_re: Int, 
}}

{:create n_composed_of_node {
    id_rn: Int, 
    id_n: Int    
}}

{:create n_composed_of_edge {
    id_rn: Int,  
    id_e: Int    
}}

{:create n_composed_of_node_label {
    id_rn: Int,
    id_n: Int,   
    ln: String  
}}

{:create n_composed_of_edge_label {
    id_rn: Int, 
    id_e: Int,   
    ln: String   
}}

{:create n_composed_of_node_prop {
    id_rn: Int,  
    id_n: Int,  
    key: String  
}}

{:create n_composed_of_edge_prop {
    id_rn: Int, 
    id_e: Int,  
    key: String  
}}


{:create e_composed_of_node {
    id_re: Int, 
    id_n: Int  
}}

{:create e_composed_of_edge {
    id_re: Int,  
    id_e: Int    
}}

{:create e_composed_of_node_label {
    id_re: Int,  
    id_n: Int,   
    ln: String  
}}

{:create e_composed_of_edge_label {
    id_re: Int,  
    id_e: Int,   
    ln: String   
}}

{:create e_composed_of_node_prop {
    id_re: Int,  
    id_n: Int,   
    key: String  
}}
{:create e_composed_of_edge_prop {
    id_re: Int,  
    id_e: Int,   
    key: String  
}}
"""

# res = client.run(query)
# print(res)

# #health check of rel creation
res = client.run('::relations')
print(res)



#index cteation

# res = client.run(""" 
# {::index create reified_node:rn_idx {id_rn}}
# {::index create reified_edge:re_idx {id_re}}

# {::index create n_composed_of_node:rn_idx {id_rn}}
# {::index create n_composed_of_node:n_idx {id_n}}

# {::index create n_composed_of_edge:rn_idx {id_rn}}
# {::index create n_composed_of_edge:e_idx {id_e}}

# {::index create e_composed_of_node:re_idx {id_re}}
# {::index create e_composed_of_node:n_idx {id_n}}

# {::index create e_composed_of_edge:re_idx {id_re}}
# {::index create e_composed_of_edge:e_idx {id_e}}
# """)   
# print(res)



