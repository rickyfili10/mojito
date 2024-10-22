from lib.mojstd.py import *
from bootCheck import *
import os

BootCheck() # Return True, so in case of plugin to start at boot it boot it 
exec_plugins() 
  
returner()
os.system("sudo python menu.py")
