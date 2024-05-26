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
            user = []
            # user = User(item[0], item[1], item[2])
            for item in result:
                user = User(item[0], item[1], item[2],item[3],item[4],item[5],item[6])
            return user
        except Exception as e:
            print(e)
            return {}

    def insertNewUser(self,dic):
        try:
            sql_check_username = 'SELECT * FROM account WHERE username = %s'
            self.myCursor.execute(sql_check_username, [dic['username']])
            result = self.myCursor.fetchall()
            if result == []:
                sql = 'INSERT INTO account (username, password,phone) VALUES ( %s, %s, %s)'
                self.myCursor.execute(sql, [dic['username'],dic['password'], dic['phone']])
                self.connect.commit()
                get_Infor = 'SELECT * FROM account WHERE username = %s'
                self.myCursor.execute(get_Infor, [dic['username']])
                result = self.myCursor.fetchall()
                user = User(result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6])
                print(user)
                return user
            else:
                msg = "username already exists"
                return msg
        except Exception as e:
            print(e)

    def UpdateUser(self,dic):
        try:
            sql = 'UPDATE account SET username = %s, phone = %s'
            self.myCursor.execute(sql, [dic['username'],dic['phone']])
            self.connect.commit()
        except Exception as e:
            print(e)
