import xml.etree.ElementTree as ET
import json
import csv
import os
import time
import concurrent.futures
from services.api_requests import fetch_title_chapter
from services.api_requests import get_latest_date


def count_words_in_title_chapter(date, title, chapter):
    retries = 5
    for attempt in range(retries):
        response = fetch_title_chapter(date, title, chapter)

        if response.status_code == 429:
            print(f"Rate limit exceeded. Retrying after {2**attempt} seconds...")
            time.sleep(2 ** attempt)
            continue
        elif response.status_code != 200:
            print(f"Failed to fetch XML for Title {title}, Chapter {chapter}. Status Code: {response.status_code}")
            return None

        root = ET.fromstring(response.content)
        return sum(len(" ".join(tag.itertext()).split()) for tag in root.iter() if tag.tag.lower() in ["p", "h1", "h2"])

    return None

def load_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

def save_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def export_to_csv(results, filename="word_counts.csv"):
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Agency", "Slug", "Title", "Chapter", "Word Count"])

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        for result in results:
            writer.writerow([result["agency"], result["slug"], result["title"], result["chapter"], result["word_count"]])

def process_agency_words(agency, ref, latest_date, processed_dates):
    title = ref["title"]
    chapter = ref["chapter"]
    amendment_date = ref.get("latest_amended_on", "not available")

    if amendment_date and processed_dates.get(f"{title}-{chapter}") != amendment_date:
        print(f"Processing: {agency['name']} - Title {title}, Chapter {chapter}")
        word_count = count_words_in_title_chapter(latest_date, title, chapter)
        if word_count is not None:
            processed_dates[f"{title}-{chapter}"] = amendment_date
            return {"agency": agency["name"], "slug": agency["slug"], "title": title, "chapter": chapter, "word_count": word_count}
    return None

import concurrent.futures
import json

import concurrent.futures
import json

def process_all_agencies_and_chapters(agency_data_file, processed_dates_file="processed_dates.json"):
    try:
        print("Loading agency data...")
        agencies_data = load_json(agency_data_file)
        if not agencies_data:
            print("No agencies data found")
            return "No agency data found."

        print(f"Loaded {len(agencies_data)} agencies")

        processed_dates = load_json(processed_dates_file) or {}
        latest_date = get_latest_date()
        print(f"Using latest date: {latest_date}")

        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(process_agency_words, agency, ref, latest_date, processed_dates): (agency, ref)
                for agency in agencies_data for ref in agency.get("cfr_references", [])
            }

            for future in concurrent.futures.as_completed(futures):
                agency, ref = futures[future]
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as e:
                    print(f"Error processing {agency['name']} - Title {ref.get('title', '')}, Chapter {ref.get('chapter', '')}: {str(e)}")

        if not results:
            return "No valid results to export."

        print(f"Exporting {len(results)} results to CSV...")
        export_to_csv(results)
        save_json(processed_dates, processed_dates_file)

        return "CSV file updated successfully"

    except Exception as e:
        print("Error in process_all_agencies_and_chapters:", str(e))
        return f"Error: {str(e)}"


