# PyLich

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/georgeholt1/pylich/unit_tests.yml)
![PyPI - Version](https://img.shields.io/pypi/v/pylich)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pylich)
![GitHub License](https://img.shields.io/github/license/georgeholt1/pylich)

A super simple Python utility to check for dead links in a website.

## Installation


### From PyPI

```bash
pip install pylich
```

### From source

Clone the repository and run the following command:

```bash
pip install .
```

## Usage

Simply provide the URL of the sitemap and `pylich` will crawl through links in the pages and check their status.

```python
from pylich import LinkChecker
checker = LinkChecker("https://www.example.com/sitemap.xml", verbose=True)
urls = checker.get_sitemap_urls()
broken_links = checker.check_links(urls)
checker.print_dead_links()
```

## Contributing

Pull requests are welcome.

Package and dependency management is done using [Poetry](https://python-poetry.org/). To install the dependencies and the package in development mode, run:

```bash
poetry install
```

To run the tests, run:

```bash
pytest
```

Pre-commit hooks are available:

```bash
pre-commit install
```