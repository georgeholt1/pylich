import pytest

from pylich import LinkChecker


@pytest.fixture
def sitemap_url():
    return "http://example.com/sitemap.xml"


@pytest.fixture
def sitemap_content():
    return """
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>http://example.com/page1</loc>
        </url>
        <url>
            <loc>http://example.com/page2</loc>
        </url>
    </urlset>
    """


@pytest.fixture
def page_content():
    return """
    <html>
    <body>
        <a href="http://example.com/broken_link">Broken Link</a>
        <a href="http://example.com/working_link">Working Link</a>
    </body>
    </html>
    """


def test_get_sitemap_urls(requests_mock, sitemap_url, sitemap_content):
    requests_mock.get(sitemap_url, text=sitemap_content)
    checker = LinkChecker(sitemap_url, verbose=True)
    urls = checker.get_sitemap_urls()
    assert urls == ["http://example.com/page1", "http://example.com/page2"]


def test_get_sitemap_urls_failure(requests_mock, sitemap_url):
    requests_mock.get(sitemap_url, status_code=404)
    checker = LinkChecker(sitemap_url, verbose=True)
    with pytest.raises(Exception, match="Failed to fetch sitemap"):
        checker.get_sitemap_urls()


def test_check_links(
    requests_mock, sitemap_url, sitemap_content, page_content
):
    requests_mock.get(sitemap_url, text=sitemap_content)
    requests_mock.get("http://example.com/page1", text=page_content)
    requests_mock.get("http://example.com/page2", text=page_content)
    requests_mock.get("http://example.com/broken_link", status_code=404)
    requests_mock.get("http://example.com/working_link", status_code=200)

    checker = LinkChecker(sitemap_url, verbose=True)
    urls = checker.get_sitemap_urls()
    broken_links = checker.check_links(urls)

    assert broken_links == [
        ("http://example.com/page1", "http://example.com/broken_link", 404),
        ("http://example.com/page2", "http://example.com/broken_link", 404),
    ]


def test_check_links_with_relative_urls(
    requests_mock, sitemap_url, sitemap_content
):
    page_content_with_relative_links = """
    <html>
    <body>
        <a href="/broken_link">Broken Link</a>
        <a href="/working_link">Working Link</a>
    </body>
    </html>
    """
    requests_mock.get(sitemap_url, text=sitemap_content)
    requests_mock.get(
        "http://example.com/page1", text=page_content_with_relative_links
    )
    requests_mock.get(
        "http://example.com/page2", text=page_content_with_relative_links
    )
    requests_mock.get("http://example.com/broken_link", status_code=404)
    requests_mock.get("http://example.com/working_link", status_code=200)

    checker = LinkChecker(sitemap_url, verbose=True)
    urls = checker.get_sitemap_urls()
    broken_links = checker.check_links(urls)

    assert broken_links == [
        ("http://example.com/page1", "http://example.com/broken_link", 404),
        ("http://example.com/page2", "http://example.com/broken_link", 404),
    ]


def test_print_dead_links(
    requests_mock, sitemap_url, sitemap_content, page_content, capsys
):
    requests_mock.get(sitemap_url, text=sitemap_content)
    requests_mock.get("http://example.com/page1", text=page_content)
    requests_mock.get("http://example.com/page2", text=page_content)
    requests_mock.get("http://example.com/broken_link", status_code=404)
    requests_mock.get("http://example.com/working_link", status_code=200)

    checker = LinkChecker(sitemap_url, verbose=True)
    urls = checker.get_sitemap_urls()
    checker.check_links(urls)
    checker.print_dead_links()

    captured = capsys.readouterr()
    assert "Dead links:" in captured.out
    assert (
        "Page URL: http://example.com/page1, Broken Link:"
        "http://example.com/broken_link, Status Code: 404" in captured.out
    )
    assert (
        "Page URL: http://example.com/page2, Broken Link:"
        "http://example.com/broken_link, Status Code: 404" in captured.out
    )


def test_print_dead_links_no_dead_links(
    requests_mock, sitemap_url, sitemap_content, capsys
):
    page_content_no_dead_links = """
    <html>
    <body>
        <a href="http://example.com/working_link">Working Link</a>
    </body>
    </html>
    """
    requests_mock.get(sitemap_url, text=sitemap_content)
    requests_mock.get(
        "http://example.com/page1", text=page_content_no_dead_links
    )
    requests_mock.get(
        "http://example.com/page2", text=page_content_no_dead_links
    )
    requests_mock.get("http://example.com/working_link", status_code=200)

    checker = LinkChecker(sitemap_url, verbose=True)
    urls = checker.get_sitemap_urls()
    checker.check_links(urls)
    checker.print_dead_links()

    captured = capsys.readouterr()
    assert "No dead links found." in captured.out
