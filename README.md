# PyLich

A super simple Python utility to check for dead links in a website.

## Installation

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

Package and dependency management is done using [Poetry](https://python-poetry.org/). To install the dependencies, run:

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