import os,subprocess
from subprocess import PIPE, STDOUT, CREATE_NO_WINDOW




dir_path = os.path.dirname(os.path.realpath(__file__))
result = subprocess.run(['netsh', 'wlan','show','networks'], stdout=subprocess.PIPE,creationflags=CREATE_NO_WINDOW)
result = result.stdout.decode('utf-8').splitlines()
cont = 0
add = 0
tmplist = []
found = False
listofconnections = []
while cont < len(result):
    if result[cont] == "    Autenticazione          : Aperta":
        tmplist = []
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
file = open(str(connection) + ".xml",'w+')
for line in newlist:
    file.write(line)
f.close()
file.close()
try:
    subprocess.run(['netsh', 'wlan', 'delete','profile', 'filename="'+ connection + '.xml"'],creationflags=CREATE_NO_WINDOW)
except:
    pass
subprocess.run(['netsh', 'wlan', 'add','profile', 'filename="'+ connection + '.xml"'],creationflags=CREATE_NO_WINDOW)
subprocess.run(['netsh', 'wlan', 'connect', 'name=' + connection],creationflags=CREATE_NO_WINDOW)
#os.remove(connection + ".xml")
