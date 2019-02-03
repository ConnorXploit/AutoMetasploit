import nmap
import multiprocessing as mp
import socket

import traceback

from flask import jsonify

def callback_escanear_red(host, scan_result):
	print('------------------')
	print(host, scan_result)

class Escaner():

	def __init__(self, rango='192.168.1.0/24', params=''):
		self.rango = rango
		self.params = params
	
	def escanear_todo(self):
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
		nm.scan(hosts=host, arguments=parametros)
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
							servicio = '-'
							if nm[h][proto][port]['state'] == 'open':
								if proto == 'tcp':
									servicio = self.escanear_host_tcp_banner_grabbing(host=h, port=port)
								puertos_abiertos.append({port : servicio})
						datos.append({proto : puertos_abiertos})
					except Exception as e:
						datos.append({'error' : 'Algo ha salido mal'})
			datos_completo.append({h : datos})
		return jsonify(datos_completo)

	def escanear_host_tcp_banner_grabbing(self, host, port):
		banner = ''
		try:
			conexion=socket.socket()
			conexion.settimeout(30)
			conexion.connect((host, int(port)))
			banner = conexion.recv(1024)
			# Devolvemos decodificada para evitar b'' como string y quitamos el salto de línea posible
			banner = str(banner, 'utf-8', 'ignore').split('\n')[0].rstrip('\r')
			conexion.shutdown(1)
			conexion.close()
			#return banner
		except Exception as e:
			banner = '?'
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
