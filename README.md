# Bird Migration Network Analysis using eBird Data

## Overview

In this project, we study bird migration by modeling it as a **temporal network** built from eBird observation data.  
Rather than following individual birds or constructing simple migration paths, we focus on **population-level migration flows**. This allows us to apply core **network science concepts** such as degree distributions, walks, community structure, and how networks evolve over time.

---

## Why a Network Approach?

Bird migration data consists of many independent observations spread across space and time. If we treat these observations as individual trajectories, the resulting structure often collapses into simple paths with trivial degree distributions, making most network measures meaningless.

By representing migration as a network, we can:
- identify important **migration hubs**
- uncover large-scale **migration corridors**
- compare migration structure across different years

This abstraction makes it possible to analyze migration patterns using the tools taught in network science.

---

## Spatial Clustering: Defining Nodes

### What we do
We first group individual observations into spatial clusters using **DBSCAN**. Each cluster represents a geographic region where birds are consistently observed, and each cluster becomes a **node** in the migration network.

### Why clustering is needed
- Individual GPS points are noisy and overly detailed.
- Clustering converts continuous space into discrete, meaningful regions.
- DBSCAN is particularly suitable because it:
  - does not require specifying the number of clusters in advance
  - identifies dense regions naturally
  - treats isolated observations as noise

### Implementation note
We use a custom DBSCAN implementation with:
- KD-tree acceleration for efficient neighbor searches
- **recursive cluster expansion (neighbors-of-neighbors)**

---

## Temporal Network Construction: Defining Edges

Simply linking clusters in a sequence (A → B → C) results in a **path-like graph** with in-degree and out-degree close to one, which is not useful for network analysis.

### Flow-based network model

Instead, we model migration as **flows between regions over time**.

### Temporal structure
- A separate network is built for each year.
- Within each year, observations are grouped by **month**.
- Edges represent transitions from month *t* to month *t+1*.

### How edge weights are defined
For each pair of consecutive months:
- Every cluster active in month *t* is connected to clusters active in month *t+1*.
- Edge weights are based on **destination attractiveness**, defined as:

\[
w_{u \to v} = \frac{\text{number of birds observed in cluster } v \text{ in month } t+1}{\text{total number of birds observed in month } t+1}
\]

### Why this makes sense
- eBird data reflects **population-level observations**, not tracked individuals.
- Exact origin–destination transitions cannot be reliably inferred.
- This weighting captures where birds tend to **concentrate next**, producing a stable and interpretable migration flow network.

### Edge persistence
Edge weights are accumulated across all month-to-month transitions within a year. As a result:
- persistent migration flows become stronger
- rare or noisy connections have less influence

---

## What the Network Represents

- **Nodes:** spatial clusters (geographic regions)
- **Edges:** directed, weighted migration flows between regions
- **Weights:** fraction of the total bird population moving into a region in the next time window

This naturally leads to:
- migration hubs
- branching and convergence patterns
- meaningful degree and strength distributions

---

## Temporal Scope

Our analysis focuses on **2016–2024**.
- **2015** is excluded due to very limited data coverage.
- **2025** is excluded because it represents a partial year with incomplete migration cycles.

Restricting the analysis to these years ensures fair and consistent comparisons over time.

---

## Community Detection: Migration Corridors

### What we do
For each yearly network:
- the directed graph is converted to an **undirected weighted graph**
- communities are detected using **greedy modularity optimization**

### Why we do this
- Communities correspond to large-scale **migration corridors or subsystems**
- Modularity quantifies how strongly separated these corridors are
- Tracking communities over time allows us to study:
  - whether migration structure is becoming more fragmented or more stable
  - the persistence of major migration pathways across years
 
---

## Node persistence
What it measures:
- Node persistence counts how many years a spatial cluster appears in the migration network, independent of how strongly it is connected in any single year.

How to interpret it:
- High-persistence nodes represent structurally stable migration regions that recur across years, suggesting persistent ecological or geographic importance.
- Low-persistence nodes may reflect transient stopovers, data sparsity, or year-specific migration shifts, and become especially interesting when they briefly achieve high centrality.

What not to claim:
- Persistence does not imply constant importance—some long-lived regions may be consistently peripheral.

---

## Walk-based connectivity (indirect flow structure)

What it measures:
- Counts of length-2 and length-3 walks quantify the abundance of indirect migration pathways through the network, beyond direct month-to-month links.

How to interpret it:
- Higher walk counts indicate a more interconnected and redundant migration structure, where regions are linked through multiple intermediary regions.
- Comparing walk-based connectivity across years reveals whether migration is becoming more diffuse and resilient or more channelized through a few dominant pathways.

What not to claim:
- Walks are not literal bird trajectories; they represent potential structural connectivity implied by aggregated flows.

---

## Betweenness vs in-strength (hub type differentiation)

What it measures:
- This comparison contrasts a node’s role as a destination hub (high in-strength) with its role as a structural connector (high betweenness).

How to interpret it:
- Regions with high in-strength but low betweenness function as endpoints or concentration zones, while regions with moderate in-strength but high betweenness act as bridges between migration corridors.
- This distinction helps explain whether importance arises from attracting many birds or from connecting otherwise weakly linked regions.

What not to claim:
- High betweenness does not imply birds physically pass through the region in sequence—it reflects structural dependency in the network.

---

## Weighted betweenness centrality (migration bottlenecks)

What it measures: 
- Weighted betweenness identifies regions that lie on many shortest weighted paths, highlighting structural bottlenecks in the migration network.

How to interpret it:
- Regions with high weighted betweenness are critical for maintaining overall migration connectivity, and their removal would disproportionately fragment the network.
- Tracking these bottlenecks over time provides insight into the network’s vulnerability and robustness.

What not to claim:
- Bottlenecks are not guaranteed physical choke points; they are abstract connectors in the population-level flow representation.
