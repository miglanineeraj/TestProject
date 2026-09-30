# CSV Analyzer API - beginner project (object oriented)
#
# What it does:
#   1. You send it a URL (a link to data on another website/server)
#   2. It downloads the data with a web request
#   3. It ACCEPTS CSV ONLY (JSON, HTML, images, etc. are rejected)
#   4. It analyzes the CSV and answers your question as JSON
#
# Run:   python csv_api.py
# Needs: pip install flask requests pandas

import io
import json
from urllib.parse import urlparse

import pandas as pd
import requests
from flask import Flask, jsonify, request

MAX_SIZE = 5 * 1024 * 1024  # refuse files bigger than 5 MB


class CSVError(Exception):
    """Our own error, used when the data is not a valid CSV."""


# ---------------------------------------------------------------
# Class 1: downloads the data and makes sure it is a CSV
# ---------------------------------------------------------------
class CSVFetcher:
    def __init__(self, timeout=10):
        self.timeout = timeout  # seconds to wait for the other server

    def fetch(self, url):
        """Download the URL and return a pandas table. Raises CSVError if not CSV."""

        # Step 1: check the URL looks valid
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise CSVError("Invalid URL. It must start with http:// or https://")

        # Step 2: request the data from the other source
        try:
            response = requests.get(url, timeout=self.timeout)
        except requests.exceptions.RequestException as error:
            raise CSVError(f"Could not download the data: {error}")

        if response.status_code != 200:
            raise CSVError(f"The other server answered with status {response.status_code}")

        # Step 3: accept CSV only
        content_type = response.headers.get("Content-Type", "").lower()
        url_is_csv = parsed.path.lower().endswith(".csv")
        type_is_csv = "csv" in content_type
        type_is_other = "html" in content_type or "json" in content_type or "xml" in content_type

        if type_is_other or not (url_is_csv or type_is_csv):
            raise CSVError("Only CSV data is accepted (got: " + (content_type or "unknown") + ")")

        if len(response.content) > MAX_SIZE:
            raise CSVError("File is too big (maximum 5 MB)")

        # Step 4: make sure the text really can be read as a CSV table
        try:
            table = pd.read_csv(io.StringIO(response.text))
        except Exception:
            raise CSVError("The file could not be read as a CSV table")

        if table.empty:
            raise CSVError("The CSV file has no data rows")

        return table


# ---------------------------------------------------------------
# Class 2: does the analysis on a table
# ---------------------------------------------------------------
class CSVAnalyzer:
    ACTIONS = ("average", "sum", "max", "min", "median")

    def __init__(self, table):
        self.table = table

    def info(self):
        """Basic information about the data."""
        preview = json.loads(self.table.head(5).to_json(orient="records"))
        return {
            "rows": len(self.table),
            "columns": list(self.table.columns),
            "preview": preview,
        }

    def calculate(self, action, column):
        """Do one calculation on one number column."""
        if column not in self.table.columns:
            raise CSVError(f"Column '{column}' not found. Columns: {list(self.table.columns)}")
        if not pd.api.types.is_numeric_dtype(self.table[column]):
            raise CSVError(f"Column '{column}' is not a number column")

        values = self.table[column]
        if action == "average":
            result = values.mean()
        elif action == "sum":
            result = values.sum()
        elif action == "max":
            result = values.max()
        elif action == "min":
            result = values.min()
        elif action == "median":
            result = values.median()
        else:
            raise CSVError(f"Unknown action '{action}'. Use: {', '.join(self.ACTIONS)}")

        return result.item()  # convert numpy number to normal Python number

    def answer(self, question):
        """Understand a question like 'average salary' and return the answer."""
        question = question.lower().strip()

        if question == "count":
            return {"answer": len(self.table)}
        if question == "columns":
            return {"answer": list(self.table.columns)}

        words = question.split()
        if len(words) != 2:
            raise CSVError("Question must look like: average salary")

        action, column = words
        return {"action": action, "column": column, "answer": self.calculate(action, column)}


# ---------------------------------------------------------------
# The web API (Flask)
# ---------------------------------------------------------------
app = Flask(__name__)
fetcher = CSVFetcher()


@app.route("/")
def home():
    return jsonify(
        message="CSV Analyzer API. Only CSV data is accepted.",
        endpoints={
            "/analyze?url=<csv link>": "basic information about the CSV",
            "/ask?url=<csv link>&question=average salary": "answer a question",
        },
    )


@app.route("/analyze")
def analyze():
    url = request.args.get("url")
    if not url:
        return jsonify(error="Missing 'url' parameter"), 400
    try:
        table = fetcher.fetch(url)
        return jsonify(CSVAnalyzer(table).info())
    except CSVError as error:
        return jsonify(error=str(error)), 400


@app.route("/ask")
def ask():
    url = request.args.get("url")
    question = request.args.get("question")
    if not url or not question:
        return jsonify(error="Missing 'url' or 'question' parameter"), 400
    try:
        table = fetcher.fetch(url)
        return jsonify(CSVAnalyzer(table).answer(question))
    except CSVError as error:
        return jsonify(error=str(error)), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
