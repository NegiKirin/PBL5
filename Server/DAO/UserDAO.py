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
            user = User(result[0], result[1], result[2],result[3],result[4],result[5],result[6])
            return user
        except Exception as e:
            print(e)
            return {}

    def insertNewUser(self,dic):
        try:
            sql_check_username = 'SELECT * FROM account WHERE username = %s'
            self.myCursor.execute(sql_check_username, [dic['username']])
            result = self.myCursor.fetchall()
            if result == None:
                sql = 'INSERT INTO account (username, password,phone) VALUES ( %s, %s, %s)'
                self.myCursor.execute(sql, [dic['username'],dict['password'], dict['phone']])
                self.connect.commit()

                get_Infor = 'SELECT * FROM account WHERE username = %s'
                self.myCursor.execute(get_Infor, [dic['username']])
                result = self.myCursor.fetchall()
                return result
            else:
                msg = "username already exists"
                return msg
        except Exception as e:
            print(e)

