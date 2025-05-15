
import wntr

def run_simulation(inp_path):
    wn = wntr.network.WaterNetworkModel(inp_path)
    sim = wntr.sim.WNTRSimulator(wn)
    results = sim.run_sim()
    return results
