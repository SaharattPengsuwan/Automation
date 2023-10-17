from flask import Flask, render_template, request, session, redirect, url_for
import paramiko
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ip = request.form['ip']
        username = request.form['username']
        password = request.form['password']
        session['ip'] = ip
        session['username'] = username
        session['password'] = password
        return redirect(url_for('command'))
    return render_template('index.html')

@app.route('/command', methods=['GET', 'POST'])
def command():
    if 'ip' not in session or 'username' not in session or 'password' not in session:
        return redirect(url_for('index'))

    output = None

    if request.method == 'POST':
        ip = session['ip']
        username = session['username']
        password = session['password']
        

        if 'interface' in request.form and 'ip_address' in request.form and 'subnet_mask' in request.form:
            interface = request.form['interface']
            ip_address = request.form['ip_address']
            subnet_mask = request.form['subnet_mask']

            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=ip, username=username, password=password, allow_agent=False, look_for_keys=False)

            remote_connection = ssh_client.invoke_shell()
            remote_connection.send('en \n')
            remote_connection.send(f'conf t \n')
            remote_connection.send(f'interface {interface} \n')
            remote_connection.send(f'ip address {ip_address} {subnet_mask} \n')
            remote_connection.send('no sh \n')
            remote_connection.send('end \n')
            time.sleep(1)

            output = remote_connection.recv(65535).decode('ascii').split('\r\n')
            ssh_client.close()

        if 'command' in request.form:
            ip = session['ip']
            username = session['username']
            password = session['password']
            command = request.form['command']

            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=ip, username=username, password=password, allow_agent=False, look_for_keys=False)

            remote_connection = ssh_client.invoke_shell()
            remote_connection.send('en \n')
            remote_connection.send(command + '\n')
            time.sleep(1)

            # อ่านผลลัพธ์และแยกแต่ละบรรทัด
            output = remote_connection.recv(65535).decode('ascii').split('\r\n')
            ssh_client.close()

        if 'num_vlan' in request.form and 'name_vlan' in request.form :
            num_vlan = request.form['num_vlan']
            name_vlan = request.form['name_vlan']

            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=ip, username=username, password=password, allow_agent=False, look_for_keys=False)

            remote_connection = ssh_client.invoke_shell()
            remote_connection.send('en \n')
            remote_connection.send(f'conf t \n')
            remote_connection.send(f'vlan {num_vlan} \n')
            remote_connection.send(f'name {name_vlan} \n')
            remote_connection.send('end \n')
            time.sleep(1)

            output = remote_connection.recv(65535).decode('ascii').split('\r\n')
            ssh_client.close()
        

        if 'interface_vlan' in request.form and 'ip_address_vlan' in request.form and 'subnet_mask_vlan' in request.form:
            interface = request.form['interface_vlan']
            ip_address = request.form['ip_address_vlan']
            subnet_mask = request.form['subnet_mask_vlan']

            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=ip, username=username, password=password, allow_agent=False, look_for_keys=False)

            remote_connection = ssh_client.invoke_shell()
            remote_connection.send('en \n')
            remote_connection.send(f'conf t \n')
            remote_connection.send(f'interface {interface} \n')
            remote_connection.send(f'ip address {ip_address} {subnet_mask} \n')
            remote_connection.send('end \n')
            time.sleep(1)

            output = remote_connection.recv(65535).decode('ascii').split('\r\n')
            ssh_client.close()   
        
        if 'vlan' in request.form and 'int' in request.form :
            vlan = request.form['vlan']
            int_sw = request.form['int']

            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=ip, username=username, password=password, allow_agent=False, look_for_keys=False)

            remote_connection = ssh_client.invoke_shell()
            remote_connection.send('en \n')
            remote_connection.send(f'conf t \n')
            remote_connection.send(f'int {int_sw} \n')
            remote_connection.send(f'switch access vlan {vlan} \n')
            remote_connection.send('end \n')
            time.sleep(1)

            output = remote_connection.recv(65535).decode('ascii').split('\r\n')
            ssh_client.close()

    return render_template('command.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
