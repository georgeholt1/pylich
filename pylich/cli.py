import argparse
import sys

from pylich import LinkChecker


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Crawl URLs from pages in a sitemap"
    )
    parser.add_argument("sitemap_url", help="URL of the sitemap")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Increase output verbosity",
    )
    args = parser.parse_args()

    try:
        checker = LinkChecker(
            sitemap_url=args.sitemap_url, verbose=args.verbose
        )
        urls = checker.get_sitemap_urls()
        broken_links = checker.check_links(urls)

        if broken_links:
            if args.verbose:
                print("Broken links found:")
                checker.print_dead_links()
            sys.exit(1)
        else:
            if args.verbose:
                print("No broken links found")
            sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
