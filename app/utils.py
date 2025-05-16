import os

def save_results(results, folder="results"):
    paths = {}
    for k, df in results.items():
        path = os.path.join(folder, f"{k}.csv")
        df.to_csv(path)
        paths[k] = path
    return paths

def summarize_results_for_gpt(results, unit):
    summary = f"Simulation results (unit: {unit}):\n"
    for name, df in results.items():
        try:
            head = df.head(3).to_markdown()
        except Exception:
            head = df.head(3).to_string()
        summary += f"\n{name.upper()} Sample:\n{head}\n"
    summary += "\nSummarize and analyze the system performance based on this data."
    return summary
