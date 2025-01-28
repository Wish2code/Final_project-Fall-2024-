# Eye Diagnosis System

## Overview
This project processes medical data to diagnose patients based on their symptoms. It integrates multiple data sources (e.g., patient vitals, scheduling, and insurance information), performs symptom-based diagnosis using ICD codes, and saves the results in a CSV file. Users can optionally view the results in a well-formatted table.

---

## Features
- Reads and merges patient data from JSON and CSV files.
- Matches patient symptoms to medical conditions using ICD/CPT codes.
- Saves diagnoses, prescriptions, and other details into a CSV file.
- Displays results in a user-friendly table format using `tabulate`.

---

## Requirements
- **Python 3.7 or higher**
- Required libraries:
  - `csv` (built-in)
  - `json` (built-in)
  - `tabulate` (install using `pip install tabulate`)

---

## File Structure
- **Input Files**:
  - `Vitals_team.json`: Contains patient vital signs and symptoms.
  - `scheduling.json`: Contains appointment scheduling details.
  - `insurance.json`: Contains patient insurance information.
  - `icd_cpt_codes_extended.csv`: Contains ICD codes, conditions, and treatments.

- **Output File**:
  - `diagnosis_results.csv`: The final diagnosis report for all patients.

---

