import nmap

class Escaner():
	def __init__(self, rango='192.168.1.0/24'):
		pass

	def escanearRed(self, red): #192.168.1.0/24
		nm = nmap.PortScanner()
		nm.scan(hosts=red, arguments='-sV')
