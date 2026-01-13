#/bin/sh

# exec cert gen ca service
docker exec microesb-postgres python3 /02-pki-management/00-main-ca.py
echo ""

# exec cert gen server service
docker exec microesb-postgres python3 /02-pki-management/01-main-server.py
echo ""

# exec cert gen client service
docker exec microesb-postgres python3 /02-pki-management/02-main-client.py
echo ""
