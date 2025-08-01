\connect "hosting-example"

-- Index: domain_name_ending
DROP INDEX IF EXISTS "sys_core.domain_name_ending";

CREATE UNIQUE INDEX IF NOT EXISTS "sys_core.domain_name_ending"
    ON sys_core."domain" USING btree
    (name ASC NULLS LAST, ending ASC NULLS LAST);

-- Index: domain_user_name_ending
DROP INDEX IF EXISTS "sys_core.domain_user_name_ending_index";

CREATE UNIQUE INDEX IF NOT EXISTS "sys_core.domain_user_name_ending_index"
    ON sys_core."domain" USING btree
    (creator_user_id ASC NULLS LAST, name ASC NULLS LAST, ending ASC NULLS LAST);

-- Index: domain_id
DROP INDEX IF EXISTS "sys_dns.domain_id";

CREATE INDEX IF NOT EXISTS "sys_dns.domain_id"
    ON sys_dns."dnsrecord" USING btree
    (domain_id ASC NULLS LAST);

-- Index: nametype_index
DROP INDEX IF EXISTS "sys_dns.nametype_index";

CREATE INDEX IF NOT EXISTS "sys_dns.nametype_index"
    ON sys_dns."dnsrecord" USING btree
    (name ASC NULLS LAST, type ASC NULLS LAST);
