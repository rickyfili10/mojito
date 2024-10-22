from lib.mojstd.py import *
from bootCheck import *
import os

BootCheck() # Return True, so in case of plugin to start at boot it boot it 
execPlugins() 
  
returner()
os.system("sudo python menu.py")
