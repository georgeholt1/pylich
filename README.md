# PyLich

A super simple Python utility to check for dead links in a website.

## Installation

Clone the repository and run the following command:

```bash
pip install .
```

## Usage

```python
from pylich import LinkChecker
checker = LinkChecker("https://www.example.com", verbose=True)
urls = checker.get_sitemap_urls()
broken_links = checker.check_links(urls)
checker.print_dead_links()
```