from tkinter import *
from PIL import ImageTk, Image
import mysql.connector
from tkinter import messagebox
import hashlib

class RegisterPage(object):
    def __init__(self, window):
        self.window = window
        self.window.geometry('500x300')
        self.window.title('Đăng ký hệ thống')

        self.var_email = StringVar()
        self.var_password = StringVar()

        self.email_label = Label(window, text="Tài khoản")
        self.email_label.pack()
        self.email_entry = Entry(window, textvariable=self.var_email)
        self.email_entry.pack()

        self.password_label = Label(window, text="Mật khẩu")
        self.password_label.pack()
        self.password_entry = Entry(window, textvariable=self.var_password, show="*")
        self.password_entry.pack()

        self.register_button = Button(window, text="Đăng ký", command=self.register)
        self.register_button.pack()

    def register(self):
        email = self.var_email.get()
        password = self.var_password.get()

        if email == "" or password == "":
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
        else:
            try:
                conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer', port='3306')
                my_cursor = conn.cursor()

                # Kiểm tra xem tài khoản đã tồn tại trong cơ sở dữ liệu chưa
                my_cursor.execute("SELECT * FROM admin WHERE Account=%s", (email,))
                row = my_cursor.fetchone()
                if row:
                    messagebox.showerror("Lỗi", "Tài khoản đã tồn tại.")
                else:
                    # Mã hóa mật khẩu trước khi lưu vào cơ sở dữ liệu
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()

                    my_cursor.execute("INSERT INTO admin (Account, Password) VALUES (%s, %s)", (email, hashed_password))
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Thông báo", "Đăng ký thành công.")
                    self.window.destroy()  # Đóng cửa sổ đăng ký sau khi đăng ký thành công
            except Exception as es:
                messagebox.showerror("Lỗi", f"Đăng ký không thành công. Lỗi: {str(es)}")

if __name__ == '__main__':
    window = Tk()
    obj = RegisterPage(window)
    window.mainloop()
