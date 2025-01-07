# COMP0035 Coursework starter repository for 2024-25

Edit the contents of this readme before submitting your coursework on Moodle.
1.Introduction
This project provides a set of tools for managing and analyzing local government housing data stored in a SQLite database. The project includes query, insert, update, join query and aggregate statistics functions.

2.Directory Structure
project/
├── coursework1/
│   └── database/
│       └── local_authority_housing.db   # SQLite database file
├── coursework2/
│   ├── section3/
│   │   ├── queries_select.py
│   │   ├── queries_insert.py
│   │   ├── queries_update.py
│   │   ├── queries_join.py
│   │   └── queries_aggregate.py
│   └── test/
│       ├── test_select.py
│       ├── test_insert.py
│       ├── test_update.py
│       ├── test_join.py
│       └── test_aggregate.py
├── requirements.txt
└── README.md

3.Installation and Configuration

Creating a Virtual Environment: python -m venv .venv

Activate the virtual environment: .\.venv\Scripts\activate

Check Python version and environment: 
where python
where pip

Install:
pip install pytest

Run the following command to confirm the pytest version: pytest --version

Running Tests:
pytest coursework2/test/test_select.py
pytest coursework2/test/test_delete.py
pytest coursework2/test/test_insert.py
pytest coursework2/test/test_update.py
pytest coursework2/test/test_join.py
pytest coursework2/test/test_aggregate.py


4.Using function codes
SELECT query function:
python coursework2/section3/queries_select.py
Insert new data:
python coursework2/section3/queries_insert.py
Update data:
python coursework2/section3/queries_update.py
JOIN query:
python coursework2/section3/queries_join.py
Aggregate query:
python coursework2/section3/queries_aggregate.py
