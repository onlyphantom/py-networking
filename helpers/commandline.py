# Demonstrate the functionality of sys.argv
#
# sys.argv contains the command-line arguments passed to the script
# 
# Example: python helpers/commandline.py -4 target.csv
# Returns: 
#   helpers/commandline.py is the name of the script
#   Number of arguments: 3
#   The arguments are: ['helpers/commandline.py', '-4', 'target.csv']

import sys
print("{} is the name of the script".format(sys.argv[0]))
print("Number of arguments: {}".format(len(sys.argv)))
print("The arguments are: {}".format(str(sys.argv)))