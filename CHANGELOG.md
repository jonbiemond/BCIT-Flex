# CHANGELOG



## v3.11.0 (2024-01-16)

### Chore

* chore(deps-dev): bump gitpython from 3.1.37 to 3.1.41

Bumps [gitpython](https://github.com/gitpython-developers/GitPython) from 3.1.37 to 3.1.41.
- [Release notes](https://github.com/gitpython-developers/GitPython/releases)
- [Changelog](https://github.com/gitpython-developers/GitPython/blob/main/CHANGES)
- [Commits](https://github.com/gitpython-developers/GitPython/compare/3.1.37...3.1.41)

---
updated-dependencies:
- dependency-name: gitpython
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`408b0fe`](https://github.com/jonbiemond/BCIT-Flex/commit/408b0feb6b671668b99f3704105b0a8d49086c2b))

* chore(deps): bump jinja2 from 3.1.2 to 3.1.3

Bumps [jinja2](https://github.com/pallets/jinja) from 3.1.2 to 3.1.3.
- [Release notes](https://github.com/pallets/jinja/releases)
- [Changelog](https://github.com/pallets/jinja/blob/main/CHANGES.rst)
- [Commits](https://github.com/pallets/jinja/compare/3.1.2...3.1.3)

---
updated-dependencies:
- dependency-name: jinja2
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`e91b2f6`](https://github.com/jonbiemond/BCIT-Flex/commit/e91b2f669bf221e9b900c4d9f8e7b8f131683cf8))

### Feature

* feat(app): add prereq table to course page

Add a table listing prerequisite courses to the course page.

Closes #86 ([`7488e79`](https://github.com/jonbiemond/BCIT-Flex/commit/7488e793db37ba5d6e0a2e8f2bf7d4d654e5806f))

* feat(scraper): parse prerequisites into db objects

Add function to parse Course prerequisite string into database objects.

Closes #84 ([`3e6d2a8`](https://github.com/jonbiemond/BCIT-Flex/commit/3e6d2a8a5bd83111b2d4c1a2d548c76bf26e59a0))

* feat(model): add Prerequisite model

- Update parsing tests to be regex based. ([`bae9f63`](https://github.com/jonbiemond/BCIT-Flex/commit/bae9f63aac6675219fb11759185168d89f93a034))


## v3.10.0 (2023-12-11)

### Chore

* chore(deps): bump werkzeug from 2.3.7 to 2.3.8

Bumps [werkzeug](https://github.com/pallets/werkzeug) from 2.3.7 to 2.3.8.
- [Release notes](https://github.com/pallets/werkzeug/releases)
- [Changelog](https://github.com/pallets/werkzeug/blob/main/CHANGES.rst)
- [Commits](https://github.com/pallets/werkzeug/compare/2.3.7...2.3.8)

---
updated-dependencies:
- dependency-name: werkzeug
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`b6f9ff4`](https://github.com/jonbiemond/BCIT-Flex/commit/b6f9ff44814a0356c34b35545c90529335401022))

### Feature

* feat(app): filter courses by favourite programs

Resolves #64, resolves #71 ([`777011b`](https://github.com/jonbiemond/BCIT-Flex/commit/777011b6da16315fd174f780a6078b2ce1b83526))

* feat(backend): support relation properties as links in ModelFilter ([`c8394ca`](https://github.com/jonbiemond/BCIT-Flex/commit/c8394ca9d9d88eaae063842d64b67b52ad94e48d))

* feat(app): mark program as favourite

Add the ability for user to mark a program as favourite.
Display favourite programs on account page.

Refactor session fixture to db_session,
to avoid name conflict with Flask session. ([`cb69bc8`](https://github.com/jonbiemond/BCIT-Flex/commit/cb69bc822c818965c753fa95359a134c1ac90d94))

* feat(app): redirect to the requested page after login ([`5b38f62`](https://github.com/jonbiemond/BCIT-Flex/commit/5b38f621dcaac04ba2c035924cc6a6ee155847ca))

* feat(app): add account page ([`61d1558`](https://github.com/jonbiemond/BCIT-Flex/commit/61d15584d52f31d5fdc1df29f6b3fc5ee2c28739))

* feat(model): add UserPreference model ([`f1047b5`](https://github.com/jonbiemond/BCIT-Flex/commit/f1047b5207cea239681ffdf69bf53523c2a1b4e9))

* feat(app): rebuild course route to include subject and code ([`0b05b44`](https://github.com/jonbiemond/BCIT-Flex/commit/0b05b44d5ad233f82dd3925a03df5a34ac93983b))

### Test

* test: improve test coverage (#79)

Add tests for authorization and `create_db` command. ([`182f19f`](https://github.com/jonbiemond/BCIT-Flex/commit/182f19f25c4d62eae07e3c9c7db608e3852673ab))

* test: improve test coverage (#78)

Improve coverage of scrape and db tests.

---------

Co-authored-by: Dominik Imrich &lt;dominik.imrich@student.tuke.sk&gt; ([`fc1e2d0`](https://github.com/jonbiemond/BCIT-Flex/commit/fc1e2d0561c519dad200e0f7498cb97d481238b2))


## v3.9.0 (2023-11-06)

### Feature

* feat(app): paginate course index

Closes #36 ([`8999ee8`](https://github.com/jonbiemond/BCIT-Flex/commit/8999ee8ca4f1ca2fff1859a96f3dd9902ab071f3))

* feat(app): implement course filters as SQL

Apply course filters via SQL instead of in state.
It is more efficient to filter courses at the database level. ([`85b62bd`](https://github.com/jonbiemond/BCIT-Flex/commit/85b62bd2affc64fdddea81250b9a60d9f4b191df))

* feat(app): add course search

Closes #61 ([`b844873`](https://github.com/jonbiemond/BCIT-Flex/commit/b844873095b61b44f57c8f4ca89e0303e64ce0d4))

### Fix

* fix(app): handle adding already included table to ModelFilter ([`a982e5e`](https://github.com/jonbiemond/BCIT-Flex/commit/a982e5e4a96816620efbb2ba33a76f1d5f9c043e))


## v3.8.0 (2023-10-27)

### Feature

* feat(app): add subject and campus select elements ([`50e1af2`](https://github.com/jonbiemond/BCIT-Flex/commit/50e1af2ef4fc11281901ab4383969114cc374384))

* feat(app): add course filter interface ([`0675fd9`](https://github.com/jonbiemond/BCIT-Flex/commit/0675fd94211cb00476f6e09f28aea76ed4db3aa9))


## v3.7.0 (2023-10-23)

### Feature

* feat(model): make course.set_id() generic and move to base

Make the set_id() method of Course more general and add it to the Base model, so it can be used on other models. ([`53565cd`](https://github.com/jonbiemond/BCIT-Flex/commit/53565cd33ac6e813c50a741b4ca59355fe329321))

### Fix

* fix(model): add offering surrogate key

Replace Offering CRN with offering_id as the primary key.
CRN is not unique beyond terms.

Fixes #60 ([`fcdaf9d`](https://github.com/jonbiemond/BCIT-Flex/commit/fcdaf9ddad8a6ec925a4153ca1d6427956afd3e0))

* fix(db): include all columns in unique constraint name ([`29c6cb0`](https://github.com/jonbiemond/BCIT-Flex/commit/29c6cb0337355643e7fb35639b3c547f78084055))


## v3.6.0 (2023-10-23)

### Chore

* chore: drop unused db_config.py ([`ba2e110`](https://github.com/jonbiemond/BCIT-Flex/commit/ba2e110d3c9f5ff345d0db26e8322de70cade44d))

### Ci

* ci: add dev to on ci ([`c54e97e`](https://github.com/jonbiemond/BCIT-Flex/commit/c54e97e7463d5949b665a84586b0b03a19cd7b87))

### Documentation

* docs: instruct to target dev branch ([`5aa5d35`](https://github.com/jonbiemond/BCIT-Flex/commit/5aa5d359792c6ec69fc2a3331ede36eff7c9ea13))

### Feature

* feat(app): add lower navbar ([`fc9fb65`](https://github.com/jonbiemond/BCIT-Flex/commit/fc9fb65e7eb3294ffd469168537f278e63688b73))

* feat(app): add program index and program page ([`dd30eaf`](https://github.com/jonbiemond/BCIT-Flex/commit/dd30eaf5b27861d34d97cb24b5557c558c310c5f))

* feat(script): add load_programs script and command ([`6cc397b`](https://github.com/jonbiemond/BCIT-Flex/commit/6cc397ba3208d4d7a7cb8d4530c6489c8ff1f595))

* feat(model): add Program model ([`15edaa7`](https://github.com/jonbiemond/BCIT-Flex/commit/15edaa73221631e72910c9e1f3c8d236c2114e77))

* feat(db): add programs.json ([`5c92b84`](https://github.com/jonbiemond/BCIT-Flex/commit/5c92b84e678169140752e979e9c29b0276932551))

### Fix

* fix(scraper): undelete objects on merge

On merge of an object set `deleted_at` to None, so it is un-deleted. ([`35ba339`](https://github.com/jonbiemond/BCIT-Flex/commit/35ba339cc538ab15a356fbf63d4e8f307af50e3f))

### Style

* style: fix table style in light mode

Fixes #55 ([`5e2d1f9`](https://github.com/jonbiemond/BCIT-Flex/commit/5e2d1f9676c69dd4f2a763cedd99828bbe2178f4))


## v3.5.1 (2023-10-19)

### Chore

* chore(deps): bump urllib3 from 2.0.6 to 2.0.7

Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.0.6 to 2.0.7.
- [Release notes](https://github.com/urllib3/urllib3/releases)
- [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
- [Commits](https://github.com/urllib3/urllib3/compare/2.0.6...2.0.7)

---
updated-dependencies:
- dependency-name: urllib3
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`0920c76`](https://github.com/jonbiemond/BCIT-Flex/commit/0920c7671d2e3a1591af76be114bb19138996176))

* chore(deps-dev): bump gitpython from 3.1.36 to 3.1.37

Bumps [gitpython](https://github.com/gitpython-developers/GitPython) from 3.1.36 to 3.1.37.
- [Release notes](https://github.com/gitpython-developers/GitPython/releases)
- [Changelog](https://github.com/gitpython-developers/GitPython/blob/main/CHANGES)
- [Commits](https://github.com/gitpython-developers/GitPython/compare/3.1.36...3.1.37)

---
updated-dependencies:
- dependency-name: gitpython
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`00fdc6a`](https://github.com/jonbiemond/BCIT-Flex/commit/00fdc6aeb5efaba6cdc318fa9cfa6751d93900ff))

### Fix

* fix: price in offering info (#59)

Closes #54 ([`82dd4a4`](https://github.com/jonbiemond/BCIT-Flex/commit/82dd4a45448e4b90285ea8675bda6ca648601d6f))


## v3.5.0 (2023-10-18)

### Chore

* chore(deps): bump urllib3 from 2.0.4 to 2.0.6

Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.0.4 to 2.0.6.
- [Release notes](https://github.com/urllib3/urllib3/releases)
- [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
- [Commits](https://github.com/urllib3/urllib3/compare/2.0.4...2.0.6)

---
updated-dependencies:
- dependency-name: urllib3
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`960b92f`](https://github.com/jonbiemond/BCIT-Flex/commit/960b92fc1baa0132b081b8bcd4cc272ac5ebbd99))

### Feature

* feat(database): intercept delete commands and replace with a soft delete

- Add SQL soft delete rule to tables.
- Update load_courses() to reinstate deleted courses. ([`b3a284c`](https://github.com/jonbiemond/BCIT-Flex/commit/b3a284c32a10808a46f00e0858d62e59579dbe7d))

* feat(model): make soft delete SQLAlchemy

Use SQLAlchemy function `with_loader_criteria()` to alter select statements instead of custom rewrite function. ([`21660cb`](https://github.com/jonbiemond/BCIT-Flex/commit/21660cba1e84dfc7444435cd81643d4a45f758bd))

* feat(model): add support for ORM joins to soft delete hook ([`2f6143d`](https://github.com/jonbiemond/BCIT-Flex/commit/2f6143d3c105df50cef5ca9c7203168039a101da))

* feat(model): add option to override soft delete select hook ([`8116aae`](https://github.com/jonbiemond/BCIT-Flex/commit/8116aaef7913fdb7a618a6f40dfc69671495b46a))

* feat(model): add soft delete fields and select hook ([`c7e5194`](https://github.com/jonbiemond/BCIT-Flex/commit/c7e5194181e45cfdf723dc6888fce65f24c770c8))

### Fix

* fix(model): handle interface changes in flask-sqlalchemy extension ([`dd5d6cb`](https://github.com/jonbiemond/BCIT-Flex/commit/dd5d6cbbfc90dc864a6b392900fcf566916f3b53))

### Style

* style: make tables easier to read ([`917036d`](https://github.com/jonbiemond/BCIT-Flex/commit/917036d94031b215b90b13e7de1077ffb947f31e))


## v3.4.3 (2023-09-17)

### Fix

* fix(model): add cancelled to not available keywords ([`8138ab1`](https://github.com/jonbiemond/BCIT-Flex/commit/8138ab1f589444497bd8b5d0ab7c8eb865c9a4c6))


## v3.4.2 (2023-09-16)

### Fix

* fix(model): mark available when status contains keyword

Fixes #46 ([`76be36b`](https://github.com/jonbiemond/BCIT-Flex/commit/76be36bc36fdbfcaa748490dcf071ee2afcac848))


## v3.4.1 (2023-09-15)

### Fix

* fix: specify text color of nav bar in light mode ([`684dd08`](https://github.com/jonbiemond/BCIT-Flex/commit/684dd080bc60eb55a6ee53adab64ff743c3d1153))


## v3.4.0 (2023-09-15)

### Chore

* chore: add LICENSE.md ([`f83ef4a`](https://github.com/jonbiemond/BCIT-Flex/commit/f83ef4a2ae4969badb6b8f2ac2ce521ad58309c9))

### Feature

* feat(scripts): merge in scraped courses ([`9b07abd`](https://github.com/jonbiemond/BCIT-Flex/commit/9b07abdca166be47d70b7643847f5cad2fff0341))

* feat(model): declare cascade behaviour

- Add server side on-delete-cascade to offering.term FK constraint. ([`85e75c3`](https://github.com/jonbiemond/BCIT-Flex/commit/85e75c3aa32dc2171758915dc916e6948f3df002))

* feat(model): add set_id to course ([`99fffae`](https://github.com/jonbiemond/BCIT-Flex/commit/99fffae2eb148c5f974c13926d76c81f7682f0a5))

* feat(model): handle composite constraints in get_by_unique ([`5525c44`](https://github.com/jonbiemond/BCIT-Flex/commit/5525c449c14c54b953ebb06dbccc60155bdd96fe))

* feat(db): add unique constraint to course ([`377a7d8`](https://github.com/jonbiemond/BCIT-Flex/commit/377a7d8202d5d27b139cbb03f5737e77565d063b))

### Test

* test: fix script location in tests/alembic.ini ([`8ca9d1c`](https://github.com/jonbiemond/BCIT-Flex/commit/8ca9d1ce924ea4a54934ee32f8a8288742b91e67))


## v3.3.0 (2023-09-13)

### Feature

* feat(app): display last updated on course page ([`508e081`](https://github.com/jonbiemond/BCIT-Flex/commit/508e0818d5dfb1379f38ea863fffb53ac2e65dfe))

* feat(model): add timestamps to Course, Offering and User ([`ea0267f`](https://github.com/jonbiemond/BCIT-Flex/commit/ea0267f5a73d3a583a7fdc21662f104d1cb720e9))


## v3.2.1 (2023-09-11)

### Documentation

* docs: detail installation steps ([`664017c`](https://github.com/jonbiemond/BCIT-Flex/commit/664017c20424e729726fd584dfd51f30bdebca29))

* docs: extend roadmap ([`ac09299`](https://github.com/jonbiemond/BCIT-Flex/commit/ac09299788a87b8c187c28dcc4a521ca766112a9))

* docs: remove poetry reference ([`ce0f7c3`](https://github.com/jonbiemond/BCIT-Flex/commit/ce0f7c3ed69c432d9826c5a3212150e529e9811d))

### Fix

* fix(db): specify encoding in create db stmt

Web scraped data may contain any variety of characters.
To be safe, set UTF-8 as the encoding so all known encodings are supported.

Fixes #38 ([`413b3b8`](https://github.com/jonbiemond/BCIT-Flex/commit/413b3b8f57e9987472ed07610b2a275181477bd1))


## v3.2.0 (2023-09-10)

### Feature

* feat(scripts): add all-subjects flag to load-db cmd

Add option to load all subjects into the database to load-db command. ([`b9e8840`](https://github.com/jonbiemond/BCIT-Flex/commit/b9e8840ff8fb04bdfda8e343f97b7989a9f19b58))

* feat(model): and is_active field to Subject

Add a field to indicate whether a subject should be web-scraped. ([`eff0a6c`](https://github.com/jonbiemond/BCIT-Flex/commit/eff0a6c5dad06f35483cad6d975bf076732fbb4f))

* feat(app): add load-subjects command ([`25d1a56`](https://github.com/jonbiemond/BCIT-Flex/commit/25d1a56c4df51f21dd7d174203366d3a55d6d1e4))


## v3.1.4 (2023-09-09)

### Fix

* fix(app): add grant schema to create cmd ([`a32e96b`](https://github.com/jonbiemond/BCIT-Flex/commit/a32e96bb2c50cf43dee964dbdbc99441b5193489))


## v3.1.3 (2023-09-09)

### Fix

* fix(app): pass db connection to upgrade command

Since an url is not set in alembic config in a deployment environment,
any alembic commands require a connection to be passed to the config. ([`40ad30c`](https://github.com/jonbiemond/BCIT-Flex/commit/40ad30c052f163f83159750b58e4af86cb57ed7c))


## v3.1.2 (2023-09-08)

### Ci

* ci: fix build command ([`d70b52d`](https://github.com/jonbiemond/BCIT-Flex/commit/d70b52d07276b9c8dabc7ad7f780c77a97b52abe))

* ci: publish to pypi ([`594ca59`](https://github.com/jonbiemond/BCIT-Flex/commit/594ca5945989b322ea321b0e30c0be73fe2d4c35))

### Documentation

* docs: update installation steps ([`b5e46ab`](https://github.com/jonbiemond/BCIT-Flex/commit/b5e46abf551d1521e5649ca8aee4ebc5f8761ba7))

### Fix

* fix(app): handle role exists ([`ff81fc6`](https://github.com/jonbiemond/BCIT-Flex/commit/ff81fc68ed6754be2c74bba8686684bca150c5a4))

* fix(app): don&#39;t connect to db if uri not set

fmu ([`a1afd2d`](https://github.com/jonbiemond/BCIT-Flex/commit/a1afd2d143b23eb9fc6558ebc41510a5b6937401))


## v3.1.1 (2023-09-08)

### Fix

* fix(app): resolve alembic script path ([`10fea34`](https://github.com/jonbiemond/BCIT-Flex/commit/10fea34a2ab0fec4e7b95d8eed0f0244ed21862f))


## v3.1.0 (2023-09-08)

### Feature

* feat(app): add cli command to upgrade database ([`defda96`](https://github.com/jonbiemond/BCIT-Flex/commit/defda96d4fa665f4227bb4579d528c69c209c285))

* feat(app): add cli command to create database ([`ec24183`](https://github.com/jonbiemond/BCIT-Flex/commit/ec24183d4875c26d86a6a29d56712e63f296b4bc))

* feat: refactor migrations into package

Move migration files inside of package, so they can be run by the user to set up a database. ([`8f6015f`](https://github.com/jonbiemond/BCIT-Flex/commit/8f6015f9009b34b38c73b21211642b22a540b6ae))

### Fix

* fix(app): add metadata to app db context ([`bf64aad`](https://github.com/jonbiemond/BCIT-Flex/commit/bf64aadfa7eae8b0198c0a8bd2824bfeb9b8b100))

### Test

* test: omit alembic files from coverage report ([`15df256`](https://github.com/jonbiemond/BCIT-Flex/commit/15df2563bb3059c78121bbfa36c02eec8a7aae24))


## v3.0.1 (2023-09-07)

### Fix

* fix(db): increase course.url allowed length ([`8406190`](https://github.com/jonbiemond/BCIT-Flex/commit/8406190d318273af0da85357ef86b792408f11c3))


## v3.0.0 (2023-09-03)

### Chore

* chore: switch db url config variables ([`7cbf342`](https://github.com/jonbiemond/BCIT-Flex/commit/7cbf3420e84cf118c558dd6ffb36798f3598e03c))

### Ci

* ci: apply missing dbtest marker to necessary tests ([`c974827`](https://github.com/jonbiemond/BCIT-Flex/commit/c9748277f2f3285f9cc9850cf341975acc916d6a))

### Documentation

* docs: add the run instruction ([`7c581ab`](https://github.com/jonbiemond/BCIT-Flex/commit/7c581abc81f7ead0f230576664d4d935c3183bf1))

### Feature

* feat(app): add index and course page to app factory ([`3333f80`](https://github.com/jonbiemond/BCIT-Flex/commit/3333f80d896881e1ee57544c9cd660b7eb2d5aaa))

* feat(app): add stylesheet ([`b9f9403`](https://github.com/jonbiemond/BCIT-Flex/commit/b9f94034eda1919dc03aea0fb7f9ecfc08d08b93))

* feat(app): add html templates for register and login ([`ba3ca49`](https://github.com/jonbiemond/BCIT-Flex/commit/ba3ca49b52331c6b9cf840c56e0c527a53e99b07))

* feat(app): add auth Blueprint ([`ccd9b6a`](https://github.com/jonbiemond/BCIT-Flex/commit/ccd9b6af5b3f4c297c5e6e9498cef67b922636ba))

* feat(model): add get_by_unique method

Add method with similar signature to session.get(),
but that returns an object by its unique constraint fields. ([`d96c04c`](https://github.com/jonbiemond/BCIT-Flex/commit/d96c04ce4f83cdece0c7be47bbdce92a952e19b8))

* feat(app): connect app to db

Extend Flask-SQLAlchemy to use SQLAlchemy Base class as Model. ([`81f65e9`](https://github.com/jonbiemond/BCIT-Flex/commit/81f65e91b79c1297a1b20964f6d127be8a5b0576))

* feat(model): add User model

- Declare User model
- Add migration for user table
- Add tests ([`ab917ab`](https://github.com/jonbiemond/BCIT-Flex/commit/ab917ab0b95e39388806f705d0cb1ef835643599))

* feat(app): configure app database connection

- Add cli command to run bcit_to_sql. ([`9f88652`](https://github.com/jonbiemond/BCIT-Flex/commit/9f88652deeccc5bda9a27035b12e0eb2a282b137))

* feat(app): add flask application factory ([`b6f0eff`](https://github.com/jonbiemond/BCIT-Flex/commit/b6f0eff21465d4643b344268543a93bf1477c9d5))

* feat(app): add courses, course and query page ([`c8009cd`](https://github.com/jonbiemond/BCIT-Flex/commit/c8009cddeda357f2ad26c1bda98c85de99f1f358))

* feat(app): add filter_courses function ([`bc81dee`](https://github.com/jonbiemond/BCIT-Flex/commit/bc81dee22e063c14f4905594c7c8059145f0dc04))

### Fix

* fix(model): make User object subscriptable

Extend MappedAsDataclass with __getitem__ and mixin to the User model. ([`506e9a2`](https://github.com/jonbiemond/BCIT-Flex/commit/506e9a237e395d3ee14200115933f24e1161c043))

### Refactor

* refactor: drop interface.py ([`6a277ca`](https://github.com/jonbiemond/BCIT-Flex/commit/6a277caebd79e88041f0bdddafd8724ab7a0ee9c))

* refactor: drop test util clone function

Replace usages of the test utility clone function with the clone method on Base. ([`354fdaa`](https://github.com/jonbiemond/BCIT-Flex/commit/354fdaadc74484ac9f60deadc49c119444f9156e))

### Test

* test(app): add app tests ([`bf736f4`](https://github.com/jonbiemond/BCIT-Flex/commit/bf736f4e15da6f92dc5947ffd9a2b478685db043))


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
