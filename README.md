# Reified Property Graph Model

## Model Definition

Our model is an **extension of the Property Graph model** that introduces:

- **Reified nodes**
- **Reified edges**
- **Multi-level abstraction**
- **Operators** to create and query them

A **reified node** or **reified edge** is a representation of a **subgraph** composed of nodes, edges, their labels, and properties.  
This subgraph is encapsulated into a single abstract object — the reified node or edge — which can:

- Have its own `id`, `labels`, and `properties`
- Be connected to other parts of the graph
- Be used to build higher-order structures and abstractions

A **reified node** or **reified edge** is considered as an abstraction level.  
A multi-level abstraction occurs when a reified node or edge contains other reified elements.

> For more details, see the [`/papers`](./papers) folder.

---

## Implementation

1. **Data Benchmarking:**
   - Generate graph data into **Cozo scripts** to construct a standard Property Graph (PG) in [CozoDB](https://cozodb.org)
   - Also convert same data into **CSV files** compatible with Neo4j

2. **Performance Benchmarking:**

   a. *Property Graph Comparison*  
   - Compare **execution time** of equivalent queries on both PG in **Neo4j** and **CozoDB**

   b. *Reified Property Graph Evaluation*  
   - Extend the Cozo PG to a **Reified Property Graph (RPG)** by:
     - Adding reified nodes and edges
     - Introducing nested abstraction levels
   - Measure how query execution time evolves in the **RPG** as we increase:
     - The number of reified nodes
     - The number of reified edges
     - The depth of nested abstractions
       
   c. *Reified Property Graph Comparison*
   - Compare **execution time** and **database insertions** of equivalent queries on both **RPG** and **HO-GDB**

---

## Repository Structure & How to Explore

| Folder | Description |
|--------|-------------|
| [`/rpg-model`](./rpg-model) | Core implementation of the **Reified Property Graph (RPG)** model using CozoDB |
| [`/SNB-Benchmark_processing`](./SNB-Benchmark_processing) | Data processing pipelines for transforming LDBC SNB datasets into different graph models and systems |
| `/SNB-Benchmark_processing/Benchmark_For_Simple_PG` | Generation of a standard Property Graph (PG) across CozoDB, Neo4j, and HO-GDB |
| `/SNB-Benchmark_processing/Benchmark_For_PG+reification` | Generation of a Property Graph with reification (RPG) for CozoDB and HO-GDB |
| [`/workloads`](./workloads) | Definition of experimental workloads, including descriptions and query implementations across systems (CozoDB, Neo4j, HO-GDB) |
| [`/papers`](./papers) | Research publications related to the RPG model (French and English versions) |

---

## Getting Started

To explore and reproduce the experiments:

1. Start by reviewing the workload scenarios and their objectives in [`/workloads`](./workloads)

2. Generate a **standard Property Graph (PG)** using CozoDB by following the pipeline in:
   - [`/SNB-Benchmark_processing/Benchmark_For_Simple_PG/PG_CozoDB`](./SNB-Benchmark_processing/Benchmark_For_Simple_PG/PG_CozoDB)

3. Load the generated PG into Neo4j using:
   - [`/SNB-Benchmark_processing/Benchmark_For_Simple_PG/PG_Neo4j`](./SNB-Benchmark_processing/Benchmark_For_Simple_PG/PG_Neo4j)

4. (Optional) Use HO-GDB representation of the standard PG via:
   - [`/SNB-Benchmark_processing/Benchmark_For_Simple_PG/PG_HO-GD`](./SNB-Benchmark_processing/Benchmark_For_Simple_PG/PG_HO-GD)

5. Upgrade the standard PG into a **Reified Property Graph (RPG)** using CozoDB:
   - [`/SNB-Benchmark_processing/Benchmark_For_PG+reification/PG+reification_CozoDB`](./SNB-Benchmark_processing/Benchmark_For_PG+reification/PG+reification_CozoDB)

6. Generate the corresponding HO-GDB representation of the RPG:
   - [`/SNB-Benchmark_processing/Benchmark_For_PG+reification/PG+reification_HO-GDB`](./SNB-Benchmark_processing/Benchmark_For_PG+reification/PG+reification_HO-GDB)

7. Execute and compare queries across systems using the implementations provided in each workload folder (`cozo/`, `neo4j/`, `hogdb/`)


---
## How to Cite This Work

If you use this work in your research, please cite the following publication:

**APA Format**:
> Benelhaj-Sghaier, S., Gillet, A., & Leclercq, É. (2024). *Knowledge graph multilevel abstraction: A property graph reification based approach*. In *Research Challenges in Information Science* (pp. 12–19). Springer.

**BibTeX**:
```bibtex
@inproceedings{Benelhaj2024, 
  title={Knowledge graph multilevel abstraction: a property graph reification based approach},
  author={Benelhaj-Sghaier, Selsebil and Gillet, Annabelle and Leclercq, {\'E}ric},
  booktitle={International Conference on Research Challenges in Information Science},
  pages={12--19},
  year={2024},
  organization={Springer}
}
```

## Special Thanks

This project is built with love, curiosity, and the goal of exploring abstraction and reification in property graphs.  
Feel free to open an issue or contribute if you're interested in **graph modeling**, **CozoDB**, or **knowledge representation**.

Big thanks to my supervisors for their continuous support and valuable advice 
