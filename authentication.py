import cv2
from mtcnn import MTCNN
import numpy as np
from datetime import datetime
import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import threading

class Database_str:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'face_recognizer'
        self.port = '3306'

class FaceRecognition:
    def __init__(self, root, db_params):
        self.root = root
        self.db = db_params

        self.root.geometry("1000x700+200+50")
        self.root.title("Face Recognition System")

        self.panel = Label(self.root)
        self.panel.pack(pady=10)

        btn = Button(self.root, text="Start", command=self.start_recognition)
        btn.pack(pady=10)

    def mark_attendance(self, student_id, student_name, face_cropped):
        now = datetime.now()
        d1 = now.strftime("%d/%m/%Y")
        dtString = now.strftime("%H:%M:%S")

        ma = "SV" + str(student_id) + d1
        masp = ma.replace("/", "")

        conn = mysql.connector.connect(host=self.db.host, user=self.db.user, password=self.db.password,
                                       database=self.db.database, port=self.db.port)
        my_cursor = conn.cursor()

        try:
            my_cursor.execute("INSERT INTO attendance VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                              (masp, student_id, student_name, None, dtString, None, d1, None, ""))
            conn.commit()
            cv2.imwrite("DiemDanhImage\ " + masp + ".jpg", face_cropped)
            self.show_attendance_info(masp, student_id, student_name, dtString)
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

        conn.close()

    def start_recognition(self):
        self.isClicked = False
        self.detector = MTCNN()

        threading.Thread(target=self.face_recog).start()

    def face_recog(self):
        self.isClicked = True

        cap = cv2.VideoCapture(0)
        cap.set(3, 800)
        cap.set(4, 580)
        cap.set(10, 150)

        while self.isClicked:
            ret, frame = cap.read()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.detector.detect_faces(frame_rgb)

            if results:
                for result in results:
                    x, y, w, h = result['box']
                    confidence = result['confidence']

                    if confidence > 0.85:
                        face_cropped = frame_rgb[y:y+h, x:x+w]
                        face_cropped = cv2.cvtColor(face_cropped, cv2.COLOR_RGB2BGR)
                        face_cropped = cv2.resize(face_cropped, (190, 190))

                        student_id = 1  # Assume student_id is known
                        student_name = "Test"  # Assume student_name is known

                        self.mark_attendance(student_id, student_name, face_cropped)

            frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
            cv2.imshow('Face Recognition', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = Tk()
    db_params = Database_str()
    obj = FaceRecognition(root, db_params)
    root.mainloop()
