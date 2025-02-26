import tkinter as tk
from tkinter import messagebox,ttk
import pyodbc as odbc


try:
    conn = odbc.connect("DRIVER={SQL SERVER};"
                          "SERVER=DESKTOP-04F1S99;"
                          "DATABASE=museum_arts;"
                          "Trusted_Connectiton=yes;")
    print("connection successful")
except Exception as e:
    print("errore",e)

ADMIN_USERNAME = "1234"
ADMIN_PASSWORD = "1234"
GUEST_USERNAME = "guest"
GUEST_PASSWORD = "guest"


def main_menu(is_guest=False):
    root.title("Art Museum Management System")
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Art Museum Management", font=("Helvetica", 50, "bold")).pack(pady=30)
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)
    tk.Button(root, text="Back", command=(welcome_screen if is_guest else admin_login), 
          font=("Helvetica", 22), bg="gray", fg="white").pack(pady=5)

    # tk.Button(root, text="Back", command=welcome_screen, font=("Helvetica", 22), bg="gray", fg="white").pack(pady=5)
    
    # View Button (Visible for both)
    tk.Button(button_frame, text="View Art Objects", command=read_art_objects, 
              font=("Helvetica", 20, "bold"), bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=10)
  
    
    if not is_guest:  # Admin-only buttons
        tk.Button(button_frame, text="Add Art Object", command=create_art_object,
                  font=("Helvetica", 20, "bold"), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Modify Art Object", command=update_art_object,
                  font=("Helvetica", 20, "bold"), bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Remove Art Object", command=delete_art_object,
                  font=("Helvetica", 20, "bold"), bg="#4CFA50", fg="white").pack(side=tk.LEFT, padx=10)
            
        # tk.Button(button_frame, text="Collection", command=add_collection_window,
        #   font=("Helvetica", 20, "bold"), bg="#F44336", fg="white").pack(side=tk.LEFT,pady=10)
        tk.Button(button_frame, text="Collection", command=add_collection_window,
          font=("Helvetica", 20, "bold"), bg="brown", fg="pink").pack(side=tk.RIGHT,pady=10)

    # Exit Button
    # tk.Button(button_frame, text="Exit", command=root.quit,
    #           font=("Helvetica", 20, "bold"), bg="#9E9E9E", fg="white").pack(side=tk.LEFT, padx=10)

def admin_login():
    login_screen("admin")

def guest_login():
    main_menu(is_guest=True)

def login_screen(user_type):
    root.title(f"{user_type.capitalize()} Login")
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text=f"{user_type.capitalize()} Username:", font=("Helvetica", 20, "bold")).pack(pady=10)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=10)
    
    tk.Label(root, text=f"{user_type.capitalize()} Password:", font=("Helvetica", 20, "bold")).pack(pady=10)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=10)
    
    def authenticate():
        if username_entry.get() == ADMIN_USERNAME and password_entry.get() == ADMIN_PASSWORD:
            main_menu(is_guest=False)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
    
    tk.Button(root, text="Login", command=authenticate,
              font=("Helvetica", 30, "bold"), bg="red", fg="white").pack(pady=10)
    tk.Button(root, text="Back", command=welcome_screen,
              font=("Helvetica", 25), bg="gray", fg="white").pack(pady=10)

def welcome_screen():
    root.title("Welcome to the Art Museum")
    root.configure(bg="#f0f8ff")
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Art Museum Management System", 
             font=("Helvetica", 50, "bold"), bg="#f0f8ff").pack(pady=40)
    
    btn_frame = tk.Frame(root, bg="#f0f8ff")
    btn_frame.pack(pady=20)
    
    tk.Button(btn_frame, text="Admin Login", command=admin_login,
              font=("Helvetica", 30), bg="blue", fg="white").pack(side=tk.LEFT, padx=20)
    tk.Button(btn_frame, text="Guest Login", command=guest_login,
              font=("Helvetica", 30), bg="purple", fg="white").pack(side=tk.LEFT, padx=20)

   



def add_collection_window():
    # Create new window
    collection_window = tk.Toplevel(root)
    collection_window.title("Add New Collection")
    collection_window.geometry("500x400")
    collection_window.state('zoomed')
    # Labels and Entry Fields
    labels = ["Collection Name:", "Type:", "Description:", "Address:", "Phone:", "Contact Person:"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(collection_window, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(collection_window, width=40)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    # Function to save the new collection
    def save_collection():
        name = entries[0].get()
        type_ = entries[1].get()
        description = entries[2].get()
        address = entries[3].get()
        phone = entries[4].get()
        contact_person = entries[5].get()

        if not name or not type_ or not address or not phone or not contact_person:
            messagebox.showerror("Error", "Please fill in all required fields!")
            return

        try:
            
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO COLLECTION (Name, Type, Description, Address, Phone, Contact_person) VALUES (?, ?, ?, ?, ?, ?)",
                (name, type_, description, address, phone, contact_person)
            )
            conn.commit()
            messagebox.showinfo("Success", "Collection added successfully!")
            collection_window.destroy()

        except odbc.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")

        finally:
            cursor.close()
            # conn.close()

    # Buttons
    tk.Button(collection_window, text="Save", command=save_collection, bg="green", fg="white").grid(row=6, column=0, columnspan=2, pady=10)
    tk.Button(collection_window, text="Back", command=main_menu, bg="gray", fg="white").grid(row=7, column=0, columnspan=2, pady=5)





def read_art_objects():
    try:
      
        cursor = conn.cursor()

        cursor.execute("SELECT Id_no, Artist, Year, Title, Description, Origin, Epoch FROM ART_OBJECTSS")
        art_objects = cursor.fetchall()

        cursor.execute("SELECT Name, Type, Description, Address, Phone, Contact_person FROM COLLECTION")
        collections = cursor.fetchall()

        read_window = tk.Toplevel(root)
        read_window.title("Art Objects & Collections")
        read_window.state('zoomed')

        if not art_objects:
            tk.Label(read_window, text="No art objects found.").pack()
        else:
            for obj in art_objects:
                details = f"ID: {obj[0]}, Artist: {obj[1]}, Year: {obj[2]}, " \
                          f"Title: {obj[3]}, Description: {obj[4]}, " \
                          f"Country of Origin: {obj[5]}, Epoch: {obj[6]}"
                tk.Label(read_window, text=details).pack()
        
        if not collections:
            tk.Label(read_window, text="No collections found.").pack()
        else:
            for col in collections:
                col_details = f"Collection Name: {col[0]}, Type: {col[1]}, Description: {col[2]}, " \
                              f"Address: {col[3]}, Phone: {col[4]}, Contact Person: {col[5]}"
                tk.Label(read_window, text=col_details).pack()

        cursor.close()
        # conn.close()

    except odbc.Error as e:
        messagebox.showerror("Error", f"Database error: {e}")

    tk.Button(read_window, text="Back", command=welcome_screen, font=("Helvetica", 22), bg="gray", fg="white").pack(pady=5)


     

def create_art_object():
    create_window = tk.Toplevel(root)
    create_window.state('zoomed')
    create_window.title("Create New Art Object")

    labels = ["Art Object ID:", "Artist Name:", "Year Created:", "Title:", "Description:", "Country of Origin:", "Epoch:"]
    entries = []

    # Create labels and entry fields
    for i, label in enumerate(labels):
        tk.Label(create_window, text=label).grid(row=i, column=0)
        entry = tk.Entry(create_window)
        entry.grid(row=i, column=1)
        entries.append(entry)

    # Function to save the new object in the database
    def new_save():
        id_no = entries[0].get()
        artist = entries[1].get()
        year = entries[2].get()
        title = entries[3].get()
        description = entries[4].get()
        country_of_origin = entries[5].get()
        epoch = entries[6].get()

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO ART_OBJECTSS (Id_no, Artist, Year, Title, Description, Origin, Epoch) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (id_no, artist, year, title, description, country_of_origin, epoch)
            )
            conn.commit()
            messagebox.showinfo("Success", "Art Object created successfully!")
            create_window.destroy()

        except odbc.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    # Add a button to save data
    tk.Button(create_window, text="Save", command=new_save).grid(row=7, column=0, columnspan=2)    
    tk.Button(create_window, text="Back", command=main_menu, font=("Helvetica", 22), bg="gray", fg="white").pack(pady=5)
  

def update_art_object():
    
    def save_updated_object():
        id_no = entries[0].get()  # ID to search
        artist = entries[1].get()
        year = entries[2].get()
        title = entries[3].get()
        description = entries[4].get()
        country_of_origin = entries[5].get()
        epoch = entries[6].get()

        try:
            cursor = conn.cursor()
            # Update query with parameterized inputs
            cursor.execute(
                """UPDATE ART_OBJECTSS 
                SET Artist=?, Year=?, Title=?, Description=?, Origin=?, Epoch=?
                WHERE Id_no=?""",
                (artist, year, title, description, country_of_origin, epoch, id_no)
            )
            
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "Art Object ID not found!")
            else:
                conn.commit()
                messagebox.showinfo("Success", "Art Object updated successfully!")
                update_window.destroy()

        except odbc.Error as e:
            conn.rollback()
            messagebox.showerror("Database Error", f"Failed to update: {e}")

    # Create update window
    update_window = tk.Toplevel(root)
    update_window.title("Update Art Object")
    update_window.state('zoomed')
    labels = [
        "Art Object ID (to update):", 
        "New Artist Name:", 
        "New Year Created:", 
        "New Title:", 
        "New Description:", 
        "New Country of Origin:", 
        "New Epoch:"
    ]
    
    entries = []
    for i, label in enumerate(labels):
        tk.Label(update_window, text=label).grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(update_window)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)

    tk.Button(
        update_window, 
        text="Save Changes", 
        command=save_updated_object,
        bg="#4CAF50",
        fg="white"
    ).grid(row=7, column=0, columnspan=2, pady=10)



def delete_art_object():
    delete_window = tk.Toplevel(root)
    delete_window.state('zoomed')
    delete_window.title("Delete Art Object or Collection")

    tk.Label(delete_window, text="Enter Art Object ID to Delete:").grid(row=0, column=0)
    id_entry = tk.Entry(delete_window)
    id_entry.grid(row=0, column=1)

    tk.Label(delete_window, text="OR Enter Collection Name to Delete:").grid(row=1, column=0)
    collection_entry = tk.Entry(delete_window)
    collection_entry.grid(row=1, column=1)

    def confirm_delete():
        id_no = id_entry.get()
        collection_name = collection_entry.get()

        if not id_no and not collection_name:
            messagebox.showerror("Error", "Please enter an Art Object ID or a Collection Name.")
            return

        try:
            cursor = conn.cursor()
            if id_no:
                cursor.execute("DELETE FROM ART_OBJECTSS WHERE Id_no = ?", (id_no,))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", f"Art Object with ID {id_no} deleted successfully!")
                else:
                    messagebox.showwarning("Not Found", f"No Art Object found with ID {id_no}.")
            
            if collection_name:
                cursor.execute("DELETE FROM COLLECTION WHERE Name = ?", (collection_name,))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", f"Collection with Name {collection_name} deleted successfully!")
                else:
                    messagebox.showwarning("Not Found", f"No Collection found with Name {collection_name}.")

        except odbc.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    tk.Button(delete_window, text="Delete", command=confirm_delete, bg="red", fg="white").grid(row=2, column=0, columnspan=2)
    tk.Button(delete_window, text="Back", command=delete_window.destroy, bg="gray", fg="white").grid(row=3, column=0, columnspan=2)


if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')

    welcome_screen()
    root.mainloop()
