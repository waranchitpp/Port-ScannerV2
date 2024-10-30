import socket,sys,threading,time
from tkinter import *


# ==== ส่วนของตัวแปรการสแกน ====
ip_s = 1
ip_f = 1024
log = []
ports = []
target = 'localhost'




# ==== ฟังก์ชันสำหรับการสแกนพอร์ต ====
def scanPort(target, port):
    try:
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        c = s.connect_ex((target, port))
        if c == 0:
            timestamp = time.strftime("[%H:%M:%S]")
            m = f'{timestamp} Port {port} \t[open]'
            log.append(m)
            ports.append(port)
            listbox.insert("end", str(m))
            updateResult()
        s.close()
    except OSError: print('> Too many open sockets Port ' + str(port))
    except:
        c.close()
        s.close()
        sys.exit()
    sys.exit()
# ==== ฟังก์ชันอัพเดตสถานะผลลัพธ์ ====
def updateResult():
    rtext = " [ " + str(len(ports)) + " / " + str(ip_f) + " ] ~ " + str(target)
    L27.configure(text = rtext)
 
def startScan():
    global ports, log, target, ip_f
    clearScan()
    log = []
    ports = []
    # รับช่วง port จาก GUI
    ip_s = int(L24.get())
    ip_f = int(L25.get())
    # เริ่มเขียน Log
    log.append('> Port Scanner')
    log.append('='*14 + '\n')
    log.append(' Target:\t' + str(target))
     
    try:
        target = socket.gethostbyname(str(L22.get()))
        log.append(' IP Adr.:\t' + str(target))
        log.append(' Ports: \t[ ' + str(ip_s) + ' / ' + str(ip_f) + ' ]')
        log.append('\n')
        # ฟังก์ชันเริ่มการสแกน
        while ip_s <= ip_f:
            try:
                scan = threading.Thread(target=scanPort, args=(target, ip_s))
                scan.setDaemon(True)
                scan.start()
            except: time.sleep(0.01)
            ip_s += 1
    except:
        m = '> Target ' + str(L22.get()) + ' not found.'
        log.append(m)
        listbox.insert(0, str(m))
# ==== บันทึกผลการสแกนลงไฟล์ .txt ====
def saveScan():
    global log, target, ports, ip_f
    log[5] = " Result:\t[ " + str(len(ports)) + " / " + str(ip_f) + " ]\n"
    with open('portscan-'+str(target)+'.txt', mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(log))
 
def clearScan():
    listbox.delete(0, 'end')

# ฟังก์ชันสำหรับการออกจากโปรแกรม
def exitProgram():
    gui.destroy()

# ==== GUI ====
gui = Tk()
gui.title('PortScaner-waranchitpp')
gui.geometry("400x600+20+20")
 
# ==== Colors ====
m1c = '#00ee00'
bgc = '#090909'
dbg = '#000000'
fgc = '#111111'
 
gui.tk_setPalette(background=bgc, foreground=m1c, activeBackground=fgc,activeForeground=bgc, highlightColor=m1c, highlightBackground=m1c)
 
# ==== Labels ====
L11 = Label(gui,   font=("Helvetica", 16, 'underline'))
L11.place(x = 180, y = 1)
 
L21 = Label(gui, text = "Target: ")
L21.place(x = 16, y = 90)
 
L22 = Entry(gui, text = "localhost")
L22.place(x = 180, y = 90)
L22.insert(0, "localhost")
 
L23 = Label(gui, text = "Ports: ")
L23.place(x = 16, y = 158)
 
L24 = Entry(gui, text = "1")
L24.place(x = 180, y = 158, width = 95)
L24.insert(0, "1")
 
L25 = Entry(gui, text = "1024")
L25.place(x = 290, y = 158, width = 95)
L25.insert(0, "1024")
 
L26 = Label(gui, text = "Results: ")
L26.place(x = 16, y = 220)
L27 = Label(gui, text = "[ ... ]")
L27.place(x = 180, y = 220)
 
# ==== Ports list ====
frame = Frame(gui)
frame.place(x = 16, y = 275, width = 370, height = 215)
listbox = Listbox(frame, width = 59, height = 6)
listbox.place(x = 0, y = 0)
listbox.bind('<<ListboxSelect>>')
scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
 
# ==== Buttons / Scans ====
B11 = Button(gui, text = "Start Scan", command=startScan)
B11.place(x = 16, y = 500, width = 170)
B21 = Button(gui, text = "Save Result", command=saveScan)
B21.place(x = 210, y = 500, width = 170)

# สร้างเมนูบาร์
menubar = Menu(gui)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Save", command=saveScan)  # เพิ่มฟังก์ชัน Save
filemenu.add_separator()  
filemenu.add_command(label="Exit", command=exitProgram)  
menubar.add_cascade(label="File", menu=filemenu)  

gui.config(menu=menubar)  # กำหนดให้ menubar เป็นเมนูหลักของหน้าต่าง gui
# ==== Start GUI ====
gui.mainloop()