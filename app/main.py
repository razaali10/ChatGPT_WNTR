from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from app.wntr_runner import run_simulation
from app.gpt_tools import validate_and_convert_txt, ask_gpt_with_results
from app.utils import save_results, summarize_results_for_gpt
import tempfile
import os

app = FastAPI()

class InpContent(BaseModel):
    content: str

@app.get("/")
def health():
    return {"status": "API is live"}

@app.post("/simulate_epanet_text")
def simulate_epanet_text(inp: InpContent):
    try:
        inp_text = validate_and_convert_txt(inp.content)
        path = tempfile.mkstemp(suffix=".inp")[1]
        with open(path, 'w') as f:
            f.write(inp_text)

        raw_results = run_simulation(path)
        os.makedirs("results", exist_ok=True)
        saved_paths = save_results(raw_results, folder="results")

        summary_text = summarize_results_for_gpt(raw_results, "unknown")
        response = ask_gpt_with_results(summary_text)

        samples = {k: v.head(3).to_dict() for k, v in raw_results.items()}

        return {
            "gpt_summary": response,
            "data_samples": samples,
            "result_paths": saved_paths
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


      

    





   
