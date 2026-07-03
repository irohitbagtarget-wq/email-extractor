import requests
import re
import time
import csv

# ============ SETTINGS ============
INPUT_FILE = "only_contact_links.txt"      # Badi wali file
OUTPUT_FILE = "extracted_emails.csv"
DELAY = 1                              # seconds (agar garam ho to 2-3 kar dena)

def extract_emails(text):
    """Text se sab emails nikaal ke list return karta hai"""
    return list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)))

def get_clean_website(url):
    """Clutch redirect link se asli website nikaalta hai"""
    try:
        if 'u=' in url:
            return requests.utils.unquote(url.split('u=')[1].split('&')[0])
    except:
        pass
    return None

# ============ MAIN CODE ============
print("🚀 Script shuru ho raha hai...")

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    links = [line.strip() for line in f if line.strip()]

results = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for i, link in enumerate(links, 1):
    print(f"Processing {i}/{len(links)} ...", end='\r')
    
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
                print(f"\n✅ Found: {email} from {website}")
    except Exception as e:
        print(f"\n❌ Error on {website}: {e}")

    time.sleep(DELAY)   # Laptop ko rest do

# Save results
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['website', 'email'])
    writer.writeheader()
    writer.writerows(results)

print(f"\n\n✅ Done! Total emails found: {len(results)}")
print(f"📁 Results saved in: {OUTPUT_FILE}")
