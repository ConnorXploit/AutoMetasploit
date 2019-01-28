import os
import sys
import socket
from core.Config import Config, ConfigInterfaces, ConfigErrores
#
# Menus para la shell llamados desde __seleccionar_menu() pasado como parametro
#
class Menu:

	def __init__(self):
		self.__cargarConfiguracion()

	def __cargarConfiguracion(self):
		self.config = Config
		self.titulo = self.config.TITULO
		self.configErrores = ConfigErrores

	def __titulo(self):
		print('')
		print('{titulo} ({ip})'.format(titulo=self.titulo, ip=self.mi_ip))
		print('')

	def __getip(self):
		self.mi_ip = ConfigInterfaces.mi_ip

	def __menu(self, parametros, parametros_selec, error=False, msg_error=''):
		cls()
		self.__getip()
		self.__titulo()
		self.__opciones(parametros=parametros, parametros_selec=parametros_selec, error=error, msg_error=msg_error)

	def __opciones(self, parametros, parametros_selec, error=False, msg_error=''):
		cont=0
		for param in parametros:
			seleccionado=' '
			for p in parametros_selec:
				if p == cont:
					seleccionado = '{simbolo_selec}'.format(simbolo_selec=self.config.SIMBOLO_SELEC)
			try:
				print('\t{cont} [ {seleccionado} ] - ({param}) {definicion}'.format(cont=cont, seleccionado=seleccionado, param=param, definicion=parametros[param]))
			except:
				print('\t\t{cont} [ {seleccionado} ] - {param}'.format(cont=cont, seleccionado=seleccionado, param=param))
			cont+=1
		print('')
		if error:
			if msg_error == '':
				msg_error = self.configErrores.NO_CONTROLADO
			print('\t[{error}] - {msg_error}'.format(error=self.configErrores.ERROR, msg_error=msg_error))
			print('')
		print('\t\t{cont} - {continuar}'.format(cont=cont, continuar=self.config.CONTINUAR))

	def __seleccion_param(self, seleccion, opciones, listaSelect):
		cont=0
		for op in opciones:
			cont+=1
		try:
			seleccion = int(seleccion)
		except:
			pass
		if isinstance(seleccion, int) and int(seleccion) >= 0 and int(seleccion) <= cont:
			borrado=False
			for param in listaSelect:
				if seleccion == param:
					borrado=True
					listaSelect.remove(seleccion)
				else:
					estaLibre=False
			if not borrado:
				listaSelect.append(seleccion)
			return ''
		else:
			return self.configErrores.SELEC_INC

	def __seleccionar_menu(self, parametros, lista_seleccionados, error=False, msg_error=''):
		self.__menu(parametros=parametros, parametros_selec=lista_seleccionados, error=error, msg_error=msg_error)
		seleccion =''
		msg_error=''
		error=False
		try:
			seleccion = input('{selecciona}: '.format(selecciona=self.config.SELECCIONA))
			return seleccion
			seleccion = int(seleccion)
		except KeyboardInterrupt:
			self.salir()
		except ValueError:
			msg_error = '{selec_inc}'.format(selec_inc=self.configErrores.SELEC_INC)
			error = True
		try:
			msg_error = self.__seleccion_param(seleccion=seleccion, opciones=parametros, listaSelect=lista_seleccionados)
			if msg_error != '':
				error = True
			self.__seleccionar_menu(parametros=parametros, lista_seleccionados=lista_seleccionados, error=error, msg_error=msg_error)
		except:
			self.__seleccionar_menu(parametros=parametros, lista_seleccionados=lista_seleccionados, error=error, msg_error=msg_error)
		

	def elegirOpcionMenu(self, parametros, parametros_selec, param_obligatorios, error=False, msg_error=''):
		cls()
		seleccion = self.__seleccionar_menu(parametros=parametros, lista_seleccionados=parametros_selec, error=error, msg_error=msg_error)
		cont=0
		for p in parametros:
			cont+=1
		if str(seleccion) in str(cont):
			if not parametros_selec:
				msg_error = '{param_obligatorio}'.format(param_obligatorio=self.configErrores.PARAMETRO_OBLIGATORIO)
				error = True
				self.elegirOpcionMenu(parametros=parametros, parametros_selec=parametros_selec, param_obligatorios=param_obligatorios, error=error, msg_error=msg_error)
			else:
				pass # Siguiente funcion de inicio() de la clase Programa()
		else:
			msg_error = ''
			error = False
			msg_error = self.__seleccion_param(seleccion=seleccion, opciones=parametros, listaSelect=parametros_selec)
			if msg_error != '':
				error = True
			self.elegirOpcionMenu(parametros=parametros, parametros_selec=parametros_selec, param_obligatorios=param_obligatorios, error=error, msg_error=msg_error)

	def salir(self):
		cls()
		print('')
		print('{salir}'.format(salir=self.config.SALIR))
		sys.exit()

def cls():
    #os.system('cls' if os.name=='nt' else 'clear')
	pass