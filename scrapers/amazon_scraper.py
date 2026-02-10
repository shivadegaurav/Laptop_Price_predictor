import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

def get_amazon_data():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
    
    # URLs to scrape (Amazon laptop search results)
    base_url = "https://www.amazon.in/s?k=laptops&page={}"
    
    laptops = []
    
    for page in range(1, 41): # Scraping first 40 pages to aim for 500+ items
        print(f"Scraping Amazon Page {page}...")
        try:
            url = base_url.format(page)
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                if page == 1:
                    with open("debug_amazon.html", "w", encoding="utf-8") as f:
                        f.write(response.text)
                        
                soup = BeautifulSoup(response.content, "html.parser")
                
                valid_items = soup.find_all("div", attrs={"data-component-type": "s-search-result"})
                
                for item in valid_items:
                    data = {}
                    
                    # Title
                    title_tag = item.find("h2")
                    if title_tag:
                        data['Title'] = title_tag.text.strip()
                    else:
                        # Fallback try finding span with text
                        spans = item.find_all("span")
                        for s in spans:
                            if len(s.text) > 30:
                                data['Title'] = s.text.strip()
                                break
                        if 'Title' not in data:
                            continue
                        
                    # Price
                    price_tag = item.find("span", class_="a-price")
                    if price_tag:
                        offscreen = price_tag.find("span", class_="a-offscreen")
                        if offscreen:
                            data['Price'] = offscreen.text.strip().replace('₹', '').replace(',', '')
                        else:
                            # Try to construct from whole + fraction if simple text fails
                            whole = price_tag.find("span", class_="a-price-whole")
                            if whole:
                                data['Price'] = whole.text.strip().replace(',', '').replace('.', '')
                            else:
                                data['Price'] = price_tag.text.strip().replace('₹', '').replace(',', '')
                    else:
                        data['Price'] = None
                    
                    # Rating
                    rating_tag = item.find("span", class_="a-icon-alt")
                    if rating_tag:
                        data['Rating'] = rating_tag.text.split(" ")[0]
                    else:
                        data['Rating'] = None
                        
                    laptops.append(data)
                
                print(f"Found {len(valid_items)} items on page {page}")
            else:
                print(f"Failed to retrieve Amazon page {page}. Status: {response.status_code}")
                
            time.sleep(2) # Respectful delay
            
        except Exception as e:
            print(f"Error scraping Amazon page {page}: {e}")
            
    df = pd.DataFrame(laptops)
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'amazon_laptops.csv')
    df.to_csv(output_path, index=False)
    print(f"Amazon data saved to {output_path}")

if __name__ == "__main__":
    get_amazon_data()
