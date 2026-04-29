
## Workload 1: Establishing a Baseline Without Reification

### Overview

This workload aims to establish a **performance baseline** in the absence of any reification mechanism.

The evaluation is conducted using the **LDBC SNB dataset**, modeled as a **standard Property Graph (PG)** without reified elements. The same dataset and queries are executed across three systems:

* **CozoDB** (our implementation of the RPG model, used here without reification)
* **Neo4j** (standard Property Graph database)
* **HO-GDB** (higher-order graph database, evaluated here in standard PG mode)

The evaluation is conducted on three LDBC SNB datasets with increasing sizes:

* **SF0.1**
* **SF0.3**
* **SF1**

This setup ensures a **fair comparison** by isolating the impact of reification and focusing solely on baseline performance.

---

### Queries Description

We used the **LDBC SNB Queries**. The textual descriptions of all queries used in this workload are available in:

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

* Establish a **baseline performance reference**
* Enable comparison across different graph systems under identical conditions
* Serve as a foundation for evaluating the impact of **reification** in subsequent workloads

---
