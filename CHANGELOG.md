# CHANGELOG



## v1.0.0 (2023-08-05)

### Ci

* ci: update release commit format ([`79a6d08`](https://github.com/jonbiemond/BCIT-Flex/commit/79a6d08416394280c1994acbc7646fcb0be08048))

* ci: update sr.yml with admin permissions ([`45544f2`](https://github.com/jonbiemond/BCIT-Flex/commit/45544f277126dacc9938f076957fa3a1dd7fbacf))

* ci: add auto versioning (#9) ([`6be6f9e`](https://github.com/jonbiemond/BCIT-Flex/commit/6be6f9efc4f556ed10058f9e37af860ec56cf565))

* ci: add ci workflow (#8)

Setup and config continuous integration. ([`28ede72`](https://github.com/jonbiemond/BCIT-Flex/commit/28ede72214cf00a69c5e4ad6a916b988fd3f1a4c))

### Documentation

* docs: add CONTRIBUTING.md ([`10c436a`](https://github.com/jonbiemond/BCIT-Flex/commit/10c436ab38ee39bbb1b0b82e3392f05e1cf0d372))

### Refactor

* refactor: separate course parsing logic into bcit_courses.py ([`b8407dc`](https://github.com/jonbiemond/BCIT-Flex/commit/b8407dc7bac65e1d6c22d97841ca9da6fe282d95))


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
