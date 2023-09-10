[![ci](https://github.com/jonbiemond/BCIT-Flex/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/jonbiemond/BCIT-Flex/actions/workflows/ci.yml)
# BCIT Flex
[www.bcitflex.tech](http://www.bcitflex.tech)

A website for easily viewing BCIT course offerings.
Features a course filter to aid in course selection.

Please feel free to report any issues, bugs or suggestions. Pull requests are welcome.

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
3. Populate the subject table with the list of subjects to scrape courses for:
```bash
flask --app bcitflex load-subjects
```
By default, subjects COMP, MATH, COMM AND BLAW are loaded. To load all subjects pass the `--all-subjects` flag.

## Usage

To run the webscraper and populate the database with the latest course offerings:
```bash
flask --app bcitflex load-db
```

To run the dev webserver:
```bash
flask --app bcitflex run
```

## Roadmap

- Filter by prerequisites
- ~~Individual Course Offerings~~
- ~~Rate My Professors~~
- ~~Web app~~
- ~~GUI~~
- Return RMP rating
- Indication of data freshness
- Program information
- User relevant course view
- User course wishlist
- User course schedule planner

## Contributors

- Sam - [0x53616D75656C](https://github.com/0x53616D75656C)
- Jonathan - [jonbiemond](https://github.com/jonbiemond)
