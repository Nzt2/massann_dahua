#masscan for Dahua DVR NVR IPC
import os,optparse

def parse_result():
    #Парсим результат массскана оставляем только Ip адресса
    file = open('res_scan.txt','r')
    Ips = open('IPs.txt','w')
    for string in file.readlines():
        line = string.split(' ')
        if not (string.startswith('#')):
            Ips.write(line[3]+'\n')
    Ips.close()

def save_xml():
    login = 'admin'
    password = 'admin'
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
    if x<=256:
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
    else:
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
def masscan(filescan):
    #Запускаем mass scan  с нужными параметрами
    print('[*] Starting scan in masscan')
    os.system('/usr/bin/masscan -p 37777 -iL %s -oL res_scan.txt --rate=500' %filescan)

def main():
    parser = optparse.OptionParser('%prog' + " -f <Scan file>")
    parser.add_option('-f', dest='file', type='string', help='Target list file Example; 192.168.1.1-192.168.11.1')
    (options, args) = parser.parse_args()
    if (options.file==None):
        print("[-] No taget file scan list\n")
        parser.print_help()
        exit(0)
    masscan(options.file)
    parse_result()
    save_xml()

main()


