import sys
import telnetlib
import time


class Ptt(object):
    def __init__(self, host, user, password):
        self._host = host
        self._user = user.encode('big5')
        self._password = password.encode('big5')
        self._telnet = telnetlib.Telnet(host)
        self._content = ''

    @property
    def is_success(self):
        if u"密碼不對" in self._content:
            print("密碼不對或無此帳號。程式結束")
            sys.exit()
        if u"您想刪除其他重複登入" in self._content:
            print("刪除其他重複登入的連線....")
            self._telnet.write(b"y\r\n")
            time.sleep(5)
            self._content = self._telnet.read_very_eager().decode('big5', 'ignore')
        if u"請按任意鍵繼續" in self._content:
            print("in front page now...")
            self._telnet.write(b"\r\n")
            time.sleep(2)
        if u"您要刪除以上錯誤嘗試" in self._content:
            print("刪除以上錯誤嘗試...")
            self._telnet.write(b"y\r\n")
            time.sleep(2)
            self._content = self._telnet.read_very_eager().decode('big5', 'ignore')
        if u"您有一篇文章尚未完成" in self._content:
            print('刪除尚未完成的文章....')
            # 放棄尚未編輯完的文章
            self._telnet.write(b"q\r\n")
            time.sleep(2)
            self._content = self._telnet.read_very_eager().decode('big5', 'ignore')
        return True

    @property
    def input_user_password(self):
        if u"請輸入代號" in self._content:
            print('input acct'.format(self._user))
            self._telnet.write(self._user + b"\r\n")
            print('input pw')
            self._telnet.write(self._password + b"\r\n")
            time.sleep(2)
            self._content = self._telnet.read_very_eager().decode('big5', 'ignore')
            return self.is_success
        return False

    def is_connect(self):
        self._content = self._telnet.read_very_eager().decode('big5', 'ignore')
        if u"系統過載" in self._content:
            print('server overload , try later')
            sys.exit(0)
        return True

    def login(self):
        if self.input_user_password:
            print("login success")
            return True
        print("ptt down, login fail")
        return False

    def logout(self):
        print("logging out...")

        self._telnet.write(b"qqqqqqqqqg\r\ny\r\n")
        time.sleep(1)
        self._telnet.close()
        print("logout success")

    def post(self, board, title, content):
        print("發文中...")
        # s 進入要發文的看板
        self._telnet.write(b's')
        self._telnet.write(board.encode('big5') + b'\r\n')
        time.sleep(1)
        self._telnet.write(b'q')
        time.sleep(2)
        # 請參考 http://donsnotes.com/tech/charsets/ascii.html#cntrl
        # Ctrl+P
        self._telnet.write(b'\x10')
        # 發文類別
        self._telnet.write(b'1\r\n')
        self._telnet.write(title.encode('big5') + b'\r\n')
        time.sleep(1)
        # Ctrl+X
        self._telnet.write(content.encode('big5') + b'\x18')
        time.sleep(1)
        # 儲存文章
        self._telnet.write(b's\r\n')
        # 不加簽名檔
        self._telnet.write(b'0\r\n')
        print("----------------------------------------------")
        print("------------------ 發文成功 ------------------")
        print("----------------------------------------------")


def main():
    host = 'ptt.cc'
    users = ['jn8029','msibd']
    password = ['et265831','r1024283']
    for i, user in enumerate(users):
        ptt = Ptt(host, user, password[i])
        time.sleep(1)
        if ptt.is_connect():
            print("using acct {}".format(user))
            if ptt.login():
                pass
        ptt.logout()
    print("done")


if __name__ == "__main__":
    main()
