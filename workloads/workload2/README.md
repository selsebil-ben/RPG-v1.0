## Workload 2: Impact of Reification on Queries Without Reification

### Overview

This workload investigates the **indirect impact of reified elements** on the performance of queries that **do not explicitly manipulate them**.

To ensure comparability, we reuse the **same set of queries as in Workload 1**, but execute them over **four different graph representations**:

* **Standard Property Graph (PG)** in CozoDB
* **Reified Property Graph (RPG)** in CozoDB
* **Standard PG** in HO-GDB (without reification)
* **PG with reification** in HO-GDB

The evaluation is conducted on three LDBC SNB datasets with increasing sizes:

* **SF0.1**
* **SF0.3**
* **SF1**

---

### Reified Elements

To perform this evaluation, the datasets are enriched with several types of **reified elements**:

#### 1. Tagged Comments

* A reified node **`taggedComment`** is created for each:

  * `comment` connected to a `tag` via `hasTag`

#### 2. Creator Relationship

* A reified edge **`create`** represents:

  * `forum` connected to `person` via `hasCreator`

---

### Complex Reified Structures

To analyze the impact of **structural complexity**, additional reified elements are introduced:

#### 3. Forum Membership

* A reified node **`forumMembership`** represents:

  * a `forum` and all its `person` members (`hasMember`)
* Property:

  * `nbMember`: total number of members

---

#### 4. Recursive Reification (Multi-level Abstraction)

To introduce hierarchical abstraction:

* **`simpleRepliedComment`**:

  * created when a `comment` replies to another `comment`

* **`repliedComment`**:

  * created when a `comment` replies to a `simpleRepliedComment`
  * extended recursively when replying to another `repliedComment`

This mechanism enables **multi-level recursive reification**.

---

### System Limitations (HO-GDB)

HO-GDB does **not support**:

* edge reification
* recursive reification

Therefore:

* Only **`taggedComment`** and **`forumMembership`** are included in HO-GDB
* These are represented as **subgraph collections**
* Additional elements (**`create`**, **`repliedComment`**) are only supported in RPG (CozoDB)

---
### Queries Description

The evaluation is conducted with **LDBC SNB Queries** (same queries used in Workload1). The textual descriptions of all queries used in this workload are available in:

```
text_queries.txt
```

---

### Query Implementations

The queries are implemented separately for each system:

* **CozoDB** implementation:

```
Query_CozoDB.py
```

* **HO-GDB** implementation:

```
Query_HOGDB.ipynb
```

* **Neo4j** implementation:

```
Query_Neo4j.cypher
```

---
### Objective

The goal of this workload is to:

* Measure the **performance overhead** introduced by reified elements
* Evaluate how reification affects queries that **do not use it directly**
* Analyze the impact of:

  * dataset size
  * number of reified elements
  * structural complexity (including recursion)

---

### Summary

This workload isolates the **cost of adding reification** to a graph, even when queries remain unchanged.
It provides key insights into the **trade-off between expressivity and performance** in graph data models.

---
