#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import multiprocessing as mp

# Mi CORE
from core import Config
from core.Menu import Menu
from core.Escaner import Escaner
from core.Dispositivo import Dispositivo

from modulos.Interfaces import Interfaces

class AutoMetasploit():
	
	def __init__(self):
		self.__cargarConfiguracion()
		self.__cargarParametros()
		self.__inicio()

	#
	# Toda la configuracion se carga aqui en variables de clase
	#
	def __cargarConfiguracion(self):
		# Cada clase, una variable de configuración
		self.config = Config.Config
		self.configInterfaces = Config.ConfigInterfaces
		self.configNmap = Config.ConfigNmap
		self.configErrores = Config.ConfigErrores

	def __cargarParametros(self):
		# Configuracion General
		self.interfaces = Interfaces()
		self.coreMenu = Menu()

		# Configuracion Interfaces
		self.mi_ip = self.configInterfaces.mi_ip
		self.interfaces_mi_pc = self.configInterfaces.interfaces_mi_pc
		self.parametros_obligatorios_interfaces = self.configInterfaces.PARAMETROS_OBLIGATORIOS

		# Configuracion Nmap
		self.parametros_nmap = self.configNmap.PARAMETROS
		self.parametros_obligatorios_nmap = self.configNmap.PARAMETROS_OBLIGATORIOS
		self.parametros_predefinidos_nmap = self.configNmap.FIJOS

		# Variables finales necesarias para conjugacion de datos
		self.interfaces_selec = []
		self.parametros_nmap_selec = []

		self.output = mp.Queue() # Multiproceso

	def get_parametros_seleccionador(self, lista, seleccionados):
		lista_selec = []
		cont=0
		for param in lista:
			if cont in seleccionados:
				lista_selec.append(param)
			cont+=1
		return lista_selec

	#
	# Inicio del programa principal
	#
	def __inicio(self):
		self.elegirInterfaz()
		self.elegirParametrosNmap()
		self.iniciarEscaneo()

	def elegirInterfaz(self):
		self.coreMenu.elegirOpcionMenu(
			parametros=self.interfaces_mi_pc, 
			parametros_selec=self.interfaces_selec, 
			param_obligatorios=self.parametros_obligatorios_interfaces)
		
	def elegirParametrosNmap(self):
		print("PARAMS:{}".format(self.parametros_predefinidos_nmap))
		self.coreMenu.elegirOpcionMenu(
			parametros=self.parametros_nmap, 
			parametros_selec=self.parametros_nmap_selec, 
			param_obligatorios=self.parametros_obligatorios_nmap, 
			predefinidos=self.parametros_predefinidos_nmap)

	def iniciarEscaneo(self):
		interfaces_params = self.get_parametros_seleccionador(lista=self.interfaces_mi_pc, seleccionados=self.interfaces_selec)
		nmap_params = self.get_parametros_seleccionador(lista=self.parametros_nmap, seleccionados=self.parametros_nmap_selec)
		nmap_params = ' '.join(nmap_params)
		procesos = []
		for inter in interfaces_params:
			procesos.append(mp.Process(target=Escaner, args=(inter, nmap_params)))
		for p in procesos:
			p.start()
		for p in procesos:
			p.join()

if __name__ == '__main__':
	script = AutoMetasploit()

# TODO Segun configuracion deberia auto importar el orden lo los menus y automaticamente coger la configuracion el AutoMetasploit() en el inicio recursivamente segun los metodos publicos de cada modulo
# TODO Solucionar que se cierren los multiprocesos al salir