
import json


import requests
from pprint import pprint
from pathlib import Path

from pathlib import Path





# Read the patient_resource_id from the file
with open('//Users/sriramyapanja/PycharmProjects/group_3_FINAL_PROJECT/src/data/patient_resource_id.txt', 'r') as file:
    patient_resource_id = file.read().strip()
print(patient_resource_id)


data_dir = Path.cwd() / 'data'

BASE_SERVER_URL = "http://137.184.71.65:8080/fhir"


def read_data(name_of_the_file):
    # Define the path to your JSON file
    py_file_path = data_dir / f"{name_of_the_file}.py"

    # Load the data from the JSON file
    try:
        with open(py_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File not found: {py_file_path}")
        exit()
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        exit()
    return data

    #data['subject']['reference'] = f"Patient/{patient_resource_id}"


def post_data(file_name, resource_name):
    # Define the URL of the API endpoint
    url = BASE_SERVER_URL + '/' + f'{resource_name}'
    data = read_data(name_of_the_file=file_name)
    # Define headers, including content-type as JSON
    headers = {
        "Content-Type": "application/json",


    }

    #patient_ob['subject']['reference'] = f"Patient/{patient_resource_id}"
    try:
        # Send POST request
        response = requests.post(url, json=data, headers=headers)
        # Check if the request was successful
        if response.status_code == 200 or response.status_code == 201:
            print(f"Data posted successfully! - {resource_name}")
            print("Response:", response.json())
        else:
            print(f"Failed to post data - {resource_name}. Status code:", response.status_code)
            print("Error:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error during request:", e)


if __name__ == '__main__':
    post_data(file_name='patient_procedure', resource_name='Procedure')
