import os
import sys
import subprocess
import json
import re

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

    def run_command(self,command,servername=None):
        if servername == None:
            servername = self.rc["default_server"]
    
        return subprocess.check_output([
                self.rc["vim_cmd"],
                "--servername",
                servername,
                "--remote-expr",
                "VimUtilsCommandOutput(\"%s\")" % command])
    

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



    def buffers_object(self,servername=None):
        if servername == None:
            servername = self.rc["default_server"]
        outp = self.run_command("buffers", servername)
        
        lines = outp.strip().split("\n")
        bufs = []

        for line in lines:
            bufar = re.split('\s+',line.strip().replace("line",""))
            if len(bufar) == 3:
                bufar.insert(1,"") #If theres no mode, insert None
            bufar[2] = bufar[2].replace("\"", "")

            buf = {
                "id" : int(bufar[0]),
                "mode" : bufar[1],
                "file" : bufar[2],
                "line" : bufar[3],
                "unlisted" : False,
                "current" : False,
                "alternate" : False,
                "active" : False,
                "hidden" : False,
                "modifiable" : True,
                "readonly" : False,
                "modified" : False,
                "readerrors" : False
            }

            for m in bufar[1]:
                if m == "u":
                    buf["unlisted"] = True
                elif m == "%":
                    buf["current"]  = True
                elif m == "#":
                    buf["alternate"] = True
                elif m == "a":
                    buf["active"] = True
                elif m == "h":
                    buf["hidden"] = True
                elif m == "-":
                    buf["modifiable"] = False
                elif m == "=":
                    buf["readonly"] = True
                elif m == "+":
                    buf["modified"] = True
                elif m == "x":
                    buf["readerror"] = True
                else:
                    continue

            bufs.append(buf)
            
        return bufs



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
            


    def get_session(self,servername=None):
        if servername == None:
            servername = self.rc["default_server"]
        out = []
        for buf in self.buffers_object(servername):
            buf["content"] = self.dump_buffer(buf["id"])
            out.append(buf)
        return out
            



