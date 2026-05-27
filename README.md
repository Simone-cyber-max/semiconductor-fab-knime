# Semiconductor FAB KNIME — Educational Model v1.0

> Virtual CMOS 90nm Front-End fab simulation with real tool specs, 
> multi-stage process data, and ML-based scrap prediction.
> Free and open source.

![KNIME](https://img.shields.io/badge/KNIME-5.x-yellow)
![License](https://img.shields.io/badge/license-MIT-green)
![Wafers](https://img.shields.io/badge/wafers-500-blue)
![Phases](https://img.shields.io/badge/phases-13-blue)

## What is this?

A fully functional KNIME Analytics Platform workflow that simulates 
a 13-phase CMOS 90nm Front-End semiconductor fab. Built for engineers, 
students, and data scientists who want to learn process data analysis 
without access to real fab data.

## Real tool specs modeled

ASML PAS5500 · ASM A412 · LAM 9400 TCP · AMAT Mirra · AMAT Quantum X ·
KLA 5200 · TEL Lithius · Axcelis Optima · AMAT Vantage · Novellus Concept2

## What's inside

- 500 synthetic wafers · 114 process features · 13 Front-End phases
- SPC drift detection with tool aging simulation
- EDA with Linear Correlation matrix and Box Plots
- ML scrap prediction: Decision Tree · Random Forest · Gradient Boosted Trees
- ROC curve · AUC = 0.714 · threshold optimization
- What-If process optimization (Etch temperature scenarios)
- Cheminformatics descriptors (HF reactivity, SC1 efficiency, Cu potential)

## Files

| File | Description |
|------|-------------|
| `Semiconductor_FAB_KNIME_v1.0.knwf` | KNIME workflow — import directly |
| `fab_v2_dataset.csv` | Synthetic dataset — copy to your KNIME project folder |
| `fab_data_generator.py` | Python script to regenerate the dataset |

## How to use

1. Install [KNIME Analytics Platform](https://www.knime.com/downloads) 5.x
2. Impo
