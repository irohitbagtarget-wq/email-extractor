import requests
import re
import time
import csv

# ============ SETTINGS ============
INPUT_FILE = "only_contact_links.txt"
OUTPUT_FILE = "extracted_emails.csv"
DELAY = 2
BATCH_SIZE = 50  # Har baar 50 links process karega

def extract_emails(text):
    return list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)))

def get_clean_website(url):
    try:
        if 'u=' in url:
            return requests.utils.unquote(url.split('u=')[1].split('&')[0])
    except:
        pass
    return None

print("🚀 Script shuru ho raha hai...")

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    links = [line.strip() for line in f if line.strip()]

results = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for i in range(0, len(links), BATCH_SIZE):
    batch = links[i:i+BATCH_SIZE]
    print(f"Processing batch {i//BATCH_SIZE + 1} ({len(batch)} links)...")
    
    for link in batch:
        website = get_clean_website(link)
        if not website:
            continue

        try:
            res = requests.get(website, headers=headers, timeout=10)
            emails = extract_emails(res.text)
            
            if emails:
                for email in emails:
                    results.append({
                        'website': website,
                        'email': email
                    })
                    print(f"✅ Found: {email}")
        except:
            pass

        time.sleep(DELAY)

    # Har batch ke baad save kar do
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['website', 'email'])
        writer.writeheader()
        writer.writerows(results)

print(f"\n✅ Done! Total emails found: {len(results)}")
