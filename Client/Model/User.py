class User:
<<<<<<< HEAD
    def __init__(self, id, name, username, password, phone, email, image):
        self.id = id
        self.name = name
=======
    def __init__(self, email, fullname, nickname, phoneNumbers, gender, age, role=0, id=None, username=None,
                 password=None):
        self.id = id
        self.role = role
>>>>>>> d40f260d798dedcaeb6eb52611c1e47372bac8fe
        self.username = username
        self.password = password
        self.phone = phone
        self.email = email
<<<<<<< HEAD
        self.image = image

    def __str__(self):
        return self.name
=======
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
>>>>>>> d40f260d798dedcaeb6eb52611c1e47372bac8fe
