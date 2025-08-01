\connect "hosting-example"

-- SCHEMA: sys_core

DROP SCHEMA IF EXISTS sys_core CASCADE;

CREATE SCHEMA IF NOT EXISTS sys_core;

-- SCHEMA: sys_dns

DROP SCHEMA IF EXISTS sys_dns CASCADE;

CREATE SCHEMA IF NOT EXISTS sys_dns;

-- SEQUENCE: sys_core.user_id_seq

DROP SEQUENCE IF EXISTS sys_core."user_id_seq";

CREATE SEQUENCE IF NOT EXISTS sys_core."user_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

-- SEQUENCE: sys_core.domain_id_seq

DROP SEQUENCE IF EXISTS sys_core."domain_id_seq";

CREATE SEQUENCE IF NOT EXISTS sys_core."domain_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

-- SEQUENCE: sys_dns.dnsrecord_id_seq

DROP SEQUENCE IF EXISTS sys_dns."dnsrecord_id_seq";

CREATE SEQUENCE IF NOT EXISTS sys_dns."dnsrecord_id_seq"
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;
