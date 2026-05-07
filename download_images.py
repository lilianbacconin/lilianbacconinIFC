import os
import urllib.request
import re
import uuid

url = 'https://lbnraw.myportfolio.com/graphismes'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

output_dir = 'assets/graphismes'
os.makedirs(output_dir, exist_ok=True)

try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    matches = set(re.findall(r'data-src=\"(https://cdn\.myportfolio\.com/[^\"]+)\"', html))
    print(f'Found {len(matches)} images')
    
    for idx, img_url in enumerate(matches):
        try:
            # Extract extension from URL, if none assume jpg
            match = re.search(r'\.(jpeg|jpg|png|gif|webp)', img_url, re.IGNORECASE)
            ext = match.group(1) if match else 'jpg'
            
            # Download the image
            filename = f'graphisme_{idx + 1}.{ext}'
            filepath = os.path.join(output_dir, filename)
            
            print(f'Downloading {img_url} to {filepath}...')
            req_img = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_img) as response, open(filepath, 'wb') as out_file:
                data = response.read()
                out_file.write(data)
                
        except Exception as e:
            print(f'Error downloading {img_url}: {e}')

    print('Download complete.')
except Exception as e:
    print('Error:', e)
