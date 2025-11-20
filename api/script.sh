#!/usr/bin/env bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'

# Add the npm binaries to your PATH
echo 'export PATH=$HOME/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Now install globally (but in your home directory)
npm install -g widdershins
