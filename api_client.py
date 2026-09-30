# API Client - uses the CSV Analyzer API to answer the user's questions
#
# Before running this, the API must be running:   python csv_api.py
# Then run this file in another terminal:         python api_client.py
# Needs: pip install requests

import requests

API_URL = "http://127.0.0.1:5000"   # where csv_api.py is running


class APIClient:
    """Talks to the CSV Analyzer API. Each method is one API call."""

    def __init__(self, api_url=API_URL):
        self.api_url = api_url

    def _get(self, endpoint, params):
        """Send a GET request to the API and return (ok, data)."""
        try:
            # params= builds the link for us:  /ask?url=...&question=...
            # (it also converts spaces to %20 automatically)
            response = requests.get(f"{self.api_url}/{endpoint}", params=params, timeout=20)
        except requests.exceptions.ConnectionError:
            return False, {"error": "Cannot reach the API. Is csv_api.py running?"}
        except requests.exceptions.RequestException as error:
            return False, {"error": str(error)}

        data = response.json()          # the API answers in JSON
        return response.status_code == 200, data

    def get_info(self, csv_url):
        """Call /analyze to get rows, columns and a preview."""
        return self._get("analyze", {"url": csv_url})

    def ask(self, csv_url, question):
        """Call /ask to get the answer to one question."""
        return self._get("ask", {"url": csv_url, "question": question})


class ConsoleApp:
    """The part that talks to the user."""

    def __init__(self, client):
        self.client = client
        self.csv_url = None

    def start(self):
        self.csv_url = input("Enter the link of the CSV file: ").strip()

        # First call: check the link and show basic information
        ok, info = self.client.get_info(self.csv_url)
        if not ok:
            print("Error:", info["error"])
            return

        print("\n--- Data loaded ---")
        print("Rows:", info["rows"])
        print("Columns:", info["columns"])

        self.question_loop()

    def question_loop(self):
        print("\nAsk a question. Examples:")
        print("  average salary   max age   sum salary   median salary   count   columns")
        print("Type 'quit' to exit.")

        while True:
            question = input("\nYour question: ").strip()

            if question.lower() == "quit":
                print("Goodbye!")
                break

            # Each question is sent to the API
            ok, data = self.client.ask(self.csv_url, question)

            if ok:
                print("Answer:", data["answer"])
            else:
                print("Error:", data["error"])


if __name__ == "__main__":
    client = APIClient()
    app = ConsoleApp(client)
    app.start()
