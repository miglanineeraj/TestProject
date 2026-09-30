# CSV Analyzer

A beginner-level Python project that reads a CSV file, shows basic information about it, and answers simple questions about the data. It is written with object-oriented programming (classes and objects).

## Features

- Loads any CSV file using pandas
- Shows the number of rows, the column names, and the first 5 rows
- Answers questions such as `average salary` or `max age`
- Handles a missing file with a friendly message instead of crashing

## Project Structure

```
csv_project/
├── csv_project_oop.py   # the main program
├── employees.csv        # example data
└── README.md            # this file
```

## Requirements

- Python 3.8 or newer
- pandas

Install pandas once:

```
pip install pandas
```

## How to Run

1. Put `csv_project_oop.py` and `employees.csv` in the same folder.
2. Open a terminal in that folder.
3. Run:

   ```
   python csv_project_oop.py
   ```

   (On Mac/Linux you may need `python3` instead of `python`.)

4. When asked, type the file name:

   ```
   Enter CSV file name (example: data.csv): employees.csv
   ```

5. Ask questions. Type `quit` to exit.

## Available Commands

| Command | What it does | Example |
|---|---|---|
| `average <column>` | Average of a number column | `average salary` |
| `sum <column>` | Sum of a number column | `sum salary` |
| `max <column>` | Largest value | `max age` |
| `min <column>` | Smallest value | `min experience` |
| `count` | Number of rows | `count` |
| `columns` | List of column names | `columns` |
| `show` | First 10 rows | `show` |
| `quit` | Exit the program | `quit` |

The `average`, `sum`, `max` and `min` commands work on number columns only (in the example file: `age`, `salary`, `experience`).

## Example Session

```
Your question: max age
Maximum of age: 50

Your question: sum salary
Sum of salary: 971000

Your question: count
Number of rows: 15

Your question: quit
Goodbye!
```

## How It Works

The program has two classes:

**`CSVAnalyzer`** holds the data and does the calculations.
- `load()` reads the CSV file into a pandas table
- `show_info()` prints an overview
- `count()`, `columns()`, `has_column()` give information about the table
- `average()`, `total()`, `maximum()`, `minimum()` calculate on one column

**`QuestionAnswerer`** talks to the user.
- `answer(question)` splits the question into words (for example `["average", "salary"]`), checks the column exists, and asks the analyzer for the result
- `run()` keeps asking questions in a loop until you type `quit`

Flow of the program:

```
Start -> ask for file name -> load CSV -> show info -> question loop -> quit
```

## Using Your Own CSV File

Your file should have column names in the first row, with values separated by commas:

```
name,department,salary
Anna,Sales,50000
Bo,Sales,60000
```

Column names in your questions must match the file exactly (lowercase works best).

## Limitations

- Questions must be exactly two words: an action and a column name
- The maths commands fail on text columns (for example `average name`)
- Grouping such as "average salary by department" is not supported

## Ideas for Improvement

- Add a `median` method and command
- Check that a column is numeric before calculating
- Add "by department" style grouping
- Draw charts with `matplotlib`
- Build a simple web interface with Streamlit

## License

Free to use for learning.
