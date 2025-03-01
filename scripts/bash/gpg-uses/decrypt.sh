#!/bin/bash

# helperr func to display usage
usage() {
  echo "Usage: $0 -f encrypted_file"
  exit 1
}

while [[ "$#" -gt 0 ]]; do
  case $1 in
    -f) encrypted_file="$2"; shift ;;
    *) usage ;;
  esac
  shift
done

if [ -z "$encrypted_file" ]; then
  echo "Error: Missing required arguments."
  usage
fi

# Check if the encrypted file exists
if [ ! -f "$encrypted_file" ]; then
  echo "Error: Encrypted file $encrypted_file not found."
  exit 1
fi

# decrypt the file
echo "Decrypting $encrypted_file..."
gpg --decrypt "$encrypted_file" > decrypted_output.txt
if [ $? -eq 0 ]; then
  echo "File decrypted successfully! Decrypted content is saved in decrypted_output.txt"
else
  echo "Error: Failed to decrypt the file."
  exit 1
fi
