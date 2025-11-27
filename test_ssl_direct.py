"""Test mutual TLS using Python's ssl module directly"""
import ssl
import socket
import json

def test_with_client_cert():
    """Test with client certificate"""
    print("Testing with client certificate (using ssl module directly)...")
    
    # Create client SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_cert_chain("client.crt", "client.key")
    context.load_verify_locations("ca.crt")
    context.check_hostname = False
    context.verify_mode = ssl.CERT_REQUIRED
    
    # Force TLS 1.2 to match server
    context.maximum_version = ssl.TLSVersion.TLSv1_2
    
    try:
        with socket.create_connection(("127.0.0.1", 8000)) as sock:
            with context.wrap_socket(sock, server_hostname="localhost") as ssock:
                print(f"  Connected! TLS version: {ssock.version()}")
                print(f"  Server cert: {ssock.getpeercert()}")
                
                # Send HTTP request
                request = b"GET / HTTP/1.1\r\nHost: localhost:8000\r\nConnection: close\r\n\r\n"
                ssock.sendall(request)
                
                # Get response
                response = b""
                while True:
                    data = ssock.recv(4096)
                    if not data:
                        break
                    response += data
                
                print(f"  Response received: {len(response)} bytes")
                # Extract JSON body
                body_start = response.find(b"\r\n\r\n")
                if body_start > 0:
                    body = response[body_start+4:]
                    # Handle chunked encoding
                    if b"\r\n" in body:
                        # Simple chunked parsing
                        lines = body.split(b"\r\n")
                        for line in lines:
                            if line.startswith(b"{"):
                                print(f"  JSON: {line.decode()}")
                                break
                    else:
                        print(f"  Body: {body.decode()}")
                        
                print("✓ SUCCESS: Connection with client cert worked!")
                
    except ssl.SSLError as e:
        print(f"✗ SSL Error: {e}")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")

def test_without_client_cert():
    """Test without client certificate - should fail"""
    print("\nTesting WITHOUT client certificate...")
    
    # Create client SSL context without client cert
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations("ca.crt")
    context.check_hostname = False
    context.verify_mode = ssl.CERT_REQUIRED
    context.maximum_version = ssl.TLSVersion.TLSv1_2
    
    try:
        with socket.create_connection(("127.0.0.1", 8000)) as sock:
            with context.wrap_socket(sock, server_hostname="localhost") as ssock:
                print(f"  Connected (unexpected)!")
                print("✗ FAIL: Should have been rejected!")
                
    except ssl.SSLError as e:
        print(f"✓ SUCCESS: Connection rejected as expected")
        print(f"  Error: {e}")
    except Exception as e:
        print(f"  Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_with_client_cert()
    test_without_client_cert()
