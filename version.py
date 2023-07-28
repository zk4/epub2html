#coding: utf-8
from pathlib import Path
import subprocess
import sys

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green

try:
    head = subprocess.check_output(["git", "rev-parse" ,"HEAD"])
except Exception as e:
    print(R + "not git repository")
    print("make you first git commit!"+W)
    sys.exit(0)

current_commit = head.strip().decode('utf-8')

versionfile = Path("./version")

lines= versionfile.read_text().split("\n")

version = lines[0]
commit = lines[1]
[mainv,modulev,minorv] = version.split(".")
if commit != current_commit:
    minorv=1+int(minorv)
    print("bump minor version")
else:
    print("No git update ,no version change! bye!")
    sys.exit(0)

newversion =f"{mainv}.{modulev}.{minorv}"
versionfile.write_text(newversion+"\n"+current_commit)
print(G + f"{version} -> {newversion}"+ W)
