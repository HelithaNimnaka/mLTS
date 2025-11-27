import httpx
import os
import ssl

# Disable any proxy settings
os.environ['NO_PROXY'] = 'localhost,127.0.0.1'
os.environ['no_proxy'] = 'localhost,127.0.0.1'

# Create custom SSL context that matches server (TLS 1.2)
ssl_context = ssl.create_default_context()
ssl_context.load_cert_chain("client.crt", "client.key")
ssl_context.load_verify_locations("ca.crt")
ssl_context.maximum_version = ssl.TLSVersion.TLSv1_2
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_REQUIRED

# Test with client cert (mutual TLS)
with httpx.Client(verify=ssl_context, proxy=None) as client:
    response = client.get("https://127.0.0.1:8000")
    print(response.json())