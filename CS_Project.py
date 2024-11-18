import csv

def read_csv(file_name):
    """Reads a CSV file and returns a list of dictionaries."""
    data = []
    with open(file_name, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def write_csv(file_name, fieldnames, data):
    """Writes a list of dictionaries to a CSV file."""
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def diagnose_patient(symptoms, icd_data):
    """Finds the best-matching ICD code for the given symptoms."""
    for row in icd_data:
        condition_symptoms = {row["symptom1"], row["symptom2"], row["symptom3"]}
        if set(symptoms) & condition_symptoms:  # Check for symptom overlap
            return row["condition"], row["icd_code"]
    return "Unknown", "DNE"

def get_prescription(icd_code, cpt_data):
    """Finds the prescription and CPT code for the given ICD code."""
    for row in cpt_data:
        if row["icd_code"] == icd_code:
            return row["prescription"], row["cpt_code"]
    return "Unknown", "DNE"

def main():
    # Load data from CSV files
    symptoms_data = read_csv("symptoms.csv")
    icd_data = read_csv("icd_codes.csv")
    cpt_data = read_csv("cpt_codes.csv")
    
    # Prepare diagnosis results
    results = []
    for patient in symptoms_data:
        patient_id = patient["patient_id"]
        symptoms = [patient["symptom1"], patient["symptom2"], patient["symptom3"]]
        
        # Diagnose based on symptoms
        diagnosis, icd_code = diagnose_patient(symptoms, icd_data)
        
        # Get prescription and CPT code
        prescription, cpt_code = get_prescription(icd_code, cpt_data)
        
        # Append result
        results.append({
            "patient_id": patient_id,
            "diagnosis": diagnosis,
            "icd_code": icd_code,
            "prescription": prescription,
            "cpt_code": cpt_code
        })
    
    # Save results to a CSV file
    fieldnames = ["patient_id", "diagnosis", "icd_code", "prescription", "cpt_code"]
    write_csv("diagnosis_results.csv", fieldnames, results)
    print("Diagnosis complete! Results saved to 'diagnosis_results.csv'.")

if __name__ == "__main__":
    main()

