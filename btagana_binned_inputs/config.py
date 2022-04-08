import numpy as np

plot_params = {
    "Jet_pt": { "BINS": np.linspace( 20, 250, 15 ), "LATEX": "Jet\ p_T" },
    "Jet_eta": { "BINS": np.linspace( -2.4, 2.4, 25 ), "LATEX": "Jet\ \eta" },
    "nJ": { "BINS": np.linspace( 0, 20, 21 ), "LATEX": "N_j" },
    "nB": { "BINS": np.linspace( 0, 20, 21 ), "LATEX": "N_b" },
    "dz": { "BINS": np.linspace( 0, 0.005, 51 ), "LATEX": "\Delta z" },
}

wp = {
    "deepCSV": {
        "LOOSE": 0.1355,
        "MEDIUM": 0.4506,
        "TIGHT": 0.7738
    },
    "deepJet": {
        "LOOSE": 0.0532,
        "MEDIUM": 0.3040,
        "TIGHT": 0.7476
    }
}

bdiscs = {
    "deepCSV": [
        "Jet_DeepCSVb", "Jet_DeepCSVbb"
    ],
    "deepJet": [
        "Jet_DeepFlavourB", "Jet_DeepFlavourBB", "Jet_DeepFlavourLEPB"
    ]
}