from microesb import microesb


class User(microesb.ClassHandler):
    def __init__(self):
        super().__init__()
        self.DB_user_id = 1


class Domain(microesb.ClassHandler):

    def __init__(self):
        super().__init__()

    def add(self):
        print("Domain add() called")
        print("DB_user_id:{}".format(self.parent_object.DB_user_id))


class Host(microesb.MultiClassHandler):

    def __init__(self):
        super().__init__()

    def add(self):
        print("Host add() called")
