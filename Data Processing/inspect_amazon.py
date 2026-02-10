from bs4 import BeautifulSoup
import os

def inspect():
    with open("debug_amazon.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, "html.parser")
    items = soup.find_all("div", attrs={"data-component-type": "s-search-result"})
    print(f"Found {len(items)} items using data-component-type.")
    
    if items:
        item = items[0]
        print("\n--- First Item HTML Snippet ---")
        print(item.prettify()[:2000]) # First 2000 chars
        
        # Try to find title
        print("\n--- Searching for Title ---")
        # Try finding ANY span with text that looks like a title (long text)
        spans = item.find_all("span")
        for span in spans:
            if len(span.text.strip()) > 30:
                print(f"Candidate Title: {span.text.strip()[:50]}... Class: {span.get('class')}")
        
        print("\n--- Searching for Price ---")
        for span in spans:
            txt = span.text.strip()
            if txt.startswith("₹") or (txt.replace(',','').isnumeric() and len(txt) > 3):
                 print(f"Candidate Price: {txt} Class: {span.get('class')}")

if __name__ == "__main__":
    inspect()
