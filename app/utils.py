import pandas as pd
import re

def extract_units_from_inp(inp_path):
    with open(inp_path, "r") as f:
        lines = f.readlines()
    for line in lines:
        if "Units" in line:
            match = re.search(r"Units\s+(\w+)", line, re.IGNORECASE)
            if match:
                return match.group(1).upper()
    return "LPS"

def convert_to_si(results, unit):
    flow_factors = {"GPM": 0.0630902, "MGD": 43.812636, "CFS": 28.3168466, "LPS": 1, "LPM": 1/60, "MLD": 11.5741}
    length_factors = {"GPM": 0.3048, "CFS": 0.3048, "MGD": 0.3048, "LPS": 1, "LPM": 1, "MLD": 1}
    ff = flow_factors.get(unit, 1)
    lf = length_factors.get(unit, 1)
    return {
        "pressure": results.node["pressure"] * lf,
        "head": results.node["head"] * lf,
        "demand": results.node["demand"] * ff,
        "flowrate": results.link["flowrate"] * ff,
        "velocity": results.link["velocity"]
    }

def save_results(results):
    paths = {}
    for k, df in results.items():
        path = f"/mnt/data/{k}_si.csv"
        df.to_csv(path)
        paths[k] = path
    return paths
