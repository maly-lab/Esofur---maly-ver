#!/bin/bash

set -e

echo "Installing EsoFur..."

# get full path of repo
DIR="$(cd "$(dirname "$0")" && pwd)"

# make sure CLI is executable
chmod +x "$DIR/esofur"

# create global command (no file copying, just linking)
sudo ln -sf "$DIR/esofur" /usr/local/bin/esofur

echo "EsoFur installed successfully!"
echo "Try: esofur run test.EsoFur"
