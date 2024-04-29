from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
import PIL.Image
import numpy as np
import random
from tkinter import messagebox
import mysql.connector
from tkcalendar import Calendar, DateEntry
from time import strftime
import cv2
import os
import re
from database_str import Database_str
from search_image import student_id
from search_image import StdImage

mydata = []


class Student:
    def __init__(self, root):
        self.root = root
        w = 1350  # chiều dài giao diện
        h = 700  # chiều rộng giao diện

        ws = self.root.winfo_screenwidth()  # độ dài màn hình
        hs = self.root.winfo_screenheight()  # độ rộng màn
        x = (ws / 2) - (w / 2)  # vị trí cách lề trái x px
        y = (hs / 2) - (h / 2)  # vị trí cách lề trên y px

        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))  # kích thước và vị trí hiển thị giao diện
        self.root.title("QLSV")
        self.root.iconbitmap('ImageFaceDetect\\gaming.ico')
        today = strftime("%d-%m-%Y")

        # thông tin kết nối database
        self.db = Database_str()

        # ======================variables================
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()  # khóa học
        self.var_semester = StringVar()  # cơ sở
        self.var_std_id = StringVar()  # id_hoc sinh
        self.var_std_name = StringVar()  # tên hoc sinh
        self.var_div = StringVar()  # lớp
        self.var_roll = StringVar()  # CMND
        self.var_gender = StringVar()  # giới tính
        self.var_dob = StringVar()  # ngày sinh
        self.var_email = StringVar()  # email
        self.var_phone = StringVar()  # SDT
        self.var_address = StringVar()  # Địa chỉ

        # ==================classvariables================
        self.var_class = StringVar()  # biến chứa Phòng
        self.var_nameclass = StringVar()  # biến tên Phòng
        # Lay thông tin Phòng
        class_array = []  # mảng thông tin Phòng
        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                       database=self.db.database, port=self.db.port)
        my_cursor = conn.cursor()
        my_cursor.execute("Select Class from class")  # truy vấn tất cả lớp trong bảng class
        data_class = my_cursor.fetchall()
        for i in data_class:  # Với mỗi lớp trong mảng Phòng : truyền thông tin lớp vào mảng Phòng
            class_array.append(i)

        img3 = PIL.Image.open(r"ImageFaceDetect\bgnt.png")  # Ảnh nền
        img3 = img3.resize((1350, 700), PIL.Image.BILINEAR)  # resize ảnh nền
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoimg3)  # label chứa ảnh nền
        bg_img.place(x=0, y=0, width=1350, height=700)

        # ==================================heading====================================
        # ====time====
        img_time = PIL.Image.open(r"ImageFaceDetect\timsearch50.png")  # Ảnh icon thời gian
        img_time = img_time.resize((27, 27), PIL.Image.BILINEAR)
        self.photoimgtime = ImageTk.PhotoImage(img_time)
        time_img = Label(self.root, image=self.photoimgtime, bg="white")
        time_img.place(x=43, y=40, width=27, height=27)

        def time():  # Hàm thời gian thay đổi mỗi giây
            string = strftime('%H:%M:%S %p')
            lbl.config(text=string)
            lbl.after(1000, time)

        lbl = Label(self.root, font=("times new roman", 11, "bold"), bg="white", fg="black")
        lbl.place(x=80, y=35, width=100, height=18)
        time()  # chạy hàm time
        lbl1 = Label(self.root, text=today, font=("times new roman", 11, "bold"), bg="white", fg="black")
        lbl1.place(x=80, y=60, width=100, height=18)

        # ====title=========
        self.txt = "Quản lý thông tin phòng"  # tiêu đề
        self.count = 0
        self.text = ''
        self.color = ["#4f4e4d", "#f29844", "red2"]
        self.heading = Label(self.root, text=self.txt, font=("times new roman", 22, "bold"), bg="white", fg="black",
                             bd=5, relief=FLAT)
        self.heading.place(x=400, y=22, width=650)
        # self.slider()
        # self.heading_color()

        main_frame = Frame(bg_img, bd=2, bg="white")  # main frame
        main_frame.place(x=24, y=90, width=1293, height=586)




        # ===============================bottomright-Class==============================
        # Thông tin Phòng và các chức năng thêm ,sửa ,xóa ,.....
        Underright_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                      font=("times new roman", 11, "bold"))
        Underright_frame.place(x=7, y=10, width=1270, height=550)



        # # search
        # self.var_com_searchclass = StringVar()  # Loại tìm kiếm lớp (theo lớp, tên lớp)
        # search_combo = ttk.Combobox(Underright_frame, font=("times new roman", 11, "bold"),
        #                             textvariable=self.var_com_searchclass,
        #                             state="readonly",
        #                             width=11)
        # search_combo["values"] = ("Lớp", "Tên lớp")
        # search_combo.current(0)
        # search_combo.grid(row=0, column=0, padx=10, pady=40, sticky=W)

        # self.var_searchclass = StringVar()  # ký tự cần tìm
        # searchstd_entry = ttk.Entry(Underright_frame, textvariable=self.var_searchclass, width=13,
        #                             font=("times new roman", 10, "bold"))
        # searchstd_entry.grid(row=0, column=1, padx=5, pady=35, sticky=W)

        # # Các nút
        img_btn4 = PIL.Image.open(r"ImageFaceDetect\btnRed.png")  # ảnh nút màu đỏ
        img_btn4 = img_btn4.resize((80, 25), PIL.Image.BILINEAR)
        self.photobtn4 = ImageTk.PhotoImage(img_btn4)
        #
        # # nút tìm kiếm
        # searchstd_btn = Button(Underright_frame, command=self.search_Classdata, text="Tìm kiếm",
        #                        font=("times new roman", 10, "bold"), bd=0, bg="white", cursor='hand2',
        #                        activebackground='white',
        #                        width=80, image=self.photobtn4, fg="white", compound="center")
        # searchstd_btn.grid(row=0, column=5, padx=3)
        #
        # # nút xem tất cả
        # showAllstd_btn = Button(Underright_frame, text="Xem tất cả", command=self.fetch_Classdata,
        #                         font=("times new roman", 10, "bold"), bd=0, bg="white", cursor='hand2',
        #                         activebackground='white',
        #                         width=80, image=self.photobtn4, fg="white", compound="center")
        # showAllstd_btn.grid(row=0, column=3, padx=3)

        # Phòng
        studentid_label = Label(Underright_frame, text="Phòng:", font=("times new roman", 12, "bold"),
                                bg="white", width=12)
        studentid_label.place(x=150, y=100, width=100)

        studentid_entry = ttk.Entry(Underright_frame, textvariable=self.var_class,
                                    font=("times new roman", 12, "bold"), width=20)
        studentid_entry.place(x=250, y=100, width=270)

        # Tên Phòng
        subsub_label = Label(Underright_frame, text="Tên Phòng:", font=("times new roman", 12, "bold"),
                             bg="white")
        subsub_label.place(x=150, y=145, width=80)

        subsub_entry = ttk.Entry(Underright_frame, width=22, textvariable=self.var_nameclass,
                                 font=("times new roman", 12, "bold"))
        subsub_entry.place(x=250, y=145, width=270)

        # btn_frame
        btn_framestd = Frame(Underright_frame, bg="white", bd=2, relief=RIDGE)
        btn_framestd.place(x=150, y=250, width=400, height=55)

        img_btn5 = PIL.Image.open(r"ImageFaceDetect\btnRed.png")
        img_btn5 = img_btn5.resize((90, 30), PIL.Image.BILINEAR)
        self.photobtn5 = ImageTk.PhotoImage(img_btn5)

        # nút thêm Phòng
        addTc_btn = Button(btn_framestd, text="Thêm", command=self.add_Classdata,
                           font=("times new roman", 11, "bold"),
                           bd=0, bg="white", cursor='hand2', activebackground='white',
                           width=90, image=self.photobtn5, fg="white", compound="center"
                           )
        addTc_btn.place(x=5, y=7)

        # nút xóa Phòng
        deleteTc_btn = Button(btn_framestd, text="Xóa", command=self.delete_Classdata,
                              font=("times new roman", 11, "bold"),
                              bd=0, bg="white", cursor='hand2', activebackground='white',
                              width=90, image=self.photobtn5, fg="white", compound="center"
                              )
        deleteTc_btn.place(x=103, y=7)

        # nút cập nhật thông tin Phòng
        updateTc_btn = Button(btn_framestd, text="Cập nhật", command=self.update_Classdata,
                              font=("times new roman", 11, "bold"),
                              bd=0, bg="white", cursor='hand2', activebackground='white',
                              width=90, image=self.photobtn5, fg="white", compound="center")
        updateTc_btn.place(x=201, y=7)

        # nút làm mới
        resetTc_btn = Button(btn_framestd, text="Làm mới", command=self.reset_Classdata,
                             font=("times new roman", 11, "bold"),
                             bd=0, bg="white", cursor='hand2', activebackground='white',
                             width=90, image=self.photobtn5, fg="white", compound="center")
        resetTc_btn.place(x=299, y=7)

        # bảng dữ liệu Phòng
        tablestd_frame = Frame(Underright_frame, bd=2, relief=RIDGE, bg="white")
        tablestd_frame.place(x=700, y=35, width=550, height=350)

        # scroll bar
        scroll_x = ttk.Scrollbar(tablestd_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(tablestd_frame, orient=VERTICAL)

        self.StudentTable = ttk.Treeview(tablestd_frame, column=(
            "class", "name"),
                                         xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.StudentTable.xview)
        scroll_y.config(command=self.StudentTable.yview)

        self.StudentTable.heading("class", text="Phòng")
        self.StudentTable.heading("name", text="Tên")

        self.StudentTable["show"] = "headings"
        self.StudentTable.column("class", width=80)
        self.StudentTable.column("name", width=80)

        self.StudentTable.pack(fill=BOTH, expand=1)
        self.StudentTable.bind("<ButtonRelease>", self.get_cursorClass)
        self.fetch_Classdata()

    # ============function decration===============
    def student_image(self):  # Xem ảnh của Người dùng
        if self.var_std_name.get() == "" or self.var_std_id.get() == "":  # Nếu txt tên hs hoặc id Người dùng trống thì báo lỗi
            messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin", parent=self.root)
        else:
            student_id(self.var_std_id.get())  # truyền id Người dùng vào form thông tin ảnh
            self.new_window = Toplevel(self.root)  # cửa sổ mới
            self.app = StdImage(self.new_window)  # Hiện thị giao diện xem ảnh

    def getNextid(self):  # Lấy ra id tiếp theo
        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                       database=self.db.database, port=self.db.port)
        my_cursor = conn.cursor()
        my_cursor.execute(
            "SELECT  Student_id from student ORDER BY Student_id DESC limit 1")  # câu lệnh truy vấn ra id tiếp theo(Vd: id cuối trong bảng là 5-> id tiếp theo=6)
        lastid = my_cursor.fetchone()
        if (lastid == None):
            self.var_std_id.set("1")  # Nếu ko có dữ liệu -> id tiếp theo=1
        else:  # Nếu có id tiếp theo bằng id cũ +1
            nextid = int(lastid[0]) + 1
            self.var_std_id.set(str(nextid))

        conn.commit()
        conn.close()
        # return  self.var_id

    def add_data(self):  # Thêm dữ liệu
        # ========check class================
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  # để Check xem email nhập vào có đúng định dạng email ko

        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                       database=self.db.database, port=self.db.port)

        my_cursor = conn.cursor()
        my_cursor.execute("select Class from `class` ")
        ckclass = my_cursor.fetchall()
        arrayClass = []
        for chc in ckclass:
            # print(chc[0])
            arrayClass.append(str(chc[0]))
        if self.var_std_name.get() == "" or self.var_std_id.get() == "" or self.var_div.get() == "":
            messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin", parent=self.root)
        elif (self.var_div.get() not in arrayClass):  # Lớp ko tồn tại thì thông báo
            messagebox.showerror("Error", "Tên Phòng không tồn tại ! Vui lòng kiểm tra lại", parent=self.root)
        elif (re.search(regex, self.var_email.get()) == None):  # check email nhập vào đúng định dạng
            messagebox.showerror("Error", "Vui lòng nhập email đúng định dạng", parent=self.root)
        elif (self.var_phone.get().isnumeric() != True):  # SDT nhạp vào đúng dạng số ko
            messagebox.showerror("Error", "Vui lòng nhập số điện thoại đúng", parent=self.root)
        elif (self.var_roll.get().isnumeric() != True):  # CMND đúng dạng số ko
            messagebox.showerror("Error", "Vui lòng nhập số CMND đúng", parent=self.root)
        else:  # Thêm thông tin Người dùng
            try:
                conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                               database=self.db.database, port=self.db.port)

                my_cursor = conn.cursor()
                my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                    self.var_std_id.get(),

                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_std_name.get(),
                    self.var_div.get(),
                    self.var_roll.get(),
                    self.var_gender.get(),
                    # self.var_dob.get(),
                    self.dob_entry.get_date().strftime('%d/%m/%Y'),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_radio1.get()
                ))
                # print(conn)
                conn.commit()  # xác thực câu lệnh
                self.fetch_data()  # In dữ liệu mới lên bảng sau khi thêm
                self.reset_data()  # reset lại các txtbox để nhập dữ liệu mới
                conn.close()  # Đóng kết nối DataBase
                messagebox.showinfo("Thành công", "Thêm thông tin Người dùng thành công",
                                    parent=self.root)  # thêm thành công
            except Exception as es:  # Nếu có lỗi -> in ra màn hình
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    # =======================fetch-data========================
    def fetch_data(self):  # Lấy tất cả thông tin Người dùng
        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                       database=self.db.database, port=self.db.port)

        my_cursor = conn.cursor()
        # câu lệnh sql truy vấn tất cả thông tin Người dùng
        my_cursor.execute(
            "Select student_id,year,semester,name,class,roll,gender,dob,email,phone,address,photosample from student")
        data = my_cursor.fetchall()

        if len(data) != 0:  # Nếu có dữ liệu hoc sinh thì hiện thị lên bảng
            self.student_table.delete(*self.student_table.get_children())  # Xóa những dữ liệu cũ ở bảng
            for i in data:  # Thêm tất cả thông tin vừa truy vấn đc lên bảng
                self.student_table.insert("", END, values=i)
            conn.commit()
        conn.close()

    # ======================get-cursor==============================
    def get_cursor(self, event=""):  # Sự kiện khi click vào bảng thì hiện chi tiết thông tin ra các txtbox
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]
        self.var_std_id.set(data[0]),
        # self.var_dep.set(data[1]),
        # self.var_course.set(data[2]),
        self.var_year.set(data[1]),
        self.var_semester.set(data[2]),
        self.var_std_name.set(data[3]),
        self.var_div.set(data[4]),
        self.var_roll.set(data[5]),
        self.var_gender.set(data[6]),
        self.dob_entry.set_date(data[7]),
        self.var_email.set(data[8]),
        self.var_phone.set(data[9]),
        self.var_address.set(data[10]),
        self.var_radio1.set(data[11]),

    def update_data(self):  # Cập nhật thông tin Người dùng
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  # check email
        if self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin", parent=self.root)
        elif (re.search(regex, self.var_email.get()) == None):
            messagebox.showerror("Error", "Vui lòng nhập email đúng định dạng", parent=self.root)
        elif (self.var_phone.get().isnumeric() != True):
            messagebox.showerror("Error", "Vui lòng nhập số điện thoại đúng", parent=self.root)
        elif (self.var_roll.get().isnumeric() != True):
            messagebox.showerror("Error", "Vui lòng nhập số CMND đúng", parent=self.root)
        else:
            try:
                # Hỏi trước khi cập nhật
                Update = messagebox.askyesno("Update", "Bạn có muốn cập nhật thông tin Người dùng này không?",
                                             parent=self.root)
                if Update > 0:  # nếu bấm yes
                    conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                                   database=self.db.database, port=self.db.port)
                    my_cursor = conn.cursor()
                    # câu lệnh sql update các thong tin Người dùng
                    my_cursor.execute("update student set Year=%s,Semester=%s,Name=%s,Class=%s,"
                                      "Roll=%s,Gender=%s,Dob=%s,Email=%s,Phone=%s,Address=%s,PhotoSample=%s where Student_id=%s",
                                      (

                                          self.var_year.get(),
                                          self.var_semester.get(),
                                          self.var_std_name.get(),
                                          self.var_div.get(),
                                          self.var_roll.get(),
                                          self.var_gender.get(),
                                          self.dob_entry.get_date().strftime('%d/%m/%Y'),
                                          self.var_email.get(),
                                          self.var_phone.get(),
                                          self.var_address.get(),
                                          self.var_radio1.get(),
                                          self.var_std_id.get()
                                      ))
                else:
                    if not Update:  # Nếu bấm no trở lại
                        return
                messagebox.showinfo("Thành công", "Cập nhật thông tin Người dùng thành công", parent=self.root)
                conn.commit()  # xác thực câu lệnh
                self.fetch_data()  # Hiện thị dữ liệu sau update
                self.reset_data()  # Lám mới các txtbox
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)

    # Delete Function
    def delete_data(self):  # Xóa thông tin Người dùng theo mã id
        if self.var_std_id.get() == "":
            messagebox.showerror("Lỗi", "Không được bỏ trống ID Người dùng", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Xoá Người dùng", "Bạn có muốn xóa Người dùng này?", parent=self.root)
                if delete > 0:
                    conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                                   database=self.db.database, port=self.db.port)
                    my_cursor = conn.cursor()
                    sql = "delete from student where Student_id=%s"  # Câu lệnh xóa Người dùng theo id Người dùng
                    val = (self.var_std_id.get(),)
                    my_cursor.execute(sql, val)
                else:
                    if not delete:
                        return
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                messagebox.showinfo("Xóa", "Xóa Người dùng thành công", parent=self.root)
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)

    # ===================Reset function====================
    def reset_data(self):  # Hàm rest cấc thong tin  txtbox
        # self.var_dep.set("Chọn chuyên ngành"),
        # self.var_course.set("Chọn hệ"),
        self.var_year.set("Chọn khóa học"),
        self.var_semester.set("Chọn cơ sở"),
        self.var_std_id.set(""),
        self.var_std_name.set(""),
        self.var_div.set(""),
        self.var_roll.set(""),
        self.var_gender.set("Nam"),
        self.dob_entry.set_date(strftime("%d/%m/%Y")),
        self.var_email.set(""),
        self.var_phone.set(""),
        self.var_address.set(""),

        self.var_radio1.set(""),
        self.getNextid()

    def search_data(self):  # Hàm tìm kiếm
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  # check email
        if self.var_com_search.get() == "" or self.var_search.get() == "":
            messagebox.showerror("Lỗi !", "Vui lòng nhập thông tin đầy đủ", parent=self.root)

        else:
            try:
                conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                               database=self.db.database, port=self.db.port)
                my_cursor = conn.cursor()  # "ID Điểm Danh", "Ngày", "ID Người dùng"
                # convert loại tìm kiếm về tên các côt trọng mysql
                if (self.var_com_search.get() == "ID Người dùng"):
                    self.var_com_search.set("Student_id")
                elif (self.var_com_search.get() == "Tên Người dùng"):
                    self.var_com_search.set("Name")
                elif (self.var_com_search.get() == "Lớp biên chế"):
                    self.var_com_search.set("Class")
                # câu lệnh tìm kiếm
                my_cursor.execute("select * from student where " + str(
                    self.var_com_search.get()) + " Like '%" + str(self.var_search.get()) + "%'")
                data = my_cursor.fetchall()
                if (len(data) != 0):  # Nếu có dữ liệu thì in lên bảng
                    self.student_table.delete(*self.student_table.get_children())
                    for i in data:
                        self.student_table.insert("", END, values=i)
                    # thông báo có bao nhiêu dữ liệu tìm kiếm đc
                    messagebox.showinfo("Thông báo", "Có " + str(len(data)) + " bản ghi thỏa mãn điều kiện",
                                        parent=self.root)
                    conn.commit()
                else:  # nếu ko có dữ liệu thông báo ko có bản ghi
                    self.student_table.delete(*self.student_table.get_children())
                    messagebox.showinfo("Thông báo", " Không có bản ghi nào thỏa mãn điều kiện", parent=self.root)
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)

    # =============generate dataset and take photo=================
    def generate_dataset(self):  # Chụp ảnh Người dùng
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  # check email
        if self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin", parent=self.root)
        elif (re.search(regex, self.var_email.get()) == None):
            messagebox.showerror("Error", "Vui lòng nhập email đúng định dạng", parent=self.root)
        elif (self.var_phone.get().isnumeric() != True):
            messagebox.showerror("Error", "Vui lòng nhập số điện thoại đúng", parent=self.root)
        elif (self.var_roll.get().isnumeric() != True):
            messagebox.showerror("Error", "Vui lòng nhập số CMND đúng", parent=self.root)
        else:
            try:  # update thông tin Người dùng
                conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                               database=self.db.database, port=self.db.port)

                my_cursor = conn.cursor()
                # my_cursor.execute("select * from student")
                # myresult=my_cursor.fetchall()
                id = self.var_std_id.get()
                # for x in myresult:
                #     id+=1
                my_cursor.execute("update student set Year=%s,Semester=%s,Name=%s,Class=%s,"
                                  "Roll=%s,Gender=%s,Dob=%s,Email=%s,Phone=%s,Address=%s,PhotoSample=%s where Student_id=%s",
                                  (

                                      self.var_year.get(),
                                      self.var_semester.get(),
                                      self.var_std_name.get(),
                                      self.var_div.get(),
                                      self.var_roll.get(),
                                      self.var_gender.get(),
                                      self.dob_entry.get_date().strftime('%d/%m/%Y'),
                                      self.var_email.get(),
                                      self.var_phone.get(),
                                      self.var_address.get(),
                                      self.var_radio1.get(),
                                      self.var_std_id.get()
                                  ))
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                # =========load haar===================
                face_classifier = cv2.CascadeClassifier(
                    "haarcascade_frontalface_default.xml")  # Model phát hiện khuôn mặt trong màn hình

                def face_cropped(img):  # Cắt khuôn mặt đã phát hiện theo hình ô vuông
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # chuyển ảnh về dạng gray để phát hiện khuôn mặt
                    faces = face_classifier.detectMultiScale(gray, 1.3, 5)  # tỉ lệ của thuật toán phát hiện khuôn mặt
                    # scaling factor 1.3
                    ##minimum neighbor 5
                    for (x, y, w, h) in faces:  # với mỗi khuôn mặt phát hiện trên khung hình, cắt khuôn mặt ra
                        face_cropped = img[y:y + h, x:x + w]

                        return face_cropped

                cap = cv2.VideoCapture(0)  # Mở camera webcam(=0) bằng thư viện xử lý ảnh opencv
                img_id = 0  # Số ảnh chụp
                while True:  # Nếu ko có lỗi mở cam
                    net, my_frame = cap.read()
                    if face_cropped(my_frame) is not None:
                        img_id += 1  # với mỗi ảnh chụp đc tăng số ảnh lên 1
                        # face=cv2.resize(face_cropped(my_frame),(190,190))
                        face = cv2.cvtColor(face_cropped(my_frame), cv2.COLOR_BGR2GRAY)
                        fill_name_path = "data/user." + str(id) + "." + str(img_id) + ".jpg"  # tên ảnh lưu vào thư mục

                        cv2.imwrite(fill_name_path, face)  # Lưu ảnh khuôn mặt vào folder data
                        cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0),
                                    2)  # in số ảnh đã chụp lên giao diện cam
                        cv2.imshow("Cropped Face", face)  # Hiện thị các ảnh đã cắt

                    if cv2.waitKey(1) == 13 or int(img_id) == 120:  # Nếu số ảnh đã chụp =120 thì dừng lại
                        break
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Kết quả", "Tạo dữ liệu khuôn mặt thành công", parent=self.root)
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)

    # ==========================TrainDataSet=======================
    def train_classifier(self):  # Hàm train model nhận diện
        data_dir = ("data")  # Thư mục chứa các ảnh chụp sinh viên
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

        faces = []
        ids = []
        for image in path:  # với từng ảnh trong thư mục
            img = PIL.Image.open(image).convert('L')  # convert ảnh về dạng pil
            imageNp = np.array(img, 'uint8')
            id = int(os.path.split(image)[1].split('.')[
                         1])  # Lấy ra id Người dùng từ tên của ảnh( ví dụ: user.1.19.jpg -> id Người dùng=1)
            faces.append(imageNp)  # truyền các ảnh vào mảng
            ids.append(id)  # truyền các id vào mảng
            cv2.imshow("Training", imageNp)  # In ra các ảnh đã chụp
            cv2.waitKey(1) == 13
        ids = np.array(ids)  # convert dạng mảng

        # =================Train data classifier and save============
        clf = cv2.face.LBPHFaceRecognizer_create()  # Tạo model
        clf.train(faces, ids)  # Tiến hành train model
        clf.write("classifier.xml")  # Lưu model đã train đc ra file classifier.xml
        cv2.destroyAllWindows()  # Hủy các cửa sổ opencv
        messagebox.showinfo("Kết quả", "Training dataset Completed", parent=self.root)  # thông báo train thành công

    # ========================================Function Student======================================

    def get_cursorClass(self, event=""):  # sự kiện ckick vào bảng Phòng
        cursor_row = self.StudentTable.focus()
        content = self.StudentTable.item(cursor_row)
        rows = content['values']
        self.var_class.set(rows[0])
        self.var_nameclass.set(rows[1])

    def add_Classdata(self):  # Thêm Phòng
        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                       database=self.db.database, port=self.db.port)
        my_cursor = conn.cursor()

        # =========check class=================
        my_cursor.execute("select Class from `class` ")  # Danh sách lớp
        ckClass = my_cursor.fetchall()
        arrayClass = []
        for chs in ckClass:
            # print(chs[0])
            arrayClass.append(str(chs[0]))
        conn.commit()
        conn.close()
        if self.var_class.get() == "" or self.var_nameclass.get() == "":
            messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin", parent=self.root)

        elif (self.var_class.get() in arrayClass):  # Kiểm tra xem lớp nhập vào đã tồn tại chưa
            messagebox.showerror("Error", "Class đã tồn tại! Vui lòng kiểm tra lại", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                               database=self.db.database, port=self.db.port)
                my_cursor = conn.cursor()
                my_cursor.execute("insert into class values(%s,%s)", (
                    self.var_class.get(),
                    self.var_nameclass.get(),
                ))
                conn.commit()
                self.fetch_Classdata()
                self.reset_Classdata()
                conn.close()
                messagebox.showinfo("Thành công", "Thêm thông tin Phòng thành công",
                                    parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def reset_Classdata(self):  # làm mới
        self.var_class.set("")
        self.var_nameclass.set("")

    def fetch_Classdata(self):  # Hiện thị các Phòng
        # global mydata
        # mydata.clear()
        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                       database=self.db.database, port=self.db.port)
        my_cursor = conn.cursor()
        my_cursor.execute("Select * from class")  # Lấy tất cả thông tin trong class
        data = my_cursor.fetchall()  # truyền dữ liệu vừa lấy đc vào biến data
        if len(data) != 0:  # nếu có dữ liệu thì in lên bảng
            self.StudentTable.delete(*self.StudentTable.get_children())
            for i in data:
                self.StudentTable.insert("", END, values=i)
                mydata.append(i)
            conn.commit()
        conn.close()

    def update_Classdata(self):  # Cập nhật thông tin Phòng
        if self.var_class == "" or self.var_nameclass.get() == "":
            messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin", parent=self.root)

        else:
            try:
                Update = messagebox.askyesno("Update", "Bạn có muốn cập nhật bản ghi này không?", parent=self.root)
                if Update > 0:
                    conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                                   database=self.db.database, port=self.db.port)
                    my_cursor = conn.cursor()
                    # Câu lệnh cập nhật Phòng
                    my_cursor.execute("UPDATE `class` SET Name = %s  WHERE "
                                      "`Class` = %s",
                                      (
                                          self.var_nameclass.get(),
                                          self.var_class.get(),
                                      ))
                else:
                    if not Update:
                        return
                messagebox.showinfo("Thành công", "Cập nhật thông tin Phòng thành công",
                                    parent=self.root)
                conn.commit()
                self.reset_Classdata()
                self.fetch_Classdata()
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)

        # Delete Function

    def delete_Classdata(self):  # Xóa Phòng
        if self.var_class == "" or self.var_nameclass.get() == "":
            messagebox.showerror("Lỗi", "Không được bỏ trống thông tin! ", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Xoá bản ghi", "Bạn có muốn xóa bản ghi này ?", parent=self.root)
                if delete > 0:
                    conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                                   database=self.db.database, port=self.db.port)
                    my_cursor = conn.cursor()
                    sql = "delete from class where Class=%s "  # Xóa Phòng với class=
                    val = (self.var_class.get(),)
                    my_cursor.execute(sql, val)
                else:
                    if not delete:
                        return
                conn.commit()
                # self.fetch_data()p
                conn.close()
                messagebox.showinfo("Xóa", "Xóa bản ghi thành công", parent=self.root)
                self.reset_Classdata()
                self.fetch_Classdata()
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)

    def search_Classdata(self):  # Tìm thông tin Phòng
        if self.var_com_searchclass.get() == "" or self.var_searchclass.get() == "":
            messagebox.showerror("Lỗi !", "Vui lòng nhập thông tin đầy đủ", parent=self.root)

        else:
            try:
                conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                               database=self.db.database, port=self.db.port)
                my_cursor = conn.cursor()  # "ID Điểm Danh", "Ngày", "ID Người dùng"
                if (self.var_com_searchclass.get() == "Lớp"):
                    self.var_com_searchclass.set("Class")
                elif (self.var_com_searchclass.get() == "Tên lớp"):
                    self.var_com_searchclass.set("Name")

                my_cursor.execute("select * from class where " + str(
                    self.var_com_searchclass.get()) + " Like '%" + str(self.var_searchclass.get()) + "%'")
                data = my_cursor.fetchall()
                if (len(data) != 0):
                    self.StudentTable.delete(*self.StudentTable.get_children())
                    for i in data:
                        self.StudentTable.insert("", END, values=i)
                    messagebox.showinfo("Thông báo", "Có " + str(len(data)) + " bản ghi thỏa mãn điều kiện",
                                        parent=self.root)
                    conn.commit()
                else:
                    self.StudentTable.delete(*self.StudentTable.get_children())
                    messagebox.showinfo("Thông báo", " Không có bản ghi nào thỏa mãn điều kiện", parent=self.root)
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()  # khoi tao cua so va gan root vao

    obj = Student(root)
    root.mainloop()  # cua so hien len
