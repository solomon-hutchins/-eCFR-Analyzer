import requests
import xml.etree.ElementTree as ET
import json
import csv
import concurrent.futures
import time
import os

# API Base URL
BASE_URL = "https://www.ecfr.gov/api/versioner/v1"

# Function to fetch the latest available date
def get_latest_date():
    url = f"{BASE_URL}/titles"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch latest date. Status Code: {response.status_code}")
        return None

    data = response.json()

    # Ensure response contains "titles" key
    if "titles" not in data or not isinstance(data["titles"], list):
        print(f"Unexpected API response format: {data}")
        return None

    # Extract valid date strings and filter out None or invalid values
    valid_dates = [title["up_to_date_as_of"] for title in data["titles"] 
                   if isinstance(title.get("up_to_date_as_of"), str)]

    if not valid_dates:
        print("No valid 'up_to_date_as_of' dates found in API response.")
        return None

    return min(valid_dates)  # Get the most recent valid date

# Function to fetch and parse XML, then count words in <p> and header tags
def count_words_in_title_chapter(date, title, chapter):
    url = f"{BASE_URL}/full/{date}/title-{title}.xml?chapter={chapter}"

    # Retry logic for handling rate-limiting (HTTP 429)
    retries = 5
    for attempt in range(retries):
        response = requests.get(url)

        if response.status_code == 429:
            print(f"Rate limit exceeded. Retrying after {2**attempt} seconds...")
            time.sleep(2 ** attempt)  # Exponential backoff
            continue
        elif response.status_code != 200:
            print(f"Failed to fetch XML for Title {title}, Chapter {chapter}. Status Code: {response.status_code}")
            return None

        # Parse the XML
        root = ET.fromstring(response.content)

        total_word_count = 0

        # Collect words from <p> and header tags
        for tag in root.iter():
            if tag.tag.lower() in ["p", "h1", "h2", "h3", "h4", "h5", "h6"]:  # Include paragraphs and headers
                text = "".join(tag.itertext())  # Get all text including nested formatting tags like <I>, <B>
                text = " ".join(text.split())  # Clean up spaces and line breaks
                total_word_count += len(text.split())  # Count words

        return total_word_count

    print(f"Exceeded retries for Title {title}, Chapter {chapter}. Skipping.")
    return None

# Function to load agency data from a separate file
def load_agency_data(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)  # Assuming the file is in JSON format
    except Exception as e:
        print(f"Error loading agency data: {e}")
        return None

# Function to load or initialize a CSV file to store results
def initialize_results_csv(filename="word_counts.csv"):
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Agency", "Slug", "Title", "Chapter", "Word Count"])
    return filename

# Function to export results to a CSV file
def export_to_csv(results, filename="word_counts.csv"):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        for result in results:
            writer.writerow([result["agency"], result["slug"], result["title"], result["chapter"], result["word_count"]])

# Function to process one agency's CFR references and count words in parallel
def process_agency_words(agency, ref, latest_date, processed_dates):
    title = ref["title"]
    chapter = ref["chapter"]

    # Get the latest amendment date from the reference, with a fallback to "not available"
    amendment_date = ref.get("latest_amended_on", "not available")

    # Check if the title/chapter needs to be recalculated based on the latest amendment date
    if amendment_date and processed_dates.get(f"{title}-{chapter}") != amendment_date:
        print(f"Recalculating for Agency: {agency['name']} | Title {title}, Chapter {chapter}...")
        word_count = count_words_in_title_chapter(latest_date, title, chapter)
        if word_count is not None:
            processed_dates[f"{title}-{chapter}"] = amendment_date  # Update last processed date
            return {
                "agency": agency["name"],
                "slug": agency["slug"],
                "title": title,
                "chapter": chapter,
                "word_count": word_count
            }
    return None

# Function to iterate over all agencies, titles, and chapters, counting words in parallel
def process_all_agencies_and_chapters(agency_data_file, processed_dates_file="processed_dates.json"):
    # Load agency data from the file
    agencies_data = load_agency_data(agency_data_file)
    if not agencies_data:
        print("Exiting: No agency data found.")
        return

    latest_date = get_latest_date()
    if not latest_date:
        print("Exiting: No valid date found.")
        return

    print(f"Using latest available date: {latest_date}")

    # Load or initialize processed dates
    processed_dates = {}
    if os.path.exists(processed_dates_file):
        with open(processed_dates_file, 'r') as file:
            processed_dates = json.load(file)

    # Create or initialize the results CSV file
    csv_file = initialize_results_csv()

    results = []

    # Create a ThreadPoolExecutor for parallel processing of agencies' CFR references
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_agency = {}

        # Submit tasks for each agency's CFR references to the thread pool
        for agency in agencies_data:
            for ref in agency["cfr_references"]:
                future = executor.submit(process_agency_words, agency, ref, latest_date, processed_dates)
                future_to_agency[future] = agency

        # Collect the results as they complete
        for future in concurrent.futures.as_completed(future_to_agency):
            result = future.result()
            if result:
                results.append(result)

    # Export results to CSV
    export_to_csv(results, csv_file)

    # Save the updated processed dates
    with open(processed_dates_file, 'w') as file:
        json.dump(processed_dates, file, indent=4)

    print("Word count data exported successfully.")

# Example: File path for saved agency data (in JSON format)
agency_data_file = "agencies_data.json"  # Update with the actual file path

# Run the process
process_all_agencies_and_chapters(agency_data_file)
