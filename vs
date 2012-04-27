#!/usr/bin/env python
import vimutils
import sys

def usage():
    print("""
Starts a vim instance as a server with name [SERVER NAME]
Usage: vs [SERVER NAME]        
    """)

def main():
    try:
        server = sys.argv[1]
        v = vimutils.VimUtils()
        if v.start_server(server) == False:
            print("Server %s already running." % (server))
            usage()
    except:
        usage()


main()
    


