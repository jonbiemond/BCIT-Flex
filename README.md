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

`pip install bcitflex`

### Prerequisites
* A [PostgreSQL instance](https://www.postgresql.org/download/) is required for the database.
* Dependency `psycopg2` requires `libpq-dev` to be installed for Ubuntu/Debian systems.
```bash
sudo apt install libpq-dev python3-dev
```
For more details see the [pycopg2 documentation](https://www.psycopg.org/docs/install.html#install-from-source) and [StackOverflow](https://stackoverflow.com/questions/5420789/how-to-install-psycopg2-with-pip-on-python).

### DB Setup

PostgreSQL is used as the DBMS.
To create and initialize the database:

1. Create a database using the cli command. Pass `--help` for more information.
```bash
flask --app bcitflex create-db
```
2. Build schema using alembic:
```bash
flask --app bcitflex upgrade-db
```
3. Populate the database with subjects from psql:
```bash
\i bcitflex/scripts/populate_subject.sql
```

## Usage

To run the webscraper and populate the database with the latest course offerings:
```bash
poetry run flask --app bcitflex load-db
```

To run the dev webserver:
```bash
poetry run flask --app bcitflex run
```

## Supports

- Displaying all course offerings for specific course
- Saving all courses to a text file for a specific subject

## TODO

- Filter by prerequisites
- ~~Individual Course Offerings~~
- ~~Rate My Professors~~
- ~~Web app~~
- ~~GUI~~
- Return RMP rating

## Contributors

- Sam - [0x53616D75656C](https://github.com/0x53616D75656C)
- Jonathan - [jonbiemond](https://github.com/jonbiemond)
