# Powerdns PostgreSQL Backend Configuration

The included pdns.conf (PowerDNS) runs pdns daemon with psql (PostgreSQL) backend.
Given SQL schemas / configuration can be used with **01-hosting-use-case** example.

Running PowerDNS with this configuration makes inserting DNS records directly
available within the configured IP setup (192.168.100.250 Resolver, 192.168.100.240
PostgreSQL server).

