import socket
import netifaces

from core.Config import ConfigInterfaces

class Interfaces:

    def __init__(self):
        self.get_my_ip()
        self.get_subred()

    def get_my_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.mi_ip = s.getsockname()[0]
        s.close()
        ConfigInterfaces.mi_ip = self.mi_ip

    def get_subred(self):
        self.interfaces_mi_pc = []
        for i in netifaces.interfaces():
            try:
                ip=netifaces.ifaddresses(i)[netifaces.AF_INET][0]['addr']
                mask=netifaces.ifaddresses(i)[netifaces.AF_INET][0]['netmask']
                mascara_bin = sum([bin(int(x)).count('1') for x in mask.split('.')])
                if ip not in '127.0.0.1':
                    self.interfaces_mi_pc.append('{}/{}'.format(ip, mascara_bin))
            except:
                pass
        ConfigInterfaces.interfaces_mi_pc = self.interfaces_mi_pc