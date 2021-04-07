#By LoreBadTime
import os,subprocess
from subprocess import PIPE, STDOUT, CREATE_NO_WINDOW

dir_path = os.path.dirname(os.path.realpath(__file__))
#getting all wifi nearby connections 
result = subprocess.run(['netsh', 'wlan','show','networks'], stdout=subprocess.PIPE,creationflags=CREATE_NO_WINDOW)
result = result.stdout.decode('utf-8').splitlines()
cont = 0
add = 0
tmplist = []
found = False
listofconnections = []
#getting all open connections and chosing the better one
while cont < len(result):
    # Run "netsh wlan show networks",to make it work you need to replace this string below with the line that you see in command output that is like 
    # " Autentication/Security          : Open "
    # Otherwise the script can have some problems running since different language 
    if result[cont] == "    Autenticazione          : Aperta":
        tmplist = []
        #getting and storing the name of the open wifi
        for char in result[cont - 2]:
            if char == ' ':
                add = add + 1
            if add >= 4 :
                tmplist.append(char)
            if add == 3 :
                add = add + 1
        connection = tmplist
        found = True
    cont = cont + 1    
connection = ''.join(connection)
# opening the Windows configuration default open wireless System file and Replacing the template with the name of the open connection
# !!! this scipt NEEDS the "connection.txt" File (provided on github page) into the same folder,or you can just hardcode the path of the file 
f = open("connection.txt",'r+')
lines=f.readlines()
listedlines = []
for line in lines:
    listedlines.append(line)
newlist = []
for line in listedlines:
    if line == '\t<name>example</name>\n':
        line = '\t<name>' + str(connection) + '</name>\n'
    if line == '\t\t\t<name>example</name>\n':
        line = '\t\t\t<name>' + str(connection) + '</name>\n'
    newlist.append(line)
#creating a new configuration file,i chose w+ to avoid errors
file = open(str(connection) + ".xml",'w+')
for line in newlist:
    file.write(line)
f.close()
file.close()
#final script load 
#this will delete the open connection(if already stored in Windows) before loading the new connection
try:
    subprocess.run(['netsh', 'wlan', 'delete','profile', 'filename="'+ connection + '.xml"'],creationflags=CREATE_NO_WINDOW)
except:
    pass
#adding and connecting the connection
subprocess.run(['netsh', 'wlan', 'add','profile', 'filename="'+ connection + '.xml"'],creationflags=CREATE_NO_WINDOW)
subprocess.run(['netsh', 'wlan', 'connect', 'name=' + connection],creationflags=CREATE_NO_WINDOW)

