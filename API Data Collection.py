import time
from pathlib import Path
import requests

Ciks= {
    "intel": "0000050863",
    "amd": "0001045810",
    "nvidia": "0000002488"
}

base_dir=Path("data/raw")
start_yr=2021