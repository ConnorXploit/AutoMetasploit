class Config:
    APP_NAME = 'AutoMetasploit'
    CREADOR = 'ConnorXploit'
    TITULO = 'Herramienta automatica de escaneos'
    CONTINUAR = 'Continuar'
    SELECCIONA = 'Selecciona una opción'
    SIMBOLO_SELEC = '*'
    SALIR = 'Saliendo de AutoMetasploit...'
    
class ConfigInterfaces:
    PARAMETROS_OBLIGATORIOS = True

class ConfigNmap:
    PARAMETROS_OBLIGATORIOS = True
    PARAMETROS = {
        '-A': 'All',
        '-O': 'Sistema Operativo', 
        '-sV': 'Versión de Protocolos',
        '-T0': 'Paranóico',
        '-T1': 'Sigiloso',
        '-T2': 'Delicado',
        '-T3': 'Normal',
        '-T4': 'Agresivo',
        '-T5': 'Demente',
        '--script=banner': 'Banner Grabbing'
    }
    PARAMETROS_DESCUBRIR_SISTEMAS = {
        '-PS': 'n TCP SYN ping',
        '-PA': 'n ping TCP ACK',
        '-PU': 'n ping UDP', 
        '-PM': 'Netmask Req',
        '-PP': 'Timestamp Req',
        '-PE': 'Echo Req',
        '-sL': 'Análisis de listado',
        '-PO': 'Ping por Protocolo',
        '-PN': 'No hacer ping',
        '-n': 'No hacer DNS',
        '-R': 'Resolver DNS en todos los sistemas objetivo',
        '--traceroute': 'Trazar ruta al sistema (para topologías de red)',
        '-sP': 'Realizar ping, igual que con –PP –PM –PS443 –PA80',
    }
    PARAMETROS_ANALISIS_PUERTOS = {
        '-sS': 'Análisis TCP CONNECT',
        '-sT': 'Análisis UDP',
        '-sU': 'Análisis SCTP INIT', 
        '-sY': 'COOKIE ECHO de SCTP',
        '-sZ': 'Protocolo IP',
        '-sO': 'Echo Req',
        '-sW': 'Ventana TCP -sN',
        '-sF': 'NULL, FIN, XMAS',
        '-sX': 'NULL, FIN, XMAS',
        '-sA': 'TCP ACK',
    }
    PARAMETROS_PUERTOS_A_ANALIZAR = {
        '-F': 'Rápido, los 100 comunes',
        '--top-ports': 'Los puertos mas usados',
        '-r': 'No aleatorio',
    }
    PARAMETROS_DURACION_EJECUCION = {
        '-T0': 'Paranoico',
        '-T1': 'Sigiloso',
        '-T2': 'Sofisticado',
        '-T3': 'Normal',
        '-T4': 'Agresivo',
        '-T5': 'Locura',
        '--min-hostgroup': '',
        '--max-hostgroup': '',
        '--min-rate': '',
        '--max-rate': '',
        '--min-parallelism': '',
        '--max-parallelism': '',
        '--min-rtt-timeout': '',
        '--max-rtt-timeout': '',
        '--initial-rtt-timeout': '',
        '--max-retries': '',
        '--host-timeout': '',
        '--scan-delay': '',
    }
    PARAMETROS_SERVICIOS_Y_VERSIONES = {
        '-sV': 'Detección de la versión de servicios',
        '--all-ports': 'No excluir puertos',
        '--version-all': 'Probar cada exploración',
        '--version-trace': 'Rastrear la actividad del análisis de versión',
        '-O': 'Activar detección del S. Operativo',
        '--fuzzy': 'Adivinar detección del SO',
        '--max-os-tries': 'Establecer número máximo de intentos contra el sistema objetivo',
    }
    PARAMETROS_EVADIR_FW_Y_IDS = {
        '-f': 'Fragmentar paquetes',
        '-D': 'd1,d2 encubrir análisis con señuelos',
        '-S': 'IP falsear dirección origen',
        '-g': 'Source falsear puerto origen',
        '--randomize-hosts': 'Orden',
        '--spoof-mac': 'MAC cambiar MAC de origen',
    }
    PARAMETROS_OTRAS_OPCIONES = {
        '-6': 'Activar análisis IPV6',
        '-A': 'Agresivo, igual que con -O -sV -sC --traceroute'
    }
    PARAMETROS_OPCIONES_INTERACTIVAS = {
        'v/V': 'Aumentar/Disminuir nivel de detalle del análisis',
        'p/P': 'Activar/Desactivar traza de paquetes'
    }
    PARAMETROS_SCRIPTS = {
        '-sC': 'realizar análisis con los scripts por defecto',
        '-script': 'Ejecutar script (o todos)',
        '--script-trace': 'Mostrar comunicación entrante y saliente',
    }
    FIJOS = ('-A', '-T3')
    TIPOS_ESCANEOS = ('Descubrir sistemas', 'Analisis de Puertos', 'Puertos a Analizar', 'Duración de Ejecución', 'Servicios y Versiones', 'Evadir FW y IDS', 'Otros opciones', 'Opciones interactivas', 'Scripts')

class ConfigErrores:
    ERROR = 'ERROR'
    NO_CONTROLADO = 'No controlado'
    SELEC_INC = 'Seleccion incorrecta'
    PARAMETRO_OBLIGATORIO = 'Debes seleccionar al menos una opcion del menu'

def print_classes():
    import sys, inspect
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            print(obj)