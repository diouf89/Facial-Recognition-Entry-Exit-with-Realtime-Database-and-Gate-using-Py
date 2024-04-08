import tkinter as tk
import subprocess
import pyttsx3
from seleniumwire import webdriver
from tkinter import messagebox
from time import sleep
import time
from datetime import datetime

entrygate = 'python entrancetestslow.py'
exitgate = 'python exittestslow.py'
datamanager = 'python EntryAdderToText.py'
parentimage = 'python ParentEncodeFile.py'
studentimage = 'python EncodeGenerator.py'

def open_database():
    speak("Opening Realtime Database")
    root.iconify()  # Minimize the window
    # Create a new instance of the Chrome driverpip install pipreqs
    driver = webdriver.Chrome()
    # Open the website
    website_url = 'https://docs.google.com/spreadsheets/d/1RLjRp2ZLL_IrP-xPBfaIe8zGWSG7UhXKRc9CClmioL8/edit?usp=sharing'
    driver.get(website_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="some-element-id"]')))
    driver.quit()
    root.deiconify()  # Restore the window after subprocess completion

def speak(text, rate=200):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

def on_enter(event):
    event.widget.config(highlightthickness=5, highlightbackground=colour3)

def on_leave(event):
    event.widget.config(highlightthickness=2, highlightbackground=colour2)

def open_entry_gate():
    speak("Opening Entry Mode")
    root.iconify()  # Minimize the window
    entry_process = subprocess.Popen(entrygate, shell=True)
    entry_process.wait()  # Wait for the subprocess to complete
    root.deiconify()  # Restore the window after subprocess completion

def open_exit_gate():
    speak("Opening Exit Mode")
    root.iconify()  # Minimize the window
    exit_process = subprocess.Popen(exitgate, shell=True)
    exit_process.wait()  # Wait for the subprocess to complete
    root.deiconify()  # Restore the window after subprocess completion

def data_manager():
    speak("Opening Database Manager")
    root.iconify()  # Minimize the window
    manager_process = subprocess.Popen(datamanager, shell=True)
    manager_process.wait()  # Wait for the subprocess to complete
    root.deiconify()  # Restore the window after subprocess completion

def check_time():
    current_time = datetime.now().time()
    if current_time < datetime.strptime('13:00:00', '%H:%M:%S').time():
        open_entry_gate()
    else:
        open_exit_gate()

    # Reset to entry mode when the time is 5 am
    if current_time.hour == 5 and current_time.minute == 0:
        open_entry_gate()

    # Check time again after 1 minute
    root.after(60000, check_time)

def check_time_button():
    speak("Checking time")
    check_time()

def image_encoder():
    # Create a loading message box
    loading_window = tk.Toplevel(root)
    loading_window.title("Loading")
    loading_label = tk.Label(loading_window, text="Encoding in Progress...", font=('Arial', 12))
    loading_label.pack(pady=100)

    speak("Encoding Started")
    root.iconify()  # Minimize the window

    # Start parentimage_process in a separate thread
    parentimage_process = subprocess.Popen(parentimage, shell=True)

    # Update the loading message box while parentimage_process is still running
    while parentimage_process.poll() is None:
        loading_window.update()
        sleep(0.1)

    speak("Parent Image Encoding Done.Processing Student Image")

    # Start studentimage_process in a separate thread
    studentimage_process = subprocess.Popen(studentimage, shell=True)

    # Update the loading message box while studentimage_process is still running
    while studentimage_process.poll() is None:
        loading_window.update()
        sleep(0.1)

    speak("Student Image Encoding Done.Encoding Complete")

    # Destroy the loading message box
    loading_window.destroy()

    messagebox.showinfo('Encoder', 'Images encoded successfully!')
    root.deiconify()  # Restore the window after subprocess completion

def exitall():
    speak("Exiting Application")
    root.destroy()

def initialize_main_menu():
    # Initialize the main menu
    root.title("Facial Recognition System")
    root.geometry('1000x850')
    root.resizable(width=False, height=False)

    main_frame = tk.Frame(root, bg=colour1, pady=55)
    main_frame.pack(fill=tk.BOTH, expand=True)
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=1)

    # Title Label
    title_label = tk.Label(
        main_frame,
        text="Facial Recognition\nMonitoring System",
        font=('Times New Roman', 50, 'bold'),
        bg=colour1,
        fg=colour3
    )
    title_label.grid(column=0, columnspan=2, row=0, pady=(0, 55))

    # Buttons
    button1 = tk.Button(
        main_frame,
        background=colour2,
        foreground=colour4,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour2,
        highlightcolor='WHITE',
        width=13,
        height=2,
        border=0,
        cursor='hand1',
        text='Entrance Mode',
        font=('Arial', 30, 'bold'),
        command=open_entry_gate
    )
    button1.grid(column=0, row=1, padx=(0, 20))
    button1.bind('<Enter>', on_enter)
    button1.bind('<Leave>', on_leave)

    button2 = tk.Button(
        main_frame,
        background=colour2,
        foreground=colour4,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour2,
        highlightcolor='WHITE',
        width=13,
        height=2,
        border=0,
        cursor='hand1',
        text='Exit Mode',
        font=('Arial', 30, 'bold'),
        command=check_time_button
    )
    button2.grid(column=1, row=1, padx=(0, 80))
    button2.bind('<Enter>', on_enter)
    button2.bind('<Leave>', on_leave)

    button3 = tk.Button(
        main_frame,
        background=colour1,
        foreground=colour2,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour2,
        highlightcolor='WHITE',
        width=13,
        height=2,
        border=3,
        cursor='hand1',
        text='Database',
        font=('Arial', 30, 'bold'),
        command=open_database
    )
    button3.grid(column=0, row=2, padx=(0, 20))
    button3.bind('<Enter>', on_enter)
    button3.bind('<Leave>', on_leave)

    button4 = tk.Button(
        main_frame,
        background=colour1,
        foreground=colour2,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour2,
        highlightcolor='WHITE',
        width=13,
        height=2,
        border=3,
        cursor='hand1',
        text='Data Manager',
        font=('Arial', 30, 'bold'),
        command=data_manager
    )
    button4.grid(column=1, row=2, padx=(0, 80))
    button4.bind('<Enter>', on_enter)
    button4.bind('<Leave>', on_leave)

    button5 = tk.Button(
        main_frame,
        background=colour1,
        foreground=colour2,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour2,
        highlightcolor='WHITE',
        width=13,
        height=2,
        border=3,
        cursor='hand1',
        text='Exit',
        font=('Arial', 30, 'bold'),
        command=exitall
    )
    button5.grid(column=1, row=3, padx=(0, 80), pady=(25,0))
    button5.bind('<Enter>', on_enter)
    button5.bind('<Leave>', on_leave)

    button6 = tk.Button(
        main_frame,
        background=colour1,
        foreground=colour2,
        activebackground=colour3,
        activeforeground=colour4,
        highlightthickness=2,
        highlightbackground=colour2,
        highlightcolor='WHITE',
        width=13,
        height=2,
        border=3,
        cursor='hand1',
        text='Encoder',
        font=('Arial', 30, 'bold'),
        command=image_encoder
    )
    button6.grid(column=0, row=3, padx=(0, 20), pady=(25,0))
    button6.bind('<Enter>', on_enter)
    button6.bind('<Leave>', on_leave)

    root.after(500, speak, "Welcome to Facial Recognition Entry and Exit Monitoring System")

# Create the root window
root = tk.Tk()

# Define colors
colour1 = '#020f12'
colour2 = '#05d7ff'
colour3 = '#65e7ff'
colour4 = 'BLACK'

# Initialize the main menu
initialize_main_menu()

# Start checking time
check_time()

# Run the Tkinter event loop
root.mainloop()
