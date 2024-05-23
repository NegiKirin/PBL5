class User:
    def __init__(self, id, name, username, password, phone, email, image):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.phone = phone
        self.email = email
        self.image = image

    def __str__(self):
        return self.name