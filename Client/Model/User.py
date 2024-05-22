class User:
    def __init__(self, email, fullname, nickname, phoneNumbers, gender, age, role=0, id=None, username=None,
                 password=None):
        self.id = id
        self.role = role
        self.username = username
        self.email = email
        self.fullname = fullname
        self.nickname = nickname
        self.phoneNumbers = phoneNumbers
        self.gender = gender
        self.age = age

        self.password = password

    '''''
    def set_username(self, name):
        self.username = name

    def set_email(self, email):
        self.email = email

    def set_fullname(self, fullname):
        self.fullname = fullname

    def set_nickname(self, nickname):
        self.nickname = nickname

    def set_phoneNumbers(self, phoneNumbers):
        self.phoneNumbers = phoneNumbers

    def set_password(self, password):
        self.password = password

    def set_gender(self, gender):
        self.gender = gender
    '''''
