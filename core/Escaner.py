import nmap
import multiprocessing as mp
import socket

def callback_escanear_red(host, scan_result):
	print('------------------')
	print(host, scan_result)

class Escaner():

	def __init__(self, rango='192.168.1.0/24', params=''):
		self.rango = rango
		self.params = params
		self.output = mp.Queue() # Multiproceso
		hosts = self.enumeracion_rapida()
		for host in hosts:
			self.escanear_host_con_parametros(host, self.params)
		procesos = []
		for host in hosts:
			self.escanear_host_con_parametros(host=self.rango, parametros=self.params)
			#procesos.append(mp.Process(target=self.escanear_host_os, args=(host,)))
			#procesos.append(mp.Process(target=self.escanear_host_name, args=(host,)))
			#procesos.append(mp.Process(target=self.escanear_host_completo, args=(host,)))
		#self.__ejecutar_multiproceso__(procesos)

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
			print('State : {}'.format(nm[host].state()))
			for proto in nm[host].all_protocols():
				print('----------')
				print('Protocol : {}'.format(proto))
				lport = nm[host][proto].keys()
				for port in lport:
					servicio = ''
					if nm[host][proto][port]['state'] == 'open':
						if proto == 'tcp':
							servicio = self.escanear_host_tcp_banner_grabbing(host, port)
							if not servicio or servicio == '' or 'None' in servicio or servicio == None: # Si no devuelve banner
								servicio = '-'
						print ('puerto : {}\tservicio: {}'.format(port, servicio))

	def escanear_host_tcp_banner_grabbing(self, host, port):
		try:
			conexion=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			conexion.connect((host, port))
			banner = conexion.recv(1024)
			# Devolvemos decodificada para evitar b'' como string y quitamos el salto de línea posible
			return str(banner.decode('utf-8').rstrip('\n'))
		except:
			return

	def escanear_host_tcp(self, host):
		pass

	def escanear_host_udp(self, host):
		pass

	def __ejecutar_multiproceso__(self, procesos):
		for p in procesos:
			p.start()
		for p in procesos:
			p.join()
