import os
import shutil
import subprocess
import sys

from common import print_and_delete, check_dll_is_static

os.chdir(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Cleanup
print_and_delete('Removing @Pythia.zip', '@Pythia.zip')
print_and_delete('Removing Pythia Python 64-bit installation', '@Pythia', 'python-37-embed-amd64')
print_and_delete('Removing Pythia Python 32-bit installation', '@Pythia', 'python-37-embed-win32')
print_and_delete('Removing 32-bit Pythia binaries', 'vcproj')
print_and_delete('Removing 64-bit Pythia binaries', 'vcproj64')

subprocess.run([sys.executable, os.path.join('tools', 'make_pbos.py')], check=True)
subprocess.run([sys.executable, os.path.join('tools', 'create_embedded_python.py'), '@Pythia'], check=True)

# Build 32-bit
print('Building 32-bit Pythia')
os.mkdir('vcproj')
os.chdir('vcproj')
subprocess.run(['cmake', '..', '-G', 'Visual Studio 15 2017'], check=True)
os.chdir('..')
subprocess.run(['cmake', '--build', 'vcproj', '--config', 'RelWithDebInfo'], check=True)

# Build 64-bit
print('Building 64-bit Pythia')
os.mkdir('vcproj64')
os.chdir('vcproj64')
subprocess.run(['cmake', '..', '-G', 'Visual Studio 15 2017 Win64'], check=True)
os.chdir('..')
subprocess.run(['cmake', '--build', 'vcproj64', '--config', 'RelWithDebInfo'], check=True)

# Post-build safety checks
check_dll_is_static(os.path.join('@Pythia', 'Pythia.dll'), allowed_imports=[b'python37.dll'])
check_dll_is_static(os.path.join('@Pythia', 'Pythia_x64.dll'), allowed_imports=[b'python37.dll'])
check_dll_is_static(os.path.join('@Pythia', 'PythiaSetPythonPath.dll'))
check_dll_is_static(os.path.join('@Pythia', 'PythiaSetPythonPath_x64.dll'))

print('Packing the resulting mod to a zip file')
shutil.make_archive('@Pythia', 'zip', root_dir='.', base_dir='@Pythia')

# TODO: Use an empty directory to build the final mod
# TODO: Fix https://github.com/overfl0/Pythia/issues/41 to build the dlls
