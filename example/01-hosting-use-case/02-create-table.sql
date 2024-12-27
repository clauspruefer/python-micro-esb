\connect "hosting-example"

-- Table: sys_core.user
CREATE TABLE IF NOT EXISTS sys_core."user"
(
    id bigint NOT NULL DEFAULT nextval('sys_core.user_id_seq'::regclass),
    name character varying NOT NULL,
    CONSTRAINT user_pkey PRIMARY KEY (id)
);

-- Table: sys_core.domain
CREATE TABLE IF NOT EXISTS sys_core."domain"
(
    id bigint NOT NULL DEFAULT nextval('sys_core.domain_id_seq'::regclass),
    name text NOT NULL,
    ending character varying,
    creator_user_id bigint NOT NULL,
    CONSTRAINT domain_pkey PRIMARY KEY (id),
    CONSTRAINT admin_user_id_fk FOREIGN KEY (creator_user_id)
        REFERENCES sys_core."user" (id) MATCH FULL
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

-- Table: sys_dns.dnsrecord
CREATE TABLE IF NOT EXISTS sys_dns."dnsrecord"
(
    id integer NOT NULL DEFAULT nextval('sys_dns.dnsrecord_id_seq'::regclass),
    domain_id integer NOT NULL,
    name character varying(255) NULL,
    type character varying(10) NOT NULL,
    content character varying(65535) NOT NULL,
    ttl integer,
    prio integer,
    CONSTRAINT dnsrecord_pkey PRIMARY KEY (id),
    CONSTRAINT domain_id_fk FOREIGN KEY (domain_id)
        REFERENCES sys_core.domain (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT c_lowercase_name CHECK (name::text = lower(name::text))
);
