import requests
import re

r = requests.get('https://rextie.com')
html = r.text

# Buscar URLs que parezcan APIs
urls = re.findall(r'https://[^"\'<>\s]+', html)

print("URLs encontradas que pueden ser APIs:")
for url in urls:
    if 'api' in url.lower() or 'graph' in url.lower() or 'rate' in url.lower():
        print(f"  {url}")
