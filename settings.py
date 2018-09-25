import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DADOS_PU = [
    # o primeiro item corresponde ao sbase
    100000,
    # do segundo item em diante são as vbase de cada setor (começando da slack)
    19000,
    500,
]

installed_apps = [
    'elementos',
    'mecanicas',

]