from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import tkinter as tk
from tkinter import *
import keyboard
import win32api
from tkinter import filedialog 
from PIL import ImageTk, Image
import tkinter



#initialising tkinter
root = tk.Tk()
root.title('QLD Registration Checker')
root.geometry("800x470")
root.config(bg="#2c3e50")
root.grid_columnconfigure(0, weight=1)
keylogger = True

#initializing values 
license_plate = 0
b_search_flag = False
license_plates = []

regocheck = True
chrome_driver_path = 'C:\webdrivers'
license_plates = []

def regoadd(license_input):
       #set flag to true when i do the submit button
       while b_search_flag is False:
        license_plate = license_input.get()
        regocheck = True
        license_plates.append(license_plate)
        inputbox.insert(INSERT, license_plate + '\n')
        return None

def regodelete(license_input):
      license_plate = license_input.get()
      if license_plates != []:
        license_plates.pop()
        delete_count = len(license_plates)
        float_delete_count = float(delete_count)
        float_delete_count_actual = float_delete_count + 1.0
        inputbox.delete(float_delete_count_actual,"end")
      return None

def regoclear(license_input):
     license_plates.clear()
     inputbox.delete("1.0","end")
     outputbox.delete("1.0","end")
     return None

def regoload():
     #add a fileloader function that parses through a .txt file.
     return None

def openfile():
     file_to_open = filedialog.askopenfilename( 
      initialdir="/", title="Select file",  
      filetypes=(("Text files", "*.txt"), ("all files", "*.*"))) 
     if file_to_open:
        with open(file_to_open, 'r') as file:
            content = file.read()
            license_plates = content.split()
            inputbox.insert(INSERT, content + '\n')
            inputbox.update_idletasks()
            check_license_plates(license_plates)

             

def cleartext():
     e1.delete(0, END)

def check_license_plates(license_plates):
    for plate_input in license_plates:
        start_time = time.time()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        qldurl = "https://www.service.transport.qld.gov.au/checkrego/application/VehicleSearch.xhtml?dswid=138"
        driver.get(qldurl)

        button = driver.find_element(By.CLASS_NAME, "ui-button")
        button.click()

        registration = driver.find_element(By.CLASS_NAME, "ui-inputfield")
        registration.send_keys(plate_input)
        button = driver.find_element(By.CLASS_NAME, "ui-button")
        button.click()

        qld_line_counter = 0
        output_dict = {}

        html = driver.page_source
        soup = BeautifulSoup(html,features='lxml')
        for tag in soup.find_all('dd'):
            qld_line_counter += 1
            if qld_line_counter == 3:
                processedoutput = tag.text
                final_output = ' '.join(line.strip() for line in processedoutput.split('\n') if line.strip())
                output_dict['result'] = final_output
                break

        if "result" not in output_dict:
            outputbox.insert(INSERT, 'This vehicle is unregistered or does not exist.' + '\n', 'unregistered')
        else:
            outputbox.insert(INSERT, output_dict['result'] + '\n')

        print(output_dict)
        driver.quit()
        inputbox.update_idletasks()
        print("--- %s seconds ---" % (time.time() - start_time))

title = tk.Label(root, text="QLD REGO CHECK", font=("Calibre", 16), bg="#2c3e50", fg="white")
title.pack(side="top", pady=(5, 0))

frame = tk.Frame(root)
frame.pack()
frame.config(bg="#2c3e50")

plateslabel = tk.Label(frame, text="Add Plates: ", font=("Calibre", 12), bg="#2c3e50", fg="white")
plateslabel.pack(side="left", padx=(0, 0), pady=(10,0))

license_name = tk.StringVar(frame, value='')
e1 = tk.Entry(frame, textvariable=license_name, width=10)
e1.pack(side="left", padx=(10, 10),pady=(10,0))

b_add = tk.Button(frame, text="  Add ", command=lambda: [regoadd(license_name), cleartext()])
b_add.pack(side="left", padx=(5, 0), pady=(10,0))

b_delete = tk.Button(frame, text="Delete", command=lambda: regodelete(license_name))
b_delete.pack(side="left", padx=(5, 0), pady=(10,0))

b_clear = tk.Button(frame, text=" Clear ", command=lambda: regoclear(license_name))
b_clear.pack(side="left", padx=(5, 475), pady=(10,0))

listlabel = tk.Label(root, text="Add by list: ", font=("Calibre", 12), bg="#2c3e50", fg="white")
listlabel.place(x=0, y=90)

b_browse = tk.Button(root, text="Browse", command=lambda: openfile())
b_browse.place(x=101,y=90)

inputbox = Text(root, width=10, height=18)
inputbox.place(x=5,y=130)

outputbox = Text(root, width=85, height=18)
outputbox.place(x=100,y=130)

outputbox.tag_config('unregistered', foreground="red")

b_search = tk.Button(root, text=" Search ", command=lambda: check_license_plates(license_plates))
b_search.place(x=5,y=440)

mylabel = tk.Label(root, text="Thomas McPherson", font=("Calibre", 9), bg="#2c3e50", fg="white")
mylabel.place(x=660, y=440)

def on_enter_pressed(event):
    regoadd(license_name)
    cleartext()

root.bind('<Return>', on_enter_pressed)
     
root.mainloop()

