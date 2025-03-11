import requests
import json

# API Base URL
BASE_URL = "https://www.ecfr.gov/api/admin/v1"

# Function to fetch agencies and their CFR references
def fetch_agencies_and_cfr_references():
    url = f"{BASE_URL}/agencies.json"  # API URL for agencies
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch agency data. Status Code: {response.status_code}")
        return None

    data = response.json()  # Convert response to JSON
    agencies_list = []

    # Function to process an agency and its CFR references
    def process_agency(agency):
        agency_entry = {
            "name": agency["name"],
            "slug": agency["slug"],
            "cfr_references": [
                {
                    "title": ref["title"],
                    "chapter": ref.get("chapter", "N/A")  # Default to "N/A" if "chapter" is missing
                }
                for ref in agency.get("cfr_references", [])
            ],
        }
        agencies_list.append(agency_entry)

        # If the agency has child agencies, process them too
        for child in agency.get("children", []):
            process_agency(child)

    # Iterate through all top-level agencies and process them
    for agency in data.get("agencies", []):
        process_agency(agency)

    return agencies_list

# Function to save agency data as JSON
def save_agency_data_to_json(agency_data, filename="agencies_data.json"):
    try:
        with open(filename, 'w') as file:
            json.dump(agency_data, file, indent=4)  # Save with nice formatting
        print(f"Agency data saved to {filename}")
    except Exception as e:
        print(f"Error saving agency data to JSON: {e}")

# Main function to fetch and save agency data
def main():
    agencies_data = fetch_agencies_and_cfr_references()
    if agencies_data:
        save_agency_data_to_json(agencies_data)

# Run the script to fetch and save agency data
main()
