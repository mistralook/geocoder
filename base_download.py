import requests
from urllib.parse import urlencode

base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
public_key = 'https://yadi.sk/d/MOuom6hWKdmx2w'  # Сюда вписываете вашу ссылку

final_url = base_url + urlencode(dict(public_key=public_key))
response = requests.get(final_url)
download_url = response.json()['href']

download_response = requests.get(download_url)
with open('prepared_base.db', 'wb') as f:
    f.write(download_response.content)
print('done!')