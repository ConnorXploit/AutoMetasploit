import os

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

		# Modulos
		self.interfaces = Interfaces()

	def __cargarParametros(self):
		# Configuracion General
		self.coreMenu = Menu()

		# Configuracion Interfaces
		self.mi_ip = self.configInterfaces.mi_ip
		self.interfaces_mi_pc = self.configInterfaces.interfaces_mi_pc
		self.parametros_obligatorios_interfaces = self.configInterfaces.PARAMETROS_OBLIGATORIOS

		# Configuracion Nmap
		self.parametros_nmap = self.configNmap.PARAMETROS
		self.parametros_obligatorios_nmap = self.configNmap.PARAMETROS_OBLIGATORIOS
		
		# Cargamos un scanner de Nmap
		self.scanner = Escaner(self.mi_ip)

		# Variables finales necesarias para conjugacion de datos
		self.interfaces_selec = []
		self.parametros_nmap_selec = []

	#
	# Inicio del programa principal
	#
	def __inicio(self):
		self.elegirInterfaz()
		self.elegirParametrosNmap()

	def elegirInterfaz(self):
		self.coreMenu.elegirOpcionMenu(parametros=self.interfaces_mi_pc, parametros_selec=self.interfaces_selec, param_obligatorios=self.parametros_obligatorios_interfaces)
		
	def elegirParametrosNmap(self):
		self.coreMenu.elegirOpcionMenu(parametros=self.parametros_nmap, parametros_selec=self.parametros_nmap_selec, param_obligatorios=self.parametros_obligatorios_nmap)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

if __name__ == '__main__':
	script = AutoMetasploit()

# TODO Segun configuracion deberia auto importar el orden lo los menus y automaticamente coger la configuracion el AutoMetasploit() en el inicio recursivamente segun los metodos publicos de cada modulo