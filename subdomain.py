import requests
import sys

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

        print(f"[+] Ditemukan {len(subdomains)} subdomain!")
        return sorted(subdomains)

    except Exception as e:
        print(f"[-] Terjadi kesalahan: {e}")
        return []

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Penggunaan: python find_subdomains.py <domain>")
        sys.exit(1)

    target_domain = sys.argv[1]
    hasil = find_subdomains(target_domain)
    for sub in hasil:
        print(sub)
