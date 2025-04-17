import requests
import sys
import socket
from http.client import HTTPConnection, HTTPSConnection
from urllib.parse import urlparse

def find_subdomains(domain):
    print(f"[+] Mencari subdomain untuk: {domain}")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print("[-] Gagal mengakses crt.sh")
            return []

        raw_data = response.json()
        subdomains = set()

        for entry in raw_data:
            name_value = entry.get('name_value', '')
            for d in name_value.split('\n'):
                if domain in d:
                    subdomains.add(d.strip())

        print(f"[+] Ditemukan {len(subdomains)} subdomain!\n")
        return sorted(subdomains)

    except Exception as e:
        print(f"[-] Terjadi kesalahan: {e}")
        return []

def check_port(host, port):
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except:
        return False

def get_http_response(subdomain, port):
    try:
        if port == 443:
            conn = HTTPSConnection(subdomain, port, timeout=3)
        else:
            conn = HTTPConnection(subdomain, port, timeout=3)

        conn.request("GET", "/")
        res = conn.getresponse()

        print(f"[RESPON] {res.status} {res.reason}")
        for header in ["Location", "Content-Type"]:
            value = res.getheader(header)
            if value:
                print(f"[RESPON] {header}: {value}")
        conn.close()
    except Exception as e:
        print(f"[RESPON] Gagal mengambil respon: {e}")

def main(domain):
    subdomains = find_subdomains(domain)
    common_ports = [80, 443]

    for sub in subdomains:
        print(f"[CEKER] {sub}")
        open_ports = []
        for port in common_ports:
            if check_port(sub, port):
                print(f"[+] Port {port} terbuka")
                get_http_response(sub, port)
                open_ports.append(port)
            else:
                print(f"[-] Port {port} tertutup")
        if not open_ports:
            print(f"{sub} => Tidak ada port terbuka\n")
        else:
            print(f"{sub} => Port terbuka: {', '.join(map(str, open_ports))}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Penggunaan: python subdomain_checker.py <domain>")
        sys.exit(1)

    target = sys.argv[1]
    main(target)
        
