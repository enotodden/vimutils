vimutils
========

Vim utilities.

A python module, vim plugin and command line utils to access
a vim instance with a servername.
This is mostly a wrapper for builtin vim functionality, but makes some tasks a lot
easier/less annoying.

### Scripts:

+ *vu* - Main script, called by all the other scripts

#####Arguments:
        usage: vu [-h] [-l] [-s] [-b] [-d DUMP_BUFFER] [-D] [-o] [-t] [-S SERVERNAME]
                  [-r RCFILE] [-C COMMAND]
                  [files [files ...]]

        positional arguments:
          files

        optional arguments:
            -h, --help            show this help message and exit
            -l, --list-servers
            -s, --start-server
            -b, --list-buffers
            -d DUMP_BUFFER, --dump-buffer DUMP_BUFFER
            -D, --dump-session
            -o, --open
            -t, --tabs
            -S SERVERNAME, --servername SERVERNAME
            -r RCFILE, --rcfile RCFILE
            -C COMMAND, --command COMMAND


            
#####General Options:
                -s, --servername
                Select a servername, defaults to the 'default_server' entry
                in the .vimutilsrc file
                Applies to all actions, except --list-servers

                -r, --rcfile
                Use a different rc file than the default one.
                Applies to all actions




##### Actions:          
                -l,--list-servers
                List all instances of vim started with the --servername argument

                -s,--start-server
                Same as `vim --servername SERVERNAME`

                -b, --list-buffers
                Runs `:buffer` in the vim instance and returns it's output

                -d, --dump-buffer
                Dumps a buffer specified by the buffer id(integer)
                Example: vu -d 19

                -D, --dump-session
                Dumps the current vim buffers and metainfo as a json blob
                
                -o, --open
                Opens the files specified with the :e command

                -t, --tabs 
                Opens the files specified with the :tabnew command

                -C, --command
                Run a command in the vim instance



+ *vs* - Start vim with servername=SERVERNAME, same as: `vu -s`
        
        $ vs myservername

    or just

        $ vs

    equivalent to

        $ gvim --servername myservername


+ *ve* - Open files as buffers in current vim server, alias for: `vu --open`

        $ ve myfile.txt myotherfile.txt 

+ *vt* - Open files as tabs in current vim server, alias for: `vu --tabs`
        
        $ vt myfile.txt myotherfile.txt

+ *vls* - List running servers, alias for: `vu --list-servers`
    
        $ vls

+ *vbls* - List open buffers, alias for: `vu --list-buffers`

        $ vbls

+ *vdb* - Dump buffer N, alias for: `vu --dump-buffer`

        $ vdb 19

+ *vds* - Dump session, print all buffers as a possibly huge json blob,alias for: `vu --dump-session`

        $ vds



### RC File

Copy example.vimutilsrc to /home/<username\>/.vimutilsrc

+ "vim_cmd" : The command to use(vim, vimx, vi, gvim etc.)
+ "default_server" : The default server name to use



### Install:
    
    $ sudo python setup.py install
    $ cp example.vimutilsrc ~/.vimutilsrc
    $ cp -rv plugin/* ~/.vim/plugin/



### TODO:
+ Add default_server switching
+ ?
