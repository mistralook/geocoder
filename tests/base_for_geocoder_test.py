import requests
from urllib.parse import urlencode


def create_base():
    base_url =\
        'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    public_key = 'https://yadi.sk/d/8o1wf4wzv2pd7A'
    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    download_url = response.json()['href']

    download_response = requests.get(download_url)
    with open('isle_of_wight_test.db', 'wb') as f:
        f.write(download_response.content)
    print('done!')


def main():
    create_base()


if __name__ == '__main__':
    main()
