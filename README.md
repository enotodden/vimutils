vimutils
========

A command line tool for a working with a Vim server from the shell.


## Quick Example


    $ vu start                  # Starts a vim server instance named 'DEFAULT'
    $ vu open /etc/hosts        # Opens the /etc/hosts file in a new buffer


## Setting Vim Binary To Use

The Vim binary used defaults to 'gvim' (no full path),
if you need to change this you can:

Set the VIMUTILS\_VIM\_CMD environment variable:

    $ export VIMUTILS_VIM_CMD=vim

Or set it each time on the command line:

    $ vu -c vim [....]

Or just edit vu.py :)




## Commands

#### servers

List running Vim servers

    $ vu servers
    MY_VIM
    MY_OTHER_VIM

#### start

Start a new Vim server.

Starts a Vim server instance and sources a vimutils helpers vimscript
in that instance.

Start using the default servername:

    $ vu start # Starts the server "DEFAULT"

Or provide a servername with the -s parameter

    $ vu -s my_vim_instance start

Or use the VIMUTILS\_DEFAULT\_SERVERNAME environment variable to 
set the servername (can be overridden by -s)
    
    $ export VIMUTILS_DEFAULT_SERVERNAME="My_server_name"
    $ vu start


The environment variable and the -s parameters can be used with any command
except for 'servers' and 'shell-aliases'.


#### open

Open one or more files as buffers in the vim instance.

    $ vu open /path/to/my/file.txt /path/to/my/other/file.txt

#### tabs

Same as 'open' but uses :tabnew

#### diff

Open a set of files in a diff-split view.

    $ vu diff ./file1.txt ./file2.txt

#### buffers

List all the buffers in the Vim instance in plain text(default)
or JSON format.
This works like ':buffers' except for writing output
to the shell instead of inside Vim.

    $ vu buffers

Or, as JSON:

    $ vu buffers --json


#### dump-buffer

Prints the contents of a buffer by buffer id (buffer number).

    $ vu dump-buffer 5

#### keys

Sends a string of keys to a Vim instance.

    $ vu keys ':echo "Hello Vim" <CR>'

#### run

Runs a command in the Vim instance prints the output.

    $ vu run ":ls"






Usage:



    usage: vu.py [-h] [-c VIM_COMMAND] [-s SERVERNAME]
                 
                 {servers,start,open,tabs,diff,buffers,dump-buffer,grep,keys,run,shell-aliases}
                 ...

    positional arguments:
      {servers,start,open,tabs,diff,buffers,dump-buffer,grep,keys,run,shell-aliases}
        servers             List running vim servers.
        start               Start a vim server.
        open                Open file(s).
        tabs                Open file(s) in tab(s).
        diff                Diff files
        buffers             List buffers.
        dump-buffer         Print the contents of a buffer (by buffer number)
        keys                Send a string of keys to the target vim server
        run                 Run a command and print the output.
            shell-aliases       Print a set of nice-to-have shell functions for your
                            .(bash|zsh)rc

    optional arguments:
      -h, --help            show this help message and exit
      -c VIM_COMMAND, --vim-command VIM_COMMAND
      -s SERVERNAME, --servername SERVERNAME
