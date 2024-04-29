import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
import pandas as pd
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
def fetch_data():
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Change password if needed
        database="face_recognizer"
    )

    # Create a cursor to execute the query
    mycursor = mydb.cursor()

    # Execute query to fetch data from the 'face_count_camera' table
    query = f"SELECT * FROM face_count_camera LIMIT 25 OFFSET {(page_number - 1) * 25}"
    mycursor.execute(query)
    rows = mycursor.fetchall()

    # Clear table before inserting new data
    table.delete(*table.get_children())

    # Insert fetched data into the table
    for row in rows:
        table.insert("", "end", values=row)

def search_data():
    keyword = search_entry.get()
    if not keyword:
        messagebox.showerror("Error", "Please enter a keyword to search.")
        return

    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Change password if needed
        database="face_recognizer"
    )

    # Create a cursor to execute the query
    mycursor = mydb.cursor()

    # Execute query to fetch data from the 'face_count_camera' table
    query = f"SELECT * FROM face_count_camera WHERE ID LIKE '%{keyword}%' OR Timestamp LIKE '%{keyword}%' OR Count LIKE '%{keyword}%' OR Image_Path LIKE '%{keyword}%' LIMIT 20"
    mycursor.execute(query)
    rows = mycursor.fetchall()

    # Clear table before inserting new data
    table.delete(*table.get_children())

    # Insert fetched data into the table
    for row in rows:
        table.insert("", "end", values=row)

def export_to_excel():
    # Ask user to select location to save the file
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")

    if file_path:
        try:
            # Get data from table
            data = [table.item(item)["values"] for item in table.get_children()]

            # Create DataFrame from data
            df = pd.DataFrame(data, columns=["ID", "Timestamp", "Count", "Image Path"])

            # Export DataFrame to Excel
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Export Successful", "Data has been exported to Excel successfully.")
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred: {str(e)}")


def export_to_pdf():
    # Ask user to select location to save the file
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf")

    if file_path:
        try:
            # Create a PDF document
            c = canvas.Canvas(file_path, pagesize=letter)

            # Add images to canvas
            row_height = 20
            for i, item in enumerate(table.get_children()):
                image_path = table.set(item, "Image Path")
                if image_path:
                    try:
                        img = Image.open(image_path)
                        img.thumbnail((100, 100))
                        img_io = BytesIO()
                        img.save(img_io, format='JPEG')
                        img_io.seek(0)
                        c.drawImage(img_io, 400, 600 - (i + 2) * row_height, width=100, height=100, preserveAspectRatio=True)
                    except Exception as e:
                        print(f"Error loading image: {e}")

            # Set up table data
            data = [["Mã", "Thoi Gían", "So Luong Nguoi", "Duong Dan Anh"]]  # Add column headers
            for item in table.get_children():
                row_data = []
                for column in table["columns"]:
                    cell_value = table.set(item, column)
                    row_data.append(cell_value)
                data.append(row_data)

            # Set up table style
            style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)])

            # Create a table object
            t = Table(data)

            # Apply table style
            t.setStyle(style)

            # Add table to canvas
            table_width = 700
            table_height = 20 * len(data) + 50
            t.wrapOn(c, table_width, table_height)
            t.drawOn(c, 72, 500 - len(data) * row_height)

            # Save the PDF
            c.save()

            messagebox.showinfo("Export Successful", "Data has been exported to PDF successfully.")
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred: {str(e)}")
def delete_selected():
    # Get selected items from the table
    selected_items = table.selection()
    if not selected_items:
        messagebox.showerror("Error", "Please select rows to delete.")
        return

    # Ask for confirmation
    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected rows?")
    if confirm:
        for item in selected_items:
            # Get the ID of the selected item
            item_id = table.item(item, "values")[0]

            # Connect to MySQL database
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Change password if needed
                database="face_recognizer"
            )

            # Create a cursor to execute the delete query
            mycursor = mydb.cursor()

            # Execute the delete query
            query = f"DELETE FROM face_count_camera WHERE ID = {item_id}"
            mycursor.execute(query)
            mydb.commit()

        # Refresh the data in the table
        fetch_data()
        messagebox.showinfo("Delete Successful", "Selected rows have been deleted.")

def show_image(event):
    # Get the selected item from the table
    selected_item = table.selection()
    if not selected_item:
        return

    # Get the image path from the selected item
    image_path = table.item(selected_item, "values")[3]  # Index 3 corresponds to the "Image Path" column

    # Load and display the image
    if image_path:
        try:
            img = Image.open(image_path)
            img.thumbnail((400, 400))  # Resize the image to fit within a 400x400 window
            img = ImageTk.PhotoImage(img)
            image_label.config(image=img)
            image_label.image = img
            image_label.configure(borderwidth=3, relief="solid")  # Add border to the image label
            image_label.pack(pady=10, padx=10)  # Add padding around the image label
        except Exception as e:
            print(f"Error loading image: {e}")


# Create Tkinter GUI
root = tk.Tk()
root.title("Data from Database")

# Set window size and position
root.geometry("1366x720+0+0")

# Không cho phép thay đổi kích thước cửa sổ
root.resizable(False, False)

# Set background color
root.configure(background="#F0F0F0")

# Create a frame for the table
frame = tk.Frame(root, bg="#F0F0F0")
frame.pack(pady=20, padx=10, fill='both', expand=True)

# Create a search frame
search_frame = tk.Frame(root, bg="#F0F0F0")
search_frame.pack(fill="x", padx=10, pady=(0, 10))
export_pdf_button = tk.Button(search_frame, text="Export to PDF", command=export_to_pdf, bg="#B3CCFF", fg="black")
export_pdf_button.pack(side="right", padx=5, pady=5)


# Create a search entry and button
search_entry = tk.Entry(search_frame, width=50)
search_entry.pack(side="left", padx=5, pady=5, ipady=4)

search_button = tk.Button(search_frame, text="Search", command=search_data, bg="#B3CCFF", fg="black")
search_button.pack(side="left", padx=5)

# Create a button to export data to Excel
export_button = tk.Button(search_frame, text="Export to Excel", command=export_to_excel, bg="#B3CCFF", fg="black")
export_button.pack(side="right", padx=5, pady=5)

# Create a button to delete selected data
delete_button = tk.Button(search_frame, text="Delete Selected", command=delete_selected, bg="#B3CCFF", fg="black")
delete_button.pack(side="right", padx=5, pady=5)

# Create a table to display data
table = ttk.Treeview(frame, columns=("ID", "Timestamp", "Count", "Image Path"), show="headings", selectmode="extended")
# Define column headings
table.heading("ID", text="ID")
table.heading("Timestamp", text="Timestamp")
table.heading("Count", text="Count")
table.heading("Image Path", text="Image Path")

# Fetch and display data from database
page_number = 1
fetch_data()

# Style the Treeview widget
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#B3CCFF", fieldbackground="#B3CCFF", foreground="black", borderwidth=1, relief="solid", padding=(10, 5))
style.map("Treeview", background=[("selected", "#347083")])
style.map("Treeview.Heading", background="#E6F3FF")

# Pack the table
table.pack(side="left", fill="both", expand=True)

# Set column width and format
table.column("ID", width=50, anchor="center")
table.column("Timestamp", width=200, anchor="center")
table.column("Count", width=80, anchor="center")  # Giảm độ rộng của cột Count
table.column("Image Path", width=400, anchor="w")  # Giảm độ rộng của cột Image Path

# Căn chỉnh văn bản trong các cột
table.heading("ID", text="ID", anchor="center")
table.heading("Timestamp", text="Timestamp", anchor="center")
table.heading("Count", text="Count", anchor="center")
table.heading("Image Path", text="Image Path", anchor="w")

# Create a label to display the selected image
image_label = tk.Label(root)
image_label.pack(pady=10)

# Bind the double click event on the table to show the image
table.bind("<Double-1>", show_image)

# Function to navigate to the next page
def next_page():
    global page_number
    page_number += 1
    fetch_data()

# Function to navigate to the previous page
def prev_page():
    global page_number
    if page_number > 1:
        page_number -= 1
        fetch_data()

# Create navigation buttons
prev_button = tk.Button(root, text="Previous", command=prev_page, bg="#B3CCFF", fg="black")
next_button = tk.Button(root, text="Next", command=next_page, bg="#B3CCFF", fg="black")
prev_button.pack(side="left", padx=10)
next_button.pack(side="right", padx=10)

# Run the Tkinter main loop
root.mainloop()
