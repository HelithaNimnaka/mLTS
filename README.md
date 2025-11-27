# mTLS Demo

A simple Python demonstration of **Mutual TLS (mTLS)** authentication using FastAPI/aiohttp and httpx.

## What is mTLS?

Mutual TLS (also called two-way SSL) ensures both the client and server authenticate each other using X.509 certificates. Unlike standard HTTPS where only the server presents a certificate, mTLS requires the client to also present a valid certificate signed by a trusted Certificate Authority (CA).

## Project Structure

- `server.py` - aiohttp server with mTLS enforcement (TLS 1.2)
- `client.py` - httpx client with proper client certificate
- `test_no_cert.py` - Test that connection fails without client cert
- `test_ssl_direct.py` - Low-level SSL test using Python's socket/ssl modules
- `regenerate_certs.sh` - Script to generate CA, server, and client certificates

## Setup

### 1. Generate Certificates

Run the certificate generation script:

```bash
bash regenerate_certs.sh
```

This creates:
- `ca.crt` / `ca.key` - Certificate Authority
- `server.crt` / `server.key` - Server certificate (valid for localhost/127.0.0.1)
- `client.crt` / `client.key` - Client certificate

### 2. Install Dependencies

```bash
pip install fastapi aiohttp httpx
```

## Usage

### Start the Server

```bash
python server.py
```

The server starts on `https://0.0.0.0:8000` with:
- Server certificate: `server.crt`
- Client verification: **REQUIRED** (mTLS enabled)
- TLS version: 1.2 (for proper client cert handling)

### Test with Client Certificate (Should Succeed)

```bash
python client.py
```

Expected output:
```json
{"message": "Hello, Mutual TLS!"}
```

### Test without Client Certificate (Should Fail)

```bash
python test_no_cert.py
```

Expected output:
```
✓ SUCCESS: Connection rejected as expected
Mutual TLS is properly enforced!
```

### Low-Level SSL Test

```bash
python test_ssl_direct.py
```

Tests both scenarios using Python's ssl module directly.

## How It Works

1. **Server Setup**: The server loads its certificate (`server.crt`) and private key (`server.key`), then configures `ssl.CERT_REQUIRED` to enforce client certificate validation against the CA (`ca.crt`).

2. **Client Setup**: The client loads its certificate (`client.crt`) and private key (`client.key`) and trusts the CA certificate (`ca.crt`) to verify the server.

3. **TLS Handshake**: During the TLS 1.2 handshake, both parties exchange and verify certificates. If either verification fails, the connection is rejected.

## Security Notes

- All certificates and private keys are in `.gitignore` and should **never** be committed
- Anyone cloning this repo must run `regenerate_certs.sh` to create their own certificates
- In production, use proper CA-signed certificates, not self-signed ones
- Consider using TLS 1.3 with proper post-handshake authentication for better security

## License

MIT
