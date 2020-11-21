# install app to dektop Ubuntu
import os

contents = """#!/usr/bin/env xdg-open
[Desktop Entry]
Version=1.0
Type=Application
Terminal=True
"""

contents2 = """#!/bin/bash
. /opt/ros/melodic/setup.bash;

"""
app_name = "ARTIV_BRIDGE"
exec_cmd = os.path.join(os.getcwd(), "start.sh")
Icon = os.path.join(os.getcwd(), "icon.ico")

contents+="\n" + "Exec=" + exec_cmd + "\n" + "Name=" + app_name  + "\n" + "Icon=" + Icon
cwd = os.path.expanduser("~")
f = open(os.path.join(cwd+"/Desktop/", app_name+".desktop"), 'w')
f.write(contents)
f.close()

f = open(os.path.join(os.getcwd(), "start.sh"), 'w')
contents2+="\n" + "cd " + os.getcwd() + ";\n" + "python artiv_bdg.py"
f.write(contents2)
f.close()



print("Allowing executing file as program ")
os.system("sudo chmod +x " + os.path.join(os.getcwd(), "start.sh"))
os.system("sudo chmod +x ~/Desktop/" + app_name+".desktop")



"""
Exec=/snap/bin/skype
Name=Skype
Icon=/snap/skype/23/usr/share/icons/hicolor/256x256/apps/skypeforlinux.png
"""
