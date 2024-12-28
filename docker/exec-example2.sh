#/bin/sh

# exec cert gen ca service
docker exec microesb-postgres python3 /02-pki-management/main-ca.py
echo ""

# exec cert gen server service
docker exec microesb-postgres python3 /02-pki-management/main-server.py
echo ""

# exec cert gen client service
docker exec microesb-postgres python3 /02-pki-management/main-client.py
echo ""

