from fastapi import FastAPI, File, UploadFile
from app.utils import extract_units_from_inp, convert_to_si, save_results
from app.wntr_runner import run_simulation
from app.gpt_tools import validate_and_convert_txt, ask_gpt_with_results
import tempfile

app = FastAPI()

@app.post("/upload")
def upload_txt(file: UploadFile = File(...)):
    try:
        txt = file.file.read().decode("utf-8")
        if not txt.strip():
            return {"error": "Uploaded file is empty."}
        inp_text = validate_and_convert_txt(txt)
        path = tempfile.mkstemp(suffix=".inp")[1]
        with open(path, 'w') as f:
            f.write(inp_text)
        return {"inp_path": path}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

@app.post("/simulate")
def simulate(inp_path: str):
    raw_results = run_simulation(inp_path)
    unit_system = extract_units_from_inp(inp_path)
    results_si = convert_to_si(raw_results, unit_system)
    saved_paths = save_results(results_si)
    return {"converted": True, "outputs": saved_paths}

@app.post("/query")
def query_analysis(prompt: str):
    return ask_gpt_with_results(prompt)


   
