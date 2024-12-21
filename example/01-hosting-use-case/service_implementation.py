import psycopg2

from microesb import microesb


class User(microesb.ClassHandler):

    def __init__(self):
        super().__init__()
        self.DB_user_id = None

    def init(self):
        with self.dbcon.cursor() as crs:
            crs.execute("""
                SELECT id
                    FROM sys_core."user"
                WHERE
                    "name" = %s""",
                (self.name,)
            )
            row = crs.fetchone()
            self.DB_user_id = row[0]


class Domain(microesb.ClassHandler):

    def __init__(self):
        super().__init__()
        self.DB_domain_id = None

    def add(self):

        self.DB_user_id = self.parent_object.DB_user_id
        self.dbcon = self.parent_object.dbcon
        print("DB_user_id:{} name:{} ending:{}".format(
            self.DB_user_id, self.name, self.ending)
        )

        print("Insert Domain")

        with self.dbcon.cursor() as crs:
            crs.execute(
                """
                SELECT id
                    FROM sys_core."domain"
                WHERE
                    creator_user_id = %s AND "name" = %s AND ending = %s""",
                (self.DB_user_id, self.name, self.ending,)
            )
            try:
                row = crs.fetchone()
                self.DB_domain_id = row[0]
            except Exception as e:
                pass

        print("DB_domain_id:{}".format(self.DB_domain_id))

        with self.dbcon.cursor() as crs:
            crs.execute(
                """
                INSERT INTO sys_core."domain"
                    (creator_user_id, "name", ending)
                VALUES
                    (%s, %s, %s)
                ON CONFLICT (creator_user_id, "name", ending) DO NOTHING
                RETURNING id
                """,
                (self.DB_user_id, self.name, self.ending)
            )
            try:
                row = crs.fetchone()
                self.DB_domain_id = row[0]
            except Exception as e:
                pass


class Host(microesb.MultiClassHandler):

    def __init__(self):
        super().__init__()
        self.name = None
        self.priority = None
        self.ttl = None

    def add(self):
        self.dbcon = self.parent_object.dbcon
        self.DB_user_id = self.parent_object.DB_user_id
        self.DB_domain_id = self.parent_object.DB_domain_id

        print("Host add() called")

        print("DB_user_id:{} DB_domain_id:{}".format(
            self.DB_user_id, self.DB_domain_id)
        )

        try:
            with self.dbcon.cursor() as crs:
                crs.execute(
                    """
                    INSERT INTO sys_dns."dnsrecord"
                        (domain_id, "name", "type", content, ttl, prio)
                    VALUES
                        (%s, %s, %s, %s, %s, %s)""",
                    (
                        self.DB_domain_id,
                        self.name,
                        self.type,
                        self.value,
                        self.ttl,
                        self.priority
                    )
                )
        except Exception as e:
            print("Insert excetion:{}".format(e))
