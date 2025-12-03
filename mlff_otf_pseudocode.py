# Initialize
i = 0
N_MD = total_md_steps
MLFF = load_initial_forcefield()
reference_dataset = []

while i < N_MD:

    # Step 1: MLFF predicts energy, forces, stress, and uncertainty
    E_pred, F_pred, S_pred, U_pred = MLFF.predict(current_structure)

    # Step 2: Decide if uncertainty is acceptable
    if U_pred < uncertainty_threshold and sampling_sufficient(current_structure):
        # Step 5: Use MLFF forces
        forces = F_pred
    else:
        # Step 3: Run first-principles (DFT) calculation
        E_dft, F_dft, S_dft = run_dft(current_structure)

        # Step 4: Add to reference dataset
        reference_dataset.append((current_structure, E_dft, F_dft, S_dft))

        # Check if retraining condition is met
        if len(reference_dataset) >= retrain_threshold or U_pred > high_uncertainty_cutoff:
            MLFF = retrain_model(reference_dataset)

        # Use DFT forces this step
        forces = F_dft

    # Step 5: Propagate dynamics using selected forces
    current_structure = propagate_structure(current_structure, forces)

    # Step 6: Update counter
    i += 1

# Termination
save_trajectory()
log_final_model(MLFF)
