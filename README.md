# Google Scholar Scraper

This Python script allows you to scrape article data from Google Scholar based on a query provided in a text file. The script extracts information such as the article's title, authors, publication year, journal name, volume, citation count, and PDF links (if available). The results are saved as RIS files for easy citation management, and PDFs can be downloaded when available.

## Features

- Fetch articles from Google Scholar based on a query
- Extract information including:
  - Title
  - Authors
  - Year of publication
  - Journal name and volume
  - PDF link (if available)
  - Citation count
- Save article metadata as `.ris` files
- Download PDFs of articles when available

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`

You can install the required packages by running:

```bash
pip install -r requirements.txt
