# Mini SQL Engine

## Overview
This project is a simplified in-memory SQL engine written in Python. It can load CSV files and execute basic SQL queries (SELECT, WHERE, COUNT).

## Features
- Load CSV data into memory
- SELECT all or specific columns
- WHERE clause with basic conditions
- COUNT aggregation
- CLI interface to run queries

## Supported SQL Grammar
- `LOAD <filename> AS <table_name>`
- `SELECT * FROM <table_name>`
- `SELECT col1, col2 FROM <table_name>`
- `SELECT * FROM <table_name> WHERE col = 'value'`
- `SELECT COUNT(*) FROM <table_name>`
- `SELECT COUNT(col_name) FROM <table_name> WHERE col = 'value'`

## Usage
1. Clone the repo:  
   `git clone https://github.com/Lavanyakana/mini-sql-engine-23A91A1228.git`

2. Go into the folder:  
   `cd mini-sql-engine-23A91A1228`

3. Run the REPL:  
   `python repl.py`

4. Example commands:
```sql
LOAD sample_users.csv AS sample;
SELECT * FROM sample;
SELECT name, age FROM sample WHERE name = 'John';
SELECT COUNT(*) FROM sample;
# Mini SQL Engine (Python)

This project is a simple SQL query engine built in Python.  
It loads CSV files and supports a limited SQL grammar including:
- SELECT *
- SELECT col1, col2
- WHERE with conditions (=, <, >)
- COUNT(*)
- Loading CSV into memory
- Running queries through a CLI (REPL)

---

## 🚀 How to Run

### 1. Install Python 3
Make sure Python is installed:
