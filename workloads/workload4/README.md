## Workload 4: Structural Cost of Reified Elements

### Overview

This workload focuses on comparing the **structural overhead induced by reified elements** in graph data models.

The comparison is performed between:

* The proposed **Reified Property Graph (RPG)** model
* The **HO-GDB** model

---

### Objective

The main goal is to evaluate the **structural cost of representing reified elements**, focusing on a `taggedComment` node as a reference case.

---

### Detailed Analysis

The analysis focuses on the **insertion cost of a reified node of type `taggedComment`**.

Creating such a node involves several structural operations:

* (i) creating the reified node
* (ii) assigning it an `id` property
* (iii) attaching the `taggedComment` label
* (iv) adding its constituent nodes:

  * `Comment`
  * `Tag` (with its property `name`)
* (v) creating the `hasTag` relationship between them

---

### Structural Cost Breakdown

The following table summarizes the number of elements inserted into both the RPG and HO-GDB models for each operation:

| Operation                                 | Added elements in RPG        | Added elements in HO-GDB          |
| ----------------------------------------- | ---------------------------- | --------------------------------- |
| Create reified node / subgraph            | 2 = node + reified_node      | 1 = node                          |
| Add label to reified node / subgraph      | 1 = node_label               | 2 = type_label + _subgraph label  |
| Add property to reified node / subgraph   | 1 = node_prop                | 1 = node property                 |
| Add node to reified node / subgraph       | 1 = n_composed_of_node       | 2 = edge + _node_membership label |
| Add node_label to reified node / subgraph | 1 = n_composed_of_node_label | 1 = node label                    |
| Add node_prop to reified node / subgraph  | 1 = n_composed_of_node_prop  | 1 = node property                 |
| Add edge to reified node / subgraph       | 1 = n_composed_of_edge       | 2 = edge + _edge_membership label |
| Add edge_label to reified node / subgraph | 1 = n_composed_of_edge_label | 1 = edge label                    |
| Add edge_prop to reified node / subgraph  | 1 = n_composed_of_edge_prop  | 1 = edge property                 |

---

### Summary of Structural Cost

Table above summarizes the number of elements inserted into both **CozoDB (RPG)** and **HO-GDB** for each operation.

Based on this breakdown, creating a single `taggedComment` reified node requires:

* **9 elements in the RPG model**
* **11 elements in the HO-GDB model**

---

### Conclusion

This workload highlights that:

> Even for a simple reified structure, the **RPG model introduces a lower structural insertion cost** compared to HO-GDB.

It provides a quantitative basis for analyzing the **storage overhead of reification mechanisms** across graph models.

---
