# import requests
# import wget
# from os import getcwd, remove, listdir, rmdir
# from shutil import rmtree, move
# from zipfile import ZipFile
# from pathlib import Path
# from configparser import ConfigParser


# config_auto_update_file = getcwd() + r'/config-auto-update.ini'
# config = ConfigParser(interpolation=None)
# config.read(config_auto_update_file)
# filename_compressed_path = getcwd() + r'/' + config.get('File', 'id') + r'-main.zip'
# dir_uncompressed_path = getcwd() + r'/' + config.get('File', 'id') + r'-main'
# junk_files = [
#     filename_compressed_path,
#     dir_uncompressed_path]
# url_last_readme = r'https://github.com/JonaRanto/' + config.get('File', 'id') + r'/raw/main/README.md'
# url_app = r'https://github.com/JonaRanto/' + config.get('File', 'id') + r'/archive/refs/heads/main.zip'


# def verificar_version():
#     print('Verificando versión')
#     page = requests.get(url_last_readme)
#     last_version = page.text.split('\n')[1].split('=')[1]
#     if not Path(getcwd() + r'/README.md').is_file():
#         resp = False
#     else:
#         my_readme = open('README.md', 'r')
#         my_version = my_readme.read().split('\n')[1].split('=')[1]
#         my_readme.close()
#         resp = False
#         if my_version == last_version: resp = True
#     return resp


# def descargar_ultima_version():
#     print('Descargando ultima version')
#     try:
#         wget.download(url_app, getcwd())
#         print('')
#         resp = True
#     except:
#         print('Ha ocurrido un error al descargar la ultima version')
#         resp = False
#     return resp
    

# def descomprimir_zip():
#     print('Descomprimiendo archivos')
#     try:
#         zip_file = ZipFile(filename_compressed_path, "r")
#         zip_file.extractall(path=getcwd())
#         # Mover todos los archivos de la carpeta que se descomprimió a la carpeta raíz
#         file_list = listdir(dir_uncompressed_path)
#         for file in file_list:
#             move(dir_uncompressed_path + r'/' + file, getcwd() + r'/' + file)
#         resp = True
#     except:
#         print('Ha ocurrido un error al descomprimir')
#         resp = False
#     return resp


# def eliminar_archivos_basura():
#     print('Eliminando archivos basura')
#     try:
#         for junk_file in junk_files:
#             if Path(junk_file).is_file():
#                 remove(junk_file)
#             elif Path(junk_file).is_dir():
#                 rmdir(junk_file)
#         resp = True
#     except:
#         print('Ha ocurrido un error al intentar eliminar los archivos basura')
#         resp = False
#     return resp


# def eliminar_todo():
#     try:
#         print('Eliminando archivos')
#         rmtree(getcwd(), ignore_errors=True)
#         resp = True
#     except:
#         resp = False
#     return resp


# if not verificar_version():
#     if eliminar_todo():
#         if descargar_ultima_version():
#             if descomprimir_zip():
#                 if eliminar_archivos_basura():
#                     print('Se ha actualizado correctamente!')
# else:
#     print('La aplicación está actualziada ^^')
