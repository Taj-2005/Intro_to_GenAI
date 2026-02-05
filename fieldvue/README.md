# Measure Interior/Exterior (Notebook)

This folder contains a Python-first Jupyter pipeline that estimates depth, builds a point cloud, detects planes/objects, and produces **approximate real-world measurements** (meters) from:

- a single RGB image (monocular, scale requires calibration),
- a short set of photos (multi-view, COLMAP SfM/MVS),
- RGB-D / SLAM-style inputs (metric if sensor provides).

## Files

- `measure_interior_exterior.ipynb`: main notebook (run this)
- `requirements.txt`: Python dependencies
- `sample_data/`: small demo image set (5 images)
- `Depth-Anything-V2/`: depth model source + checkpoints (used by notebook)

## Quickstart (recommended)

1. Create/activate a Python environment (venv/conda) compatible with your OS.
2. Install Python deps:

```bash
pip install -r requirements.txt
```

3. Open the notebook in VS Code or Jupyter:

- VS Code: open `measure_interior_exterior.ipynb` and run cells top-to-bottom.
- Jupyter: `jupyter lab` → open the notebook.

## Notes on heavy dependencies

- **COLMAP** is typically installed via system package managers.
  - macOS: `brew install colmap`
  - Ubuntu: `sudo apt-get install colmap` (or build from source for newer versions)
- **Detectron2** and **PlaneRCNN** are optional in the notebook and may be difficult on macOS/Python versions.
  - The notebook defaults to a pure-Python semantic segmentation fallback using `transformers` when Detectron2 is unavailable.

## Data & privacy

Avoid uploading sensitive interior photos to third-party services. This notebook is designed to run locally.

