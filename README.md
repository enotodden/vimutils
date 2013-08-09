vimutils
========

A command line tool for a working with a Vim server from the shell.


## Quick Example


    $ vu start                  # Starts a vim server instance named 'DEFAULT'
    $ vu open /etc/hosts        # Opens the /etc/hosts file in a new buffer


## Installing

    $ git clone https://github.com/enotodden/vimutils
    $ cd vimutils/
    $ ./install.sh
    $ echo 'source ~/.vimutils.shell' >> ~/.bashrc  # or other shell rc

## Commands

Names in parenthesis are shell aliases (~/.vimutils.shell)

#### servers (vls)

List running Vim servers

    $ vu servers
    MY_VIM
    MY_OTHER_VIM

#### start (vs)

Start a new Vim server.

Starts a Vim server instance and sources a vimutils helpers vimscript
in that instance.

    $ vu start


#### open (ve)

Open one or more files as buffers in the vim instance.

    $ vu open /path/to/my/file.txt /path/to/my/other/file.txt

#### tabs (vt)

Same as 'open' but uses :tabnew

#### diff (vd)

Open a set of files in a diff-split view.

    $ vu diff ./file1.txt ./file2.txt

#### buffers (vbls)

List all the buffers in the Vim instance in plain text(default)
or JSON format.
This works like ':buffers' except for writing output
to the shell instead of inside Vim.

    $ vu buffers

Or, as JSON:

    $ vu buffers --json


#### dump-buffer (vdb)

Prints the contents of a buffer by buffer id (buffer number).

    $ vu dump-buffer 5

#### keys (vk)

Sends a string of keys to a Vim instance.

    $ vu keys ':echo "Hello Vim" <CR>'

#### run (vr)

Runs a command in the Vim instance prints the output.

    $ vu run ":ls"


#### grep (vgrep)

Search the contents of the buffers in the Vim instance using a Python
regular expression.

    $ vu grep '^import'

## Changing the vim command or default server name

Copy example.vimutils.json to ~/.vimutils.json in your home directory,
use the -s and -c parameters or use the `$VIMUTILS_VIM` and 
`$VIMUTILS_DEFAULT_SERVER` environment variables.



