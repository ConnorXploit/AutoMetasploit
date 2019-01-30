class Dispositivo():
	
	def __init__(self, host='', os='', puertos_abiertos=[], servicios={}, nombre=''):
		self.host = host
		self.os = os
		self.puertos_abiertos = puertos_abiertos
		self.servicios = servicios
		self.nombre = nombre
	
	def set_nombre(self, nombre):
		self.nombre = nombre

	def set_puerto_abierto(self, puerto):
		if not puerto in self.puertos_abiertos:
			self.puertos_abiertos.append(puerto)

	def set_servicio_abierto(self, puerto, servicio):
		if self.servicios:
			for p_serv in self.servicios.keys():
				if p_serv == puerto:
					self.servicios[a] = servicio
		else:
			self.servicios[puerto] = servicio

	def set_nombre(self, nombre):
		self.nombre = nombre