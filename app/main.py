from fastapi import FastAPI, File, UploadFile
from app.utils import extract_units_from_inp, convert_to_si, save_results, summarize_results_for_gpt
from app.wntr_runner import run_simulation
from app.gpt_tools import validate_and_convert_txt, ask_gpt_with_results
import tempfile
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "✅ EPANET-WNTR API is alive"}

@app.post("/simulate_epanet")
def simulate_epanet(file: UploadFile = File(...)):
    try:
        txt = file.file.read().decode("utf-8")
        if not txt.strip():
            return {"error": "Uploaded file is empty."}
        inp_text = validate_and_convert_txt(txt)
        path = tempfile.mkstemp(suffix=".inp")[1]
        with open(path, 'w') as f:
            f.write(inp_text)

        raw_results = run_simulation(path)
        unit_system = extract_units_from_inp(path)
        results_si = convert_to_si(raw_results, unit_system)

        os.makedirs("results", exist_ok=True)
        saved_paths = save_results(results_si, folder="results")

        summary_text = summarize_results_for_gpt(results_si, unit_system)
        response = ask_gpt_with_results(summary_text)

        samples = {k: v.head(3).to_dict() for k, v in results_si.items()}

        return {
            "unit_system": unit_system,
            "gpt_summary": response,
            "data_samples": samples,
            "result_paths": saved_paths
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

    





   
