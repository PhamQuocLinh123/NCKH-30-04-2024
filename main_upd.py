from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from datetime import *
import time
import smtplib
import random
import PIL.Image
from tkinter import messagebox
from user_upd import Student
#
from face_recognition import Face_Recognition
from attendance import Attendance
from face_recognition import new_tcid
from PIL import Image
import os
from lesson import Lesson
from import_csv import InsertData
from report_attendance import Report
from database_str import Database_str
import mysql.connector
import subprocess

value_from_p1 = None

def new_print(value):
    global value_from_p1
    value_from_p1 = value
    print(value_from_p1)



class Face_Recognition_System(Toplevel):
    def __init__(self, window):
        """takes window as arguments to show all the attributes and keep let them get advantage of the methods,
        that have been created to provide them various feature"""

        Toplevel.__init__(self)
        self.window = window
        self.geometry("1460x750+0+0")
        self.title("Hệ thống xác nhận danh tính và đếm số người")
        self.iconbitmap('ImageFaceDetect\\gaming.ico')
        self.resizable(False, False)
        self.admin_dashboard_frame = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\6.jpg')
        self.image_panel = Label(self, image=self.admin_dashboard_frame)
        self.image_panel.pack(fill='both', expand='yes')

        new_tcid(value_from_p1)

        # thông tin kết nối database
        self.db = Database_str()


        # self.slider()
        # self.heading_color()

        # =========account===========
        # ===lấy thông tin tài khoản=============
        self.account = StringVar()
        self.p_password=StringVar()
        self.n_password=StringVar()
        self.c_password=StringVar()

        def open_login_page():
            login_page_path = r"D:\Nghiên cứu khoa học-2024\face_recognizer\LoginPage.py"
            os.system(f"python {login_page_path}")

        def main():
            # Kiểm tra xem LoginPage.py đã được mở chưa
            login_page_open = False
            for proc in psutil.process_iter():
                if proc.name() == 'python' and proc.cmdline() == ['python', 'LoginPage.py']:
                    login_page_open = True
                    break

            # Nếu LoginPage.py chưa được mở, mở nó trước
            if not login_page_open:
                open_login_page()

            # Tiếp tục thực hiện các thao tác khác
            # Ví dụ: mở trang khác sau khi LoginPage.py đã được mở

        if (value_from_p1 == "0"):#Nếu thông tin truyền từ form login là 0 -> tài khoản admin
            self.account.set("admin")
        elif (value_from_p1 == None):#Nếu chạy riêng file main thì coi như tài khoản admin
            self.account.set("admin")
        else:
            try:
                conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                           database=self.db.database, port=self.db.port)
                my_cursor = conn.cursor()
                my_cursor.execute("select Email from teacher where Teacher_id=%s", (
                    value_from_p1,
                ))
                row = my_cursor.fetchone()
                self.account.set(str(row[0]))
                # self.account = row[0]
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self)

        # ========================================================================
        # ============================Date and time==============================
        # ========================================================================
        self.clock_image = ImageTk.PhotoImage(file="ImageFaceDetect/time.png")
        self.date_time_image = Label(self, image=self.clock_image, bg="white")
        self.date_time_image.place(x=35, y=45)

        self.date_time = Label(self)
        self.date_time.place(x=65, y=35)
        self.time_running()

        # ========================================================================
        # ============================Current user================================
        # ========================================================================
        self.current_user_image = ImageTk.PhotoImage(file="ImageFaceDetect/current_user.png")
        self.current_user_label = Label(self, image=self.current_user_image, bg="white")
        self.current_user_label.place(x=1000, y=47)

        self.current_user = Label(self, bg="white",
                                  font=("times new roman", 10, "bold"), fg="green")
        self.current_user.place(x=1030, y=48)

        # ========================================================================
        # ============================Home button====================================
        # ========================================================================
        self.home = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\trangchu.jpg')
        self.home_button = Button(self, image=self.home,
                                  font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2", command=self.click_home)

        self.home_button.place(x=30, y=100)
        self.click_home()

        # ========================================================================
        # ============================Manage button===============================
        # ========================================================================
        self.manage = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\quanly.jpg')
        self.manage_button = Button(self, image=self.manage,
                                    font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2", command=self.click_manage)

        self.manage_button.place(x=32, y=220)

        # ========================================================================
        # ============================View button===============================
        # ========================================================================
        self.view = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\nhandien1.jpg')
        self.view_button = Button(self, image=self.view,
                                  font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2", command=self.face_recognition)
        self.view_button.place(x=30, y=340)

        # ========================================================================
        # ============================Setting button===============================
        # ========================================================================
        # First setting button
        self.setting_image1 = Image.open('ImageFaceDetect\\dem1.jpg')
        self.setting_image1 = self.setting_image1.resize((108, 105), Image.BILINEAR)
        self.setting_image1 = ImageTk.PhotoImage(self.setting_image1)
        self.setting_button1 = Button(self, image=self.setting_image1,
                                      font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white",
                                      borderwidth=0, background="white", cursor="hand2",
                                      command=self.open_show_face_count)
        self.setting_button1.place(x=30, y=460)  # Position the first setting button)

        # ========================================================================
        # ============================Exit button===============================
        # ========================================================================
        self.exit = Image.open('ImageFaceDetect\\dem.jpg')
        self.exit = self.exit.resize((108, 105), Image.BILINEAR)
        self.exit = ImageTk.PhotoImage(self.exit)

        self.exit_button = Button(self, image=self.exit,
                                  font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white",
                                  borderwidth=0, background="white", cursor="hand2", command=self.open_face_count)
        self.exit_button.place(x=28, y=580)
        self.exit = Image.open('ImageFaceDetect\\dem.jpg')
        self.exit = self.exit.resize((108, 105), Image.BILINEAR)
        self.exit = ImageTk.PhotoImage(self.exit)

        self.exit_button = Button(self, image=self.exit,
                                  font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white",
                                  borderwidth=0, background="white", cursor="hand2", command=self.open_face_count)
        self.exit_button.place(x=28, y=580)




        # ========================================================================
        # ============================Logout button===============================
        # ========================================================================
        # Load the image and resize it
        additional_image = Image.open('ImageFaceDetect\\tieude5.jpg')
        additional_image = additional_image.resize((900, 85), Image.BILINEAR)
        self.additional = ImageTk.PhotoImage(additional_image)

        # Create the button with the resized image
        self.additional_button = Button(self, image=self.additional,
                                        font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                        , borderwidth=0, background="white", cursor="hand2",
                                        command=self)
        self.additional_button.place(x=300, y=0)  # Adjust the position of the button

        self.logout = Image.open('ImageFaceDetect\\dx2.jpg')  # Open the image

        self.logout = ImageTk.PhotoImage(self.logout)  # Convert the image to Tkinter PhotoImage

        # Create the logout button using the resized image
        self.logout_button = Button(self, image=self.logout,
                                    font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2", command=self.click_logout)
        self.logout_button.place(x=1340, y=100)  # Position the button

        # Load the image and resize it
        setting_image = Image.open('ImageFaceDetect\\dmk2.jpg')

        self.setting = ImageTk.PhotoImage(setting_image)

        # Create the button with the resized image
        self.setting_button = Button(self, image=self.setting,
                                     font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                     , borderwidth=0, background="white", cursor="hand2", command=self.click_setting)
        self.setting_button.place(x=1340, y=220)  # Position the button

        # Load the image and resize it
        second_image = Image.open('ImageFaceDetect\\demtuanh.jpg')  # Thay đổi path theo đường dẫn của bạn
        # Convert the image to PhotoImage
        second_image_tk = ImageTk.PhotoImage(second_image)

        # Create the button with the resized image
        second_button = Button(self, image=second_image_tk,
                               font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white",
                               borderwidth=0, background="white", cursor="hand2", command=self.mo_du_lieu_dem_tu_anh)
        second_button.place(x=1340, y=340)  # Thay đổi 10 nếu cần

        # Remember to keep a reference to the image object to prevent it from being garbage collected
        second_button.image = second_image_tk

        # Load another image and resize it
        another_image = Image.open('ImageFaceDetect\\demtucam.jpg')
        another_image_tk = ImageTk.PhotoImage(another_image)

        # Create another button with the resized image
        another_button = Button(self, image=another_image_tk,
                                font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white",
                                borderwidth=0, background="white", cursor="hand2", command=self.mo_du_lieu_dem_tu_video)
        another_button.place(x=1340, y=460)

        # Remember to keep a reference to this image object as well
        another_button.image = another_image_tk

        # Load the first image and resize it
        first_image = Image.open('ImageFaceDetect\\thongke.jpg')
        first_image_tk = ImageTk.PhotoImage(first_image)

        # Create the first button with the resized image
        first_button = Button(self, image=first_image_tk,
                              font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white",
                              borderwidth=0, background="white", cursor="hand2", command=self.thongkedulieu)
        first_button.place(x=1340, y=580)

        # Remember to keep a reference to the first image object
        first_button.image = first_image_tk

    def click_home(self):
        # ===========variable============
        self.student = StringVar()
        self.teacher = StringVar()
        self.classCount = StringVar()


        home_frame = Frame(self)
        home_frame.place(x=145, y=105, height=576, width=1181)

        self.home_dashboard_frame = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\nen8.jpg')
        self.home_panel = Label(home_frame, image=self.home_dashboard_frame, bg="red")
        self.home_panel.pack(fill='both', expand='yes')

        try:

            conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                           database=self.db.database, port=self.db.port)
            my_cursor = conn.cursor()
            # ======== to==========
            my_cursor.execute("select count(*) from student")
            count_st = my_cursor.fetchone()
            self.student.set(count_st[0])
            # =======attendance========
            my_cursor.execute("select count(*) from attendance")
            count_class = my_cursor.fetchone()
            self.classCount.set(count_class[0])
            # =======đi muộn=============
            my_cursor.execute("select  count(*) from face_count")
            count_tc = my_cursor.fetchone()
            self.teacher.set(count_tc[0])

            # ========không điểm danh=======
            # not_in_attendance_table

            conn.commit()
            conn.close()



        except BaseException as msg:
            print(msg)
        total_students = Label(home_frame, text=f" TỔNG {self.student.get()} NGƯỜI DÙNG \n TRONG HỆ THỐNG  ",
                               font=("times new roman",20, "bold"),
                               background="white", fg='#000000')
        total_students.place(x=175, y=130)
        #
        total_teacher = Label(home_frame, text=f" TỔNG {self.teacher.get()} LẦN ĐẾM \n SỐ KHUÔN MẶT",
                                font=("times new roman", 20, "bold"),
                                background="white", fg='#000000')
        total_teacher.place(x=760, y=130)
        #
        # total_class = Label(home_frame, text=f" TỔNG \n {self.classCount.get()}\n PHÒNG",
        #                          font=("times new roman", 30, "bold"),
        #                          background="white", fg='#e67c0b')
        # total_class.place(x=830, y=90)
        #
        total_class = Label(home_frame, text=f"TỔNG {self.classCount.get()} LẦN XÁC \n ĐỊNH DANH TÍNH ",
                            font=("times new roman", 20, "bold"),
                            background="white", fg='#000000')
        total_class.place(x=195, y=380)
        #
        img_ex = PIL.Image.open(r"ImageFaceDetect\excel.png")
        img_student = img_ex.resize((90, 90), Image.Resampling.BILINEAR)
        self.photoimgsv = ImageTk.PhotoImage(img_student)

        self.ex_button = Button(home_frame, image=self.photoimgsv,
                                    font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2", command=self.excel_data)
        self.ex_button.place(x=760,y=325,width=260,height=180)

    def click_manage(self):
        """ opens new frame from where one can go to manage students, employees, departments, course, section
        and batch"""
        manage_frame = Frame(self, bg="white")
        manage_frame.place(x=145, y=105, height=576, width=1181)

        self.manage_dashboard_frame = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\imgg4.jpg')
        self.manage_panel = Label(manage_frame, image=self.manage_dashboard_frame, bg="white")
        self.manage_panel.pack(fill='both', expand='yes')

        # =============Button================
        img_btn1 = Image.open(r"ImageFaceDetect\student2.png")
        img_btn1 = img_btn1.resize((60, 88), Image.BILINEAR)
        self.photobtn1 = ImageTk.PhotoImage(img_btn1)

        button_student = Button(manage_frame, text="Người Dùng", font=("times new roman", 14, "bold"), command=self.student_details,
                    image=self.photobtn1, cursor="hand2",
                    activebackground="white", bg="white", borderwidth=0, compound="top")
        button_student.place(x=320, y=100, width=127, height=127)

        #nút thống kê các bản điểm danh
        img_btn2 = Image.open(r"ImageFaceDetect\ghichu.png")
        img_btn2 = img_btn2.resize((60, 88), Image.BILINEAR)
        self.photobtn2 = ImageTk.PhotoImage(img_btn2)

        button_att = Button(manage_frame, text="Danh Tính", font=("times new roman", 14, "bold"),
                                command=self.attendance_data,
                                image=self.photobtn2, cursor="hand2",
                                activebackground="white", bg="white", borderwidth=0, compound="top")
        button_att.place(x=770, y=100, width=127, height=127)

        #nút quản lý buổi học
        img_btn3 = Image.open(r"ImageFaceDetect\lesson.png")
        img_btn3 = img_btn3.resize((60, 88), Image.BILINEAR)
        self.photobtn3 = ImageTk.PhotoImage(img_btn3)

        button_att = Button(manage_frame, text="", font=("times new roman", 14, "bold"),
                            command=self.lesson_data,
                            image=self.photobtn3, cursor="hand2",
                            activebackground="white", bg="white", borderwidth=0, compound="top")
        button_att.place(x=770, y=350, width=127, height=127)
        # nút thống kê hệ thống
        img_btn4 = Image.open(r"ImageFaceDetect\report.png")
        img_btn4 = img_btn4.resize((60, 88), Image.BILINEAR)
        self.photobtn4 = ImageTk.PhotoImage(img_btn4)

        button_att = Button(manage_frame, text="Thống kê", font=("times new roman", 14, "bold"),
                            command=self.report_data,
                            image=self.photobtn4, cursor="hand2",
                            activebackground="white", bg="white", borderwidth=0, compound="top")
        button_att.place(x=320, y=350, width=127, height=127)




    def click_setting(self):
        """ Allows user to change their password using old password, validations, update entry data to database
        table containing that email or username is done in this method"""
        setting_frame = Frame(self, bg="white")
        setting_frame.place(x=145, y=105, height=576, width=1181)
        self.setting_dashboard_frame = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\fromdmk1.jpg')
        self.setting_panel = Label(setting_frame, image=self.setting_dashboard_frame, bg="white")
        self.setting_panel.pack(fill='both', expand='yes')

        txt = "Đổi mật khẩu"

        heading = Label(setting_frame, text=txt, font=('times new roman', 20, "bold"), bg="white",
                        fg='black',
                        bd=5,
                        relief=FLAT)
        heading.place(x=410, y=27, width=350)

        # ========================================================================
        # ============================Username====================================
        # ========================================================================

        self.username_label = Label(setting_frame, text="Tài khoản ", bg="white", fg="#4f4e4d",
                                    font=("times new roman", 13, "bold"))
        self.username_label.place(x=415, y=90)
        # print(self.account)
        self.username_entry = Entry(setting_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",textvariable=self.account,
                                    font=("times new roman ", 11),state="disabled",)
        self.username_entry.place(x=450, y=118, width=300)

        # ========================================================================
        # ============================PreviousPassword============================
        # ========================================================================

        self.p_password_label = Label(setting_frame, text="Mật khẩu cũ ", bg="white", fg="#4f4e4d",
                                      font=("times new roman", 13, "bold"))
        self.p_password_label.place(x=415, y=180)

        self.p_password_entry = Entry(setting_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",textvariable=self.p_password,
                                      font=("times new roman ", 12), show='*')
        self.p_password_entry.place(x=450, y=207, width=300)  # trebuchet ms

        # ========================================================================
        # ============================New Password============================
        # ========================================================================

        self.n_password_label = Label(setting_frame, text="Mật khẩu mới ", bg="white", fg="#4f4e4d",
                                      font=("times new roman", 13, "bold"))
        self.n_password_label.place(x=415, y=270)

        self.n_password_entry = Entry(setting_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",textvariable=self.n_password,
                                      font=("times new roman ", 12), show='*')
        self.n_password_entry.place(x=450, y=298, width=300)  # trebuchet ms

        # ========================================================================
        # ============================Confirm Password============================
        # ========================================================================

        self.c_password_label = Label(setting_frame, text="Nhập lại mật khẩu ", bg="white", fg="#4f4e4d",
                                      font=("times new roman", 13, "bold"))
        self.c_password_label.place(x=415, y=360)

        self.c_password_entry = Entry(setting_frame, highlightthickness=0, relief=FLAT, bg="white", fg="#6b6a69",textvariable=self.c_password,
                                      font=("times new roman ", 12), show='*')
        self.c_password_entry.place(x=450, y=388, width=300)  # trebuchet ms

        # ========================================================================
        # ============================Submit button================================
        # ========================================================================

        self.submit = ImageTk.PhotoImage \
            (file='ImageFaceDetect\\xacnhandoimk.jpg')

        self.submit_button = Button(setting_frame, image=self.submit,
                                    font=("times new roman", 13, "bold"), relief=FLAT, activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2",
                                    command=self.reset_pass)
        self.submit_button.place(x=520, y=450)

    def reset_pass(self):
        if self.p_password_entry.get()=="":
            messagebox.showerror("Error","Vui lòng nhập mật khẩu cũ",parent=self)
        elif self.n_password_entry.get()=="":
            messagebox.showerror("Error","Vui lòng nhập mật khẩu mới",parent=self)
        elif self.c_password_entry.get()=="":
            messagebox.showerror("Error", "Hãy nhập lại mật khẩu",parent=self)
        elif self.n_password_entry.get()!="" and self.n_password_entry.get()!=self.c_password_entry.get():
            messagebox.showerror("Error", "Vui lòng nhập lại mật khẩu đúng", parent=self)
        elif self.p_password_entry.get()==self.n_password_entry.get():
            messagebox.showerror("Error", "Mật khẩu mới trùng với mật khẩu mới", parent=self)
        else:
            if(self.username_entry.get()=="admin"):
                conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                           database=self.db.database, port=self.db.port)
                my_cursor = conn.cursor()
                my_cursor.execute(
                    "SELECT  Password from admin where Account=%s ",
                    (self.username_entry.get(),))
                row = my_cursor.fetchone()
                if str(row[0])!=self.p_password_entry.get():
                    messagebox.showerror("Error","Mật khẩu cũ sai !!! ",parent=self)
                else:
                    my_cursor.execute("update admin set Password=%s where Account=%s",(self.n_password_entry.get(),self.username_entry.get(),))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thông báo","Đổi mật khẩu thành công",parent=self)
                    self.p_password.set("")
                    self.n_password.set("")
                    self.c_password.set("")
            else:
                conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                           database=self.db.database, port=self.db.port)
                my_cursor = conn.cursor()
                my_cursor.execute(
                    "SELECT  Password from teacher where Teacher_id=%s ",
                    (str(value_from_p1),))
                row = my_cursor.fetchone()
                if str(row[0])!=self.p_password_entry.get():
                    messagebox.showerror("Error", "Mật khẩu cũ sai !!! ", parent=self)
                else:
                    my_cursor.execute("update teacher set Password=%s where Teacher_id=%s",
                                      (self.n_password_entry.get(), str(value_from_p1),))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Thông báo", "Đổi mật khẩu thành công", parent=self)
                    self.p_password.set("")
                    self.n_password.set("")
                    self.c_password.set("")


    def face_recognition(self):
        self.new_window=Toplevel(self)
        self.app=Face_Recognition(self.new_window)
    def student_details(self):
        self.new_window=Toplevel(self)
        self.app=Student(self.new_window)
    def attendance_data(self):
        self.new_window=Toplevel(self)
        self.app=Attendance(self.new_window)

    def lesson_data(self):
        self.new_window = Toplevel(self)
        self.app = Lesson(self.new_window)
    def report_data(self):
        self.new_window=Toplevel(self)
        self.app=Report(self.new_window)

    def excel_data(self):
        self.new_window = Toplevel(self)
        self.app = InsertData(self.new_window)


    def click_exit(self):
        """ Allows user to terminates the program when chosen yes"""
        self.deiconify()
        ask = messagebox.askyesnocancel("Xác nhận thoát", "Bạn chắc chắn muốn đóng chương trình?", parent=self)
        if ask is True:
            self.quit()

    def click_logout(self):
        """Logouts the user to login page from where they will require password in order to login again"""
        Exit = messagebox.askyesno("Đăng xuất", "Bạn có chắc chắn muốn đăng xuất không?", parent=self)
        if (Exit > 0):
            self.destroy()
            self.window.show()
        else:
            if not Exit:
                return

    def slider(self):
        """creates slides for heading by taking the text,
        and that text are called after every 100 ms"""
        if self.count >= len(self.txt):
            self.count = -1
            self.text = ''
            self.heading.config(text=self.text)

        else:
            self.text = self.text + self.txt[self.count]
            self.heading.config(text=self.text)
        self.count += 1

        self.heading.after(100, self.slider)

    def heading_color(self):
        """
        configures heading label every 50 ms
        :return: new random color.

        """
        fg = random.choice(self.color)
        self.heading.config(fg=fg)
        self.heading.after(50, self.heading_color)

    def time_running(self):
        """ displays the current date and time which is shown at top left corner of admin dashboard"""
        self.time = time.strftime("%H:%M:%S")
        self.date = time.strftime('%d/%m/%Y')
        concated_text = f"  {self.time} \n {self.date}"
        self.date_time.configure(text=concated_text, font=("times new roman", 13, "bold"), relief=FLAT
                                 , borderwidth=0, background="white", foreground="black")
        self.date_time.after(100, self.time_running)

    # def open_face_count(self):
    #     os.startfile("face_count.py")

    def open_face_count(self):#hàm này để run file face_count
        # Function to open show_face_count.py
        os.system("python face_count.py")

    def open_show_face_count(self):
        # Function to open show_face_count.py
        os.system("python face_count_camera.py")
    def mo_du_lieu_dem_tu_anh(self):
        os.system("python show_face_count.py")
    def mo_du_lieu_dem_tu_video(self):
        os.system("python show_face_count_camera.py")
    def thongkedulieu(self):
        os.system("python report_attendance.py")
if __name__ == '__main__':
    window = Tk()  # khoi tao cua so va gan root vao
    obj = Face_Recognition_System(window)
    window.mainloop()  # cua so hien len

