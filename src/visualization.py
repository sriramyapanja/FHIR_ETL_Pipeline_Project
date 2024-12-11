import json
import requests
from pprint import pprint
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime

from src.registration import data_dir

BASE_URL = "https://in-info-web20.luddy.indianapolis.iu.edu/apis/default/fhir"


def get_access_token_from_file():
    file_path = Path(data_dir / "access_token.json")
    if not file_path.exists():
        print("Error: access_token.json file not found.")
        return None
    try:
        with open(file_path, 'r') as json_file:
            json_data = json.load(json_file)
            access_token = json_data.get("access_token")
        return access_token
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error reading access token from file: {e}")
        return None


def get_headers():
    access_token = get_access_token_from_file()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    return headers


def fetch_patients_and_insights():
    """
    Fetch patients and derive insights such as age distribution.
    """
    url = f'{BASE_URL}/Patient'
    response = requests.get(url=url, headers=get_headers())

    if response.status_code == 200:
        data = response.json()
        age_groups = {"0-17": 0, "18-34": 0, "35-49": 0, "50-64": 0, "65+": 0, "unknown": 0}

        if "entry" in data:
            for item in data["entry"]:
                birth_date = item["resource"].get("birthDate", None)
                if birth_date:
                    age = calculate_age(birth_date)
                    if age < 18:
                        age_groups["0-17"] += 1
                    elif 18 <= age <= 34:
                        age_groups["18-34"] += 1
                    elif 35 <= age <= 49:
                        age_groups["35-49"] += 1
                    elif 50 <= age <= 64:
                        age_groups["50-64"] += 1
                    else:
                        age_groups["65+"] += 1
                else:
                    age_groups["unknown"] += 1

        # Print insights
        print("Insights from FHIR Patient Data:")
        for group, count in age_groups.items():
            print(f"{group}: {count} patients")

        # Visualization
        visualize_age_distribution(age_groups)

    else:
        print(f"Error fetching patients: {response.status_code}, {response.text}")


def calculate_age(birth_date):
    """
    Calculate the age of a patient based on their birth date.
    """
    birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def visualize_age_distribution(age_groups):
    """
    Create a bar chart for age group distribution.
    """
    groups = list(age_groups.keys())
    counts = list(age_groups.values())

    plt.figure(figsize=(10, 6))
    plt.bar(groups, counts, color=['skyblue', 'orange', 'green', 'red', 'purple', 'gray'])
    plt.title("Patient Age Group Distribution")
    plt.xlabel("Age Groups")
    plt.ylabel("Number of Patients")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


if __name__ == "__main__":
    print("Fetching insights and visualizations from FHIR data...\n")

    # Fetch and analyze patients based on age groups
    fetch_patients_and_insights()
