## Workload 3: Performance of Reification-Aware Queries

### Overview

This workload evaluates the performance of **queries that explicitly exploit reification mechanisms**.

The proposed **RPG model implemented in CozoDB** is compared against the **HO-GDB model implemented in Neo4j**. The evaluation is conducted on three LDBC SNB datasets of increasing scale:

* **SF0.1**
* **SF0.3**
* **SF1**
---

### Evaluation Focus

This scenario analyzes the impact of key parameters related to reification:

* **P1:** Number of reified nodes
* **P2:** Number of reified edges
* **P3:** Number of elements composing a reified element
* **P4:** Depth of multi-level abstractions

These parameters allow us to study how different aspects of reification affect query performance.
---

### Queries Description
for each key parameters, we proposed aa set of queries. The textual descriptions of all queries used in this workload are available in:

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

---

### Reified Elements

As in previous workloads, the SNB datasets are enriched (when applicable) with:

* **`taggedComment`** → reified nodes representing tagged comments
* **`forumMembership`** → reified nodes representing forum membership structures
* **`repliedComment`** → multi-level recursive reified nodes
* **`create`** → reified edges representing creation relationships

---

### Query Coverage and System Constraints

Due to the limitations of the HO-GDB model:

* Supported queries:

  * **R1**
  * **R2**
  * **R5**

* Not supported in HO-GDB (only in RPG):

  * **R3**
  * **R4**
  * **R6**

---

### Objective

The main goal of this workload is to:

* Evaluate the **performance of reification-aware queries**
* Study the impact of structural reification parameters (P1–P4)
* Compare **expressivity vs performance trade-offs** between RPG and HO-GDB
* Demonstrate the advantages of the proposed RPG model for advanced graph querying



