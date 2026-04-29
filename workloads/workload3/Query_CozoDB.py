import timeit
import time
from pycozo.client import Client

client = Client('rocksdb', 'snbsf01.db')




R1="""
?[associated_node, associated_nlabel, associated_nprop,associated_edge, associated_elabel, associated_eprop] :=
id_rn = 35184372090193,
*n_composed_of_node[id_rn, associated_node], *node_label[associated_node, associated_nlabel],*n_composed_of_node_prop[id_rn,associated_node, associated_nprop],
*n_composed_of_edge[id_rn, associated_edge], *edge_label[associated_edge, associated_elabel],*n_composed_of_edge_prop[id_rn,associated_edge, associated_eprop]
"""

R2="""
?[tagNode] :=
  *reified_node[r_id],
  *n_composed_of_node[r_id, tagNode],
  *node_label[tagNode, "tag"],
  *node_prop[tagNode, "name", "Izmir_University"]
"""
R3="""
?[associated_node, associated_label, associated_prop] :=
id_re = 1477966,
*e_composed_of_node[id_re, associated_node], *node_label[associated_node, associated_label],*node_prop[associated_node, associated_prop, value]

?[associated_node, associated_nlabel, associated_nprop, associated_edge, associated_elabel, associated_eprop] :=
id_re = 1477966,
*e_composed_of_node[id_re, associated_node], 
*node_label[associated_node, associated_nlabel],
*e_composed_of_node_prop[id_re,associated_node, associated_nprop],
*e_composed_of_edge[id_re, associated_edge], 
*edge_label[associated_edge, associated_elabel],
*e_composed_of_edge_prop[id_re, associated_edge, associated_eprop]
"""



R4="""
?[created_comment] :=
*edge_label[id_re, "create"],
*e_composed_of_node[id_re, created_comment], *node_label[created_comment, "comment"],*node_prop[created_comment, "creationDate", 1313591219961],
*e_composed_of_node[id_re, creator], *node_label[creator, "person"],*node_prop[creator, "locationIP", "46.16.217.105"]
"""

R5a = """
# Filter forumMembership nodes where nbMember > 150
filtered_forum[n_rn] :=
    *node_prop[n_rn, 'nbMember', nb],
    nb > 150

# Retrieve persons belonging to each forumMembership
forum_member[n_rn, person] :=
    filtered_forum[n_rn],
    *n_composed_of_node[n_rn, person],
    *node_label[person, 'person']

# Retrieve locationIP of each member
member_ip[person, ip] :=
    forum_member[n_rn, person],
    *node_prop[person, 'locationIP', ip]

# Final result
?[person, ip] :=
    member_ip[person, ip]
"""

R5b = """
# Filter forumMembership nodes where nbMember < 150
filtered_forum[n_rn] :=
    *node_prop[n_rn, 'nbMember', nb],
    nb < 150

# Retrieve persons belonging to each forumMembership
forum_member[n_rn, person] :=
    filtered_forum[n_rn],
    *n_composed_of_node[n_rn, person],
    *node_label[person, 'person']

# Retrieve locationIP of each member
member_ip[person, ip] :=
    forum_member[n_rn, person],
    *node_prop[person, 'locationIP', ip]

# Final result
?[person, ip] :=
    member_ip[person, ip]
"""

R6 = """
# Find comment-to-comment reply relationships (c1 -> c2)
comment_reply[c1, c2, e] :=
    *edge[e, c1, c2],
    *edge_label[e, "replyOf"],
    *node_label[c1, "comment"],
    *node_label[c2, "comment"]

# Identify simpleRepliedComment containing this edge
simple_src[src, c1, c2] :=
    comment_reply[c1, c2, e],
    src = 35184372391657,
    *n_composed_of_edge[src, e],
    *node_label[src, "simpleRepliedComment"]

# First level of recursive reification: repliedComment (level 1)
rc1[src, rc1] :=
    simple_src[src, _, _],
    *n_composed_of_node[rc1, src],
    *node_label[rc1, "repliedComment"]

# Second level of recursive reification: repliedComment (level 2)
rc2[rc1, rc2] :=
    rc1[_, rc1],
    *n_composed_of_node[rc2, rc1],
    *node_label[rc2, "repliedComment"]

# Final result
?[c1] :=
    simple_src[src, c1, c2],
    rc1[src, rc1],
    rc2[rc1, rc2]
"""
#---------------------------------------
#claculate the mean of 10 executions
n = 10
times = []

for _ in range(n):
    start = time.time()  
    client.run(R1)
    end = time.time()  
    times.append((end - start) * 1000)  # en ms

mean = sum(times) / n
print(f"Temps moyen sur {n} exécutions : {mean:.3f} ms")








