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

| Folder                          | Description                                                                 |
|---------------------------------|-----------------------------------------------------------------------------|
| [`/_1_Workloads Design & Objectives`](./_1_Workloads_Design_&_Objectives)| Explain the senario of each workload and its objective|
| [`/_2_Benchmark_PG_CozoDB`](./_2_Benchmark_PG_CozoDB)     | Generate graph data into Cozo scripts to build a standard PG in cozoDB|
| [`/_3_PG_from_cozoDB_to_Neo4j`](./_3_PG_from_cozoDB_to_Neo4j) | Scripts to convert Cozo scripts into CSV files for Neo4j                  |
| [`/_4_RPG_cozoDB`](./_4_RPG_cozoDB) | Scripts to upgrade the standard PG into a Reified Property Graph (RPG)     |
| [`/_5_RPG_HOGDB`](./_5_RPG_HOGDB) | Scripts to convert Cozo scripts of an RPG into  HO-GDB    |
| [`/_6_Queries_&_Results`](./_6_Queries_&_Results) | Query scripts and experimental results             |

---

## Getting Started

To get started:

1. have a look on workloads design and their objectives in [`/_1_Workloads Design & Objectives`](./_1_Workloads_Design_&_Objectives)
2. Follow the setup instructions in [`/_2_Benchmark_PG_CozoDB`](./_2_Benchmark_PG_CozoDB) to get the standard PG in cozoDB
3. Load the standrd PG into Neo4j using the CSV files from [`/_3_PG_from_cozoDB_to_Neo4j`](./_3_PG_from_cozoDB_to_Neo4j)
4. Add reified elments with [`/_4_RPG_cozoDB`](./_4_RPG_cozoDB)
5. Use the standard PG in Neo4j and add subgraph nodes to get a HO-GDB using [`/_5_RPG_HOGDB`](./_5_RPG_HOGDB) 
6. Analyze performance using queries in [`/_6_Queries_&_Results`](./_6_Queries_&_Results)

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
