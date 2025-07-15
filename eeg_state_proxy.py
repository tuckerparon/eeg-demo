import pandas as pd
import numpy as np
import os
from config import EDF_FILE_PATH, PLOT_DIR

# Load band power data
band_power_file = os.path.join(PLOT_DIR, f"{EDF_FILE_PATH}_band_powers.csv")
df = pd.read_csv(band_power_file)

# Calculate Proxies
df['Fear_BetaAlpha'] = df['Beta'] / df['Alpha']
df['Flow_ThetaAlpha'] = df['Theta'] / df['Alpha']

# -----------------------------
# INTERPRETATION GUIDELINES:
#
# 1. FEAR: Beta / Alpha Ratio
#    - Proxy: Heightened beta relative to alpha has been linked to increased anxiety or fear response.
#    - Guideline (these are placeholders not based on research.):
#         - ~1.5–2.5 = Moderate arousal
#         - >2.5     = Elevated anxiety/fear response
#    - Source: https://www.sciencedirect.com/science/article/pii/S0975947624002092
#      ("An increase in the alpha/beta ratio indicates a more relaxed state" - I interpreted the opposite of this as fear)
#
# 2. FLOW: Theta / Alpha Ratio
#    - Proxy: Higher theta relative to alpha linked to flow state in tasks involving immersion and creativity.
#    - Guideline (these are placeholders not based on research.):
#         - ~2.5–3.5 = Possible flow
#         - >3.5     = High engagement / potential flow state
#    - Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC5855042/
#      ("From the results, the flow state was characterized by increased theta activities in the frontal areas and moderate alpha activities in the frontal and central areas")
# -----------------------------

# Save proxies to CSV
output_path = os.path.join(PLOT_DIR, f"{EDF_FILE_PATH}_state_proxies.csv")
df[['Channel', 'Fear_BetaAlpha', 'Flow_ThetaAlpha']].to_csv(output_path, index=False)

# Print summary
print("\n--- Summary Proxies ---")
print(f"Fear_Beta/Alpha: {df['Fear_BetaAlpha'].mean():.4f}")
print(f"Flow_Theta/Alpha: {df['Flow_ThetaAlpha'].mean():.4f}")