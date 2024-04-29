import tkinter as tk
from tkinter import Label, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import os
import dlib
import mysql.connector
from datetime import datetime

class Database_str:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''  # Thay đổi thành mật khẩu của bạn nếu có
        self.database = 'face_recognizer'
        self.port = '3306'

class FaceCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HỆ THỐNG ĐẾM SỐ LƯỢNG NGƯỜI TỪ ẢNH")
        self.root.geometry("1350x700")
        self.root.resizable(False, False)

        # Load the background image and resize it
        img3 = Image.open(r"ImageFaceDetect\bgnt4.jpg")
        img3 = img3.resize((1350, 700), Image.BILINEAR)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        # Create a label to hold the background image
        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=0, width=1350, height=700)

        self.db = Database_str()

        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Create a label to hold the background image
        background_label = tk.Label(main_frame, image=self.photoimg3)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        title_label = tk.Label(main_frame, text="HỆ THỐNG ĐẾM SỐ LƯỢNG NGƯỜI TỪ ẢNH", font=("Arial", 30, "bold"))
        title_label.pack(pady=20)

        input_frame = tk.Frame(main_frame, bg="#36ADF1")  # Change background color
        input_frame.pack(side="left", padx=40, pady=10)

        self.input_label = tk.Label(input_frame, text="Ảnh đầu vào", font=("Arial", 20), bg="#36ADF1")
        self.input_label.pack(pady=(10, 5))

        input_canvas_frame = tk.Frame(input_frame, bg="#36ADF1")  # Change background color
        input_canvas_frame.pack(padx=10, pady=10)

        self.input_canvas = tk.Canvas(input_canvas_frame, width=400, height=300, bg="white",
                                      highlightthickness=0)  # Change background color
        self.input_canvas.pack()

        processed_frame = tk.Frame(main_frame, bg="#36ADF1")  # Change background color
        processed_frame.pack(side="right", padx=40, pady=10)

        self.processed_label = tk.Label(processed_frame, text="Ảnh sau khi xử lý", font=("Arial", 20), bg="#36ADF1")
        self.processed_label.pack(pady=(10, 5))

        processed_canvas_frame = tk.Frame(processed_frame, bg="#36ADF1")  # Change background color
        processed_canvas_frame.pack(padx=10, pady=10)

        self.processed_canvas = tk.Canvas(processed_canvas_frame, width=400, height=300, bg="white",
                                          highlightthickness=0)  # Change background color
        self.processed_canvas.pack()

        self.count_label = tk.Label(processed_frame, text="", font=("Arial", 18), bg="#36ADF1", fg="black")
        self.count_label.pack(pady=10)

        button_frame = tk.Frame(main_frame)
        button_frame.pack(side="bottom", padx=0, pady=20)

        self.select_img = ImageTk.PhotoImage(Image.open(r"ImageFaceDetect\themanh.jpg"))
        self.select_button = tk.Button(button_frame, image=self.select_img, command=self.select_image)
        self.select_button.pack(side="left", padx=15)

        self.count_img = ImageTk.PhotoImage(Image.open(r"ImageFaceDetect\xuly.jpg"))
        self.count_button = tk.Button(button_frame, image=self.count_img, command=self.count_faces)
        self.count_button.pack(side="left", padx=0)

    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if hasattr(self, 'image_path'):
            self.image = cv2.imread(self.image_path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.image = cv2.resize(self.image, (400, 300))
            self.display_input_image()

    def display_input_image(self):
        self.input_photo = ImageTk.PhotoImage(Image.fromarray(self.image))
        self.input_canvas.create_image(200, 150, anchor=tk.CENTER, image=self.input_photo)

    def count_faces(self):
        if hasattr(self, 'image_path'):
            num_faces, processed_image = self.count_faces_in_image(self.image_path)
            self.display_processed_image(processed_image, num_faces)
            self.count_label.config(text=f"Số lượng người: {num_faces}")
            self.insert_face_count(self.image_path, num_faces)
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn ảnh trước.")

    def count_faces_in_image(self, image_path):
        detector = dlib.get_frontal_face_detector()
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 0)

        return len(faces), image

    def display_processed_image(self, processed_image, num_faces):
        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
        processed_image = cv2.resize(processed_image, (400, 300))
        self.processed_photo = ImageTk.PhotoImage(Image.fromarray(processed_image))
        self.processed_canvas.create_image(200, 150, anchor=tk.CENTER, image=self.processed_photo)

    def insert_face_count(self, image_name, count):
        try:
            conn = mysql.connector.connect(
                host=self.db.host,
                user=self.db.user,
                password=self.db.password,
                database=self.db.database,
                port=self.db.port
            )
            cursor = conn.cursor()
            timestamp = datetime.now()

            # Save the image to the img_face_count directory
            save_dir = 'img_face_count'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            save_path = os.path.join(save_dir, os.path.basename(image_name))
            cv2.imwrite(save_path, cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR))

            # Insert the record into the database
            cursor.execute("INSERT INTO face_count (image_name, timestamp, count) VALUES (%s, %s, %s)",
                           (save_path, timestamp, count))
            conn.commit()
            messagebox.showinfo("Success", "Đã đếm thành công.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Lỗi: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceCounterApp(root)
    root.mainloop()
