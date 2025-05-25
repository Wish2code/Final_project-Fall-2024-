import csv
import json
from tabulate import tabulate


def read_json(file_name):
    """Reads a JSON file and returns the parsed data."""
    try:
        with open(file_name, mode='r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Could not parse JSON from '{file_name}': {e}")
        return []
    except Exception as e:
        print(f"An error occurred while reading '{file_name}': {e}")
        return []


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
        condition_symptoms = {row["symptom1"].strip(), row["symptom2"].strip(), row["symptom3"].strip()}
        if len(set(symptoms) & condition_symptoms) > 1:  # Check for symptom overlap
            return (
                row["condition"],
                row["icd_code"],
                row["prescription"],
                row["severity"],
                row["SOD"],
                row["diagnosis_status"],
                row.get("Insurance", "Unknown")
            )
    return "Unknown", "DNE", "Unknown", "Unknown", "Unknown", "Unknown", "Unknown"


def merge_patient_data(vitals, scheduling, insurance):
    """Merges data from vitals, scheduling, and insurance sources."""
    merged_data = []
    for patient in vitals:
        patient_email = patient["personal_info"]["email"][0]
        schedule = next((item for item in scheduling if item["patient_email"] == patient_email), {})
        insurance_info = next((item for item in insurance if item["patient_email"] == patient_email), {})

        merged_patient = {
            **patient,
            "appointment_date": schedule.get("appointment_date", "N/A"),
            "appointment_time": schedule.get("time", "N/A"),
            "insurance_provider": insurance_info.get("insurance_provider", "N/A"),
            "policy_number": insurance_info.get("policy_number", "N/A"),
            "coverage_details": insurance_info.get("coverage_details", "N/A"),
        }
        merged_data.append(merged_patient)
    return merged_data


def main():
    # File paths
    vitals_file = "Vitals_team.json"
    scheduling_file = "scheduling.json"
    insurance_file = "insurance.json"
    icd_cpt_file = "icd_cpt_codes_extended.csv"
    results_file = "diagnosis_results.csv"

    # Load data
    vitals_data = read_json(vitals_file)
    scheduling_data = read_json(scheduling_file)
    insurance_data = read_json(insurance_file)
    icd_cpt_data = read_csv(icd_cpt_file)

    #print(vitals_data)

    # Validate data
    if not vitals_data or not icd_cpt_data:
        print("Error: Missing or incomplete data files. Please check your input files.")
        return

    # Merge data
    merged_data = merge_patient_data(vitals_data, scheduling_data, insurance_data)

    # Prepare diagnosis results
    results = []
    for patient in merged_data:
        patient_info = patient["personal_info"]
        health_data = patient["health_data"]
        symptoms = health_data["symptoms"]
        patient_email = patient_info["email"][0]

        # Diagnose based on symptoms
        diagnosis, icd_code, prescription, severity, SOD, diagnosis_status, insurance = diagnose_patient(symptoms, icd_cpt_data)

        # Get CPT code
        cpt_code = next((row["cpt_code"] for row in icd_cpt_data if row["icd_code"] == icd_code), "DNE")

        # Append result
        results.append({
            "patient_email": patient_email,
            "diagnosis": diagnosis,
            "icd_code": icd_code,
            "prescription": prescription,
            "cpt_code": cpt_code,
            "Eye": health_data["affected-eye"][0],
            "Onset_date": health_data["onset"],
            "Insurance": insurance,
            "Diagnosis_status": diagnosis_status,
            "SOD": SOD,
            "Severity": severity,
            "appointment_date": patient.get("appointment_date", "N/A"),
            "appointment_time": patient.get("appointment_time", "N/A"),
            "insurance_provider": patient.get("insurance_provider", "N/A"),
            "policy_number": patient.get("policy_number", "N/A"),
            "coverage_details": patient.get("coverage_details", "N/A"),
        })

    # Save results to a CSV file
    fieldnames = [
        "patient_email", "diagnosis", "icd_code", "prescription", "cpt_code",
        "Eye", "Onset_date", "Diagnosis_status", "SOD", "Severity", "Insurance",
        "appointment_date", "appointment_time", "insurance_provider",
        "policy_number", "coverage_details"
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

        # Use tabulate to create a table
        print(tabulate(rows, headers=header, tablefmt="grid"))
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
    except Exception as e:
        print(f"An error occurred while displaying '{file_name}': {e}")


if __name__ == "__main__":
    main()
    r = input('Do you want to view the diagnosis results (Y or N)?: ')
    if r.upper() == 'Y':
        print("\nDiagnosis Results:")
        display_results("diagnosis_results.csv")
    else:
        print('HAVE A GOOD DAY!! :)')

