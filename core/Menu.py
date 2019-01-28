import os
import sys
import socket
from core.Config import Config, ConfigErrores
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
		print('{} ({})'.format(self.titulo, self.mi_ip))
		print('')

	def __getip(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		self.mi_ip = s.getsockname()[0]
		s.close()

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
					seleccionado = '*'
			try:
				print('\t{} [ {} ] - ({}) {}'.format(cont, seleccionado, param, parametros[param]))
			except:
				print('\t\t{} [ {} ] - {}'.format(cont, seleccionado, param))
			cont+=1
		print('')
		if error:
			if msg_error == '':
				msg_error = self.configErrores.NO_CONTROLADO
			print('\t[{}] - {}'.format(self.configErrores.ERROR, msg_error))
			print('')
		print('\t\t{} - {}'.format(cont, self.config.CONTINUAR))

	def __seleccion_param(self, seleccion, opciones, listaSelect):
		cont=0
		for op in opciones:
			cont+=1
		if int(seleccion) >= 0 and int(seleccion) <= cont:
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
			seleccion = input('{}: '.format(self.config.SELECCIONA))
			return int(seleccion)
		except KeyboardInterrupt:
			self.salir()
		except ValueError:
			msg_error = '{}'.format(self.configErrores.SELEC_INC)
			error = True
			self.__menu(parametros=parametros, parametros_selec=lista_seleccionados, error=error, msg_error=msg_error)
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
				msg_error = '{}'.format(self.configErrores.PARAMETRO_OBLIGATORIO)
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
		print('{}'.format(self.config.SALIR))
		sys.exit()

def cls():
    os.system('cls' if os.name=='nt' else 'clear')