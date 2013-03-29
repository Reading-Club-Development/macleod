'''
Created on 2013-03-22

@author: Torsten Hahmann
'''

import sys
from src.ClifModuleSet import ClifModuleSet

if __name__ == '__main__':
    import sys
    # global variables
    options = sys.argv
    options.reverse()
    options.pop()
    m = ClifModuleSet(options.pop())

    if '-cumulate' in options:
        # translate into a single tptp file
        file = m.get_single_ladr_file()
        print ""
        print "+++++++++++++++++++++"
        print "Files created:"
        print ""
        print file
        print "+++++++++++++++++++++"
    else:
        files = m.get_ladr_files()
        print ""
        print "+++++++++++++++++++++"
        print "Files created:"
        print ""
        for file in files:
            print file
        print "+++++++++++++++++++++"
   