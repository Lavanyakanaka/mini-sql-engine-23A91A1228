Mini SQL Database Engine
A simplified, in-memory SQL query engine built from scratch in Python.
This project demonstrates the core principles of database query processing by implementing a parser and execution engine for basic SQL operations.

Features
Load data from CSV files into memory
Parse and execute SQL queries
Support for SELECT, FROM, WHERE, and COUNT operations
Interactive command-line interface (REPL)
Comprehensive error handling
Modular design: parser, engine, CLI separated
Supported SQL Grammar
SELECT Statement
SELECT * FROM table
SELECT column1, column2 FROM table
SELECT COUNT(*) FROM table
SELECT COUNT(column_name) FROM table

WHERE Clause
SELECT * FROM table WHERE column = 'value'
SELECT * FROM table WHERE column != 'value'
SELECT * FROM table WHERE column > 100
SELECT * FROM table WHERE column < 100
SELECT * FROM table WHERE column >= 100
SELECT * FROM table WHERE column <= 100

Supported Operators

= : Equal to

!= : Not equal to

> : Greater than

< : Less than

>= : Greater than or equal to

<= : Less than or equal to

Limitations

Only single WHERE condition supported (no AND/OR)

String values must be enclosed in single quotes

Table name is derived from the CSV filename (without .csv extension)

Installation

1. Clone this repository:
git clone https://github.com/PavaniVattikolla/mini-sql-engine.git
cd mini-sql-engine
2. Install required dependencies:
pip install faker
Python's csv module is built-in; no installation needed.

Setup
Generate Sample Data

Run the generator to create sample CSV files:
python generate_sample_data.py

This will create:

-> data/employees.csv – 50 rows of employee data

-> data/products.csv – 30 rows of product data

Tip: Using data/ folder keeps CSVs separate and organized.

Usage
Start CLI
python cli.py

Commands

LOAD <filepath> – Load a CSV file

SELECT … – Run SQL queries

HELP – Show commands and grammar

EXIT / QUIT – Exit the CLI

Examples
-- Select all columns
SELECT * FROM employees

-- Select specific columns
SELECT name, age, salary FROM employees

-- Filter with WHERE clause
SELECT * FROM employees WHERE age > 30
SELECT name, department FROM employees WHERE country = 'USA'

-- Count rows
SELECT COUNT(*) FROM employees
SELECT COUNT(name) FROM employees WHERE department = 'Engineering'

Error Handling

Invalid SQL syntax

Non-existent columns or tables

Missing CSV files

Type mismatches in WHERE

Unsupported SQL operations

Project Structure
mini-sql-engine/
│
├── cli.py                  # Command-line interface
├── engine.py               # Query execution engine
├── parser.py               # SQL parser
├── generate_sample_data.py # Sample data generator
├── README.md               # Project documentation
├── .gitignore
├── LICENSE                 # (Add MIT or other license)
└── data/                   # CSV files
    ├── employees.csv
    └── products.csv


Future Enhancements

Support multiple WHERE conditions (AND/OR)

JOIN operations between tables

Additional aggregate functions (SUM, AVG, MIN, MAX)

ORDER BY and LIMIT

INSERT, UPDATE, DELETE operations

Persistent storage for tables

Automated test suite

Requirements

Python 3.7+

faker library (for sample data generation)

Author

Created as part of the Partnr Network Global Placement Program.
