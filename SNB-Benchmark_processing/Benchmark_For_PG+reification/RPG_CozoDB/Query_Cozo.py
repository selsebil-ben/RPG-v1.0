import timeit
import time
from pycozo.client import Client

client = Client('rocksdb', 'snbsf1.db')
# res=client.run('::relations ')
# print(res) 

#143
is1 ="""
?[fn, ln, br,ip,brw,city_name] := n=7375, *node_label[n, "person"], *node_prop[n, "firstName", fn], *node_prop[n, "lastName", ln], *node_prop[n, "locationIP", ip], *node_prop[n, "birthday", br], *node_prop[n, "browserUsed", brw],  *edge_label[e, "isLocatedIn"], *edge[e,n,n2],*node_label[n2, l], l = "place", *node_prop[n2, "name", city_name]
"""

is2v1 ="""
recent_msgs[msg_id, msg_date] := person_id =1129, *edge[e1, msg_id, person_id], *edge_label[e1, "hasCreator"], *node_label[msg_id, lbl], (lbl == "post" or  lbl == "comment"), *node_prop[msg_id, "creationDate", msg_date], :order  -msg_date  :limit 10

recent_with_post[msg_id, msg_date, post_id, orig_poster_id] := recent_msgs[msg_id, msg_date], *edge[e2, msg_id, post_id], *edge_label[e2, "replyOf"], *node_label[post_id, "post"], *edge[e3, post_id, orig_poster_id], *edge_label[e3, "hasCreator"]

recent_with_post[msg_id, msg_date, msg_id, orig_poster_id] := recent_msgs[msg_id, msg_date], *node_label[msg_id, "post"], *edge[e3, msg_id, orig_poster_id], *edge_label[e3, "hasCreator"]

?[msg_id, msg_date, post_id, orig_poster_id] := recent_with_post[msg_id, msg_date, post_id, orig_poster_id] 
 """
is2="""
#récupérer les 10 messages récents du user
recent_msgs[msg_id, msg_date] :=
    person_id = 1129,
    *edge[e1, msg_id, person_id], 
    *edge_label[e1, "hasCreator"],
    *node_label[msg_id, lbl],
    (lbl == "post" or lbl == "comment"),
    *node_prop[msg_id, "creationDate", msg_date],
    :order -msg_date :limit 10
#remonter la chaîne replyOf until the final Post 
# Base case : un commentaire qui répond directement à un Post
orig_post[c, p] :=
    *node_label[c, "comment"],
    *edge[e, c, p],
    *edge_label[e, "replyOf"],
    *node_label[p, "post"]

# Recursive case : Comment --> Comment --> ... ---> Post
orig_post[c, p] :=
    *node_label[c, "comment"],
    *edge[e, c, c2],
    *edge_label[e, "replyOf"],
    *node_label[c2, "comment"],
    orig_post[c2, p]
    
#cas des Posts (trivial)
msg_post[msg_id, post_id] :=
    recent_msgs[msg_id, _],
    *node_label[msg_id, "post"],
    post_id = msg_id

# cas des commentaires (utilise orig_post)
msg_post[msg_id, post_id] :=
    recent_msgs[msg_id, _],
    *node_label[msg_id, "comment"],
    orig_post[msg_id, post_id]
#final queryy
?[msg_id, msg_date, post_id, orig_poster_id] := recent_msgs[msg_id, msg_date],
    msg_post[msg_id, post_id],
    *edge[e3, post_id, orig_poster_id],
    *edge_label[e3, "hasCreator"]
"""
# print(client.run(is2))

is3 ="""
?[friend_id, since] :=
p1 == 94,
    *edge[e, p1, friend_id],
    *edge_label[e, "knows"],
    *edge_prop[e, "creationDate", since],
    """


is4 = """
?[content, creation_date] :=
    m=2061584302087,
    *node_prop[m, "content", content],
    *node_prop[m, "creationDate", creation_date]

"""


is5 = """
?[author_id] :=
    m=2061584302087,
    *edge[eid, m, author_id],
    *edge_label[eid, "hasCreator"]

"""


is6 = """
# --- CASE 1: message is a post ---
forum_of_message[msg_id, forum_id, mod_id] :=
    msg_id=1236950581250,
    *node_label[msg_id, "post"],
    *edge[e1, forum_id, msg_id],
    *edge_label[e1, "containerOf"],
    *edge[e2, forum_id, mod_id],
    *edge_label[e2, "hasModerator"]

# --- CASE 2: message is a comment (replyOf -> post) ---
forum_of_message[msg_id, forum_id, mod_id] :=
    msg_id=1236950581250,
    *node_label[msg_id, "comment"],
    *edge[e1, msg_id, post_id],
    *edge_label[e1, "replyOf"],
    *node_label[post_id, "post"],        
    *edge[e2, forum_id, post_id],
    *edge_label[e2, "containerOf"],
    *edge[e3, forum_id, mod_id],
    *edge_label[e3, "hasModerator"]

# --- Final output ---
?[forum_id, mod_id] :=
    msg_id=1236950581250,
    forum_of_message[msg_id, forum_id, mod_id]

"""


is7="""
# bidirectional knows relation
knows_pair[p1, p2] :=
    *edge[e, p1, p2], *edge_label[e, "knows"]
knows_pair[p1, p2] :=
    *edge[e, p2, p1], *edge_label[e, "knows"]

#  replies info + knows boolean
replies[reply_id, replyAuthor, messageAuthor, knows_flag] :=
    *edge[e1, reply_id, msg_id],
    *edge_label[e1, "replyOf"],
    msg_id == 2061584302089,
    *node_label[reply_id, "comment"],

    *edge[e2, reply_id, replyAuthor],
    *edge_label[e2, "hasCreator"],
    *edge[e3, msg_id, messageAuthor],
    *edge_label[e3, "hasCreator"],

    # same author = false
    (replyAuthor == messageAuthor),
    knows_flag = false

replies[reply_id, replyAuthor, messageAuthor, knows_flag] :=
    *edge[e1, reply_id, msg_id],
    *edge_label[e1, "replyOf"],
    msg_id == 2061584302089,
    *node_label[reply_id, "comment"],

    *edge[e2, reply_id, replyAuthor],
    *edge_label[e2, "hasCreator"],
    *edge[e3, msg_id, messageAuthor],
    *edge_label[e3, "hasCreator"],

    # different authors + friends = true
    (replyAuthor != messageAuthor),
    knows_pair[replyAuthor, messageAuthor],
    knows_flag = true

replies[reply_id, replyAuthor, messageAuthor, knows_flag] :=
    *edge[e1, reply_id, msg_id],
    *edge_label[e1, "replyOf"],
    msg_id == 2061584302089,
    *node_label[reply_id, "comment"],

    *edge[e2, reply_id, replyAuthor],
    *edge_label[e2, "hasCreator"],
    *edge[e3, msg_id, messageAuthor],
    *edge_label[e3, "hasCreator"],

    # different authors + no friendship = false
    (replyAuthor != messageAuthor),
    not knows_pair[replyAuthor, messageAuthor],
    knows_flag = false

?[reply_id, replyAuthor, messageAuthor, knows_flag] :=
    replies[reply_id, replyAuthor, messageAuthor, knows_flag]

"""


ic1 ="""

#BFS : profondeur 1
reach1[n_start, n1, dist] :=
    n_start=2199023256684,
    *edge[e,n_start, n1],
    *edge_label[e, 'knows'],
    dist=1

#BFS : profondeur 2
reach2[n_start, n2, dist] :=
    reach1[n_start, n1, 1],
    *edge[e, n1, n2],
    *edge_label[e, 'knows'],
    dist=2,
    n2 != n_start

#BFS : profondeur 3
reach3[n_start, n3, dist] :=
    reach2[n_start, n2, 2],
    *edge[e, n2, n3],
    *edge_label[e, 'knows'],
    dist=3,
    n3 != n_start

# Union des reachables
reachable[n_start, n, dist] :=
    reach1[n_start, n, dist]
  or reach2[n_start, n, dist]
  or reach3[n_start, n, dist]

# filter by given firstName
filtered[n, dist] :=
    reachable[n_start, n, dist],
    *node_prop[n, 'firstName', 'Boy']

# Récupérer les workplaces
workplace[n, company_loc] :=
    *edge[e, n, c],
    *edge_label[e, 'workAt'],
    *edge[e2, c, p],
    *edge_label[e2, 'isLocatedIn'],
    *node_prop[p, 'name', company_loc]

# Récupérer les places of study
studyplace[n, school_loc] :=
   *edge[e, n, s],
    *edge_label[e, 'studyAt'],
    *edge[e2, s, p],
    *edge_label[e2, 'isLocatedIn'],
    *node_prop[p, 'name', school_loc]

# Récupérer les coordonnées of a frieend
person_info[n, ln, br,  cr, gr, brw, ip, em, sp, city_name] := *node_prop[n, "lastName", ln], *node_prop[n, "locationIP", ip], *node_prop[n, "birthday", br], *node_prop[n, "creationDate", cr],*node_prop[n, "gender", gr],*node_prop[n, "browserUsed", brw],  *node_prop[n, "email", em], *node_prop[n, "speaks", sp], *edge_label[e, "isLocatedIn"], *edge[e,n,n2],*node_label[n2, "place"], *node_prop[n2, "name", city_name]

# Résultat final
?[person_id, dist, ln, br,  cr, gr, brw, ip,  city_name, companies, universities, em, sp] :=
    filtered[person_id, dist],
    person_info[person_id, ln, br,  cr, gr, brw, ip, em, sp, city_name],
    workplace[person_id, companies],
    studyplace[person_id, universities]


"""

ic3="""

# path Depth 1 : direct friends of person_id 
reach1[person_id, f1] := person_id=1129,
    *edge[e, person_id, f1],
    *edge_label[e, "knows"],
    f1 != person_id

# pathh Depth 2 : friends-of-friends FOF
reach2[person_id, f2] :=
person_id = 1129,
    reach1[person_id, x],
    *edge[e, x, f2],
    *edge_label[e, "knows"],
    f2 != person_id

# Union of friends n FOF 
friends[p] :=
    reach1[person_id, p]
  or reach2[person_id, p]


# Find the country where a Person p lives
person_country[p, country_name] :=
    *edge[e1, p, city],
    *edge_label[e1, "isLocatedIn"],
    *edge[e2, city, country],
    *edge_label[e2, "isPartOf"],
    *node_prop[country, "name", country_name]


# Filter persons who are NOT living in country X or Y(foreigners)
foreign_person[p] :=
country_x = "China",
country_y = "France",
    friends[p],
    person_country[p, ctry],
    ctry != country_x,
    ctry != country_y

# Messages (posts or comments) created by a person respecting a certain ceationDate
message[p, m] :=
start_date =1341100800000,
duration_days =2,
end_date = start_date + duration_days * 86400000,
    *edge[e, m, p],
    *edge_label[e, "hasCreator"],
    *node_prop[m, "creationDate", date],
    date >= start_date,
    date < end_date,
    (
        *node_label[m, "post"]
      or *node_label[m, "comment"]
    )

# Country where a message was created
message_country[m, ctry] :=
    *edge[e1, m, place],
    *edge_label[e1, "isLocatedIn"],
    *edge[e2, place, country],
    *edge_label[e2, "isPartOf"],
    *node_prop[country, "name", ctry]

# Count messages in Country X
msg_count_x[p, count(m)] :=
    country_x = "China",
    foreign_person[p],
    message[p, m],
    message_country[m, ctry],
    ctry = country_x
    
# Count messages in Country Y
msg_count_y[p, count(m)] :=
country_y = "France",
    foreign_person[p],
    message[p, m],
    message_country[m, ctry],
    ctry = country_y
   

# Count persons who posted in BOTH countries
both_counts[p, xcnt, ycnt, cnt] :=
    msg_count_x[p, xcnt],
    msg_count_y[p, ycnt],
    cnt=xcnt+ycnt


# Person identity (firstName, lastName)
person_info[p, fn, ln] :=
    *node_prop[p, "firstName", fn],
    *node_prop[p, "lastName", ln]

# Final result
?[p, fn, ln, xcnt, ycnt, total] :=
    both_counts[p, xcnt, ycnt, total],
    person_info[p, fn, ln]


"""

ic13="""

# Define the subgraph of KNOWS edges
friendEdges[from, to] := *edge[e, from, to], *edge_label[e, "knows"]

# Input nodes (single-row relations)
starting[start_idx] <- [[3528]]
goal[goal_idx]     <- [[8796093026629]]

# Compute shortest path (BFS) between person1 and person2
paths[start, goal, path] <~ ShortestPathBFS(friendEdges[from, to],
                                            starting[start_idx],
                                            goal[goal_idx])

# Output rules:
? [len] := starting[start_idx], goal[goal_idx], start_idx == goal_idx, len = 0
? [path] := starting[start_idx], goal[goal_idx], paths[start_idx, goal_idx, path], len = length(path)
? [len] := starting[start_idx], goal[goal_idx], not paths[start_idx, goal_idx, _], len = -1

"""

ic14= """ 
# Définir le graphe orienté des relations KNOWS
knowsEdges[from, to] :=
    *edge[e, from, to],
    *edge_label[e, "knows"]

# Définir les IDs de départ et d'arrivée
start_person[] <- [[3528]]
end_person[]   <- [[8796093026629]]

# Chercher les 3 plus courts chemins (orientés)
paths[start, end, cost, path] <~ 
    KShortestPathYen(knowsEdges[from, to], start_person[], end_person[], k: 3, undirected: false)

# Générer les paires de noeuds consécutifs pour chaque chemin
pairs[path, a, b] :=
    paths[start, end, cost, path],
    w in windows(path, 2),
    a = get(w, 0),
    b = get(w, 1)

# Nombre de réponses (commentaires) d'une personne A à un post de B
postCount[a, b, count(c)] :=
    *node_label[c, "comment"],
    *edge[e1, c, a],
    *edge_label[e1, "hasCreator"],
    *edge[e2, c, p],
    *edge_label[e2, "replyOf"],
    *node_label[p, "post"],
    *edge[e3, p, b],
    *edge_label[e3, "hasCreator"]

# Nombre de réponses (commentaires) d'une personne A à un commentaire de B
commentCount[a, b, count(c)] :=
    *node_label[c, "comment"],
    *edge[e1, c, a],
    *edge_label[e1, "hasCreator"],
    *edge[e2, c, c2],
    *edge_label[e2, "replyOf"],
    *node_label[c2, "comment"],
    *edge[e3, c2, b],
    *edge_label[e3, "hasCreator"]

# Calcul du poids entre deux personnes A et B
pairWeight[a, b, weight] :=
    postCount[a, b, p1],
    commentCount[a, b, c1],
    postCount[b, a, p2],
    commentCount[b, a, c2],
    weight = p1 * 1.0 + c1 * 0.5 + p2 * 1.0 + c2 * 0.5

# Somme du poids total par chemin 
pathWeight[path, sum(w)] :=
    pairs[path, a, b],
    pairWeight[a, b, w]

# Résultat final : chaque chemin, sa longueur et son poids total
?[path, len, totalWeight] :=
    paths[start, end, cost, path],
    pathWeight[path, totalWeight],
     len= length(path)


"""
#print(client.run(ic14))
 

# # exécuter 10 fois auto 
# n = 10
# times = []

# for _ in range(n):
#     start = time.time()  
#     client.run(ic3)
#     end = time.time()  
#     times.append((end - start) * 1000)  # en ms

# mean = sum(times) / n
# print(f"Temps moyen sur {n} exécutions : {mean:.3f} ms")




# n = 10
# times = []

# for _ in range(n):
#     start = time.time()  
#     client.run(is2)
#     end = time.time()  
#     res =(end - start )* 1000  # en ms
#     print(res)
#     times.append(res)

# mean = sum(times) / n
# print(f"Temps moyen sur {n} exécutions : {mean:.3f} ms")


# --------
# exécuter 10 fois auto , need to import db 
# code = "client.run(is1)"
# duration = timeit.timeit(code, number=10)  
# print("Temps moyen par exécution :", (duration / 10)*1000, "ms")




res = client.run('?[n] := *reified_node[n]')
print(res)

# res = client.run('?[n, k] := *node_prop[n, k,v] , n=94')

# print(res)

# res = client.run('?[n, l] := *node_label[n, l] , l="person"')
# print(res)
# res = client.run('?[ l] := *node_label[1399, l] ')
# print(res)


# res = client.run('?[e, ns, nd] := *edge[e, ns, nd]')
# print(res)

# res = client.run("?[l] := *node_label[143, l]")
# print(res)

# res = client.run("?[n, l] := *edge_label[n, l]")
# print(res)

# res = client.run('?[fn] :=  *edge[id_e,  p1, p2],*edge_label[id_e, "knows"], p1 =94, node_prop[p2, "firstName",fn]')
    
# print(res)

# res = client.run('?[v] :=   n =94, k="firstName", *node_prop[n, k, v]')
    
# print(res)

# res = client.run('::relations')
    
# print(res)