## 🤝 How to submit a contribution

To make a contribution, follow the following steps:

1. Fork and clone this repository.
2. To install, follow installation steps in the [README.md](https://github.com/jonbiemond/BCIT-Flex#installation), but use `poetry install` instead of `pip`.
3. Make changes in a new branch including the issue number. e.g. `git checkout -b 42-new-feature`.
4. If you modified the code (new feature or bug-fix), please add tests for it.
5. Check the linting. [see below](https://github.com/jonbiemond/BCIT-Available-Courses/blob/main/CONTRIBUTING.md#-linting)
6. Ensure that all tests pass. [see below](https://github.com/jonbiemond/BCIT-Available-Courses/blob/main/CONTRIBUTING.md#-testing)
7. Submit a pull request.

For more details about pull requests, please read [GitHub's guides](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).


### 📦 Package manager

We use `poetry` as our package manager. You can install poetry by following the instructions [here](https://python-poetry.org/docs/#installation).

Please DO NOT use pip or conda to install the dependencies. Instead, use poetry:

```bash
poetry install
```

### 📌 Pre-commit

To ensure our standards, make sure to install pre-commit before start to contribute.

```bash
pre-commit install
```

### 🧹 Linting

We use `ruff` to lint our code. You can run the linter by running the following command:

```bash
ruff .
```

Make sure that the linter does not report any errors or warnings before submitting a pull request.

### 📎 Code Format with `black`

We use `black` to reformat the code by running the following command:

```bash
black . 
```

### 🧪 Testing

We use `pytest` to test our code. You can run the tests by running the following command:

```bash
pytest .
```

### ☂ Code coverage

We use `pytest-cov` to measure our test coverage. After adding new tests run:

```bash
pytest --cov=bcitflex tests/
```

Make sure that all tests pass before submitting a pull request.
