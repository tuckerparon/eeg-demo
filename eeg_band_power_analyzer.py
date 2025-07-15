import mne
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from config import EDF_FILE_PATH, DATA_DIR, PLOT_DIR, EEG_BANDS, FACIAL_CHANNELS

# Load the EDF file
raw = mne.io.read_raw_edf(f'{DATA_DIR}/{EDF_FILE_PATH}.edf', preload=True)

# Apply bandpass filter to remove slow drift and high-freq noise
raw.filter(0.5, 45, fir_design="firwin")

# Pick only the facial channels
raw.pick_channels(FACIAL_CHANNELS)

# Compute PSD using Welch’s method
psds = raw.compute_psd(
    method="welch",
    fmin=0.5,
    fmax=45,
    n_fft=512,
    n_per_seg=320,
    n_overlap=160,
)
freqs = psds.freqs
psds = psds.get_data()

# Plot and save PSD figures
for i, ch_name in enumerate(raw.ch_names):
    plt.figure(figsize=(10, 5))
    plt.semilogy(freqs, psds[i], label=ch_name)
    plt.title(f"Power Spectral Density - {ch_name}")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power (uV^2/Hz)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{PLOT_DIR}/{EDF_FILE_PATH}_PSD_{ch_name.replace('.', '')}.png")
    plt.close()

# Function to compute total power in a band using integration (trapz)
def band_power(psds, freqs, band):
    low, high = band
    idx = np.logical_and(freqs >= low, freqs <= high)
    if not np.any(idx):  # safety check
        return np.zeros(psds.shape[0])
    return np.trapz(psds[:, idx], freqs[idx], axis=1)

# Create a dictionary to hold results
band_power_dict = {'Channel': raw.ch_names}

# Compute band power for each band and channel
print("\n--- EEG Band Powers (µV^2/Hz) ---")
for band_name, band_range in EEG_BANDS.items():
    power = band_power(psds, freqs, band_range)
    band_power_dict[band_name] = power
    print(f"\n{band_name} Band ({band_range[0]}–{band_range[1]} Hz):")
    for ch, val in zip(raw.ch_names, power):
        print(f"{ch}: {val:.2e}")

# Save results to CSV
df = pd.DataFrame(band_power_dict)
csv_path = os.path.join(PLOT_DIR, f"{EDF_FILE_PATH}_band_powers.csv")
df.to_csv(csv_path, index=False, float_format="%.2e")
