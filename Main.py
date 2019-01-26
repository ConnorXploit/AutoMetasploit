import nmap
import socket
import os
from netaddr import IPNetwork

import netifaces

class Escaner():
	def __init__(self, rango):
		pass
	def escanearRed(self, red): #192.168.1.0/24
		nm = nmap.PortScanner()
		nm.scan(hosts=red, arguments='-sV')
	
class Dispositivo():
	pass

class Programa():
	
	mi_ip = ''

	parametros = {
		'-O':'Sistema Operativo', 
		'-A': 'All', 
		'-sV':'Version de Protocolos'
	}

	interfaces_selec = []
	parametros_selec = []

	def __init__(self):
		self.inicio()
	
	def menu_parametros(self, error=False):
		cls()
		print('Herramienta automatica de escaneos ({})'.format(self.mi_ip))
		print('')
		self.funcionesNmap()
		print('')
		if error:
			print('Has elegido una opción incorrecta')

	def menu_interfaces(self):
		cls()
		self.get_subred()
		print('Herramienta automatica de escaneos ({})'.format(self.mi_ip))
		print('')
		print('\tElegir objetivo')
		cont=0
		seleccionado=' '
		for interfaz in self.interfaces_mi_pc:
			print('\t\t{} [ {} ] - {}'.format(cont, seleccionado, interfaz))
			cont+=1
		print('')
		# Poner continuar solo si está seleccionado alguno
		print('\t\t{} - Continuar'.format(cont))

	def get_my_ip(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		self.mi_ip = s.getsockname()[0]
		s.close()

	def funcionesNmap(self):
		cont=0
		for param in self.parametros:
			seleccionado=' '
			for p in self.parametros_selec:
				if p == cont:
					seleccionado = '*'
			print('\t{} [ {} ] - ({}) {}'.format(cont, seleccionado, param, self.parametros[param]))
			cont+=1

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

	# Modular - Llamado por elegirObjetivo y seleccion escaneo
	def seleccion_param(self, seleccion, opciones, listaSelect):
		if seleccion >= 0 and seleccion <= len(opciones)-1:
			borrado=False
			for param in listaSelect:
				if seleccion == param:
					borrado=True
					listaSelect.remove(seleccion)
				else:
					estaLibre=False
			if not borrado:
				listaSelect.append(seleccion)
		else:
			print('Seleccion incorrecta')

	def elegirObjetivo(self):
		seleccion = self.seleccionEscaneo(self.menu_interfaces, self.interfaces_selec)
		if seleccion == str(len(self.interfaces_mi_pc)):
			pass
		else:
			self.seleccion_param(seleccion, self.interfaces_mi_pc, self.interfaces_selec)
			self.elegirObjetivo()
		
	def seleccionEscaneo(self, menu, lista_seleccionados):
		menu.__call__()
		seleccion =''
		try:
			seleccion = input('Selecciona una opción: ')
			return int(seleccion)
		except ValueError:
			if seleccion.lower() == 'scan':
				pass
			else: 
				menu.__call__(True)
		try:
			self.seleccion_param(seleccion_parametro, self.parametros, lista_seleccionados)
			self.seleccionEscaneo()
		except:
			self.seleccionEscaneo(menu, lista_seleccionados)

	def inicio(self):
		self.get_my_ip()
		self.elegirObjetivo()
		self.seleccionEscaneo(self.menu_parametros, self.parametros_selec)

def cls():
    #os.system('cls' if os.name=='nt' else 'clear')
	pass

programa = Programa()
