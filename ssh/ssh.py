import paramiko


hostname = '172.17.4.42'
port = 22
username = 'root'
password = 'sccpassword'

if __name__ == "__main__":
    paramiko.util.log_to_file('paramiko.log')
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.load_system_host_keys()
    s.connect(hostname, port, username, password)
    stdin, stdout, stderr = s.exec_command('sudo df -h')
    print (stdout.readlines())
    s.close()