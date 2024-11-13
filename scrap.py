import requests
from bs4 import BeautifulSoup
import json

def clean_text(text):
    """Remove extra spaces and newlines from text."""
    return " ".join(text.strip().split())

def save_to_json(data, filename="scraped_data.json"):
    """Save data to JSON format."""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def scrape_page(url):
    try:
        # Send HTTP request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Structured data dictionary
        structured_data = {
            'title': clean_text(soup.title.string) if soup.title else 'No title found',
            'headings': [],
            'paragraphs': [],
            'links': [],
            'metadata': []
        }

        # Extract headings (h1, h2, h3, h4, h5, h6)
        for level in range(1, 7):  # Loop through h1 to h6 tags
            headings = soup.find_all(f'h{level}')
            for h in headings:
                structured_data['headings'].append({
                    'type': f'h{level}',
                    'content': clean_text(h.get_text())
                })

        # Extract all paragraphs (p)
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            structured_data['paragraphs'].append({
                'type': 'p',
                'content': clean_text(p.get_text())
            })

        # Extract all links (a)
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href:
                # Normalize relative URLs to absolute URLs
                full_url = requests.compat.urljoin(url, href)
                structured_data['links'].append({
                    'type': 'a',
                    'content': full_url
                })

        # Extract metadata (meta tags)
        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            meta_info = {}
            if meta.get('name'):
                meta_info['name'] = meta.get('name')
                meta_info['content'] = meta.get('content', '')
            elif meta.get('property'):
                meta_info['property'] = meta.get('property')
                meta_info['content'] = meta.get('content', '')
            
            if meta_info:
                structured_data['metadata'].append(meta_info)

        # Display the structured data
        print(f"Title: {structured_data['title']}\n")
        print("Headings:")
        for heading in structured_data['headings']:
            print(f"  {heading['type'].upper()}: {heading['content']}")
        
        print("\nParagraphs:")
        for para in structured_data['paragraphs']:
            print(f"  {para['content']}")
        
        print("\nLinks:")
        for link in structured_data['links']:
            print(f"  {link['content']}")
        
        print("\nMetadata:")
        for meta in structured_data['metadata']:
            print(f"  {meta}")

        # Save data to JSON (optional)
        save_to_json(structured_data)
        print("\nData saved to 'scraped_data.json'.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")

# Example URL to scrape
url = 'https://www.geeksforgeeks.org/android-tutorial/?ref=footer'
scrape_page(url)
