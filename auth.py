class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def auth(self, input_password):
        return self.password == input_password
