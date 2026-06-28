import os
import time
import urllib.request


def fetch(url):
    with urllib.request.urlopen(url, timeout=5) as response:
        return response.status, response.read().decode('utf-8')


def test_container_stack():
    base_url = os.environ.get('BASE_URL', 'http://127.0.0.1:5000')
    error = None
    for _ in range(30):
        try:
            status, body = fetch(f'{base_url}/healthz')
            if status == 200 and 'ok' in body:
                break
        except Exception as exc:
            error = exc
        time.sleep(2)
    else:
        raise AssertionError(f'application did not become healthy: {error}')

    status, body = fetch(base_url)
    assert status == 200
    assert '<title>TempConverter</title>' in body
    assert 'CI Student' in body
    assert 'CI College' in body
