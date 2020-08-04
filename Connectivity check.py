from netmiko import ConnectHandler
import getpass
import telnetlib
from netmiko.ssh_exception import SSHException
from pythonping import ping

device_list=open('mydevices.txt')
telnet_device=[]
ssh_device=[]
unreachable_device=[]
ping_only=[]
user = input("Enter username: ")
password = getpass.getpass()

for device_ip in device_list:
    device_ip=device_ip.strip()
    iosv_l2 = {
    'device_type': 'cisco_ios',
    'ip': device_ip,
    'username': user,
    'password': password,
    'secret': password
    }
    print("Testing for IP:", iosv_l2['ip']) 
    try:      
        net_connect = ConnectHandler(**iosv_l2)
        net_connect.enable()
        #output = net_connect.send_command('sh run | sec Vlan')
        #print (output)
        ssh_device.append(iosv_l2['ip'])
    except SSHException:
        #print ("SSH is not enabled for device ", iosv_l2['ip'] ,". We are trying telnet now" )
        try:
            user = iosv_l2['username']
            password = iosv_l2['password']
            tn = telnetlib.Telnet(iosv_l2['ip'])
            tn.read_until(b"Username: ")
            tn.write(user.encode('ascii') + b"\n")
            if password:
                tn.read_until(b"Password: ")
                tn.write(password.encode('ascii') + b"\n")

            #tn.write(b"show run | sec Vlan\n")
            #tn.write(b"exit\n")
            #print(tn.read_all().decode('ascii'))
            telnet_device.append(iosv_l2['ip'])
        except Exception as e:
            response_list = ping(iosv_l2['ip'], size=40, count=10)
            if response_list.success():
                ping_only.append(iosv_l2['ip'])
            else:
                unreachable_device.append(iosv_l2['ip'])
            print ("################## Error occured for device IP:", iosv_l2['ip']," ################## \n" ,"*************************** Start of Error Message ***************************** \n")
            print (e ,"\n\n*************************** End of Error Message *****************************\n")
              
    except Exception as e:
        if response_list.success():
            ping_only.append(iosv_l2['ip'])
        else:
            unreachable_device.append(iosv_l2['ip'])
        print ("################## Error occured for device IP:", iosv_l2['ip']," ################## \n" ,"*************************** Start of Error Message ***************************** \n")
        print (e ,"\n\n*************************** End of Error Message *****************************\n")
print ("SSH enabled devices: ", ssh_device)
print ("SSH not enabled but telnet enabled devices: ", telnet_device)
print ("Pingable only devices: ", ping_only)
print ("Unreachable devices: ", unreachable_device)

