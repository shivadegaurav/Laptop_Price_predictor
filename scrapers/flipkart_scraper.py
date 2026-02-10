import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

def get_flipkart_data():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
    
    # URLs to scrape (Flipkart laptop search results)
    base_url = "https://www.flipkart.com/search?q=laptops&page={}"
    
    laptops = []
    
    for page in range(1, 41): # Scraping first 40 pages to aim for 500+ items
        print(f"Scraping Flipkart Page {page}...")
        try:
            url = base_url.format(page)
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                # Debug: Save first page HTML
                if page == 1:
                    with open("debug_flipkart.html", "w", encoding="utf-8") as f:
                        f.write(response.text)
                
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Check for different Flipkart layouts
                # Layout found in debug: data-id based
                items = soup.find_all("div", attrs={"data-id": True})
                
                count = 0
                for item in items:
                    data = {}
                    
                    # Title
                    title_tag = item.find("div", class_="RG5Slk")
                    if not title_tag:
                         title_tag = item.find("div", class_="_4rR01T") # Old class
                    if not title_tag:
                         title_tag = item.find("a", class_="s1Q9rs") # Grid class
                    
                    if title_tag:
                        data['Title'] = title_tag.text.strip()
                    else:
                        # Sometimes hidden or different structure
                        continue
                        
                    # Price
                    price_tag = item.find("div", class_="hZ3P6w")
                    if not price_tag:
                         price_tag = item.find("div", class_="_30jeq3") # Old class
                        
                    if price_tag:
                        data['Price'] = price_tag.text.strip().replace('₹', '').replace(',', '')
                    else:
                        data['Price'] = None
                    
                    # Rating
                    rating_tag = item.find("div", class_="MKiFS6")
                    if not rating_tag:
                         rating_tag = item.find("div", class_="_3LWZlK") # Old class
                    
                    if rating_tag:
                        data['Rating'] = rating_tag.text.strip()
                    else:
                        data['Rating'] = None
                        
                    # Features/Specs (List items)
                    ul_tag = item.find("ul", class_="HwRTzP")
                    if not ul_tag:
                         ul_tag = item.find("ul", class_="_1xgFaf") # Old class
                         
                    if ul_tag:
                        features = [li.text for li in ul_tag.find_all("li")]
                        data['Features'] = " | ".join(features)
                    else:
                        data['Features'] = ""
                        
                    laptops.append(data)
                    count += 1
                
                print(f"Found {count} items on page {page}")
            else:
                print(f"Failed to retrieve Flipkart page {page}. Status: {response.status_code}")
                
            time.sleep(2)
            
        except Exception as e:
            print(f"Error scraping Flipkart page {page}: {e}")
            
    df = pd.DataFrame(laptops)
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'flipkart_laptops.csv')
    df.to_csv(output_path, index=False)
    print(f"Flipkart data saved to {output_path}")

if __name__ == "__main__":
    get_flipkart_data()
