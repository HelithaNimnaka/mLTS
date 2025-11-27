#!/bin/sh

# Clean up old certificates
rm -f ca.key ca.crt ca.srl
rm -f server.key server.csr server.crt
rm -f client.key client.csr client.crt

# 1. Generate CA (Certificate Authority)
openssl genrsa -out ca.key 2048
openssl req -new -x509 -days 365 -key ca.key -out ca.crt -subj "/CN=MyCA"

# 2. Generate Server Certificate with localhost
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr -subj "/CN=localhost"

# Create server config for SAN
cat > server_ext.cnf << EOF
subjectAltName = DNS:localhost,IP:127.0.0.1
EOF

openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365 -extfile server_ext.cnf
rm server_ext.cnf

# 3. Generate Client Certificate
openssl genrsa -out client.key 2048
openssl req -new -key client.key -out client.csr -subj "/CN=client"
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365

echo "Certificates regenerated successfully!"
echo "Server certificate is now valid for localhost and 127.0.0.1"
