import serial
import struct
import tkinter as tk
import tkinter.messagebox as messagebox
import mysql.connector
import hashlib
import os
import configparser
import sys
import webbrowser

def open_linked_in():
    url = "https://www.linkedin.com/in/krzymowski/"
    webbrowser.open(url)

# Funkcja do odczytywania danych z pliku config.ini
def read_config(section, option):
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config.get(section, option)

# Funkcja do generowania soli
def generate_salt():
    return os.urandom(16).hex()

# Funkcja do haszowania hasła z soleniem
def hash_password(password, salt):
    salted_password = password + salt
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
    return hashed_password

# Funkcja do sprawdzania autentyczności użytkownika
def authenticate_user(email, password):
    try:
        conn = mysql.connector.connect(
            host=database_login_host,
            user=database_login_user,
            password=database_login_password,
            database=database_login_name
        )
        cursor = conn.cursor()

        sql = "SELECT email, password FROM users WHERE email = %s"
        cursor.execute(sql, (email,))
        user_data = cursor.fetchone()

        if not user_data:
            return False

        saved_password = user_data[1]

        # Hasło jest zapisane w formacie tekstowym, nie ma potrzeby haszowania z soleniem
        if saved_password == password:
            return True
        else:
            return False

    except mysql.connector.Error as error:
        messagebox.showerror("Błąd połączenia z bazą danych", f"{error}")
        return False

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Dane do połączenia z bazą danych
database_login_host = read_config('Database_Login', 'host')
database_login_name = read_config('Database_Login', 'database')
database_login_user = read_config('Database_Login', 'user')
database_login_password = read_config('Database_Login', 'password')

database_test_host = read_config('Database_Test', 'host')
database_test_name = read_config('Database_Test', 'database')
database_test_user = read_config('Database_Test', 'user')
database_test_password = read_config('Database_Test', 'password')

port = read_config('Serial', 'port')
baudrate = read_config('Serial', 'baudrate')

authenticated_email = None

# Dodaj funkcję do obsługi zamknięcia okna logowania
def on_login_window_close():
    sys.exit()

# Tworzenie okna logowania
root_login = tk.Tk()
root_login.title("Cell test - Login")
root_login.protocol("WM_DELETE_WINDOW", on_login_window_close)
root_login.iconbitmap("logo.ico")
root_login.geometry("250x125")

# Tworzenie etykiety i pola tekstowego dla email
label_email = tk.Label(root_login, text="Email:")
label_email.pack()

text_email = tk.Text(root_login, height=1, width=20)
text_email.pack()

# Tworzenie etykiety i pola tekstowego dla hasła
label_password = tk.Label(root_login, text="Password:")
label_password.pack()

text_password = tk.Entry(root_login, show="*")
text_password.pack()

def login():
    global authenticated_email  # Use the global variable

    email = text_email.get("1.0", "end-1c")
    password = text_password.get()

    if authenticate_user(email, password):
        authenticated_email = email.split("@")[0]  # Set the authenticated email to the global variable
        root_login.destroy()
    else:
        messagebox.showerror("Login error", "Invalid email or password")


# Przycisk "Zaloguj"
button_login = tk.Button(root_login, text="Log in", command=login)
button_login.pack()

link_label = tk.Label(root_login, text="B.Krzymowski", fg="black", cursor="hand2", font=("Arial", 4))
link_label.pack(anchor=tk.W)
link_label.bind("<Button-1>", lambda e: open_linked_in())

root_login.mainloop()

# Użytkownik został zalogowany, kontynuujemy dalszą część programu

# Tworzenie okna głównego
root = tk.Tk()
root.title(authenticated_email)
root.iconbitmap("logo.ico")
root.geometry("400x225")

# Tworzenie etykiety i pola tekstowego dla ID
label_id = tk.Label(root, text="ID:")
label_id.pack()

text_id = tk.Text(root, height=1, width=20)
text_id.pack()

# Tworzenie rozwijanej listy wyboru typu baterii
label_battery = tk.Label(root, text="Battery Type:")
label_battery.pack()

selected_battery = tk.StringVar(value="18650")
combo_battery = tk.OptionMenu(root, selected_battery, "18650", "21700")
combo_battery.pack()

# Tworzenie etykiety dla rezystancji
label_resistance = tk.Label(root, text="")
label_resistance.pack()

label_resistance_value = tk.Label(root, text="")
label_resistance_value.pack()

# Tworzenie etykiety dla napięcia
label_voltage = tk.Label(root, text="")
label_voltage.pack()

label_voltage_value = tk.Label(root, text="")
label_voltage_value.pack()

# Przycisk "SAVE"
button_save = tk.Button(root, text="SAVE")
button_save.pack()

link_label = tk.Label(root, text="B.Krzymowski", fg="black", cursor="hand2", font=("Arial", 4))
link_label.pack(anchor=tk.W)
link_label.bind("<Button-1>", lambda e: open_linked_in())

def save_data():
    # Odczytanie wartości z pól tekstowych i rozwijanej listy
    global authenticated_email  # Use the global variable
    id_value = text_id.get("1.0", "end-1c")
    battery_value = selected_battery.get()
    resistance_value_text = label_resistance_value["text"].split(": ")[1]  # Get the resistance value text
    voltage_value_text = label_voltage_value["text"].split(": ")[1]  # Get the voltage value text

    resistance_value_text = resistance_value_text.replace(' mΩ', '')
    voltage_value_text = voltage_value_text.replace(' V', '')

    resistance_value = float(resistance_value_text)
    voltage_value = float(voltage_value_text)

    # Połączenie z bazą danych
    try:
        conn = mysql.connector.connect(
            host=database_test_host,
            user=database_test_user,
            password=database_test_password,
            database=database_test_name
        )
        cursor = conn.cursor()

        # Wstawienie danych do tabeli
        sql = "INSERT INTO celltest (serial, type, impedance, voltage, user) VALUES (%s, %s, %s, %s, %s)"
        values = (id_value, battery_value, resistance_value, voltage_value, authenticated_email)  # Use the authenticated email
        cursor.execute(sql, values)

        conn.commit()

        tk.messagebox.showinfo("Success", "The data has been added to the database.")

        # Wyczyszczenie pól tekstowych po dodaniu danych
        text_id.delete("1.0", tk.END)

    except mysql.connector.Error as error:
        tk.messagebox.showerror("Error", f"Database connection error: {error}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

button_save.config(command=save_data)

def update_values():
    with serial.Serial(port, baudrate) as ser:
        pkt = ser.read(10)
        status_disp, r_range_code, r_disp, sign_code, v_range_code, v_disp = struct.unpack('BB3s BB3s', pkt)

        r_disp = struct.unpack('I', r_disp + b'\x00')[0]
        resistance = float(r_disp) / 1e4

        r_disp_code = (status_disp & 0xF0) >> 4

        if r_disp_code == 0x05:
            r_unit_disp = 'mΩ'
        elif r_disp_code == 0x06:
            r_unit_disp = 'mΩ'
            resistance = 'OL'
        elif r_disp_code == 0x09:
            r_unit_disp = 'Ω'
        elif r_disp_code == 0x0a:
            r_unit_disp = 'Ω'
            resistance = 'OL'
        else:
            print(f"Unknown display code '{status_disp:#x}'")

        r_unit = r_unit_disp

        if r_range_code == 1:
            r_range = '0-20 mΩ'
            r_range_unit = 'mΩ'
        elif r_range_code == 2:
            r_range = '0-200 mΩ'
            r_range_unit = 'mΩ'
        elif r_range_code == 3:
            r_range = '0-2 Ω'
            r_range_unit = 'Ω'
        elif r_range_code == 4:
            r_range = '0-20 Ω'
            r_range_unit = 'Ω'
        elif r_range_code == 5:
            r_range = '0-200 Ω'
            r_range_unit = 'Ω'
        elif r_range_code == 6:
            r_range = 'AUTO'
            r_range_unit = None
        else:
            r_range = None
            r_range_unit = None
            print(f"Unknown resistance range code '{r_range_code:#x}'")

        if r_range_unit and r_unit_disp != r_range_unit:
            print(f"Display unit '{r_unit_disp}' override by range unit '{r_range_unit}' for selected range '{r_range}'")
            # Range unit has preference
            r_unit = r_range_unit

        resistance_text = f"RESISTANCE: {resistance} {r_unit}"

        sign_multiplier = None
        if sign_code == 1:
            sign_multiplier = 1.0
        elif sign_code == 0:
            sign_multiplier = -1.0
        else:
            print(f"Unknown sign code '{sign_code:#x}'")

        v_disp = struct.unpack('I', v_disp + b'\x00')[0]
        voltage = sign_multiplier * float(v_disp) / 1e4

        v_disp_code = (status_disp & 0x0F)
        if v_disp_code == 0x04:
            pass  # Nop, everything is OK
        elif v_disp_code == 0x08:
            voltage = 'OL'

        if v_range_code == 1:
            v_range = '0-20 V'
        elif v_range_code == 2:
            v_range = '0-100 V'
        elif v_range_code == 3:
            v_range = 'AUTO'
        else:
            v_range = 'Unknown'
            print(f"Unknown voltage range code '{v_range_code:#x}'")

        voltage_text = f"VOLTAGE: {voltage} V"

        label_resistance_value.config(text=resistance_text)
        label_voltage_value.config(text=voltage_text)

    root.after(1000, update_values)

update_values()

root.mainloop()