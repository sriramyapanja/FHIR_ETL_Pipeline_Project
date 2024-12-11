# ETL Pipeline page

[Home](./index.md) ||
[BPMN Model](./bpmn.md) ||
[Use Case Model](./use_case.md) ||
[ETL Pipeline](./etl_pipeline.md) ||
[Insights](./insights.md) ||
[Team Contributions](./team_contrib.md) ||
[About](./about.md) ||

##  ETL Pipeline Documentation

This documentation outlines the ETL (Extract, Transform, Load) process used to transfer patient condition data from one API (OpenEMR) to another (Primary Care EHR API). The pipeline consists of three primary steps: Extraction, Transformation, and Loading. Below is a detailed breakdown of each step, including Python code snippets and descriptions of how each task is handled.

1. Extraction: Retrieving Data from the Source API (OpenEMR)
API Endpoint Details:
The source API utilizes the FHIR standard to expose patient condition data.

Base URL for OpenEMR API:
https://in-info-web20.luddy.indianapolis.iu.edu/apis/default/fhir

Condition Resource Endpoint:
Condition?patient={patient_resource_id}
This endpoint retrieves all conditions for a specific patient.

Patient Resource Endpoint:
Patient/{patient_resource_id}
This provides detailed patient information such as demographics.

Authentication/Authorization:
The API requires Bearer Token authentication.

The access token is retrieved from a local JSON file (access_token.json).

Function to Retrieve Access Token:

```
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
```
## Error handling:

If the access token file is missing, the process stops.
If the JSON file is malformed or missing a required key, an error message is printed, and None is returned.

API Request Example:
Python code

```
def get_snomed_code(patient_resource_id):
    url = f'{BASE_URL}/Condition?patient={patient_resource_id}'
    response = requests.get(url=url, headers=get_headers())
    data = response.json()
    if 'entry' in data:
        conditions = data['entry']
        snomed_code = conditions[30]['resource']['code']['coding'][0]['code']
        # Further processing...
```

2.Transformation: Cleaning and Structuring Data

The transformation step prepares the extracted data to match the target API format.

Techniques for Cleaning and Structuring Data:

Handling Missing Fields: When fields such as severity are missing, placeholder values like "Not Available" are used to maintain consistency.
Mapping Source Data to Target Format: Data like SNOMED CT codes, body site information, and patient details are accurately mapped to match the target API’s structure.

Tools Used:

SNOMED CT Lookup: To enrich the data with additional details like SNOMED CT child terms and body site information, the pipeline interacts with external systems via the BASE_HERMES_URL.

Example: Fetching SNOMED Child Term:

python code
```
def expression_constraint(concept_id):
    search_string = f"<! {concept_id}"
    response = requests.get(f'{BASE_HERMES_URL}/search?constraint={search_string}')
    data = response.json()
    if len(data):
        first_item_from_results = data[0]
        return first_item_from_results['conceptId'], first_item_from_results['preferredTerm']
```
Data Mapping: The fetched data from OpenEMR is transformed into the correct format required by the Primary Care EHR API.

Data Formatting Example:

python code

```
new_condition_dict['code']['coding'][0]['code'] = child_code
new_condition_dict['code']['coding'][0]['display'] = child_pref_term
new_condition_dict['code']['text'] = child_pref_term
new_condition_dict['bodySite'][0]['coding'][0]['code'] = site_code
new_condition_dict['bodySite'][0]['coding'][0]['display'] = bodysite_description
new_condition_dict['bodySite'][0]['text'] = bodysite_description
new_condition_dict['severity']['coding'][0]['code'] = "Not available"
new_condition_dict['subject']['reference'] = f"Patient/{patient_resource_id}"
```
3. Loading: Posting Data to the Target API (Primary Care EHR)
After transforming the data, it is sent to the target API using an HTTP POST request.

Process Involved:

Target API Endpoint:
The data is uploaded to the Primary Care EHR API at:
http://137.184.71.65:8080/fhir/Condition

Sending the Data:
The transformed data, stored in new_condition_dict, is included in the body of a POST request to the API.

Headers:
The Content-Type is set to application/json to indicate that the data is being sent in JSON format.

POST Request Example:

python code

```
def post_data(file_name, resource_name):
    url = BASE_SERVER_URL + '/' + f'{resource_name}'
    data = read_data(name_of_the_file=file_name)
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            print(f"Data posted successfully! - {resource_name}")
            print("Response:", response.json())
        else:
            print(f"Failed to post data - {resource_name}. Status code:", response.status_code)
            print("Error:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error during request:", e)
```
Error Handling:

If the POST request fails (e.g., due to an invalid token or data formatting issue), an error message with the status code is printed.
Network-related errors are caught and displayed as exceptions.

## Challenges and Solutions
1. Handling Missing Data:
Missing fields, such as body site or severity, are handled by assigning placeholder values (e.g., "Not available") to ensure the data structure remains intact.
2. Data Mapping Issues:
SNOMED CT code mismatches are resolved by performing multiple lookups (e.g., expression_constraint and get_body_site) to ensure correct terms are used.
3. API Authorization:
The access token is retrieved from a local file, and the process stops if the file is missing or if the token is invalid.
Summary of the ETL Pipeline
Extraction: Data is fetched from OpenEMR’s FHIR API using a GET request with Bearer token authentication.
Transformation: The data is cleaned and mapped to the required format, enriching it with SNOMED CT codes and body site information.
Loading: The cleaned and transformed data is posted to the Primary Care EHR API using a POST request.
Each step involves making requests to APIs, processing the data, and uploading it to the target system, ensuring proper integration between the source and target APIs.