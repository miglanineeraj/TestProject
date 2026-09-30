# CSV Analyzer

A beginner-level Python project, written with object-oriented programming, that reads CSV data and answers simple questions about it.

The project has three parts:

1. **Local program** - analyzes a CSV file on your computer
2. **API** - a web service that downloads a CSV from a link, **accepts CSV only**, and answers questions as JSON
3. **API client** - a program that uses the API from code to answer the user's questions

## Project Structure

```
csv_project/
├── csv_project_oop.py      # Part 1: local program (classes)
├── csv_api.py              # Part 2: the API (Flask)
├── api_client.py           # Part 3: client that uses the API
├── employees.csv           # example data
├── requirements.txt        # packages to install
├── simple_csv_project.py   # first simple version (no classes)
├── csv_analyst.py          # advanced version (free-form questions)
└── README.md               # this file
```

## Requirements

- Python 3.8 or newer
- Packages: flask, requests, pandas

Install them once:

```
pip install -r requirements.txt
```

On Mac/Linux you may need `python3` and `pip3` instead of `python` and `pip`.

## Example Data

`employees.csv` has 15 employees with the columns `name`, `department`, `age`, `salary`, `experience`. The number columns are `age`, `salary` and `experience`.

---

## Part 1: Local Program

Analyzes a CSV file in the same folder.

```
python csv_project_oop.py
```

Enter `employees.csv` when asked, then ask questions.

| Command | What it does | Example |
|---|---|---|
| `average <column>` | Average of a number column | `average salary` |
| `sum <column>` | Sum of a number column | `sum salary` |
| `max <column>` | Largest value | `max age` |
| `min <column>` | Smallest value | `min experience` |
| `count` | Number of rows | `count` |
| `columns` | Column names | `columns` |
| `show` | First 10 rows | `show` |
| `quit` | Exit | `quit` |

---

## Part 2: The API

The API downloads data from another source (a link), checks that it is a CSV, analyzes it, and returns JSON.

### What it accepts

Only CSV. It rejects:
- links that are not `http://` or `https://`
- responses that are JSON, HTML or XML
- files larger than 5 MB
- text that cannot be read as a CSV table

### Endpoints

| Endpoint | What it does |
|---|---|
| `/` | Welcome message and list of endpoints |
| `/analyze?url=<csv link>` | Rows, columns and a 5-row preview |
| `/ask?url=<csv link>&question=<question>` | Answer to one question |

Questions supported by `/ask`: `average`, `sum`, `max`, `min` and `median` followed by a number column (for example `median salary`), plus `count` and `columns`.

### Answers and errors

Successful answer:
```json
{"action": "max", "answer": 50, "column": "age"}
```

Error (status 400):
```json
{"error": "Only CSV data is accepted (got: application/json)"}
```

### How it works

```
Request -> Flask route -> CSVFetcher.fetch() -> CSVAnalyzer -> JSON answer
```

**`CSVFetcher`** downloads and validates
- `fetch(url)` checks the URL, sends the web request, checks the status code, accepts CSV only, checks the size, and returns a pandas table

**`CSVAnalyzer`** analyzes the table
- `info()` returns rows, columns and a preview
- `calculate(action, column)` runs one calculation on a number column
- `answer(question)` reads a text question and returns the result

**Flask routes** connect the links to the classes. Every problem is raised as a `CSVError` and returned as a JSON error message.

---

## Part 3: API Client

`api_client.py` uses the API from code. It asks for a CSV link, then sends each question to the API and prints the answer.

- **`APIClient`** makes the API calls: `get_info(csv_url)` calls `/analyze`, and `ask(csv_url, question)` calls `/ask`
- **`ConsoleApp`** talks to the user: `start()` and `question_loop()`

Use it in your own code:

```python
from api_client import APIClient

client = APIClient()
ok, data = client.ask("http://127.0.0.1:8000/employees.csv", "average salary")
print(data["answer"] if ok else data["error"])
```

---

## How to Run the API and Client

Use three terminals, all opened in the project folder. Start them in this order.

**Terminal 1: serve `employees.csv` as a link**
```
python -m http.server 8000
```
The file is now available at `http://127.0.0.1:8000/employees.csv`.

**Terminal 2: start the API**
```
python csv_api.py
```
The API runs at `http://127.0.0.1:5000`.

**Terminal 3: run the client**
```
python api_client.py
```

Example session:
```
Enter the link of the CSV file: http://127.0.0.1:8000/employees.csv

--- Data loaded ---
Rows: 15
Columns: ['name', 'department', 'age', 'salary', 'experience']

Your question: max age
Answer: 50
```

Keep terminals 1 and 2 open while using terminal 3. Press `Ctrl+C` to stop a terminal.

If your CSV is already online (a link that returns CSV data), you can skip terminal 1 and paste that link instead.

## Testing the API in the Browser

With terminals 1 and 2 running, open:

```
http://127.0.0.1:5000/analyze?url=http://127.0.0.1:8000/employees.csv
http://127.0.0.1:5000/ask?url=http://127.0.0.1:8000/employees.csv&question=average salary
```

Expected answers for `employees.csv`:

| Question | Answer |
|---|---|
| `average salary` | about 64733.33 |
| `sum salary` | 971000 |
| `median salary` | 60000 |
| `max age` | 50 |
| `min experience` | 2 |
| `count` | 15 |

To test the CSV-only rule, create a file `data.json` containing `{"a": 1}` in the folder and open `.../analyze?url=http://127.0.0.1:8000/data.json`. The API answers with an error.

## Troubleshooting

| Problem | Cause and fix |
|---|---|
| `Missing 'url' parameter` | The link has no `?url=...`. Use `/analyze?url=<csv link>`, with one `?` and `&` between parameters. In a terminal, put the whole link in quotes |
| `Cannot reach the API` | `csv_api.py` is not running. Start terminal 2 first |
| `Could not download the data` | Terminal 1 is not running, or it was started in a folder without `employees.csv` |
| `Only CSV data is accepted` | The link returns JSON, HTML or something else, not CSV |
| `Column '...' is not a number column` | You used a text column such as `name` with `average`, `sum`, `max`, `min` or `median` |
| `No module named ...` | Run `pip install -r requirements.txt` |
| `Address already in use` | An old server is still running. Close it or use another port |

## Limitations

- Questions must be two words: an action and a column name (or `count` / `columns`)
- The maths commands work on number columns only
- Grouping such as "average salary by department" is not supported in the API (the advanced `csv_analyst.py` supports it for local files)

## Security Note

The API downloads any link it is given, so it is meant for learning on your own computer. Before putting it online, add an allow-list of trusted domains and turn off `debug=True` in `csv_api.py`.

## Ideas for Improvement

- Add grouping questions to the API
- Add a POST endpoint to accept a CSV link in the request body
- Draw charts with `matplotlib`
- Build a web page with Streamlit for the client
- Write automatic tests

## License

Free to use for learning.
