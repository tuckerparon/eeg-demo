import mne
import pandas as pd
from config import DATA_DIR, EDF_FILE_PATH

# Load your EDF file
raw = mne.io.read_raw_edf(f'{DATA_DIR}/{EDF_FILE_PATH}.edf', preload=True)

# Get raw data and times
data, times = raw.get_data(return_times=True)  # data shape: (n_channels, n_samples)

# Convert from volts to microvolts
data_uv = data * 1e6

# Transpose so each row is a time point, each column is a channel
df = pd.DataFrame(data_uv.T, columns=raw.ch_names)

# Add time as first column
df.insert(0, "Time (s)", times)

# Save to CSV
df.to_csv(f'{DATA_DIR}/{EDF_FILE_PATH}.csv', index=False)
print("Saved EEG data to eeg_raw_data.csv")