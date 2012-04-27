import os
import sys
import subprocess
import json

VIMUTILS_DEFAULT_RC = os.path.join(os.environ["HOME"], ".vimutilsrc")

class VimUtils(object):

    def __init__(self,rcfile=VIMUTILS_DEFAULT_RC):
        self.rcfile = rcfile
        f = open(rcfile,"r")
        self.rc = json.loads(f.read())
        f.close()


    def write_rc(self):
        f = open(self.rcfile,"w")
        f.write(json.dumps(self.rc))
        f.close()

    def servers(self):
        try:
            result = subprocess.check_output([self.rc["vim_cmd"], "--serverlist"]).strip().split("\n")
            return result
        except:
            return None

    def start_server(self, servername=None):
        if servername == None:
            servername = self.rc["default_server"]
        if servername in self.servers():
            return False
        else:
            cmdstr = "%s --servername %s" % (self.rc["vim_cmd"], servername)
            return 0 == os.system(cmdstr)


    def has_server(self, servername):
        if servername in self.servers():
            return True
        else:
            return False

    def open_files(self, files, servername=None):
        if servername == None:
            servername = self.rc["default_server"]
        for f in files:
            f = os.path.realpath(f)
            cmds = [self.rc["vim_cmd"], "--servername", servername, "--remote-send", "<ESC>:e %s <CR>" % (f)]
            if subprocess.call(cmds) != 0:
                raise Exception
        return True

    def open_tabs(self, files, servername=None):
        if servername == None:
            servername = self.rc["default_server"]
        cmdstr = "%s --servername %s --remote-tab-silent " % (self.rc["vim_cmd"], servername)
        for f in files:
            cmdstr += " " + f + " "
        if os.system(cmdstr) != 0:
            raise Exception

    def buffers(self, servername=None):
        if servername == None:
            servername = self.rc["default_server"]
        return subprocess.check_output([
                self.rc["vim_cmd"],"--servername", servername, "--remote-expr", "VimUtilsCommandOutput(\":buffers\")"]) 

    def dump_buffer(self, bufno, servername=None):
        if servername == None:
            servername = self.rc["default_server"]
        filename = subprocess.check_output([
                    self.rc["vim_cmd"],
                    "--servername",
                    servername,
                    "--remote-expr",
                    "VimUtilsWriteBufferToTmpFile(\"%s\")" % (str(bufno))
                ]).strip()
        f = open(filename, "r")
        contents = f.read()
        f.close()
        return contents
            


            



