#/bin/sh

# execute python micro-esb example
docker exec microesb-postgres python3 /01-hosting-use-case/main.py

# select inserted domain record
docker exec microesb-postgres psql -U postgres -d hosting-example -c 'select * from sys_core."domain"'

# select inserted host records
docker exec microesb-postgres psql -U postgres -d hosting-example -c 'select * from sys_dns."dnsrecord"'

