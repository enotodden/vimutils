vimutils
========

Vim utilities

### Scripts:

+ *vs* - Start vim with servername=SERVERNAME
        
        $ vs myservername

    or just

        $ vs

    equivalent to

        $ gvim --servername myservername


+ *ve* - Open files as buffers in current vim server

        $ ve myfile.txt myotherfile.txt 

+ *vt* - Open files as tabs in current vim server
        
        $ vt myfile.txt myotherfile.txt

+ *vls* - List running servers
    
        $ vls

+ *vbls* - List open buffers

        $ vbls

+ *vdb* - Dump buffer N

        $ vdb 19


### RC File

Copy example.vimutilsrc to /home/<username\>/.vimutilsrc

+ "vim_cmd" : The command to use(vim, vimx, vi, gvim etc.)
+ "default_server" : The default server name to use



### Install:
    
    $ sudo python setup.py install
    $ cp example.vimutilsrc ~/.vimutilsrc
    $ cp -rv plugin/* ~/.vim/plugin/



### TODO:
+ Add buffer-list parsing
+ Add --servername command line options to scripts
+ Add default_server switching
+ --help command line options
+ ?
