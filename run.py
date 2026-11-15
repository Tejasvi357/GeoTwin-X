"""
GeoTwin-X: Project Launcher
"""

import sys
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*70)
    print("  🪐 GeoTwin-X: Planetary Analog Search Engine (NASA Space Apps)")
    print("  Server launching on: http://127.0.0.1:8000")
    print("="*70 + "\n")
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=False, app_dir=PROJECT_DIR)
