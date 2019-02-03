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
    FIJOS = ('-A', '-T3')

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