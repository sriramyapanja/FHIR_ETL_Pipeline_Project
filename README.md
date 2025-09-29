
# ETL Pipeline Documentation
### Project Description
We developed an ETL pipeline integrating with FHIR APIs to streamline healthcare data management. The pipeline extracts, transforms, and loads patient data into target systems, ensuring interoperability and consistency. This project shows how effective data integration using technology can improve patient care and healthcare workflows.


## Healthcare Data Migration - OpenEMR to Primary Care EHR

This documentation outlines the ETL (Extract, Transform, Load) process used to transfer patient condition data from OpenEMR to a Primary Care EHR system using FHIR standards. The pipeline ensures seamless data migration while maintaining clinical accuracy and data integrity.

---

## Project Overview

**Objective**: Migrate patient condition data from OpenEMR FHIR API to Primary Care EHR API while enriching data with SNOMED CT terminology and maintaining clinical workflow continuity.

**Technology Stack**: Python, FHIR APIs, SNOMED CT Hermes API, JSON data processing

**Data Standards**: FHIR R4, SNOMED CT, Healthcare interoperability standards

---

##  Architecture Overview


### Data Flow
1. **Extract**: Retrieve patient and condition data from OpenEMR
2. **Transform**: Clean, validate, and enrich data with SNOMED CT terminology
3. **Load**: Post standardized data to Primary Care EHR system

---

##  API Endpoints

### Source System (OpenEMR)
- **Base URL**: `https://in-info-web20.luddy.indianapolis.iu.edu/apis/default/fhir`
- **Patient Endpoint**: `Patient/{patient_resource_id}`
- **Condition Endpoint**: `Condition?patient={patient_resource_id}`

### Target System (Primary Care EHR)
- **Base URL**: `http://137.184.71.65:8080/fhir`
- **Patient Endpoint**: `Patient`
- **Condition Endpoint**: `Condition`
- **Observation Endpoint**: `Observation`
- **Procedure Endpoint**: `Procedure`

### External Services
- **SNOMED CT Hermes**: For terminology lookup and data enrichment

---

## Authentication

### Bearer Token Authentication
```python
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

**Security Features**:
- Token-based authentication for secure API access
- Error handling for missing or invalid tokens
- Local token storage with validation

---

##  ETL Process Details

### 1. Extraction Phase

**Patient Data Retrieval**:
```python
def get_fhir_patient(patient_resource_id):
    url = f'{BASE_URL}/Patient/{patient_resource_id}'
    response = requests.get(url=url, headers=get_headers())
    data = response.json()
    # Process patient demographics, addresses, identifiers
```

**Condition Data Retrieval**:
```python
def search_condition(patient_resource_id):
    url = f'{BASE_URL}/Condition?patient={patient_resource_id}'
    response = requests.get(url=url, headers=get_headers())
    data = response.json()
    # Extract SNOMED CT codes and clinical data
```

### 2. Transformation Phase

**Data Cleaning and Validation**:
- Handle missing fields with appropriate placeholders
- Validate SNOMED CT codes against terminology services
- Map source data to target API format requirements
- Enrich data with additional clinical terminology

**SNOMED CT Enrichment**:
```python
def expression_constraint(concept_id):
    search_string = f"<! {concept_id}"
    response = requests.get(f'{BASE_HERMES_URL}/search?constraint={search_string}')
    data = response.json()
    if len(data):
        first_item_from_results = data[0]
        return first_item_from_results['conceptId'], first_item_from_results['preferredTerm']
```

**Data Mapping**:
```python
# Transform condition data
new_condition_dict['code']['coding'][0]['code'] = child_code
new_condition_dict['code']['coding'][0]['display'] = child_pref_term
new_condition_dict['bodySite'][0]['coding'][0]['code'] = site_code
new_condition_dict['severity']['coding'][0]['code'] = "Not available"
```

### 3. Loading Phase

**Data Upload Process**:
```python
def post_data(file_name, resource_name):
    url = BASE_SERVER_URL + '/' + f'{resource_name}'
    data = read_data(name_of_the_file=file_name)
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code in [200, 201]:
            print(f"Data posted successfully! - {resource_name}")
        else:
            print(f"Failed to post data - {resource_name}. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error during request:", e)
```

---

## Implementation Tasks

### Task 1: Parent SNOMED Term Processing
- Extract patient conditions from OpenEMR
- Retrieve parent SNOMED CT terms via Hermes API
- Create new Patient and Condition resources
- Post to Primary Care EHR system

### Task 2: Child SNOMED Term Processing
- Reuse patient data from Task 1
- Query child terms using SNOMED CT hierarchy
- Transform and post enriched condition data

### Task 3: Observation Resource Creation
```python
observation_data = {
    "resourceType": "Observation",
    "code": {"coding": [{"code": "85354-9", "display": "Blood pressure panel"}]},
    "valueQuantity": {"systolic": 120, "diastolic": 80},
    "subject": {"reference": f"Patient/{patient_resource_id}"},
    "effectiveDateTime": "2024-12-10"
}
```

### Task 4: Procedure Resource Creation
```python
procedure_data = {
    "resourceType": "Procedure",
    "code": {"coding": [{"code": "428191000124101", "display": "Blood test procedure"}]},
    "subject": {"reference": f"Patient/{patient_resource_id}"},
    "performedDateTime": "2024-12-10"
}
```

---

## Error Handling & Data Quality

### Missing Data Management
- **Placeholder Values**: Use "Not Available" for missing severity or other optional fields
- **Validation Rules**: Ensure required FHIR fields are populated
- **Data Integrity**: Maintain referential integrity between Patient and Condition resources

### API Error Handling
- **Authentication Failures**: Graceful handling of token expiration
- **Network Issues**: Retry mechanisms and error logging
- **Data Validation**: Response code validation (200/201 for success)

### SNOMED CT Mapping Challenges
- **Code Resolution**: Multiple lookup strategies for terminology matching
- **Hierarchy Navigation**: Parent-child relationship traversal
- **Body Site Mapping**: Accurate anatomical location identification

---

## Getting Started

### Prerequisites
- Python 3.7+
- Access to OpenEMR FHIR API
- SNOMED CT Hermes API access
- Primary Care EHR API credentials

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/etl-pipeline.git
cd etl-pipeline

# Install dependencies
pip install -r requirements.txt

# Set up authentication
# Place your access_token.json in the data directory
```

### Configuration
1. **Update API endpoints** in configuration files
2. **Add authentication tokens** to `access_token.json`
3. **Configure data directories** for input/output files
4. **Set up logging** for monitoring and debugging

### Running the Pipeline
```python
# Execute main ETL process
if __name__ == '__main__':
    patient_resource_id = '985ac75c-54cd-47ab-afe1-93d52db5ba48'
    get_snomed_code(patient_resource_id=patient_resource_id)
```

---

## Project Structure
# ETL Pipeline

## src
- extraction.py
- transformation.py
- loading.py
- utils.py

## data
- access_token.json
- patient_resource_id.txt

## config
- api_config.py

## tests
- test_pipeline.py

## root
- requirements.txt
- README.md

---

## Key Features

### Data Enrichment
- **SNOMED CT Integration**: Automatic terminology lookup and validation
- **Clinical Context**: Body site and severity mapping
- **Terminology Standards**: FHIR-compliant code systems

### Interoperability
- **FHIR Compliance**: Full R4 standard implementation
- **Healthcare Standards**: SNOMED CT, LOINC integration
- **API Integration**: RESTful service communication

### Data Quality
- **Validation Rules**: Clinical data validation
- **Error Handling**: Comprehensive error management
- **Audit Trail**: Complete data lineage tracking

---

## Business Value

### Clinical Benefits
- **Data Continuity**: Seamless patient care transitions
- **Terminology Standardization**: Consistent clinical coding
- **Interoperability**: System-to-system data exchange

### Technical Benefits
- **Scalability**: Handles large patient datasets
- **Reliability**: Robust error handling and validation
- **Maintainability**: Modular, well-documented codebase

---

## Contact & Support

**Project Lead**: Sri Ramya Panja
- **Email**: sriramyapanja123@gmail.com
- **LinkedIn**: [www.linkedin.com/in/sriramyapanja](https://www.linkedin.com/in/sriramyapanja)

---


*This ETL pipeline demonstrates expertise in healthcare data interoperability, FHIR standards implementation, and clinical terminology management - essential skills for healthcare informatics professionals.*



Project's website can be accessed using the link below

 https://sriramyapanja.github.io/FHIR_ETL_Pipeline_Project/
