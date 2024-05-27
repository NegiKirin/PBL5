class User:
    def __init__(self, id, lastname, firstname, email, username, password, gender, id_role, avatar,phone):
        self.id = id
        self.lastname = lastname
        self.firstname = firstname
        self.email = email
        self.username = username
        self.password = password
        self.gender = gender
        self.id_role = id_role
        self.avatar = avatar
        self.phone = phone

    def __str__(self):
        return self.username