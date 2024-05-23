from Server.Model.User import User
from Server.Util import Connection


class UserDAO:
    def __init__(self):
        self.connect = Connection.getConnect()
        self.myCursor = self.connect.cursor()

    def findByUsernameAndPassword(self, dic):
        try:
            sql = 'SELECT * FROM account WHERE username = %s AND password = %s'
            self.myCursor.execute(sql, [dic['username'], dic['password']])
            result = self.myCursor.fetchall()
            # item = result[0]
            # user = User(item[0], item[1], item[2])
            user = User(1, "phuc", "123", "123", "123", "1312", "123")
            return user
        except Exception as e:
            print(e)
            return {}
