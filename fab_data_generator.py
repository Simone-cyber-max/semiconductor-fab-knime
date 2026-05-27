"""
=============================================================================
Semiconductor FAB KNIME — Synthetic Data Generator v2.0
=============================================================================
Project : Semiconductor FAB KNIME (Educational Model)
Process : CMOS 90nm Front-End — 13 phases
Wafers  : 500
Features: 114 columns
Tools   : ASML PAS5500, AMAT Mirra, LAM 9400 TCP, KLA 5200,
          TEL Lithius, Aviza Atmos, ASM A412, AMAT Quantum X,
          Axcelis Optima, Akrion Gamma, AMAT Vantage, AMAT Producer,
          AMAT Endura
Author  : Simone Scavo
GitHub  : github.com/[tuo-user]/semiconductor-fab-knime
License : MIT — 2026
=============================================================================

PHASES:
  F01 — Pre-clean & substrate prep       (Akrion Gamma wet bench)
  F02 — STI oxidation                    (Aviza Atmos furnace)
  F03 — Gate oxidation                   (ASM A412 furnace)
  F04 — Poly-Si deposition               (AMAT Producer LPCVD)
  F05 — Gate lithography                 (ASML PAS5500 + TEL Lithius)
  F06 — Poly gate etch + wet clean       (LAM 9400 TCP + Akrion Gamma)
  F07 — LDD ion implant                  (AMAT Quantum X)
  F08 — Spacer CVD + etch               (AMAT Producer + LAM 9400)
  F09 — S/D implant + RTA               (Axcelis Optima + AMAT Vantage)
  F10 — Silicidation CoSi2              (AMAT Endura PVD)
  F11 — ILD CVD + CMP                   (AMAT Producer + AMAT Mirra)
  F12 — Contact etch + W-plug           (LAM 9400 + Novellus Concept2)
  F13 — Metal-1 PVD + CMP              (AMAT Endura + AMAT Mirra)

OUTPUT:
  fab_synthetic_500w_13ph.csv
  - 500 rows (wafers)
  - 114 columns (process parameters + cheminformatics + quality flags)
=============================================================================
"""

import numpy as np
import pandas as pd

# ── Reproducibility ──────────────────────────────────────────────────────────
SEED = 42
np.random.seed(SEED)
N = 500  # wafers

# ── Tool lists per phase ──────────────────────────────────────────────────────
F01_TOOLS = ["AkrionGamma_01", "AkrionGamma_02", "AkrionGamma_03"]
F02_TOOLS = ["AvizaAtmos_01", "AvizaAtmos_02"]
F03_TOOLS = ["ASM_A412_01", "ASM_A412_02", "ASM_A412_03"]
F04_TOOLS = ["AMAT_Producer_01", "AMAT_Producer_02"]
F05_TOOLS = ["ASML_PAS5500_01", "ASML_PAS5500_02"]
F05_TRACK = ["TEL_Lithius_01", "TEL_Lithius_02"]
F06_DRY_TOOLS = ["LAM_9400TCP_01", "LAM_9400TCP_02", "LAM_9400TCP_03"]
F06_WET_TOOLS = ["AkrionGamma_04", "AkrionGamma_05"]
F07_TOOLS = ["AMAT_QuantumX_01", "AMAT_QuantumX_02"]
F08_CVD_TOOLS = ["AMAT_Producer_03", "AMAT_Producer_04"]
F08_ETCH_TOOLS = ["LAM_9400TCP_04", "LAM_9400TCP_05"]
F09_IMP_TOOLS = ["Axcelis_Optima_01", "Axcelis_Optima_02"]
F09_RTA_TOOLS = ["AMAT_Vantage_01", "AMAT_Vantage_02"]
F10_TOOLS = ["AMAT_Endura_01", "AMAT_Endura_02"]
F11_CVD_TOOLS = ["AMAT_Producer_05", "AMAT_Producer_06"]
F11_CMP_TOOLS = ["AMAT_Mirra_01", "AMAT_Mirra_02", "AMAT_Mirra_03"]
F12_ETCH_TOOLS = ["LAM_9400TCP_06", "LAM_9400TCP_07"]
F12_CVD_TOOLS = ["Novellus_Concept2_01", "Novellus_Concept2_02"]
F13_PVD_TOOLS = ["AMAT_Endura_03", "AMAT_Endura_04"]
F13_CMP_TOOLS = ["AMAT_Mirra_04", "AMAT_Mirra_05"]

SHIFTS = ["Day", "Afternoon", "Night"]

# ── Helper: tool-aging drift ──────────────────────────────────────────────────
def aging_drift(batch_idx, amplitude=0.03):
    """Simulate tool aging: slow linear drift + random noise over batch index."""
    return amplitude * (batch_idx / N) + np.random.normal(0, amplitude * 0.2, N)


# ── Batch / lot metadata ──────────────────────────────────────────────────────
BatchIdx = np.arange(1, N + 1)
Batch = ["LOT_" + str(i).zfill(4) for i in BatchIdx]
Shift = np.random.choice(SHIFTS, N, p=[0.4, 0.35, 0.25])

# ── F01 — Pre-clean (Akrion Gamma) ───────────────────────────────────────────
F01_Tool = np.random.choice(F01_TOOLS, N)
F01_HF_pct = np.clip(np.random.normal(0.5, 0.05, N), 0.3, 0.7)
F01_CleanTime_s = np.clip(np.random.normal(120, 5, N), 100, 140)
F01_DIWater_Mohm = np.clip(np.random.normal(18.0, 0.3, N), 17.0, 18.2)
F01_Scrap = (F01_HF_pct > 0.65).astype(int)

# ── F02 — STI Oxidation (Aviza Atmos) ───────────────────────────────────────
F02_Tool = np.random.choice(F02_TOOLS, N)
F02_OxTemp_C = np.clip(np.random.normal(1000, 5, N) + aging_drift(BatchIdx, 8), 985, 1020)
F02_OxTime_min = np.clip(np.random.normal(90, 4, N), 80, 105)
F02_O2Flow_slm = np.clip(np.random.normal(10, 0.5, N), 8.5, 11.5)
F02_STI_Thickness_nm = np.clip(350 + 0.8 * (F02_OxTemp_C - 1000) + np.random.normal(0, 4, N), 320, 380)
F02_Scrap = (np.abs(F02_STI_Thickness_nm - 350) > 20).astype(int)

# ── F03 — Gate Oxidation (ASM A412) ─────────────────────────────────────────
F03_Tool = np.random.choice(F03_TOOLS, N)
F03_OxTemp_C = np.clip(np.random.normal(850, 3, N) + aging_drift(BatchIdx, 5), 840, 865)
F03_OxTime_min = np.clip(np.random.normal(25, 1.5, N), 20, 30)
F03_O2Flow_slm = np.clip(np.random.normal(5, 0.3, N), 4.0, 6.0)
# Deal-Grove model: thickness depends on T and time
F03_GateOx_nm = np.clip(2.0 + 0.012 * (F03_OxTemp_C - 840) + 0.08 * F03_OxTime_min
                         + np.random.normal(0, 0.1, N), 1.5, 3.5)
F03_Scrap = ((F03_GateOx_nm < 1.8) | (F03_GateOx_nm > 3.2)).astype(int)

# ── F04 — Poly-Si deposition (AMAT Producer LPCVD) ──────────────────────────
F04_Tool = np.random.choice(F04_TOOLS, N)
F04_Temp_C = np.clip(np.random.normal(620, 4, N), 610, 635)
F04_SiH4_sccm = np.clip(np.random.normal(100, 5, N), 85, 115)
F04_Pressure_mTorr = np.clip(np.random.normal(200, 10, N), 175, 225)
F04_PolySi_nm = np.clip(150 + 0.5 * (F04_Temp_C - 620) + np.random.normal(0, 3, N), 135, 165)
F04_Scrap = (np.abs(F04_PolySi_nm - 150) > 12).astype(int)

# ── F05 — Gate Lithography (ASML PAS5500 + TEL Lithius) ─────────────────────
F05_Stepper = np.random.choice(F05_TOOLS, N)
F05_Track = np.random.choice(F05_TRACK, N)
F05_CD_nm = np.clip(np.random.normal(100, 3, N) + aging_drift(BatchIdx, 4), 90, 112)
F05_Overlay_nm = np.clip(np.random.normal(8, 2, N), 3, 16)
F05_Focus_um = np.clip(np.random.normal(0.0, 0.05, N), -0.15, 0.15)
F05_Dose_mJcm2 = np.clip(np.random.normal(25, 0.5, N), 23, 27)
F05_EPC_nm = np.clip(np.random.normal(2.0, 0.5, N), 0.5, 4.0)
F05_Scrap = ((F05_CD_nm > 108) | (F05_Overlay_nm > 14)).astype(int)

# ── F06 — Poly gate etch (LAM 9400 TCP) + Wet strip (Akrion) ────────────────
F06_Dry_Tool = np.random.choice(F06_DRY_TOOLS, N)
F06_Wet_Tool = np.random.choice(F06_WET_TOOLS, N)
F06_RF_Power_W = np.clip(np.random.normal(600, 20, N), 555, 650)
F06_Pressure_mTorr = np.clip(np.random.normal(8, 0.5, N), 6.5, 9.5)
F06_Cl2_sccm = np.clip(np.random.normal(50, 3, N), 42, 58)
F06_HBr_sccm = np.clip(np.random.normal(150, 5, N), 135, 165)
F06_PolyCD_nm = np.clip(F05_CD_nm - 2 + 0.005 * (F06_RF_Power_W - 600)
                         + np.random.normal(0, 1.5, N), 88, 110)
# Wet etch parameters
F06_HF_pct = np.clip(np.random.normal(5.0, 0.3, N), 4.0, 6.2)
F06_Etch_Temp_C = np.clip(np.random.normal(25, 2, N)
                           + (Shift == "Night").astype(int) * 2.5, 20, 32)
F06_EtchTime_s = np.clip(np.random.normal(60, 3, N), 50, 72)
F06_Scrap = ((F06_PolyCD_nm < 90) | (F06_PolyCD_nm > 108)
             | (F06_Etch_Temp_C > 30)).astype(int)

# ── F07 — LDD Ion Implant (AMAT Quantum X) ───────────────────────────────────
F07_Tool = np.random.choice(F07_TOOLS, N)
F07_Energy_keV = np.clip(np.random.normal(30, 1.5, N), 26, 34)
F07_Dose_cm2 = np.clip(np.random.normal(3e13, 5e11, N), 2.5e13, 3.5e13)
F07_Tilt_deg = np.clip(np.random.normal(7, 0.3, N), 6.0, 8.0)
F07_Uniformity_pct = np.clip(np.random.normal(1.5, 0.3, N), 0.8, 2.8)
F07_Scrap = (F07_Uniformity_pct > 2.5).astype(int)

# ── F08 — Spacer CVD + Etch (AMAT Producer + LAM 9400) ──────────────────────
F08_CVD_Tool = np.random.choice(F08_CVD_TOOLS, N)
F08_Etch_Tool = np.random.choice(F08_ETCH_TOOLS, N)
F08_TEOS_sccm = np.clip(np.random.normal(1000, 30, N), 930, 1070)
F08_CVD_Temp_C = np.clip(np.random.normal(400, 5, N), 388, 415)
F08_Spacer_nm = np.clip(80 + 0.2 * (F08_CVD_Temp_C - 400)
                         + np.random.normal(0, 2, N), 72, 88)
F08_EtchBack_nm = np.clip(np.random.normal(78, 2, N), 70, 86)
F08_Scrap = (np.abs(F08_Spacer_nm - F08_EtchBack_nm) > 8).astype(int)

# ── F09 — S/D Implant (Axcelis Optima) + RTA (AMAT Vantage) ─────────────────
F09_Imp_Tool = np.random.choice(F09_IMP_TOOLS, N)
F09_RTA_Tool = np.random.choice(F09_RTA_TOOLS, N)
F09_Energy_keV = np.clip(np.random.normal(10, 1.0, N), 7.5, 13)
F09_Dose_ions_cm2 = np.clip(np.random.normal(1e15, 2e13, N), 9e14, 1.1e15)
F09_RTA_Temp_C = np.clip(np.random.normal(1050, 5, N)
                          + aging_drift(BatchIdx, 6), 1035, 1068)
F09_RTA_Time_s = np.clip(np.random.normal(10, 0.5, N), 8.5, 11.5)
# Matthews model: sheet resistance inversely related to dose
F09_SheetRes_ohmSq = np.clip(80 - 0.003 * (F09_Dose_ions_cm2 - 1e15)
                              + 0.2 * (F09_RTA_Temp_C - 1050)
                              + np.random.normal(0, 2, N), 60, 100)
F09_Scrap = ((F09_SheetRes_ohmSq > 90) | (F09_RTA_Temp_C > 1063)).astype(int)

# ── F10 — Silicidation CoSi2 (AMAT Endura PVD) ───────────────────────────────
F10_Tool = np.random.choice(F10_TOOLS, N)
F10_Co_thickness_nm = np.clip(np.random.normal(8, 0.3, N), 7.0, 9.0)
F10_Anneal1_C = np.clip(np.random.normal(500, 5, N), 488, 515)
F10_Anneal2_C = np.clip(np.random.normal(750, 5, N), 738, 765)
F10_CoSi2_Rs_ohmSq = np.clip(4.0 + 0.05 * (500 - F10_Anneal2_C)
                              + np.random.normal(0, 0.3, N), 3.0, 6.0)
F10_Scrap = (F10_CoSi2_Rs_ohmSq > 5.5).astype(int)

# ── F11 — ILD CVD (AMAT Producer) + CMP (AMAT Mirra) ────────────────────────
F11_CVD_Tool = np.random.choice(F11_CVD_TOOLS, N)
F11_CMP_Tool = np.random.choice(F11_CMP_TOOLS, N)
F11_ILD_nm_pre = np.clip(np.random.normal(600, 10, N), 575, 625)
F11_CMP_Pressure_psi = np.clip(np.random.normal(3.0, 0.15, N), 2.6, 3.5)
F11_CMP_Speed_rpm = np.clip(np.random.normal(80, 3, N), 72, 90)
# Preston equation: MRR proportional to pressure × speed
F11_MRR_nmmin = np.clip(120 * F11_CMP_Pressure_psi * (F11_CMP_Speed_rpm / 80)
                         + np.random.normal(0, 5, N), 280, 430)
F11_ILD_nm_post = np.clip(F11_ILD_nm_pre - 5 * (F11_MRR_nmmin / 60)
                           + np.random.normal(0, 3, N), 390, 430)
F11_WIWNU_pct = np.clip(np.random.normal(2.5, 0.5, N), 1.0, 4.5)
F11_Scrap = ((F11_WIWNU_pct > 4.0) | (F11_ILD_nm_post < 395)).astype(int)

# ── F12 — Contact etch (LAM 9400) + W-plug (Novellus Concept2) ───────────────
F12_Etch_Tool = np.random.choice(F12_ETCH_TOOLS, N)
F12_CVD_Tool = np.random.choice(F12_CVD_TOOLS, N)
F12_CF4_sccm = np.clip(np.random.normal(40, 2, N), 35, 46)
F12_CHF3_sccm = np.clip(np.random.normal(20, 1.5, N), 16, 25)
F12_ContactAR = np.clip(np.random.normal(8.0, 0.3, N), 7.0, 9.0)
F12_WF6_sccm = np.clip(np.random.normal(60, 3, N), 52, 70)
F12_W_plug_Rs = np.clip(np.random.normal(15, 1.5, N), 11, 20)
F12_Scrap = (F12_W_plug_Rs > 18).astype(int)

# ── F13 — Metal-1 PVD (AMAT Endura) + CMP (AMAT Mirra) ──────────────────────
F13_PVD_Tool = np.random.choice(F13_PVD_TOOLS, N)
F13_CMP_Tool = np.random.choice(F13_CMP_TOOLS, N)
F13_TiN_nm = np.clip(np.random.normal(30, 1.5, N), 26, 35)
F13_Al_nm = np.clip(np.random.normal(500, 10, N), 475, 525)
F13_CMP_Pressure_psi = np.clip(np.random.normal(2.5, 0.1, N), 2.2, 2.9)
F13_Metal_Rs_ohmSq = np.clip(0.065 + 0.001 * (500 - F13_Al_nm)
                              + np.random.normal(0, 0.003, N), 0.055, 0.085)
F13_Scrap = (F13_Metal_Rs_ohmSq > 0.078).astype(int)

# ── Cheminformatics descriptors (wet etch F06) ───────────────────────────────
# Arrhenius reactivity: k = [HF] * exp(-Ea / RT), Ea=40 kJ/mol
Ea = 40000          # J/mol
R = 8.314           # J/(mol·K)
T_K = F06_Etch_Temp_C + 273.15
Chem_ReactivityIndex = np.clip(F06_HF_pct * np.exp(-Ea / (R * T_K)), 0, 0.05)

# pH: -log10(sqrt(Ka * C)), Ka HF = 6.8e-4
Ka_HF = 6.8e-4
Chem_pH_Bath = np.clip(-np.log10(np.sqrt(Ka_HF * F06_HF_pct)), 1.5, 3.5)

# Etch rate nm/min (empirical, calibrated to F06 conditions)
k0 = 500
Chem_EtchRate_nmMin = np.clip(k0 * F06_HF_pct * np.exp(-Ea / (R * T_K)), 30, 120)

# Selectivity SiO2/Si (decreases with T and [HF])
Chem_Selectivity = np.clip(50 - 0.8 * (F06_Etch_Temp_C - 25)
                            - 5 * (F06_HF_pct - 5), 20, 60)

# ── Final SCRAP label ─────────────────────────────────────────────────────────
# Weighted combination of phase scraps — propagation model
# Night shift adds +15% scrap probability
phase_scrap_sum = (F01_Scrap + F02_Scrap + F03_Scrap + F04_Scrap
                   + F05_Scrap + F06_Scrap + F07_Scrap + F08_Scrap
                   + F09_Scrap + F10_Scrap + F11_Scrap + F12_Scrap
                   + F13_Scrap)

night_factor = (Shift == "Night").astype(int) * 0.15
scrap_prob = np.clip(0.1 + 0.06 * phase_scrap_sum + night_factor
                     + 0.002 * aging_drift(BatchIdx, 1), 0, 1)
SCRAP_FINAL = (np.random.random(N) < scrap_prob).astype(int)

# ── Assemble DataFrame ────────────────────────────────────────────────────────
df = pd.DataFrame({
    # Lot metadata
    "BatchIdx":             BatchIdx,
    "Batch":                Batch,
    "Shift":                Shift,

    # F01 Pre-clean
    "F01_Tool":             F01_Tool,
    "F01_HF_pct":           F01_HF_pct.round(4),
    "F01_CleanTime_s":      F01_CleanTime_s.round(1),
    "F01_DIWater_Mohm":     F01_DIWater_Mohm.round(3),
    "F01_Scrap":            F01_Scrap,

    # F02 STI oxidation
    "F02_Tool":             F02_Tool,
    "F02_OxTemp_C":         F02_OxTemp_C.round(2),
    "F02_OxTime_min":       F02_OxTime_min.round(1),
    "F02_O2Flow_slm":       F02_O2Flow_slm.round(2),
    "F02_STI_Thickness_nm": F02_STI_Thickness_nm.round(2),
    "F02_Scrap":            F02_Scrap,

    # F03 Gate oxidation
    "F03_Tool":             F03_Tool,
    "F03_OxTemp_C":         F03_OxTemp_C.round(2),
    "F03_OxTime_min":       F03_OxTime_min.round(1),
    "F03_O2Flow_slm":       F03_O2Flow_slm.round(2),
    "F03_GateOx_nm":        F03_GateOx_nm.round(3),
    "F03_Scrap":            F03_Scrap,

    # F04 Poly-Si deposition
    "F04_Tool":             F04_Tool,
    "F04_Temp_C":           F04_Temp_C.round(2),
    "F04_SiH4_sccm":        F04_SiH4_sccm.round(1),
    "F04_Pressure_mTorr":   F04_Pressure_mTorr.round(1),
    "F04_PolySi_nm":        F04_PolySi_nm.round(2),
    "F04_Scrap":            F04_Scrap,

    # F05 Lithography
    "F05_Stepper":          F05_Stepper,
    "F05_Track":            F05_Track,
    "F05_CD_nm":            F05_CD_nm.round(2),
    "F05_Overlay_nm":       F05_Overlay_nm.round(2),
    "F05_Focus_um":         F05_Focus_um.round(4),
    "F05_Dose_mJcm2":       F05_Dose_mJcm2.round(2),
    "F05_EPC_nm":           F05_EPC_nm.round(2),
    "F05_Scrap":            F05_Scrap,

    # F06 Gate etch + wet clean
    "F06_Dry_Tool":         F06_Dry_Tool,
    "F06_Wet_Tool":         F06_Wet_Tool,
    "F06_RF_Power_W":       F06_RF_Power_W.round(1),
    "F06_Pressure_mTorr":   F06_Pressure_mTorr.round(2),
    "F06_Cl2_sccm":         F06_Cl2_sccm.round(1),
    "F06_HBr_sccm":         F06_HBr_sccm.round(1),
    "F06_PolyCD_nm":        F06_PolyCD_nm.round(2),
    "F06_HF_pct":           F06_HF_pct.round(3),
    "F06_Etch_Temp_C":      F06_Etch_Temp_C.round(2),
    "F06_EtchTime_s":       F06_EtchTime_s.round(1),
    "F06_Scrap":            F06_Scrap,

    # F07 LDD implant
    "F07_Tool":             F07_Tool,
    "F07_Energy_keV":       F07_Energy_keV.round(2),
    "F07_Dose_cm2":         np.round(F07_Dose_cm2, 2),
    "F07_Tilt_deg":         F07_Tilt_deg.round(2),
    "F07_Uniformity_pct":   F07_Uniformity_pct.round(3),
    "F07_Scrap":            F07_Scrap,

    # F08 Spacer
    "F08_CVD_Tool":         F08_CVD_Tool,
    "F08_Etch_Tool":        F08_Etch_Tool,
    "F08_TEOS_sccm":        F08_TEOS_sccm.round(1),
    "F08_CVD_Temp_C":       F08_CVD_Temp_C.round(2),
    "F08_Spacer_nm":        F08_Spacer_nm.round(2),
    "F08_EtchBack_nm":      F08_EtchBack_nm.round(2),
    "F08_Scrap":            F08_Scrap,

    # F09 S/D implant + RTA
    "F09_Imp_Tool":         F09_Imp_Tool,
    "F09_RTA_Tool":         F09_RTA_Tool,
    "F09_Energy_keV":       F09_Energy_keV.round(2),
    "F09_Dose_ions_cm2":    np.round(F09_Dose_ions_cm2, 2),
    "F09_RTA_Temp_C":       F09_RTA_Temp_C.round(2),
    "F09_RTA_Time_s":       F09_RTA_Time_s.round(2),
    "F09_SheetRes_ohmSq":   F09_SheetRes_ohmSq.round(3),
    "F09_Scrap":            F09_Scrap,

    # F10 Silicidation
    "F10_Tool":             F10_Tool,
    "F10_Co_thickness_nm":  F10_Co_thickness_nm.round(3),
    "F10_Anneal1_C":        F10_Anneal1_C.round(2),
    "F10_Anneal2_C":        F10_Anneal2_C.round(2),
    "F10_CoSi2_Rs_ohmSq":  F10_CoSi2_Rs_ohmSq.round(4),
    "F10_Scrap":            F10_Scrap,

    # F11 ILD + CMP
    "F11_CVD_Tool":         F11_CVD_Tool,
    "F11_CMP_Tool":         F11_CMP_Tool,
    "F11_ILD_nm_pre":       F11_ILD_nm_pre.round(2),
    "F11_CMP_Pressure_psi": F11_CMP_Pressure_psi.round(3),
    "F11_CMP_Speed_rpm":    F11_CMP_Speed_rpm.round(1),
    "F11_MRR_nmmin":        F11_MRR_nmmin.round(2),
    "F11_ILD_nm_post":      F11_ILD_nm_post.round(2),
    "F11_WIWNU_pct":        F11_WIWNU_pct.round(3),
    "F11_Scrap":            F11_Scrap,

    # F12 Contact + W-plug
    "F12_Etch_Tool":        F12_Etch_Tool,
    "F12_CVD_Tool":         F12_CVD_Tool,
    "F12_CF4_sccm":         F12_CF4_sccm.round(1),
    "F12_CHF3_sccm":        F12_CHF3_sccm.round(1),
    "F12_ContactAR":        F12_ContactAR.round(3),
    "F12_WF6_sccm":         F12_WF6_sccm.round(1),
    "F12_W_plug_Rs":        F12_W_plug_Rs.round(3),
    "F12_Scrap":            F12_Scrap,

    # F13 Metal-1
    "F13_PVD_Tool":         F13_PVD_Tool,
    "F13_CMP_Tool":         F13_CMP_Tool,
    "F13_TiN_nm":           F13_TiN_nm.round(2),
    "F13_Al_nm":            F13_Al_nm.round(2),
    "F13_CMP_Pressure_psi": F13_CMP_Pressure_psi.round(3),
    "F13_Metal_Rs_ohmSq":   F13_Metal_Rs_ohmSq.round(5),
    "F13_Scrap":            F13_Scrap,

    # Cheminformatics (wet etch F06)
    "Chem_ReactivityIndex": Chem_ReactivityIndex.round(6),
    "Chem_pH_Bath":         Chem_pH_Bath.round(4),
    "Chem_EtchRate_nmMin":  Chem_EtchRate_nmMin.round(3),
    "Chem_Selectivity":     Chem_Selectivity.round(3),

    # Final quality label
    "SCRAP_FINAL":          SCRAP_FINAL,
})

# ── Save ──────────────────────────────────────────────────────────────────────
output_file = "fab_synthetic_500w_13ph.csv"
df.to_csv(output_file, index=False)

# ── Summary ───────────────────────────────────────────────────────────────────
scrap_rate = SCRAP_FINAL.mean() * 100
print(f"{'='*60}")
print(f"  Semiconductor FAB — Synthetic Dataset v2.0")
print(f"{'='*60}")
print(f"  Wafers      : {N}")
print(f"  Columns     : {len(df.columns)}")
print(f"  Phases      : 13 (F01–F13)")
print(f"  SCRAP rate  : {scrap_rate:.1f}%")
print(f"  Night shift : {(Shift=='Night').sum()} wafers ({(Shift=='Night').mean()*100:.0f}%)")
print(f"  Output file : {output_file}")
print(f"{'='*60}")
print(f"\nColumn list ({len(df.columns)} total):")
for i, col in enumerate(df.columns):
    print(f"  {i+1:3d}. {col}")
