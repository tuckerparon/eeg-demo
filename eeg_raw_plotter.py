import mne
import matplotlib.pyplot as plt
import os

from config import DATA_DIR, PLOT_DIR, EDF_FILE_PATH, FACIAL_CHANNELS 

# Load the EDF file
raw = mne.io.read_raw_edf(f"{DATA_DIR}/{EDF_FILE_PATH}.edf", preload=True)

# Select only the facial channels that are present in the raw data
available_facial_channels = [ch for ch in FACIAL_CHANNELS if ch in raw.ch_names]
raw.pick(available_facial_channels)

# Apply bandpass filter to remove slow drift and high-frequency noise
raw.filter(0.5, 45, fir_design="firwin")

# Create plot directory
plot_dir = "plots"
os.makedirs(plot_dir, exist_ok=True)

# Plot and save raw data
fig = raw.plot(n_channels=len(available_facial_channels), scalings='auto', show=True)
fig.savefig(os.path.join(plot_dir, f"{EDF_FILE_PATH}.png")) # for static save
plt.show() # for interactive

