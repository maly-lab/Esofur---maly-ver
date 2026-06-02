#!/bin/bash

echo "Installing EsoFur..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

sudo ln -sf "$SCRIPT_DIR/esofur" /usr/local/bin/esofur
sudo chmod +x "$SCRIPT_DIR/esofur"

echo "Installed successfully!"
echo "Try: esofur run test.EsoFur"
