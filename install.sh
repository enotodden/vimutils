#!/usr/bin/env bash

if [ -z "$PREFIX" ]; then
    PREFIX="/usr/local";
fi

install -m 0755 ./vu.py "$PREFIX/bin/vu"
install -m 0644 ./example.vimutils.json $HOME/.vimutils.json
vu shell-aliases > $HOME/.vimutils.shell
echo "Installed.."
echo "Please add the line 'source ~/.vimutils.shell' to your .bashrc to use the short aliases"
