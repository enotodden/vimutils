import os
import sys
import subprocess
import json
import re


def readfile(filename):
    f = open(filename, "r")
    c = f.read()
    f.close()
    return c

def writefile(filename, contents):
    f = open(filename, "w")
    f.write(contents)
    f.close()

VIMUTILS_DEFAULT_RC = os.path.join(os.environ["HOME"], ".vimutilsrc")

class VimUtils(object):

    def __init__(self,servername=None,rcfile=None):
        if rcfile == None:
            rcfile = VIMUTILS_DEFAULT_RC

        self.rcfile = rcfile
        self.rc = json.loads(readfile(self.rcfile))
        self.vim = self.rc["vim_cmd"]
        self.server = self.rc["default_server"]
        if servername != None:
            self.server = servername
    
    def write_rc(self):
        writefile(self.rcfile,json.dumps(self.rc))

    def servers(self):
        try:
            result = subprocess.check_output([self.vim, "--serverlist"]).strip().split("\n")
            return result
        except:
            return None

    def start(self):
        if self.server in self.servers():
            return False
        else:
            cmdstr = "%s --servername %s" % (self.vim, self.server)
            return 0 == os.system(cmdstr)


    def has_server(self, servername):
        if servername in self.servers():
            return True
        else:
            return False

    def run_command(self,command):
        return subprocess.check_output([
                self.vim,
                "--servername",
                self.server,
                "--remote-expr",
                "VimUtilsCommandOutput(\"%s\")" % command])


    def open_file(self,f):
      f = os.path.realpath(f)
      cmds = [self.vim, "--servername", self.server, "--remote-send", "<ESC>:e %s <CR>" % (f)]
      if subprocess.call(cmds) != 0:
        raise Exception
      return True

    def open_files(self, files):
        for f in files:
            f = os.path.realpath(f)
            cmds = [self.vim, "--servername", self.server, "--remote-send", "<ESC>:e %s <CR>" % (f)]
            if subprocess.call(cmds) != 0:
                raise Exception
        return True

    def open_diff_files(self, files):
      self.open_file(files[0])
      for f in files[1:]:
        f  = os.path.realpath(f)
        self.run_command(":diffsplit %s" % (f))


    def open_tabs(self, files):
        cmdstr = "%s --servername %s --remote-tab-silent " % (self.vim, self.server)
        for f in files:
            cmdstr += " " + f + " "
        if os.system(cmdstr) != 0:
            raise Exception


    def buffers(self):
        return subprocess.check_output([
                self.vim,"--servername", self.server, "--remote-expr", "VimUtilsCommandOutput(\":buffers\")"])



    def buffers_object(self):
        outp = self.run_command("buffers")

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



    def dump_buffer(self, bufno):
        filename = subprocess.check_output([
                    self.vim,
                    "--servername",
                    self.server,
                    "--remote-expr",
                    "VimUtilsWriteBufferToTmpFile(\"%s\")" % (str(bufno))
                ]).strip()
        contents = readfile(filename)
        return contents



    def get_session(self):
        out = []
        for buf in self.buffers_object():
            buf["content"] = self.dump_buffer(buf["id"])
            out.append(buf)
        return out


