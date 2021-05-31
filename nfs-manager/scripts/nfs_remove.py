#!/usr/bin/env python3

"""
	Cockpit NFS manager - Cockpit plugin for managing NFS.
	Copyright (C) 2021 Sam Silver <ssilver@45drives.com>
	This file is part of Cockpit NFS.
	Cockpit NFS manager is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
	Cockpit NFS manager is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.
	You should have received a copy of the GNU General Public License
	along with Cockpit NFS manager.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
import subprocess
from optparse import OptionParser

# Name: reset_config
# Receives: Nothing
# Does: Export new shared directory as well as restart the nfs system.
# Returns: Nothing
def reset_config():
    try:
        subprocess.run(["exportfs", "-a"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Exporting new share permissions...")
    except OSError:
        print("Could not exportfs -a. Error: " + OSError)
        sys.exit(1)
    try:
        subprocess.run(["systemctl", "restart", "nfs-kernel-system"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Restarting nfs-kernel-system...")
    except OSError:
        print("Could not restart nfs-kernel-system, do you have it on your system?")
        sys.exit(1)

# Name: remove_nfs
# Receives: Name and del_dir
# Does: Parses /etc/exports for the names of NFS(s) to be deleted, remove them from list.
# Then rewrite /etc/exports with new file. Delete directroy if flagged.
# Returns: Nothing
def remove_nfs(name):
    try:
        does_exist = False
        file = open("/etc/exports", "r")
        lines = file.readlines()
        file.close()
        for i in range(0, len(lines), 1):
            if("Name:" in lines[i]):
                if(name + "\n" in lines[i]):
                    print("Removing: " + lines[i])
                    lines.remove(lines[i])
                    print("Removing: " + lines[i])
                    lines.remove(lines[i])
                    does_exist = True
                    break
        
        if does_exist:
            print("Rewriting exports...")
            file = open("/etc/exports", "w")
            file.write("".join(lines))
            file.close()
            reset_config()
        else:
            print("That NFS does not exist.")
            sys.exit(1)

    except OSError:
        print(OSError)
        sys.exit(1) 

# Name: main
# Receives: nothing
# Does: Checks all the arguments and flags. Makes sure the user entered enough
# arguments. Chucks arguments into make_nfs function
# Returns: Nothing
def main():
    parser = OptionParser()
    (options, args) = parser.parse_args()
    if len(args) < 1:
        print("Not enough arguments!\nnfs_remove <name>")
        sys.exit(1)
    remove_nfs(args[0])


if __name__ == "__main__":
    main()
    sys.exit(0)