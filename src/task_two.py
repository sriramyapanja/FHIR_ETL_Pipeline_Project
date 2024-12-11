import json
import requests
from pathlib import Path
from src.registration import data_dir
from src.data_templates import new_condition_dict

BASE_URL = "https://in-info-web20.luddy.indianapolis.iu.edu/apis/default/fhir"
PRIMARY_CARE_SERVER_URL = "http://137.184.71.65:8080/fhir"
BASE_HERMES_URL = 'http://159.65.173.51:8080/v1/snomed'
BASE_HERMES_URL2 = 'http://159.65.173.51:8080/v1/snomed/concepts'


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


def expression_constraint(concept_id):
    search_string = f"<! {concept_id}"
    response = requests.get(f'{BASE_HERMES_URL}/search?constraint={search_string}')
    data = response.json()
    if len(data):
        first_item_from_results = data[0]
        first_concept_id = first_item_from_results['conceptId']
        first_concept_term = first_item_from_results['preferredTerm']
        return first_concept_id, first_concept_term

def get_body_site(snomed_id):
    response = requests.get(f'{BASE_HERMES_URL2}/{snomed_id}/extended')
    data = response.json()
    parent_relationships = data['directParentRelationships']
    finding_site= parent_relationships['363698007']
    finding_site_code= finding_site[0]
    finding_site_description_response = requests.get(f'{BASE_HERMES_URL2}/{finding_site_code}/extended')
    finding_site_data= finding_site_description_response.json()
    finding_site_description = finding_site_data['preferredDescription']['term']
    return finding_site_code, finding_site_description

def get_snomed_code(patient_resource_id):
    url = f'{BASE_URL}/Condition?patient={patient_resource_id}'
    response = requests.get(url=url, headers=get_headers())
    data = response.json()
    if 'entry' in data:
        conditions = data['entry']
        thirty_condition = conditions[30]
        snomed_code = thirty_condition['resource']['code']['coding'][0]['code']
        child = expression_constraint(concept_id=snomed_code)
        child_code = child[0]
        child_pref_term = child[1]
        print(child_pref_term)
        body_site = get_body_site(snomed_id=child_code)
        site_code = body_site[0]
        bodysite_description = body_site[1]

        url = f'{BASE_URL}/Patient/{patient_resource_id}'
        response = requests.get(url=url, headers=get_headers())
        data = response.json()

        new_condition_dict['onsetDateTime'] = data['address'][0]['period']['start']
        new_condition_dict['code']['coding'][0]['code'] = child_code
        new_condition_dict['code']['coding'][0]['display'] = child_pref_term
        new_condition_dict['code']['text'] = child_pref_term
        with open(data_dir / 'patient_resource_id.txt', 'r') as f:
            patient_resource_id = f.readline()
        new_condition_dict['bodySite'][0]['coding'][0]['code'] = site_code
        new_condition_dict['bodySite'][0]['coding'][0]['display'] = bodysite_description
        new_condition_dict['bodySite'][0]['text'] = bodysite_description

        new_condition_dict['severity']['coding'][0]['code']= "Not available"
        new_condition_dict['severity']['coding'][0]['display']= "Not Available"
        new_condition_dict['subject']['reference'] = f"Patient/{patient_resource_id}"




        try:
            headers = {
                'Accept': "application/json"
            }
            url = PRIMARY_CARE_SERVER_URL + '/' + 'Condition'
            response = requests.post(url=url, json=new_condition_dict, headers=headers)
            if response.status_code == 200 or response.status_code == 201:
                response_data = response.json()
                #pprint(response_data)
                print('Condition resource created.')
            else:
                print(f'Error - {response.status_code}')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    patient_resource_id = '985ac75c-54cd-47ab-afe1-93d52db5ba48'
    get_snomed_code(patient_resource_id=patient_resource_id)