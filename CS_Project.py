#New
import csv
from tabulate import tabulate


def read_csv(file_name):
    """Reads a CSV file and returns a list of dictionaries."""
    try:
        with open(file_name, mode='r') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred while reading '{file_name}': {e}")
        return []


def write_csv(file_name, fieldnames, data):
    """Writes a list of dictionaries to a CSV file."""
    try:
        with open(file_name, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print(f"An error occurred while writing to '{file_name}': {e}")


def diagnose_patient(symptoms, icd_data):
    """Finds the best-matching ICD code for the given symptoms."""
    for row in icd_data:
        condition_symptoms = {row["symptom1"], row["symptom2"], row["symptom3"]}
        if set(symptoms) & condition_symptoms:  # Check for symptom overlap
            return (
                row["condition"],
                row["icd_code"],
                row["prescription"],
                row["severity"],
                row["SOD"],
                row["diagnosis_status"]
            )
    return "Unknown", "DNE", "Unknown", "Unknown", "Unknown", "Unknown"


def process_symptoms(patient):
    """Extracts and processes symptoms from patient data."""
    return [
        patient.get("symptom1", "").strip(),
        patient.get("symptom2", "").strip(),
        patient.get("symptom3", "").strip()
    ]


def main():
    # File paths
    symptoms_file = "symptoms.csv"
    icd_cpt_file = "icd_cpt_codes_extended.csv"
    results_file = "diagnosis_results.csv"

    # Load data from CSV files
    symptoms_data = read_csv(symptoms_file)
    icd_cpt_data = read_csv(icd_cpt_file)

    # Validate data
    if not symptoms_data or not icd_cpt_data:
        print("Error: Missing or incomplete data files. Please check your input files.")
        return

    # Prepare diagnosis results
    results = []
    for patient in symptoms_data:
        patient_id = patient["patient_id"]
        symptoms = process_symptoms(patient)
        eye = patient.get("Eye", "N/A")
        onset_date = patient.get("Onset_date", "N/A")

        # Diagnose based on symptoms
        diagnosis, icd_code, prescription, severity, SOD, diagnosis_status = diagnose_patient(symptoms, icd_cpt_data)

        # Get CPT code
        cpt_code = next((row["cpt_code"] for row in icd_cpt_data if row["icd_code"] == icd_code), "DNE")

        # Append result
        results.append({
            "patient_id": patient_id,
            "diagnosis": diagnosis,
            "icd_code": icd_code,
            "prescription": prescription,
            "cpt_code": cpt_code,
            "Eye": eye,
            "Onset_date": onset_date,
            "Diagnosis_status": diagnosis_status,
            "SOD": SOD,
            "Severity": severity
        })

    # Save results to a CSV file
    fieldnames = [
        "patient_id", "diagnosis", "icd_code", "prescription", "cpt_code",
        "Eye", "Onset_date", "Diagnosis_status", "SOD", "Severity"
    ]
    write_csv(results_file, fieldnames, results)
    print(f"Diagnosis complete! Results saved to '{results_file}'.")


def display_results(file_name):
    """Reads the diagnosis results file and displays it in a fancy table format."""
    try:
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
        
        if not data:
            print("No data found in the results file.")
            return

        # Separate the header and the rows
        header = data[0]
        rows = data[1:]

        # Use tabulate to create a fancy table
        print(tabulate(rows, headers=header, tablefmt="grid"))
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
    except Exception as e:
        print(f"An error occurred while displaying '{file_name}': {e}")


if __name__ == "__main__":
    main()
    print("\nDiagnosis Results:")
    display_results("diagnosis_results.csv")
