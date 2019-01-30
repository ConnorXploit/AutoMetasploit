import nmap
import multiprocessing as mp
import socket
import codecs
import sys

# Mi CORE
from core.Config import Config

def callback_escanear_red(host, scan_result):
	print('------------------')
	print(host, scan_result)

class Escaner():

	def __init__(self, rango='192.168.1.0/24', params=''):
		self.rango = rango
		self.params = params
		self.config = Config
		self.output = mp.Queue() # Multiproceso
		hosts = self.enumeracion_rapida()
		#for host in hosts:
		#	self.escanear_host_con_parametros(host, self.params)
		procesos = []
		for host in hosts:
			#self.escanear_host_con_parametros(host=self.rango, parametros=self.params)
			procesos.append(mp.Process(target=self.escanear_host_con_parametros, args=(host, self.params)))
			#procesos.append(mp.Process(target=self.escanear_host_os, args=(host,)))
			#procesos.append(mp.Process(target=self.escanear_host_name, args=(host,)))
			#procesos.append(mp.Process(target=self.escanear_host_completo, args=(host,)))
		self.__ejecutar_multiproceso__(procesos)

	def enumeracion_rapida(self):
		print('[*] - Enumerando rápidamente la red ({rango} {argumento})'.format(rango=self.rango, argumento='-sP'))
		nm = nmap.PortScanner()
		nm.scan(hosts=self.rango, arguments='-sP')
		hosts = nm.all_hosts()
		return hosts

	def escanear_host_completo(self, host):
		print('[*] - Escaneando host completo ({host})'.format(host=host))
		nm = nmap.PortScanner()
		nm.scan(host, arguments='-A')
		try:
			print(nm[host])
		except:
			print(nm)

	def escanear_host_os(self, host):
		print('[*] - Buscando versión de SO ({host})'.format(host=host))
		nm = nmap.PortScanner()
		nm.scan(host, arguments='-O')
		try:
			print(nm[host])
		except:
			print(nm)

	def escanear_host_name(self, host):
		print('[*] - Buscando nombre del dispositivo ({host})'.format(host=host))
		nm = nmap.PortScanner()
		nm.scan(host, arguments='-sL')
		try:
			print(nm[host])
		except:
			print(nm)

	def escanear_host_con_parametros(self, host, parametros):
		print('[*] - Escaneo con Parámetros ({host} {param})'.format(host=host, param=parametros))
		nm = nmap.PortScanner()
		res = nm.scan(host, arguments=parametros)
		for host in nm.all_hosts():
			print('----------------------------------------------------')
			print('Host : {} ({})'.format(host, nm[host].hostname()))
			if 'up' in nm[host].state():
				for proto in nm[host].all_protocols():
					print('----------')
					print('Protocol : {}'.format(proto))
					lport = nm[host][proto].keys()
					for port in lport:
						servicio = ''
						if nm[host][proto][port]['state'] == 'open':
							servicio = self.escanear_host_tcp_banner_grabbing(host, port)
							print('SERVICIO: {}'.format(servicio))
							try:
								if not servicio or servicio == '' or 'None' in servicio or servicio == None: # Si no devuelve banner
									servicio = '-'
							except:
								pass
							print ('puerto : {}\tservicio: {}'.format(port, servicio))

	def escanear_host_tcp_banner_grabbing(self, host, port):
		banner = ''
		try:
			conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			conn.connect((host, port))
			print('[+] Conexion con {}:{} valida'.format(host, str(port)))
			conn.settimeout(60)
			banner = conn.recv(1024)
			return banner.strip()
			#return codecs.encode(banner, 'hex_codec')
			#return str(banner.decode('utf-8').rstrip('\n'))
		except Exception as e:
			print('[+] Conexion con {}:{} fallida: {}'.format(host, str(port), e))
		finally:
			conn.close()
			return banner

	def escanear_host_tcp(self, host):
		pass

	def escanear_host_udp(self, host):
		pass

	def __ejecutar_multiproceso__(self, procesos):
		try:
			for p in procesos:
				p.start()
			for p in procesos:
				p.join()
		except KeyboardInterrupt:
			self.salir()

	def salir(self):
		cls()
		print('')
		print('{salir}'.format(salir=self.config.SALIR))
		sys.exit()

def cls():
	os.system('cls' if os.name=='nt' else 'clear')
