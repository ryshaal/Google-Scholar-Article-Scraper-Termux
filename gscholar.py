import os
import requests
from bs4 import BeautifulSoup

# ANSI escape code untuk warna biru dan kuning
BLUE = '\033[94m'
RESET = '\033[0m'
YELLOW = '\033[93m'

# Mendapatkan path dari direktori tempat script berada
script_dir = os.path.dirname(os.path.abspath(__file__))

# Menentukan lokasi input dan output relatif terhadap lokasi script
query_file_path = os.path.join(script_dir, 'input_query', 'query.txt')
output_dir = os.path.join(script_dir, 'output')

def fetch_google_scholar_info(query):
    # URL pencarian Google Scholar
    search_url = "https://scholar.google.com/scholar"
    params = {'hl': 'id', 'q': query}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Melakukan permintaan ke Google Scholar
    response = requests.get(search_url, params=params, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ambil semua artikel yang ditemukan
        articles = soup.find_all('div', class_='gs_ri')
        results = []
        for article in articles:
            # Ambil judul artikel
            title_tag = article.find('h3', class_='gs_rt')
            title = title_tag.get_text() if title_tag else 'No title available'
            
            # Ambil link artikel utama (bukan PDF)
            link = title_tag.find('a')['href'] if title_tag and title_tag.find('a') else None

            # Cari link PDF yang ada di tombol PDF (biasanya di samping judul)
            pdf_link = None
            pdf_tag = article.find('div', class_='gs_or_ggsm')
            if pdf_tag:
                pdf_link = pdf_tag.find('a')['href'] if pdf_tag.find('a') else None

            # Ambil penulis, tahun terbit, dan nama jurnal
            author_year_tag = article.find('div', class_='gs_a')
            author_year = author_year_tag.get_text() if author_year_tag else 'No author/year available'
            
            # Memisahkan nama penulis, tahun, nama jurnal, dan volume
            if author_year != 'No author/year available':
                author_info = author_year.split('-')
                if len(author_info) >= 3:
                    authors = author_info[0].strip()
                    year = author_info[1].strip().split()[-1]
                    journal_info = author_info[2].strip()
                else:
                    authors = author_info[0].strip()
                    year = "Unknown"
                    journal_info = "Unknown"
            else:
                authors, year, journal_info = "Unknown", "Unknown", "Unknown"
            
            # Memisahkan nama jurnal dan volume jika memungkinkan
            journal_name = journal_info.split(',')[0] if ',' in journal_info else journal_info
            volume = journal_info.split(',')[1].strip() if ',' in journal_info and len(journal_info.split(',')) > 1 else 'Unknown'

            # Ambil kutipan (citation)
            citation_div = article.find('div', class_='gs_fl')
            citation = "No citation available"
            if citation_div:
                citation_info = citation_div.find_all('a')
                if citation_info and len(citation_info) > 0:
                    citation = citation_info[2].get_text() if len(citation_info) > 2 else "No citation link"

            results.append({
                'title': title,
                'authors': authors,
                'year': year,
                'journal_name': journal_name,
                'volume': volume,
                'link': link,
                'pdf_link': pdf_link,  # Menambahkan link PDF
                'citation': citation
            })
        return results
    else:
        print("Error fetching data:", response.status_code)
        return None

def save_article_as_ris(article, output_dir):
    # Pastikan direktori output ada
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Bersihkan judul untuk digunakan sebagai nama file (hapus karakter yang tidak valid)
    safe_title = ''.join(c for c in article['title'] if c.isalnum() or c in (' ', '_')).rstrip()
    
    # Jika judul terlalu panjang, potong agar tidak melebihi batas nama file
    if len(safe_title) > 50:
        safe_title = safe_title[:50].rstrip()

    output_file_path = os.path.join(output_dir, f"{safe_title}.ris")
    
    # Simpan artikel dalam format RIS
    with open(output_file_path, 'w') as file:
        file.write("TY  - JOUR\n")
        file.write(f"TI  - {article['title']}\n")
        file.write(f"AU  - {article['authors']}\n")
        file.write(f"PY  - {article['year']}\n")
        file.write(f"JO  - {article['journal_name']}\n")
        file.write(f"VL  - {article['volume']}\n")
        if article['link']:
            file.write(f"UR  - {article['link']}\n")
        file.write("ER  - \n\n")  # Mengakhiri entri RIS

    print(f"Artikel disimpan sebagai file RIS: {output_file_path}")

def download_pdf(article, output_dir):
    if article['pdf_link']:
        # Bersihkan judul untuk digunakan sebagai nama file
        safe_title = ''.join(c for c in article['title'] if c.isalnum() or c in (' ', '_')).rstrip()
        
        # Jika judul terlalu panjang, potong
        if len(safe_title) > 50:
            safe_title = safe_title[:50].rstrip()
        
        pdf_file_path = os.path.join(output_dir, f"{safe_title}.pdf")

        try:
            # Download file PDF
            response = requests.get(article['pdf_link'])
            with open(pdf_file_path, 'wb') as pdf_file:
                pdf_file.write(response.content)
            print(f"PDF disimpan di: {pdf_file_path}")
        except Exception as e:
            print(f"Gagal mengunduh PDF: {e}")
    else:
        print(f"Tidak ada link PDF untuk artikel ini: {article['title']}")

# Periksa apakah file query ada
if os.path.exists(query_file_path):
    with open(query_file_path, 'r') as file:
        query = file.read().strip()

    # Mengambil artikel dari Google Scholar
    articles = fetch_google_scholar_info(query)

    if articles:
        # Menampilkan artikel di terminal dan menyimpan dalam file RIS serta PDF
        for i, article in enumerate(articles, start=1):
            print(f"{i}. {YELLOW}𝗝𝘂𝗱𝘂𝗹:{RESET} {article['title']}")
            print(f"{BLUE}𝗣𝗲𝗻𝘂𝗹𝗶𝘀:{RESET} {article['authors']}")
            print(f"{BLUE}𝗧𝗮𝗵𝘂𝗻:{RESET} {article['year']}")
            print(f"{BLUE}𝗝𝘂𝗿𝗻𝗮𝗹:{RESET} {article['journal_name']}")
            print(f"{BLUE}𝗩𝗼𝗹.:{RESET} {article['volume']}")
            print(f"{BLUE}𝗟𝗶𝗻𝗸 𝗣𝗗𝗙:{RESET} {article['pdf_link']}")
            print(f"{BLUE}𝗖𝗶𝘁𝗮𝘁𝗶𝗼𝗻:{RESET}  {article['citation']}\n")

            # Simpan setiap artikel sebagai file RIS dengan judul sebagai nama file
            save_article_as_ris(article, output_dir)

            # Download PDF jika ada
            download_pdf(article, output_dir)
    else:
        print("Tidak ada artikel yang ditemukan.")
else:
    print(f"File query tidak ditemukan di path: {query_file_path}")