import paramiko
import time
import threading

reachable_ip = []
unreachable_ip = []

def ping_device(host,password):

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname='10.0.12.1', username='advait', password=password)
    remote_connection = ssh_client.invoke_shell()
    cmd = 'ping ' + host + ' timeout 1 \n'
    remote_connection.send(cmd)
    time.sleep(2)
    output = remote_connection.recv(65536)
    output = output.decode()
    temp_lst = output.split(':')
    temp_lst2 = temp_lst[1].split('\n')
    if temp_lst2[1].strip() == '.':
        time.sleep(5)
        unreachable_ip.append(host)
    elif temp_lst2[1].strip() == '!!!!!':
        reachable_ip.append(host)

def create_threads(host_list, function, password):
    threads = []
    for host in host_list:
        th = threading.Thread(target = function, args = (host,password))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

f = open('ip.txt', 'r')
ip_list = []
for i in f:
    ip_list.append(i.strip())

start = time.time()

create_threads(ip_list, ping_device, 'cisco')

end = time.time()

print 'total time: ' + str(end-start)
print 'reachable ip address list: '
print reachable_ip
print 'unreachable ip address list: '
print unreachable_ip
