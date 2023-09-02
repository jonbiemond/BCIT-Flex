[![ci](https://github.com/jonbiemond/BCIT-Flex/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/jonbiemond/BCIT-Flex/actions/workflows/ci.yml)
# BCIT Flex
Webscrape BCIT available courses, quickly view course offerings and write the information to a text file

Please feel free to report any issues, bugs or suggestions. Pull requests are welcome.

The information is

- Code
- Name
- Prerequisites
- Credits
- URL
- Offerings
  - Instructor
  - Price
  - Duration
  - Meeting Times
  - Status
  - Rate My Professor URLs

## Installation

- Clone the repository
- Install the requirements `poetry install`

### DB Setup

PostgreSQL is used as the DBMS.
To create and initialize the database:

1. Create a database named `bcitflex` from psql:
```bash
\i bcitflex/scripts/init_db.sql
```
2. Add user credentials to [.pgpass file](https://www.postgresql.org/docs/current/libpq-pgpass.html)
```text
*:*:*:python_app:<password>
```
3. Build schema using alembic:
```bash
poetry run alembic upgrade head
```
4. Populate the database with subjects from psql:
```bash
\i bcitflex/scripts/populate_subject.sql
```
5. Save database connection string to `<PROJECT DIR>/instance/config.py`:
```python
DATABASE = "postgresql://python_app@localhost:5432/bcitflex"
```

## Usage

To run the webscraper and populate the database with the latest course offerings:
```bash
poetry run flask --app bcitflex load-db
```

## Supports

- Displaying all course offerings for specific course
- Saving all courses to a text file for a specific subject

## TODO

- Filter by prerequisites
- ~~Individual Course Offerings~~
- ~~Rate My Professors~~
- WebAssembly
- ~~GUI~~
- Return RMP rating

## Contributors

- Sam - [0x53616D75656C](https://github.com/0x53616D75656C)
- Jonathan - [jonbiemond](https://github.com/jonbiemond)
