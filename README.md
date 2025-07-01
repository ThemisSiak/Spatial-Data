# Spatial Data Indexing and Nearest Neighbor Search

This project implements two key techniques in spatial data management:
- **Sort-Tile-Recursive (STR) Bulk Loading** of an R-tree
- **Incremental Nearest Neighbor Search** using a Best-First traversal

It was developed as part of the course ΜΥΕ041 - Διαχείριση Σύνθετων Δεδομένων at the University of Ioannina.

## Features

- Uses 1024-byte nodes, supports leaf and internal nodes
- Calculates:
  - Tree height
  - Number of nodes per level
  - Average MBR area per level
- Outputs a custom text-based R-tree format
- Performs incremental k-NN search with live priority queue output

## How to Run

```bash
# Build the R-tree
python meros1.py output_tree.txt

# Run k-NN Search
python meros2.py output_tree.txt 39.7 116.5 5
```

## Input Format

- Input file: `Beijing_restaurants.txt`
- First line: number of records
- Following lines: `x y` coordinates (one per restaurant)

## Output Format

Tree file:
```
<root-node-id>
<node-id>, <n>, <f>, (ptr1, geo1), (ptr2, geo2), ...
```

Example:
```
0
0, 2, 0, (1, x1 y1 x2 y2), (2, x1 y1 x2 y2)
1, 2, 1, (101, x y), (102, x y)
```

##  Notes

- Does **not** depend on `pandas` or interactive tools
- Works with alternate input files
- Designed to simulate memory/disk blocks via array/vector node management

---

## Author

- Themistokleia Siakavara

---
