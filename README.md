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

## How to Use

1. Clone this repository:

    ```bash
    git clone https://github.com/ryshaal/Google-Scholar-Scraping/
    ```
2. Navigate to the project directory:
    ```bash
    cd Google-Scholar-Scraping
    ```

3. Create a text file for your query:
In the `input_query` folder, create a file named `query.txt` and enter your search query.

4. Run the script:
    ```bash
    python gscholar.py
    ```

5. Output: 
The script will display the article information in the terminal and save the metadata as a `.ris` file in the `output` folder. If a PDF link is available, the script will download the PDF to the same folder.

**Example Query**

In the `input_query/query.txt` , you might add a search query like:
```plaintext
machine learning applications in education
```

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`

You can install the required packages by running:

```bash
pip install -r requirements.txt
