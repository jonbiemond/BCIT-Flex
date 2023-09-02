# CHANGELOG



## v2.3.2 (2023-09-02)

### Fix

* fix(model): change Course.credits to type REAL

Type FLOAT(2) is automatically converted to REAL by postgres.
Consequently, the model and database fall out of sync, and `alembic check` will fail.
Explicitly declare credits as datatype REAL to avoid pre-commit failing. ([`7c993ef`](https://github.com/jonbiemond/BCIT-Flex/commit/7c993efd4fe3452c7cf363648e8522d6142fcd7e))

### Refactor

* refactor: drop legacy modules ([`9030b10`](https://github.com/jonbiemond/BCIT-Flex/commit/9030b10f8004379c1ee6206b382bb7430e3cd6f1))


## v2.3.1 (2023-09-01)

### Fix

* fix(model): leave primary key validation to the database

Do not validate that new object&#39;s PKs will not result in an integrity error. ([`2db074e`](https://github.com/jonbiemond/BCIT-Flex/commit/2db074e63c819ac603488b527f430ec35ebee104))


## v2.3.0 (2023-08-31)

### Chore

* chore(model): make course id seq explicit ([`364be1a`](https://github.com/jonbiemond/BCIT-Flex/commit/364be1a4f2a2c4eab6d063f7dcce836bac6055c8))

### Feature

* feat(model): add clone method

Add method to clone an object and its relationships. ([`f8c863f`](https://github.com/jonbiemond/BCIT-Flex/commit/f8c863f6a957f5b48e18f9bf46dca3facf4e4ed7))


## v2.2.0 (2023-08-11)

### Feature

* feat(model): add to_string method to Offering

Use tabulate to beautify meetings as string. ([`e0703bb`](https://github.com/jonbiemond/BCIT-Flex/commit/e0703bb23a107e568a189475e50e8dd4c5fa0ff8))

* feat(model): expose Meeting attributes in Offering ([`020b848`](https://github.com/jonbiemond/BCIT-Flex/commit/020b848df272f080afe7e080edfb114d1aaefaf2))

### Fix

* fix(model): add building to Meeting

Fix parse meeting_node to include building and room. ([`198fd4d`](https://github.com/jonbiemond/BCIT-Flex/commit/198fd4db0c62c110481c6848ba04acbf7fc3f9a9))


## v2.1.0 (2023-08-10)

### Documentation

* docs: add DB init instructions ([`895db50`](https://github.com/jonbiemond/BCIT-Flex/commit/895db50f402b188be53e58c3bef63b9aff7ff460))

### Feature

* feat(scripts): add parse_meeting_node

Drop tests for bcit_to_sql as they were overcomplicated and a bit redundant. ([`78b6056`](https://github.com/jonbiemond/BCIT-Flex/commit/78b6056334ed59a52cdef5678e077f4fa05794f2))

* feat(model): add Term model

- Declare term model and add table to the databse.
- Define relationship to term in offering model.
- Add term parsing functions to scrape_and_load.py.
- Update tests as necessary. ([`76ba22b`](https://github.com/jonbiemond/BCIT-Flex/commit/76ba22b60a857fb6fdfb38f7ee3f3bb7ec0457e6))

* feat(db): add meeting table

Drop server side partitioned sequence if favour of
SQLAlchemy/Python default. This solution may be less performant
but plays nicer with SQLAlchemy. Remove alembic migration d76.
Add next_meeting_id function to increment meeting_id before objects are persisted to the database. ([`cf07c1b`](https://github.com/jonbiemond/BCIT-Flex/commit/cf07c1ba22cb737cd4509d14e4cded3cae1222bc))

* feat(db): add nssequence_nestval function ([`8aac743`](https://github.com/jonbiemond/BCIT-Flex/commit/8aac743942a65d92684cb076789b7acb2870cb4d))

* feat(model): add Meeting model ([`d0eb4ed`](https://github.com/jonbiemond/BCIT-Flex/commit/d0eb4eda786df484f9a6917bca8868bfdf8a53e5))


## v2.0.0 (2023-08-06)

### Chore

* chore: update poetry.lock ([`eb36983`](https://github.com/jonbiemond/BCIT-Flex/commit/eb369836952900b472e2fa244155b20ce575a623))

* chore: update README.md format ([`6a9aa8d`](https://github.com/jonbiemond/BCIT-Flex/commit/6a9aa8d9e151a944ffb21d701f5249e7eb2fad1e))

### Documentation

* docs: add pytest-cov to CONTRIBUTING.md ([`eb77a7d`](https://github.com/jonbiemond/BCIT-Flex/commit/eb77a7d8fc21ebe0be6394f4d24570b9280f8b0b))

### Feature

* feat(gui): update simple_gui to work with database ([`8883bbe`](https://github.com/jonbiemond/BCIT-Flex/commit/8883bbe08471f138535f8b300f0dda95775cb50a))

* feat: add populate_subject.sql

Add SQL script to easily populate the subject table. ([`de27efd`](https://github.com/jonbiemond/BCIT-Flex/commit/de27efdc25e43ec18ee68683d481e3e825dfb6e9))

* feat(model): add to_string to Course ([`4a1672b`](https://github.com/jonbiemond/BCIT-Flex/commit/4a1672b76999c451d90604087d217f35c5fbbaea))

* feat(model): add get_course to Subject ([`6b9b8e4`](https://github.com/jonbiemond/BCIT-Flex/commit/6b9b8e4f1eef27264685a74a75ca3cc93b56a8a8))

* feat(model): add meeting_time to Offering ([`c4f71ca`](https://github.com/jonbiemond/BCIT-Flex/commit/c4f71ca2ae42418988b1114e5906c491a0c88437))

* feat(model): get CRN in parse_offering_node

Alter offering.crn to string and drop sequence.
Closes #2 ([`55a429e`](https://github.com/jonbiemond/BCIT-Flex/commit/55a429e74c3abc76fdb7daf271ba70067128180b))

* feat: add bcit_to_sql

Add a webscraping and loading script with tests.
- Add get_course_urls()
- Add extract_models()
- Add load_models()
- Add bcit_to_sql() ([`5d3b651`](https://github.com/jonbiemond/BCIT-Flex/commit/5d3b651a5442e8205f0556fbe4ba7a9d491a6991))

* feat: add prep_db and scrape_course_urls

- Add course_list_response.pkl to test data. ([`d8ca836`](https://github.com/jonbiemond/BCIT-Flex/commit/d8ca8369c1d560f8b372ee743cd6301fbdce290e))

* feat: delete children passively

Let the database handle cascades for unloaded children. ([`e8e2601`](https://github.com/jonbiemond/BCIT-Flex/commit/e8e26015c43b2b4ddc71af7b082d317aa2802c43))

* feat: add on delete cascade to fk constraints

Replace python types with SQLAlchemy types in models. ([`7342927`](https://github.com/jonbiemond/BCIT-Flex/commit/7342927ad58ab3f59aab47809b75e7ba2c44f80e))

* feat: add Subject model ([`38a725c`](https://github.com/jonbiemond/BCIT-Flex/commit/38a725ce9971dbf8e8c40f407e8991c924242a7d))

* feat: add offering_count and is_available ([`caf8e0e`](https://github.com/jonbiemond/BCIT-Flex/commit/caf8e0edf0ee2cfba700832e1468b635487d89e3))

* feat: factor out course parsing logic

Abstract course parsing logic into separate function.
Add CoursePage class to couple url to HTMLParser. ([`5e1aae5`](https://github.com/jonbiemond/BCIT-Flex/commit/5e1aae5dd7933a8594aaf3e2f080241fbda7f648))

* feat: add Course model

Declare, add migration and tests for the Course model. ([`c974126`](https://github.com/jonbiemond/BCIT-Flex/commit/c974126869830b562839401c50fa77d0ffe07770))

* feat: add Offering model

- Refactor MeetingTable into a separate file, at least temporarily,
to maker refactoring Offering easier.
- Declare the Offering model.
- Add tests for Offering and remove old offering tests.
- Add migration for Offering model.
- Update .pre-commit-config.yaml ruff hook version to match project dependency.
- Add RUF012 to ruff ignore, because it is violated by SQLAlchemy __table_args__. ([`ae55ebd`](https://github.com/jonbiemond/BCIT-Flex/commit/ae55ebd6ebfe80672151213abfffe5a89dccc853))

* feat: alembic init

Initialize alembic for database migrations and
  update dependencies. ([`0c13528`](https://github.com/jonbiemond/BCIT-Flex/commit/0c135288f01ade95ec40f07a1d29cf7968aec755))

### Fix

* fix(db): alter course field types

Alter course.url to VARCHAR(120) to allow for longer URLs.
Alter course.prerequisites to TEXT. ([`80bd5f8`](https://github.com/jonbiemond/BCIT-Flex/commit/80bd5f8e2445f7e52d7ef0deff652e2097345293))

* fix: add new_offering fixture to test_course.py

The new_course fixture, of course_id 2, was assigned
the conftest offering fixture of course_id 1. ([`87a20a7`](https://github.com/jonbiemond/BCIT-Flex/commit/87a20a7dcdceca2187aa7c9873cb0bf052d855b4))

### Refactor

* refactor: drop modules.subject.py

- Add TODO comments ([`36414bb`](https://github.com/jonbiemond/BCIT-Flex/commit/36414bbf0fe42c79d7f9b797318b3ad113b73e16))

* refactor: extract_course_data.py to scrape_and_load.py ([`de08363`](https://github.com/jonbiemond/BCIT-Flex/commit/de08363dc7a9b6e7742e04bb3ee62bac9a10123c))

* refactor: chunk out course-parsing logic into smaller units

Maintaining and testing is easier if the logic is separated by object. ([`595471b`](https://github.com/jonbiemond/BCIT-Flex/commit/595471ba1b9566b007974ebac2c70331fcf5e5f5))

### Test

* test: add dbtest decorator ([`f2f5357`](https://github.com/jonbiemond/BCIT-Flex/commit/f2f53571e3e2c7cc5b3036c80314c80274da6448))

* test: add string rep test ([`714ad56`](https://github.com/jonbiemond/BCIT-Flex/commit/714ad5622b4d80c537c85b9153518de13bde62c1))

* test: pre-populate test database

Populate the test database with test data during setup.
This way, tests can be more independent and there&#39;s less redundancy. ([`356cc08`](https://github.com/jonbiemond/BCIT-Flex/commit/356cc080add407886a629b20fe164a110ed94088))

* test: configure test database

Tests should be self-contained.
Run tests in a separate test database.
Configure alembic to run setup test db with migrations. ([`26e3b17`](https://github.com/jonbiemond/BCIT-Flex/commit/26e3b17c10df6c829f858e26b0033cb5d967d9f0))

* test: add offering db transaction tests ([`c72629e`](https://github.com/jonbiemond/BCIT-Flex/commit/c72629e3d165fc2328006c67947baf800b57f660))

* test: add test for parse_offering_node()

- Add load_test_data.py script for extracting and loading test_data.
- Add Response test data. ([`189e5b4`](https://github.com/jonbiemond/BCIT-Flex/commit/189e5b41860bbe1aa5ebb25c110ae50a25c8d410))

### Unknown

* tests: clean up redundant tests ([`cc6fed4`](https://github.com/jonbiemond/BCIT-Flex/commit/cc6fed476283bc1032696f01b3a7658d3157113e))

* tests: add @dbtest mark to db dependant texts

Add @dbtest decorator for tests that connect to the database.
Use non-db fixture in test_parse_offering_node. ([`1432850`](https://github.com/jonbiemond/BCIT-Flex/commit/14328500c1667264613fc53abdbcbd0a8101f0b6))

* lint: add black hook to alembic.ini

- Add alembic hook to .pre-commit-config.yaml ([`23ed218`](https://github.com/jonbiemond/BCIT-Flex/commit/23ed21856533c478bad7295b11e5699b688c1d08))


## v1.0.0 (2023-08-06)

### Ci

* ci: disable upload to release for semantic-release ([`796c101`](https://github.com/jonbiemond/BCIT-Flex/commit/796c101c0b955afe4d8be0f99ada7f117cbdec05))

* ci: update release commit format ([`79a6d08`](https://github.com/jonbiemond/BCIT-Flex/commit/79a6d08416394280c1994acbc7646fcb0be08048))

* ci: update sr.yml with admin permissions ([`45544f2`](https://github.com/jonbiemond/BCIT-Flex/commit/45544f277126dacc9938f076957fa3a1dd7fbacf))

* ci: add auto versioning (#9) ([`6be6f9e`](https://github.com/jonbiemond/BCIT-Flex/commit/6be6f9efc4f556ed10058f9e37af860ec56cf565))

* ci: add ci workflow (#8)

Setup and config continuous integration. ([`28ede72`](https://github.com/jonbiemond/BCIT-Flex/commit/28ede72214cf00a69c5e4ad6a916b988fd3f1a4c))

### Documentation

* docs: add CONTRIBUTING.md ([`10c436a`](https://github.com/jonbiemond/BCIT-Flex/commit/10c436ab38ee39bbb1b0b82e3392f05e1cf0d372))

### Refactor

* refactor: separate course parsing logic into bcit_courses.py ([`b8407dc`](https://github.com/jonbiemond/BCIT-Flex/commit/b8407dc7bac65e1d6c22d97841ca9da6fe282d95))

### Unknown

* v1.0.0

Manual release by Jonathan Biemond. ([`ea9bd12`](https://github.com/jonbiemond/BCIT-Flex/commit/ea9bd12bda2789a7aa33f2fef99616ec78828dec))


## v0.1.1 (2023-07-23)

### Fix

* fix: update requests dependency

Since Requests v2.3.0, Requests has been vulnerable to potentially leaking Proxy-Authorization headers to destination servers, specifically during redirects to an HTTPS origin. ([`daec4e2`](https://github.com/jonbiemond/BCIT-Flex/commit/daec4e26906c980dc5b5f12d4a964df554c94ad0))


## v0.1.0 (2023-07-23)

### Build

* build: migrate to poetry

Add black, ruff and pre-commit. ([`ea796aa`](https://github.com/jonbiemond/BCIT-Flex/commit/ea796aa2c49a758d3587a9712586079956caaee3))

### Unknown

* Merge branch &#39;user-interface&#39;

# Conflicts:
#	main.py ([`bba2a01`](https://github.com/jonbiemond/BCIT-Flex/commit/bba2a019750738767e3343e84a2fc49b1d142539))

* Drop main.py

Functionality refactored into subject.py and interface.py. ([`3ff8c23`](https://github.com/jonbiemond/BCIT-Flex/commit/3ff8c23fce1bbc01c3e44ac2088678f700539f57))

* Add not_on_any_days() to Offering

-Refactor weekdays variable into constant. ([`c2f6486`](https://github.com/jonbiemond/BCIT-Flex/commit/c2f6486380cb17dfc02f76ec22f1b49aac6014bc))

* Update test_offering_not_on_days() to take a list of days

-Add test to check for Exception when day is not valid. ([`8904291`](https://github.com/jonbiemond/BCIT-Flex/commit/89042914d52bc9c877898c1efa7944e4f2e2ed0a))

* Add location() to MeetingTable ([`466732b`](https://github.com/jonbiemond/BCIT-Flex/commit/466732b5eb0c0fbef030e3abca9572a725f7a421))

* Add time methods to MeetingTable

Add start_time() and end_time() to MeetingTable. ([`83d273a`](https://github.com/jonbiemond/BCIT-Flex/commit/83d273a1b8dd93dbb3ab1de6e1b8f99b8f21ecd5))

* Add days() to MeetingTable ([`f117a62`](https://github.com/jonbiemond/BCIT-Flex/commit/f117a627ce04ae3a474da04034dff03b9398cbea))

* Add date methods to MeetingTable

Add start_date() and end_date() to MeetingTable. ([`d56fdda`](https://github.com/jonbiemond/BCIT-Flex/commit/d56fdda87fb20c2175d681f96ab9051fecac21eb))

* Test: update MeetingTable date tests

Expect exceptions instead of values of None when dates are missing or invalid. ([`4d358be`](https://github.com/jonbiemond/BCIT-Flex/commit/4d358beb786c1d57d880bfcb68e2f72be43d711e))

* Test: add MeetingTable attribute tests

Add __init__.py to modules to simplify import into tests. ([`d98f753`](https://github.com/jonbiemond/BCIT-Flex/commit/d98f75356380606028f69880cf95183d3c90a170))

*  Update interface.py styling to support beautified meeting times ([`c30614f`](https://github.com/jonbiemond/BCIT-Flex/commit/c30614f63646b48c2598098e271990715a9e465b))

* Beautify meeting times

- Add MeetingTable class to offering.py to hold meeting data
- Parse meeting_time row into list of elements to pass to MeetingTable
- Display MeetingTable with tabulate
- Update requirements.txt with tabulate ([`30a2b95`](https://github.com/jonbiemond/BCIT-Flex/commit/30a2b9506025bd9fd41a988db9f62563d64826bd))

* Update main.py

Bug fix - Filtered out courses with status label &#34;Seats Available&#34; ([`b86e9b4`](https://github.com/jonbiemond/BCIT-Flex/commit/b86e9b4007da273782b2d07cbade3eb9982341b1))

* Add icon to simple_gui() ([`8910ca4`](https://github.com/jonbiemond/BCIT-Flex/commit/8910ca47295128a056f897065d8bc7947a6915e1))

* Update simple_gui() style

- Add tooltip to Save button
- Remove scroll bar from some popups
- Add title to subject error popup ([`b8e1d64`](https://github.com/jonbiemond/BCIT-Flex/commit/b8e1d649cea3c2178de4ca48d04d116071b77229))

* Handle invalid subject input

- Update dropdown items formatting to show available offerings. ([`bce421f`](https://github.com/jonbiemond/BCIT-Flex/commit/bce421f147df59e052cceb9bd4f92eefd946b4d4))

* Update README.md with GUI usage

Add GUI usage steps with images. Add Contributors section. ([`d14a9c4`](https://github.com/jonbiemond/BCIT-Flex/commit/d14a9c41347d4c92b13689b5938fcb677fb79fff))

* Add Course.offering_count() ([`c5a717c`](https://github.com/jonbiemond/BCIT-Flex/commit/c5a717ccb7452346533c57069d98e926560813ec))

* Set custom theme ([`abce9a0`](https://github.com/jonbiemond/BCIT-Flex/commit/abce9a0e9b3c6cd3c9c65083c221899691083a72))

* Change simple_gui() layout

Change layout to be more intuitive and add input field titles.
Make Combo element readonly. ([`313c486`](https://github.com/jonbiemond/BCIT-Flex/commit/313c486a2cbb6f993ad5f35634fb9d7939c12413))

* Add course selection dropdown to simple_gui() ([`dedaacf`](https://github.com/jonbiemond/BCIT-Flex/commit/dedaacf13087ec987cb74dccd209790e9bd65abe))

* Raise exception if URL response returns an error ([`9189bf7`](https://github.com/jonbiemond/BCIT-Flex/commit/9189bf75280e963555db974608dbc099160e090b))

* Raise error if subject does not have any courses

- Light refactoring.
- Set ThreadPoolExecutor to default number of threads, to avoid potential inefficiencies. ([`dc81f04`](https://github.com/jonbiemond/BCIT-Flex/commit/dc81f04ecc2cd73b802091a284f97d9e7422af40))

* Fix multithreading in available_courses()

Rewrite ThreadPoolExecutor() context block to successfully implement multithreading. ([`56eac0c`](https://github.com/jonbiemond/BCIT-Flex/commit/56eac0c6cbec2780004fd44bb2b66e2daa47046e))

* Update README.md ([`badbbac`](https://github.com/jonbiemond/BCIT-Flex/commit/badbbac59721746a4095d4880741683505385593))

* Add .gitignore file ([`7d44b7e`](https://github.com/jonbiemond/BCIT-Flex/commit/7d44b7e845202ccec3aa4579448d9962c656df71))

* Add To File button to simple_gui()

- Store Subject objects in dictionary for multiple loops. ([`1e30eb8`](https://github.com/jonbiemond/BCIT-Flex/commit/1e30eb89dfdd838490cb177bcd7671ddc7aebc62))

* Add Offering status attribute

- Return all offerings regardless of status.
- Get status from status_node and pass to Offering.
- Add feature to Course.to_string() to default to available offerings only. ([`e41fdf2`](https://github.com/jonbiemond/BCIT-Flex/commit/e41fdf289748a8f53f6874d263ecaa2c8154a3b6))

* Add simple_gui() to interface.py

- Update requirements.txt ([`45ec873`](https://github.com/jonbiemond/BCIT-Flex/commit/45ec8738faf7ef2af7d6883be2fc0c412d9dd80c))

* Fix get_valid_course() ([`2cc18e0`](https://github.com/jonbiemond/BCIT-Flex/commit/2cc18e0622ef1b4e3749ab0d6c89d850e2fee628))

* Add .to_string() method to Course and Offering

-Update Subject.to_file() to use Course.to_string()
-Add subject attribute to Course
-Update parse_url() to pass subject and code to Course separately ([`7bb0a0c`](https://github.com/jonbiemond/BCIT-Flex/commit/7bb0a0c1f3b683af8c2c3549327a8fb9d5576f9d))

* Copy changes to subject.py ([`5ecf1eb`](https://github.com/jonbiemond/BCIT-Flex/commit/5ecf1eb569121a66b9d6f75ae95b05f171d0becd))

* Merge remote-tracking branch &#39;origin/main&#39; into user-interface ([`9ee5106`](https://github.com/jonbiemond/BCIT-Flex/commit/9ee5106cea4c89ac41ca449cfcd799f776e90af0))

* Add interface.py

Rename main.py to interface.py. Revert main.py back to source branch to maintain merge compatibility. ([`5f222c2`](https://github.com/jonbiemond/BCIT-Flex/commit/5f222c2cefee40a2d7384c3b25f930bd0eaf10f0))

* Update main.py ([`501ac70`](https://github.com/jonbiemond/BCIT-Flex/commit/501ac708948fd22bc5ff42a4f4c9acfb6c28308c))

* Update main.py ([`c3c61cc`](https://github.com/jonbiemond/BCIT-Flex/commit/c3c61ccc8d3d038dbded2563b2a28272fe9b4ae6))

* Update main.py ([`9193b32`](https://github.com/jonbiemond/BCIT-Flex/commit/9193b325c826fb3aeb5e995983036dc6184a8136))

* Add subject.py

- Move parse_url functions from main.py to subject.py module.
- Create Subject class to hold Course list and methods.
- Add get_valid_course() to main.py. ([`0d74008`](https://github.com/jonbiemond/BCIT-Flex/commit/0d74008dbc6cf3005d090c6245fc89318e66b6c2))

* Update README.md ([`8e0aefa`](https://github.com/jonbiemond/BCIT-Flex/commit/8e0aefa53b39478c0b5ac41458068a92a73916bf))

* Add files via upload ([`c94158b`](https://github.com/jonbiemond/BCIT-Flex/commit/c94158b765e3d5d4cd9e33f47d35f9090da8e1ba))
