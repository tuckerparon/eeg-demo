# config.py
# Folder to save plots
PLOT_DIR = "plots"

# Folder to save data
DATA_DIR = "data"

# Path to your EDF file
EDF_FILE_PATH = "S001R01"

# EEG frequency bands of interest
EEG_BANDS = {
    "Delta": (0.5, 4),
    "Theta": (4, 8),
    "Alpha": (8, 12),
    "Beta": (12, 30),
    "Gamma": (30, 45),
}

# Facial EEG channels that are typically free of hair and usable with adhesive electrodes
FACIAL_CHANNELS = [
    # Forehead (Prefrontal)
    "Fp1.", "Fp2.", "Fpz.",

    # Anterior Frontal (just above the eyebrows)
    "Af7.", "Af3.", "Afz.", "Af4.", "Af8.",

    # Frontal (mid-forehead and sides)
    "F7..", "F5..", "F3..", "F1..", "Fz..", "F2..", "F4..", "F6..", "F8..",
]