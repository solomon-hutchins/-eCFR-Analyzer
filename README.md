
# **eCFR Word Count Graphing Tool**

This project provides a web application that allows users to visualize word counts from the eCFR (Electronic Code of Federal Regulations). It enables the following features:

- **Bar chart of word counts by agency and title**: This visualizes the word count for a specific word across different titles and agencies.
- **Cumulative word count over time**: This shows how a specific word’s occurrences change over time, with cumulative counts displayed in a line chart.

## **Features**

1. **Word Count by Agency and Title**:
    - Bar chart displaying the total word count for a specific word across different agencies and titles in the eCFR.

2. **Word Count Over Time (Cumulative)**:
    - Line chart showing the cumulative occurrences of a specific word over time (e.g., per day). The points on the graph are displayed in red with red borders for clarity.

3. **Search Interface**:
    - A search bar that allows users to input a word and a date to track its occurrences over time.

4. **CSV Data Export**:
    - The app also supports fetching the word count data in CSV format.

## **Technologies Used**

- **Frontend**:
    - HTML5, CSS3, JavaScript
    - **Chart.js** for visualizing the word counts
    - **PapaParse** for parsing CSV files
- **Backend**:
    - Python with **Flask** for serving the app
    - **Requests** library to interact with the eCFR API
    - **CSV** for data management
- **Other**:
    - **eCFR API** for fetching regulatory data based on search queries.

## **Installation and Hosting Locally**

To run this project locally, follow the steps below.

### **Prerequisites**
Ensure you have **Python** and **pip** installed on your system.

### **Steps to Run Locally**

1. **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Install the required dependencies**:
    Create a virtual environment and install the necessary libraries:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. **Run the Flask application**:
    Inside your project directory, run the Flask app:
    ```bash
    python app.py
    ```

4. **Access the application**:
    Once the server is running, open your browser and navigate to:
    ```
    http://127.0.0.1:5000/
    ```

    You should now see the application running locally.

### **Requirements**

- Python 3.x
- Flask
- Requests
- Chart.js (included in the HTML)
- PapaParse (included in the HTML)

The dependencies are listed in the `requirements.txt` file. You can install them using `pip`:
```bash
pip install -r requirements.txt
```

### **Running the Application**

1. Open the app in a web browser at `http://127.0.0.1:5000/`.
2. **Word Count by Agency and Title**:
   - This will automatically load and display a bar chart of word counts across agencies and titles.
3. **Search Word Count Over Time**:
   - Enter a word and date, then click **Search and Plot** to see the cumulative word count over time. The graph will show cumulative counts per date.
4. **Refresh Graph**:
   - Click the **Refresh Graph** button to fetch the latest data and update the chart.

### **App Features**

- **Word Count Chart**:
    - This chart visualizes the total occurrences of a given word across different **agencies** and **titles**.
    - The data is visualized as a **stacked bar chart**, with each title's word count represented by a different color.

- **Cumulative Word Count Chart**:
    - This chart shows the **cumulative count** of a word’s occurrences over time.
    - The points on the chart are displayed in **red** with red borders for visibility.

- **Agency Table**:
    - Below the charts, there is a table that displays the agency names and their corresponding numbers.
    - The agencies are ordered by their numerical identifiers.

## **File Structure**

```
/project-root
│
├── app.py                  # Main Python Flask app
├── requirements.txt        # List of dependencies
├── /templates
│   └── index.html          # Frontend HTML file
└── /services
    └── data_processing.py  # Backend data processing (API requests, CSV handling)
```

### **Key Files**

1. **`app.py`**:
    - This file contains the main Flask application, handling routing, and serving both static content and dynamic data to the frontend.

2. **`index.html`**:
    - This is the frontend HTML file that renders the word count graphs and handles user input for word search and date selection.

3. **`data_processing.py`**:
    - This file contains the logic for fetching data from the eCFR API, processing it, and formatting it for display.

## **Important Notes**

- **API Rate Limits**: The eCFR API has a rate limit. If you are querying it frequently, make sure to handle rate-limiting and retries to avoid being blocked.
- **CSV File**: The word count data is exported as a CSV file. This file can be manually updated or refreshed by clicking the **Refresh Graph** button.