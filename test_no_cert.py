import httpx
import ssl
import os

# Disable any proxy settings
os.environ['NO_PROXY'] = 'localhost,127.0.0.1'
os.environ['no_proxy'] = 'localhost,127.0.0.1'

ca_cert = "ca.crt"

# Test without client cert - should fail at TLS handshake
print("Testing without client cert...")
print("This should fail if mutual TLS is properly enforced\n")

try:
    with httpx.Client(verify=ca_cert, timeout=10.0, proxy=None) as client:
        response = client.get("https://127.0.0.1:8000")
        print(f"❌ FAIL: Connection succeeded without client cert!")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print("\nMutual TLS is NOT properly enforced!")
except httpx.ConnectError as e:
    print(f"✓ SUCCESS: Connection rejected as expected")
    print(f"Error: {e}")
    print("\nMutual TLS is properly enforced!")
except Exception as e:
    print(f"Unexpected error: {type(e).__name__}: {e}")
