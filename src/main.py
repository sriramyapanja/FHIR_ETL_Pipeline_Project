import requests
from credentials import BASE_SERVER_URL

# Optional: Define any parameters you want to include in the request
params = {
    "key1": "value1",
    "key2": "value2"
}

# Optional: Define headers, if needed
headers = {
    "Accept": "application/json",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}


def get_all_resources(resource_name):
    try:
        url = BASE_SERVER_URL + '/' + f'{resource_name}?_count=150&_sort=_lastUpdated'
        # Send GET request
        response = requests.get(url, headers=headers)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse JSON response if available
            data = response.json()
            print(f"Resource {resource_name} retrieved successfully!")
            if 'entry' in data:
                for item in data['entry']:
                    print(item['fullUrl'])
            else:
                print("No data retrieved successfully!")
        else:
            print("Failed to retrieve data. Status code:", response.status_code)
            print("Error:", response.text)

    except requests.exceptions.RequestException as e:
        print("Error during request:", e)


def get_resource(resource_name, resource_id):
    try:
        url = BASE_SERVER_URL + '/' + f'{resource_name}' '/' + f'{resource_id}'
        # Send GET request
        response = requests.get(url, headers=headers)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse JSON response if available
            data = response.json()
            print(data)
            print(f"{resource_name} retrieved successfully!")
            print(f"Resource ID: {data['id']}")
            resource_url = BASE_SERVER_URL + '/' + f'{resource_name}' + '/' f"{data['id']}"
            print(f"Resource URL: {resource_url}")
            print(f"Website URL: http://137.184.71.65:8000/{resource_name.lower()}/{data['id']}")
            print()
        else:
            print("Failed to retrieve data. Status code:", response.status_code)
            print("Error:", response.text)

    except requests.exceptions.RequestException as e:
        print("Error during request:", e)


def print_resources():
    get_all_resources(resource_name='Patient')
    get_all_resources(resource_name='Practitioner')
    get_all_resources(resource_name='Observation')
    get_all_resources(resource_name='Procedure')
    get_all_resources(resource_name='Condition')
    print()


def print_resource():
    get_resource(resource_name='Patient', resource_id=1)
    get_resource(resource_name='Practitioner', resource_id=4)
    get_resource(resource_name='Observation', resource_id=5)
    get_resource(resource_name='Procedure', resource_id=6)
    get_resource(resource_name='Condition', resource_id=7)


if __name__ == '__main__':
    print_resources()
    print_resource()
