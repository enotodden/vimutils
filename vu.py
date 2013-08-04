#!/usr/bin/env python

import os
import sys
import argparse
import re
import json
import subprocess
import StringIO
import time
import tempfile

START_SERVER = "{vim} --servername {servername}"

LIST_SERVERS = "{vim} --serverlist"

RUN_COMMAND = """{vim} --servername {servername} --remote-expr \
'VimUtilsCommandOutput(\"{cmd}\")'"""

OPEN_TABS = """{vim} --servername {servername} --remote-tab-silent {files}"""

OPEN = """{vim} --servername {servername} --remote {files}"""

DUMP_BUFFER = """{vim} --servername {servername} --remote-expr \
'VimUtilsWriteBufferToTmpFile(\"{bufno}\")'"""

SEND_KEYS = """{vim} --servername {servername} --remote-send '{keys}'"""

VIMSCRIPT = """\
function! VimUtilsCommandOutput(cmd)
	redir => message
	silent execute a:cmd
	redir END
	return message
endfunction

"Write a buffer to a tmp file and return the tmp filename
function! VimUtilsWriteBufferToTmpFile(bufno)
python << EOF
import vim
import random
tmpfile = "/tmp/vimutils_" + str(random.randint(1,19928))
current_buffer = str(vim.current.buffer.number)
vim.command(":buffer " + vim.eval("a:bufno"))
vim.command("silent execute \\":write " + tmpfile + "\\"")
vim.command("silent execute \\":buffer " + current_buffer + "\\"")
EOF
	redir => bb
    :py print tmpfile
    redir END
    return bb
endfunction
"""

HELP_SERVERS = "List running vim servers."
HELP_START = "Start a vim server."
HELP_OPEN = "Open file(s)."
HELP_TABS = "Open file(s) in tab(s)."
HELP_DIFF = "Diff files"
HELP_BUFFERS = "List buffers."
HELP_DUMP_BUFFER = "Print the contents of a buffer (by buffer number)"
HELP_GREP = "Search the buffers using a Python regular expression."
HELP_KEYS = "Send a string of keys to the target vim server"
HELP_RUN = "Run a command and print the output."

HELP_SHELL_ALIASES = "Print a set of nice-to-have shell functions for your .(bash|zsh)rc"
HELP_NO_FULL_PATH = "Don't use the full path of this script"



def sh(cmd):
    p = subprocess.Popen(cmd,
                         shell=True,
                         stdout=subprocess.PIPE)
    r = p.wait()
    out, err = p.communicate()
    return r, out, err


class Server:

    def __init__(self, servername="default", vim="gvim", autostart=True):
        self.servername = servername.upper()
        self.vim = vim
        self.use_autostart = autostart

    def list_servers(self):
        try:
            r, so, se =  sh(LIST_SERVERS.format(vim=self.vim))
            assert r == 0
            servers = so.strip().split("\n")
            return servers
        except:
            raise
            return []

    def is_running(self):
        servers = self.list_servers()
        return self.servername in servers

    def run(self, s):
        s = s.replace('"', '\\"')
        return sh(RUN_COMMAND.format(vim=self.vim,
                                     servername=self.servername,
                                     cmd=s))

    def send_keys(self, keys):
        return sh(SEND_KEYS.format(vim=self.vim, servername=self.servername,
                                   keys=keys))

    def start(self):
        if self.is_running(): return False
        tf = tempfile.NamedTemporaryFile()
        with open(tf.name, "w") as f:
            f.write(VIMSCRIPT)
        r = os.system(START_SERVER.format(vim=self.vim,
                                          servername=self.servername))
        # Wait for server to start
        while not self.is_running():
            time.sleep(0.1)

        if r == 0:
            r, out, err = self.send_keys(":source "+tf.name+" <CR>")
            if r != 0:
                return False
            r, out, err = self.send_keys(":echo \"Started By VimUtils\" <CR>")
            return True
        return False
        
    def open(self, files):
        if type(files) != list:
            files = [files]
        return os.system(OPEN.format(vim=self.vim, 
                                     servername=self.servername,
                                     files=" ".join(files)))

    def open_tabs(self, files):
        if type(files) != list:
            files = [files]
        return os.system(OPEN_TABS.format(vim=self.vim,
                                          servername=self.servername,
                                          files=" ".join(files)))

    def open_diff(self, files):
        self.open(files[0])
        for f in files[1:]:
            f = os.path.realpath(f)
            self.run(":diffsplit %s" % (f))

    def buffers_str(self):
        r, out, err = self.run(":buffers")
        return out

    def buffers(self):
        r, out, err = self.run(":buffers")
        lines = out.strip().split("\n")
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
        r, out, err = sh(DUMP_BUFFER.format(vim=self.vim,
                                            servername=self.servername,
                                            bufno=str(bufno)))
        filename = out.strip()
        with open(filename) as f:
            return f.read()

    def dump_buffers(self):
        out = []
        for buf in self.buffers():
            if buf["id"]:
                out.append(self.dump_buffer(buf["id"]))
        return out

    
    def search_buffers(self, expr, **kwargs):
        
        buffers = self.buffers()
        expr = re.compile(expr)
        matches = []

        for buf in buffers:
            lines = self.dump_buffer(buf["id"]).split("\n")
            lineno = 1
            for line in lines:
                if re.search(expr, line):
                    matches.append({
                        "lineno" : lineno,
                        "buf" : buf,
                        "line" : line
                    })
                lineno = lineno + 1
        return matches

def get_config():
    conf = {
        "vim" : "gvim",
        "default_server" : "default"
    }
    config_file = os.path.join(os.environ["HOME"], ".vimutils.json")
    if os.path.isfile(config_file):
        with open(config_file) as f:
            c = json.loads(f.read())
            if "vim" in c:
                conf["vim"] = c["vim"]
            if "default_server" in c:
                conf["default_server"] = c["default_server"]



def vimutils(servername=None, **kwargs):
    vim = kwargs.get("vim", None)
    if not vim:
        vim = os.environ.get("VIMUTILS_VIM_CMD", "gvim")
    if not servername:
        servername = os.environ.get("VIMUTILS_DEFAULT_SERVERNAME", "default")
    s = Server(servername, vim)
    return s

def handle_servers(s, args):
    print("\n".join(s.list_servers()))

def handle_start(s, args):
    r = s.start()
    if not r:
        sys.stderr.write("Could not start vim server '%s': " % (s.servername))
        if s.is_running():
            sys.stderr.write("Already running")
        else:
            sys.stderr.write("Unknown Error")
        sys.stderr.write("\n")
        exit(1)

def handle_open(s, args):
    s.open(args.files)


def handle_tabs(s, args):
    s.open_tabs(args.files)


def handle_diff(s, args):
    s.open_diff(args.files)

def handle_buffers(s, args):
    if args.json:
        print(json.dumps({"buffers":s.buffers()}, indent=2))
    else:
        print(s.buffers_str())

def handle_dump_buffer(s, args):
    print(s.dump_buffer(args.bufno))

def handle_grep(s, args):
    try:
        results = s.search_buffers(args.expr)
    except re.error as e:
        sys.stderr.write("Invalid regular expression:\n")
        sys.stderr.write(str(e)+"\n")
        exit(1)
    for result in results:
        print("%d:%s:%d: %s" % (result["buf"]["id"],
                                result["buf"]["file"],
                                result["lineno"],
                                result["line"]))

def handle_keys(s, args):
    s.send_keys(args.keys)

def handle_run(s, args):
    r, out, err = s.run(args.cmdstr)
    print(out)


SHELL_ALIASES = """\
ve () {{
    {vu} open "$@";
}}

vt () {{
    {vu} tabs "$@";
}}

vd () \{{
    {vu} diff "$@";
}}
"""

def handle_shell_aliases(s, args):
    path = os.path.realpath(__file__)
    if args.no_full_path:
        path = os.path.basename(path)
    print(SHELL_ALIASES.format(vu=path))

def main():

    argp = argparse.ArgumentParser()
    subp = argp.add_subparsers()

    argp.add_argument("-c","--vim-command", default="gvim")
    argp.add_argument("-s", "--servername", default="default")

    argp_servers = subp.add_parser("servers", help=HELP_SERVERS)
    argp_servers.set_defaults(func=handle_servers)

    argp_start = subp.add_parser("start", help=HELP_START)
    argp_start.set_defaults(func=handle_start)

    argp_open = subp.add_parser("open", help=HELP_OPEN)
    argp_open.add_argument("files", nargs="*")
    argp_open.set_defaults(func=handle_open)

    argp_tabs = subp.add_parser("tabs", help=HELP_TABS)
    argp_tabs.add_argument("files", nargs="*")
    argp_tabs.set_defaults(func=handle_tabs)

    argp_diff = subp.add_parser("diff", help=HELP_DIFF)
    argp_diff.add_argument("files", nargs="*")
    argp_diff.set_defaults(func=handle_diff)

    argp_buffers = subp.add_parser("buffers", help=HELP_BUFFERS)
    argp_buffers.add_argument("-j", "--json", action="store_true",
                              help="Output in json format")
    argp_buffers.set_defaults(func=handle_buffers)

    argp_dump_buffer = subp.add_parser("dump-buffer", help=HELP_DUMP_BUFFER)
    argp_dump_buffer.add_argument("bufno", type=int, action="store")
    argp_dump_buffer.set_defaults(func=handle_dump_buffer)

    argp_grep = subp.add_parser("grep")
    argp_grep.add_argument("expr", action="store")
    argp_grep.set_defaults(func=handle_grep)

    argp_keys = subp.add_parser("keys", help=HELP_KEYS)
    argp_keys.add_argument("keys", action="store")
    argp_keys.set_defaults(func=handle_keys)

    argp_run = subp.add_parser("run", help=HELP_RUN)
    argp_run.add_argument("cmdstr", action="store")
    argp_run.set_defaults(func=handle_run)

    argp_shell_aliases = subp.add_parser("shell-aliases",
                                         help=HELP_SHELL_ALIASES)
    argp_shell_aliases.add_argument("-P",
                                    "--no-full-path",
                                    action="store_true",
                                    help=HELP_NO_FULL_PATH)
    argp_shell_aliases.set_defaults(func=handle_shell_aliases)

    args = argp.parse_args()
    s = vimutils(args.servername, vim=args.vim_command)

    if args.func not in [handle_start, handle_servers,
                         handle_shell_aliases]:
        if not s.is_running():
            s.start()

    args.func(s,args)



if __name__ == "__main__":
    main()

