import requests

def fetch_package_info(package_name):
    url = f"https://registry.npmjs.org/{package_name}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch package info for '{package_name}'. Status Code: {response.status_code}")
        package_info = response.json()
        return package_info
    except requests.RequestException as e:
        raise Exception(f"Error fetching package info for '{package_name}': {str(e)}")
    except ValueError as e:
        raise Exception(f"Error parsing JSON for '{package_name}': {str(e)}")