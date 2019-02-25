import nmap
import multiprocessing as mp
import socket
import json

import traceback

from flask import jsonify

def callback_escanear_red(host, scan_result):
	print('------------------')
	print(host, scan_result)

class Escaner():

	def __init__(self, rango='192.168.1.0/24', params='-sV -T4'):
		self.rango = rango
		self.params = params
	
	def escanear_todo(self):
		self.output = mp.Queue() # Multiproceso
		hosts = self.enumeracion_rapida()
		datos = []
		for host in hosts:
			datos.append(self.escanear_host_con_parametros(host, self.params))
			#procesos.append(mp.Process(target=self.escanear_host_completo, args=(host,)))
		#self.__ejecutar_multiproceso__(procesos)
		return datos

	def enumeracion_rapida(self):
		print('[*] - Enumerando rápidamente la red ({rango} {argumento})'.format(rango=self.rango, argumento='-T4 -n -sn'))
		nm = nmap.PortScanner()
		nm.scan(hosts=self.rango, arguments='-T4 -n -sn')
		hosts = nm.all_hosts()
		return hosts

	def escanear_host_completo(self, host):
		return self.escanear_host_con_parametros(host=host, parametros='-A')

	def escanear_host_os(self, host):
		print('[*] - Buscando versión de SO ({host})'.format(host=host))
		nm = nmap.PortScanner()
		nm.scan(host, arguments='-O')
		print(nm.csv())

	def escanear_host_name(self, host):
		print('[*] - Buscando nombre del dispositivo ({host})'.format(host=host))
		nm = nmap.PortScanner()
		nm.scan(host, arguments='-sL')
		print(nm.csv())

	def escanear_host_con_parametros(self, host, parametros):
		if not host and self.rango:
			host = self.rango
		if not parametros and self.params:
			parametros = self.params
		print('[*] - Escaneo con Parámetros ({host} {param})'.format(host=host, param=parametros))
		nm = nmap.PortScanner()
		nm.scan(hosts=host, arguments=parametros)
		#print(nm.csv())
		datos_completo = []
		for h in nm.all_hosts():
			datos = []
			nombre_host = nm[h].hostname()
			if nombre_host:
				datos.append({'nombre' : nombre_host})

			state = nm[h].state()
			if not 'up' in state:
				datos.append({'estado' : 'apagado'})
			else:
				for proto in nm[h].all_protocols():
					lport = nm[h][proto].keys()
					puertos_abiertos = []
					try:
						for port in lport:
							banner = '-'
							if nm[h][proto][port]['state'] == 'open':
								datos_puerto = []
								if proto == 'tcp' and not '--script=banner' in parametros:
									banner = self.escanear_host_tcp_banner_grabbing(host=h, port=port)
								if banner != '':
									datos_puerto.append({'banner' : banner})
								if nm[h][proto][port]['name']:
									datos_puerto.append({'servicio' : nm[h][proto][port]['name']})
								if nm[h][proto][port]['product']:
									datos_puerto.append({'producto' : nm[h][proto][port]['product']})
								if nm[h][proto][port]['extrainfo']:
									datos_puerto.append({'extrainfo' : nm[h][proto][port]['extrainfo']})
								if nm[h][proto][port]['version']:
									datos_puerto.append({'version' : nm[h][proto][port]['version']})
								if nm[h][proto][port]['conf']:
									datos_puerto.append({'conf' : nm[h][proto][port]['conf']})
								if nm[h][proto][port]['cpe']:
									datos_puerto.append({'cpe' : nm[h][proto][port]['cpe']})
								puertos_abiertos.append({port : datos_puerto})
						datos.append({proto : puertos_abiertos})
					except Exception:
						datos.append({'error' : 'Algo ha salido mal'})
			datos_completo.append({h : datos})
		return datos_completo

	def escanear_host_tcp_banner_grabbing(self, host, port):
		banner = ''
		try:
			conexion=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			conexion.settimeout(2)
			conexion.connect((host, int(port)))
			banner = conexion.recv(1024)
			# Devolvemos decodificada para evitar b'' como string y quitamos el salto de línea posible
			banner = str(banner, 'utf-8', 'ignore').split('\n')[0].rstrip('\r')
			conexion.shutdown(1)
			conexion.close()
			#return banner
		except Exception as e:
			banner = '?'
		if banner == '?':
			banner = self.escanear_host_con_parametros(host, '-p {} -sV --script=banner'.format(port))
		return banner

	def escanear_host_tcp(self, host):
		pass

	def escanear_host_udp(self, host):
		pass

	def __ejecutar_multiproceso__(self, procesos):
		for p in procesos:
			p.start()
		for p in procesos:
			p.join()
