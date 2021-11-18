# pyrmaid

[WORK IN PROGRESS]

A python library for converting python objects to UML diagrams using mermaid-js.

## Contributing

Contributions to this project are always welcome!

### Getting Started

1. Activate your virtual environment of choice and install `poetry`.

    ```shell
    pip install poetry
    ```

2. Install the project:

    ```shell
    poetry install --no-root
    ```

### Development Checks

During development a number of checks can be made against the code
base. This is recommended before commiting anything to the repository.
Each of the following can be executed from the root of the project.

- Code linting:

    ```shell
    flake8
    ```

- Typing analysis:

    ```shell
    mypy .
    ```

- Code formatting:

    ```shell
    black --check .
    ```

- Docstring styling

    ```shell
    pydocstyle .
    ```

- Running the tests

    ```shell
    python -m pytest -vvv
    ```
