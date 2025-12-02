On-the-Fly Machine Learning Forcefield (MLFF) Generation Algorithm

⸻

Formal Workflow Algorithm (Numbered Pseudocode)

Input: Initial atomic configuration, initial MLFF, FP calculator (e.g., VASP), threshold values for uncertainty, max steps N_MD, update size N_update

Output: Trained MLFF model and MD trajectory

⸻

	1.	Initialize:
1.1 Load initial MLFF model and reference dataset.
1.2 Set step counter i = 0.
	2.	While i < N_MD, do:
2.1 MLFF prediction:
	•	Predict energy E_ML, forces F_ML, stress S_ML, and uncertainty U for current atomic configuration.
2.2 Evaluate uncertainty:
	•	If U < U_threshold:
	•	Accept ML prediction.
	•	Go to Step 2.5.
	•	Else:
	•	Proceed to Step 2.3.
2.3 First-principles (FP) calculation:
	•	Perform FP calculation (e.g., DFT) to obtain E_FP, F_FP, S_FP.
	•	Store structure and FP data as a candidate sample.
2.4 Dataset management and retraining:
	•	If number of new samples >= N_update, or U > U_max:
	•	Update reference dataset.
	•	Retrain MLFF using updated data.
2.5 Propagate dynamics:
	•	If MLFF was used in Step 2.2:
	•	Update positions/velocities using F_ML.
	•	Else:
	•	Update using F_FP.
2.6 Increment step counter: i += 1
2.7 Go back to Step 2.
	3.	End loop:
	•	Output trained MLFF model and MD trajectory.

⸻

Flowchart Diagram Version

[Start] --> [Initialize model and counters]
   --> [Predict E, F, S, U via MLFF]
   --> [Is U < threshold?]
        |Yes| --> [Use MLFF forces] --> [Propagate] --> [i += 1] --> [i < N_MD?]-->|Yes| back to Predict
        | No|
           v
     [Run DFT calculation]
           |
   [Add to reference dataset]
           |
   [Need retraining?]-->|Yes|-->[Retrain MLFF]
           |No                         |
           v                          v
       [Use DFT forces] --> [Propagate] --> [i += 1] --> [i < N_MD?]-->|Yes| back to Predict
                                                          |
                                                       [No]
                                                         v
                                                   [Terminate]


⸻

Python-Style Pseudocode

for i in range(N_MD):
    E_ML, F_ML, S_ML, U = MLFF.predict(structure)

    if U < U_threshold:
        forces = F_ML
        used_fp = False
    else:
        E_FP, F_FP, S_FP = run_fp_calculation(structure)
        add_to_dataset(structure, E_FP, F_FP, S_FP)
        forces = F_FP
        used_fp = True

    if dataset_needs_update():
        MLFF.retrain()

    structure.update(forces)


⸻

VASP-Compatible Script Logic
	•	Step 1: Run vasp_std when FP is required, output data to OUTCAR, CONTCAR, etc.
	•	Step 2: Parse OUTCAR for E, F, and S using scripts or vasprun.xml
	•	Step 3: Add CONTCAR + energies to training dataset folder.
	•	Step 4: Use an external ML engine (e.g., DeePMD-kit, GAP, MALA) to retrain.
	•	Step 5: Update POTCAR, KPOINTS, INCAR, and continue MD via VASP or LAMMPS with MLFF.

⸻

Methods Section Text (for Publication)

An on-the-fly machine learning forcefield (MLFF) scheme was employed to accelerate molecular dynamics while preserving first-principles accuracy. At each MD step, the MLFF predicted energies, forces, and stress tensors, along with associated uncertainties. If the predicted uncertainty exceeded a predefined threshold, a DFT calculation was performed using VASP. These high-fidelity results were incorporated into a growing reference dataset. Once sufficient new data had been accumulated or prediction uncertainty exceeded a critical limit, the MLFF was retrained. MD propagation continued using either MLFF or DFT forces depending on reliability. This adaptive scheme ensured efficient yet accurate exploration of the potential energy surface.

⸻

Optional Variants

Shortened Version (for Posters or Presentations)
	1.	Predict with MLFF (energy, forces, uncertainty).
	2.	If uncertainty high → run DFT, store results.
	3.	If enough new data → retrain MLFF.
	4.	Propagate MD using reliable forces.
	5.	Repeat until max steps reached.

Extended Version (With Temperature Control, Logging)
	•	Add T_control module to keep temperature using Nose-Hoover.
	•	Log prediction type per frame (ML or DFT).
	•	Include time estimation and parallel batching for DFT jobs.

⸻

Let me know if you want any of this adapted for a specific MLFF library (e.g., DeePMD-kit, GAP, NequIP) or platform (LAMMPS, ASE).
