import requests

BASE_URL = "https://www.ecfr.gov/api/versioner/v1"

from datetime import datetime, timedelta

def get_latest_date():
    url = "https://www.ecfr.gov/api/versioner/v1/titles"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        titles = data.get("titles", [])
        valid_dates = [title.get("up_to_date_as_of") for title in titles if title.get("up_to_date_as_of")]

        if valid_dates:
            latest_date_str = min(valid_dates)  # Get the latest date as a string
            print(f"Latest date found: {latest_date_str}")

            # Convert to datetime object
            latest_date = datetime.strptime(latest_date_str, "%Y-%m-%d")

            # Subtract 3 days
            new_date = latest_date - timedelta(days=3)

            # Convert back to string in the same format
            new_date_str = new_date.strftime("%Y-%m-%d")
            print(f"Using latest date: {new_date_str}")
            return new_date_str

    print("No valid dates found, returning None")
    return None


def fetch_title_chapter(date, title, chapter):
    url = f"{BASE_URL}/full/{date}/title-{title}.xml?chapter={chapter}"
    return requests.get(url)
