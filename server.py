from fastapi import FastAPI, Request
import ssl
import asyncio
from aiohttp import web
import aiohttp

app = FastAPI()

@app.get("/")
def secure_endpoint():
    return {"message": "Hello, Mutual TLS!"}

# Create aiohttp app for mutual TLS support
async def handle_request(request):
    """Handle request and return JSON response"""
    return web.json_response({"message": "Hello, Mutual TLS!"})
def create_ssl_context():
    """Create SSL context with mutual TLS (client cert required)"""
    # Use TLS 1.2 for proper client cert handling during handshake
    # TLS 1.3 has post-handshake auth which is more complex
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    # Disable TLS 1.3 to ensure client cert is requested during handshake
    ssl_context.maximum_version = ssl.TLSVersion.TLSv1_2
    
    ssl_context.load_cert_chain("server.crt", "server.key")
    ssl_context.load_verify_locations("ca.crt")
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    ssl_context.check_hostname = False
    
    return ssl_context

if __name__ == "__main__":
    print("\nStarting server on https://0.0.0.0:8000")
    print("Server cert: server.crt")
    print("CA cert: ca.crt")
    print("Client cert verification: REQUIRED (mutual TLS)")
    print("TLS Version: 1.2 (forced for proper client cert handling)")
    print("\nServer is running. Test with:")
    print("  python client.py      (with client cert - should succeed)")
    print("  python test_no_cert.py (without client cert - should fail)\n")
    
    # Create aiohttp app
    aiohttp_app = web.Application()
    aiohttp_app.router.add_get("/", handle_request)
    
    # Create SSL context
    ssl_ctx = create_ssl_context()
    
    # Run with aiohttp which properly supports mutual TLS
    web.run_app(aiohttp_app, host="0.0.0.0", port=8000, ssl_context=ssl_ctx)