from pathlib import Path

# File Paths

# Data directory (relative to project root)
DATA_DIR = Path("data")

# Species-specific data files
BKPWAR_PATH = DATA_DIR / "ebd_bkpwar_smp_relOct-2025" / "ebd_bkpwar_smp_relOct-2025.txt"

# Output paths
OUTPUT_DIR = Path("output")
GRAPH_PICKLE = OUTPUT_DIR / "migration_graph.gpickle"
NODES_CSV = OUTPUT_DIR / "migration_nodes.csv"
EDGES_CSV = OUTPUT_DIR / "migration_edges.csv"
NETWORK_HTML = OUTPUT_DIR / "migration_network.html"

# EBIRD COLUMN NAMES

BIRD_COLS = [
    "GLOBAL UNIQUE IDENTIFIER",
    "OBSERVATION DATE",
    "COMMON NAME",
    "OBSERVATION COUNT",
    "COUNTRY",
    "STATE",
    "COUNTY",
    "LOCALITY",
    "LATITUDE",
    "LONGITUDE",
]

# Renamed columns for easier access
COL_RENAME = {
    "GLOBAL UNIQUE IDENTIFIER": "id",
    "OBSERVATION DATE": "date",
    "COMMON NAME": "species",
    "OBSERVATION COUNT": "count",
    "LATITUDE": "lat",
    "LONGITUDE": "lon",
}

# Analysis Parameters

# Time filtering
YEARS_RECENT = 10  # Focus on most recent N years

# Spatial clustering (DBSCAN)
GRID_PRECISION_DEG = 0.01  # ~1.1 km grid cells for aggregation
EPS_KM = 25                # DBSCAN neighborhood radius in km
MIN_SAMPLES = 3            # Minimum points to form a cluster

# Temporal network construction
K_EDGES = 10               # Minimum outgoing edges per cluster
MIN_FRAC = 0.1             # Keep edges ≥ 10% of strongest connection

# Visualization
FIGSIZE_STANDARD = (12, 6)
FIGSIZE_LARGE = (14, 8)