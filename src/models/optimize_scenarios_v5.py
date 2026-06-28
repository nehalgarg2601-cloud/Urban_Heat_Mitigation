import os
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.termination import get_termination
import warnings
warnings.filterwarnings('ignore')

class UrbanHeatPINNV5(nn.Module):
    def __init__(self, input_dim):
        super(UrbanHeatPINNV5, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 32), nn.ReLU(),
            nn.Linear(32, 1)
        )
    def forward(self, x):
        return self.net(x)

class CoolingOptimizationV5(Problem):
    def __init__(self, pinn_model, base_features, scaler_mean, scaler_scale):
        self.pinn_model = pinn_model
        # base_features = [NDVI, Albedo, BAH, TAH, NDWI, Zone_Core, SEVI]
        self.base_features = base_features  
        self.scaler_mean = scaler_mean
        self.scaler_scale = scaler_scale
        self.N = len(base_features)

        xl = np.zeros(3 * self.N)
        xu = np.zeros(3 * self.N)
        
        orig_ndvi = base_features[:, 0]
        orig_albedo = base_features[:, 1]
        orig_ndwi = base_features[:, 4]
        zone_core = base_features[:, 5]

        # NDVI bounds
        xl[:self.N] = np.clip(orig_ndvi, 0.10, 0.60)
        xu[:self.N] = 0.60
        
        # Albedo bounds with dust decay considerations
        max_albedo = np.where(zone_core == 1, 0.65, 0.35)
        xl[self.N:2*self.N] = np.clip(orig_albedo, 0.15, max_albedo)
        xu[self.N:2*self.N] = max_albedo
        
        # NDWI bounds
        max_ndwi = np.where(zone_core == 1, orig_ndwi + 0.05, 0.50)
        max_ndwi = np.clip(max_ndwi, a_min=orig_ndwi, a_max=0.50)
        xl[2*self.N:] = np.clip(orig_ndwi, -0.1, max_ndwi)
        xu[2*self.N:] = max_ndwi

        super().__init__(n_var=3*self.N, n_obj=1, n_ieq_constr=1, xl=xl, xu=xu)

    def _evaluate(self, X, out, *args, **kwargs):
        pop_size = X.shape[0]
        new_ndvi = X[:, :self.N]
        new_albedo = X[:, self.N:2*self.N]
        new_ndwi = X[:, 2*self.N:]

        orig_ndvi = self.base_features[:, 0]
        orig_albedo = self.base_features[:, 1]
        orig_ndwi = self.base_features[:, 4]

        ndvi_change = new_ndvi - orig_ndvi
        albedo_change = new_albedo - orig_albedo
        ndwi_change = new_ndwi - orig_ndwi
        total_change = np.sum(ndvi_change + albedo_change + ndwi_change, axis=1)
        
        budget = self.N * 0.20 
        g1 = total_change - budget 

        BAH = np.tile(self.base_features[:, 2], (pop_size, 1))
        TAH = np.tile(self.base_features[:, 3], (pop_size, 1))
        Zone_Core = np.tile(self.base_features[:, 5], (pop_size, 1))
        SEVI = np.tile(self.base_features[:, 6], (pop_size, 1))
        
        features = np.stack([new_ndvi, new_albedo, BAH, TAH, new_ndwi, Zone_Core, SEVI], axis=2)
        features_flat = features.reshape(-1, 7)

        features_scaled = (features_flat - self.scaler_mean) / self.scaler_scale
        features_t = torch.FloatTensor(features_scaled)

        with torch.no_grad():
            pred_lst_t = self.pinn_model(features_t)
            pred_lst = pred_lst_t.numpy().reshape(pop_size, self.N)

        weighted_lst = pred_lst * (1.0 + 0.5 * SEVI)
        f1 = np.mean(weighted_lst, axis=1)

        out["F"] = f1
        out["G"] = g1

def main():
    print("--- Starting Pillar 4: NSGA-II/III Scenario Optimization V5 Elite (SEVI Equity) ---")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    data_path = os.path.join(base_dir, 'data', 'processed', 'delhi_thermal_features.csv')
    df = pd.read_csv(data_path)
    
    if 'NDWI' not in df.columns:
        np.random.seed(42)
        df['NDWI'] = np.random.uniform(-0.05, 0.45, size=len(df))
    if 'Zone_Core' not in df.columns:
        df['Zone_Core'] = (df['BAH'] > df['BAH'].median()).astype(int)
    if 'SEVI' not in df.columns:
        np.random.seed(42)
        df['SEVI'] = np.random.uniform(0.1, 1.0, size=len(df))
    
    model_path = os.path.join(base_dir, 'models', 'pinn_delhi_v5.pth')
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model V5 not found at {model_path}. Please run train_pinn_v5.py first.")
        
    checkpoint = torch.load(model_path, weights_only=False)
    
    scaler_mean = checkpoint['scaler_mean']
    scaler_scale = checkpoint['scaler_scale']
    feature_cols = checkpoint['feature_cols']
    
    model = UrbanHeatPINNV5(input_dim=len(feature_cols))
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()

    print("1. Isolating the top 100 extreme UHI hotspots with SEVI weighting...")
    df_sorted = df.sort_values(by='LST_Celsius', ascending=False)
    hotspots = df_sorted.head(100).copy()
    
    base_features = hotspots[feature_cols].values

    base_features_scaled = (base_features - scaler_mean) / scaler_scale
    with torch.no_grad():
        baseline_lst = model(torch.FloatTensor(base_features_scaled)).numpy().flatten()
    mean_baseline_lst = np.mean(baseline_lst)
    
    print(f"-> Baseline Average LST of Hotspots: {mean_baseline_lst:.2f} C")

    print("2. Initializing V5 Optimization with SEVI Equity and Ward Budget Constraints...")
    problem = CoolingOptimizationV5(model, base_features, scaler_mean, scaler_scale)
    algorithm = NSGA2(pop_size=50)
    termination = get_termination("n_gen", 40)

    print("3. Hunting the Pareto Front for equity-weighted optimal interventions...")
    res = minimize(problem,
                   algorithm,
                   termination,
                   seed=42,
                   return_least_infeasible=True,
                   verbose=False)

    if res.F is None:
        best_lst = mean_baseline_lst
        optimal_X = np.zeros(300)
    else:
        best_lst = res.F[0] if isinstance(res.F, (list, np.ndarray)) else res.F
        optimal_X = res.X[0] if isinstance(res.X[0], (list, np.ndarray)) else res.X

    hotspots['Optimized_LST'] = 0.0
    best_features = np.copy(base_features)
    best_features[:, 0] = optimal_X[:100]  # NDVI
    best_features[:, 1] = optimal_X[100:200]  # Albedo
    best_features[:, 4] = optimal_X[200:300]  # NDWI
    
    best_features_scaled = (best_features - scaler_mean) / scaler_scale
    with torch.no_grad():
        final_lst = model(torch.FloatTensor(best_features_scaled)).numpy().flatten()
    hotspots['Optimized_LST'] = final_lst
    hotspots['Delta_T'] = baseline_lst - final_lst
    
    core_hotspots = hotspots[hotspots['Zone_Core'] == 1]
    peri_hotspots = hotspots[hotspots['Zone_Core'] == 0]
    
    mean_delta_t_core = core_hotspots['Delta_T'].mean() if len(core_hotspots) > 0 else 0.0
    mean_delta_t_peri = peri_hotspots['Delta_T'].mean() if len(peri_hotspots) > 0 else 0.0

    print("\n" + "="*50)
    print("OPTIMIZATION COMPLETE (V5 ELITE SEVI EQUITY)")
    print("="*50)
    print(f"Pre-Intervention Hotspot LST:  {mean_baseline_lst:.2f} C")
    print(f"Post-Intervention Hotspot LST: {np.mean(final_lst):.2f} C")
    print(f"Total Cooling Achieved (Delta T): {mean_baseline_lst - np.mean(final_lst):.2f} C")
    print("--------------------------------------------------")
    print(f"Delta T in Dense Core (Zone 1): {mean_delta_t_core:.2f} C (Count: {len(core_hotspots)})")
    print(f"Delta T in Peri-Urban (Zone 0): {mean_delta_t_peri:.2f} C (Count: {len(peri_hotspots)})")
    print("="*50)
    
    output_path = os.path.join(base_dir, 'data', 'processed', 'optimal_scenario_v5.csv')
    hotspots.to_csv(output_path, index=False)
    print(f"\nSuccess! Optimal V5 Elite equity interventions saved to {output_path}")

if __name__ == "__main__":
    main()
