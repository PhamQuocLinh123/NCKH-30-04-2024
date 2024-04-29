from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch
import tkinter as tk
from PIL import Image, ImageTk
import threading

# Khởi tạo camera
video = cv2.VideoCapture(0)
# Load model KNN
with open('dataset/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)
with open('dataset/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

# Load pre-trained face detection classifier
facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Khởi tạo biến chứa hình nền
imgBackground = cv2.imread("nen.jpg")

# Tên cột trong file CSV
COL_NAMES = ['NAME', 'TIME']


# Hàm nói
def speak(str1):
    speak = Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)


# Hàm tính khoảng cách Euclidean giữa hai điểm
def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))


# Hàm lưu dữ liệu
def save_data(faces):
    ts = time.time()
    date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
    timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
    exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")

    # Biến để lưu trữ tên được nhận dạng
    recognized_name = None

    for (x, y, w, h) in faces:
        crop_img = frame[y:y + h, x:x + w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)

        # Dự đoán nhãn và độ tin cậy từ khu vực khuôn mặt
        output = knn.predict(resized_img)

        # Tính toán khoảng cách Euclidean đến các điểm láng giềng
        distances, indices = knn.kneighbors(resized_img)

        # Chỉ xem xét nhãn là "Unknown" nếu khoảng cách lớn hơn ngưỡng độ chính xác tối thiểu
        min_distance = np.min(distances)
        if min_distance <= 50:  # Có thể điều chỉnh ngưỡng này
            output = ['Unknown']
        else:
            # Lưu trữ tên của người được nhận dạng
            recognized_name = output[0]

        attendance = [str(output[0]), str(timestamp)]
        if exist:
            speak("Attendance Taken..")
            time.sleep(5)
            with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(attendance)
        else:
            speak("Attendance Taken..")
            time.sleep(5)
            with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)

    # Trả về tên được nhận dạng (hoặc "Unknown" nếu không có tên được nhận dạng)
    return recognized_name


# Hàm xử lý sự kiện khi nhấn button Thoát
def exit_program():
    video.release()
    cv2.destroyAllWindows()
    root.destroy()


# Hàm lưu dữ liệu (thread)
def save_data_thread():
    faces = facedetect.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 1.3, 5)
    recognized_name = save_data(faces)
    if recognized_name is not None:
        # Nếu có tên được nhận dạng, hiển thị tên
        print("Recognized name:", recognized_name)
    else:
        # Nếu không có tên được nhận dạng, hiển thị "Unknown"
        print("Unknown")


# Tạo cửa sổ tkinter
root = tk.Tk()
root.title("Attendance System")

# Tạo button để lưu dữ liệu
button_save = tk.Button(root, text="Save Data", command=save_data_thread)
button_save.pack(side=tk.LEFT, padx=10, pady=10)

# Tạo button để thoát chương trình
button_exit = tk.Button(root, text="Exit", command=exit_program)
button_exit.pack(side=tk.RIGHT, padx=10, pady=10)

# Tạo cửa sổ hiển thị video
video_frame = tk.Label(root)
video_frame.pack(padx=10, pady=10)


def update_frame():
    global frame
    ret, frame = video.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
            cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)

            crop_img = frame[y:y + h, x:x + w, :]
            resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
            output = knn.predict(resized_img)

            cv2.putText(frame, str(output[0]), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame)
        frame_pil = frame_pil.resize((640, 480), Image.BILINEAR)

        # Convert frame_pil back to BGR array before assigning to imgBackground
        frame_bgr = np.array(frame_pil)
        imgBackground[162:162 + 480, 55:55 + 640] = cv2.cvtColor(frame_bgr, cv2.COLOR_RGB2BGR)

        # Convert imgBackground back to RGB before creating the Tkinter PhotoImage
        imgBackground_rgb = cv2.cvtColor(imgBackground, cv2.COLOR_BGR2RGB)
        imgBackground_tk = ImageTk.PhotoImage(image=Image.fromarray(imgBackground_rgb))

        # Update video_frame
        video_frame.img = imgBackground_tk
        video_frame.config(image=imgBackground_tk)

    root.after(10, update_frame)


update_frame()
root.mainloop()
