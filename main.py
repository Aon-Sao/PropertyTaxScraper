#!/usr/bin/env python
from pathlib import Path

import scrape_ascent
import extract_neighborhood_sales_from_ascent_data
import scrape_univers
import extract_data_from_univers_html
import extract_data_from_ascent_and_univers_html


def main():
    Path("./data").mkdir(parents=True, exist_ok=True)
    scrape_ascent.main()
    extract_neighborhood_sales_from_ascent_data.main()
    scrape_univers.main()
    extract_data_from_univers_html.main()
    extract_data_from_ascent_and_univers_html.main()


if __name__ == "__main__":
    main()
