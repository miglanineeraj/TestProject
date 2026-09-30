import os

import pandas as pd


class CSVAnalyzer:
    """Loads a CSV file and does the analysis."""

    def __init__(self, filename):
        self.filename = filename
        self.data = None          # will hold the table after loading

    def resolve_path(self):
        """Use the script directory for relative paths."""
        if os.path.isabs(self.filename):
            return self.filename
        project_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(project_dir, self.filename)

    def load(self):
        """Read the CSV file. Returns True if it worked."""
        try:
            absolute_path = self.resolve_path()
            self.data = pd.read_csv(absolute_path)
            return True
        except FileNotFoundError:
            print("File not found:", self.filename)
            return False
        except PermissionError:
            print("Permission denied while reading:", self.filename)
            return False
        except OSError as exc:
            print(f"Could not read file '{self.filename}': {exc}")
            return False

    def show_info(self):
        print("\n--- Basic Information ---")
        print("Rows:", self.count())
        print("Columns:", self.columns())
        print("\nFirst 5 rows:")
        print(self.data.head())

    def count(self):
        return len(self.data)

    def columns(self):
        return list(self.data.columns)

    def has_column(self, name):
        return name in self.data.columns

    def average(self, column):
        return self.data[column].mean()

    def total(self, column):
        return self.data[column].sum()

    def maximum(self, column):
        return self.data[column].max()

    def minimum(self, column):
        return self.data[column].min()


class QuestionAnswerer:
    """Understands the user's question and asks the analyzer for the answer."""

    def __init__(self, analyzer):
        self.analyzer = analyzer

    def answer(self, question):
        question = question.lower().strip()

        if question == "count":
            return f"Number of rows: {self.analyzer.count()}"
        if question == "columns":
            return f"Columns: {self.analyzer.columns()}"
        if question == "show":
            return str(self.analyzer.data.head(10))

        words = question.split()          # "average salary" -> ["average", "salary"]
        if len(words) == 2 and self.analyzer.has_column(words[1]):
            action, column = words

            if action == "average":
                return f"Average of {column}: {self.analyzer.average(column)}"
            if action == "sum":
                return f"Sum of {column}: {self.analyzer.total(column)}"
            if action == "max":
                return f"Maximum of {column}: {self.analyzer.maximum(column)}"
            if action == "min":
                return f"Minimum of {column}: {self.analyzer.minimum(column)}"
            return "Unknown action. Try: average, sum, max, min"

        return "Sorry, I didn't understand. Example: average salary"

    def run(self):
        """Keep asking questions until the user types quit."""
        print("\nAsk a question. Examples:")
        print("  average <column>   sum <column>   max <column>   min <column>")
        print("  count              columns        show           quit")

        while True:
            question = input("\nYour question: ")
            if question.lower().strip() == "quit":
                print("Goodbye!")
                break
            print(self.answer(question))


# ---------------- main program ----------------
if __name__ == "__main__":
    filename = input("Enter filename (default: employees.csv): ") or "employees.csv"

    analyzer = CSVAnalyzer(filename)
    if analyzer.load():
        analyzer.show_info()
        bot = QuestionAnswerer(analyzer)
        bot.run()
