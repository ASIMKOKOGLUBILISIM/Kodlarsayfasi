import subprocess

def block_ip(ip):
    command = (
        f'netsh advfirewall firewall add rule '
        f'name="BLOCK_{ip}" dir=in action=block remoteip={ip}'
    )
    subprocess.run(command, shell=True)
    print(f"🔥 IP BLOCKLANDI: {ip}")