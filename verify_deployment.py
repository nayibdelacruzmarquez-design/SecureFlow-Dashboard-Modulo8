import urllib.request
import json
import sys

def check_service(url):
    try:
        response = urllib.request.urlopen(url, timeout=5)
        if response.status == 200:
            data = json.loads(response.read().decode())
            print(f"[SUCCESS] {url} is healthy: {data}")
            return True
    except Exception as e:
        print(f"[ERROR] Failed to reach {url}: {e}")
        return False

if __name__ == "__main__":
    print("Verificando servicios desplegados localmente...")
    health_ok = check_service("http://localhost:8000/health")
    if health_ok:
        sys.exit(0)
    else:
        sys.exit(1)
        