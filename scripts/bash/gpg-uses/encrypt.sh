#!/bin/bash

# helper func to display usage
usage() {
  echo "Usage: $0 -e recipient_email -f file_to_encrypt -pk public_key_file"
  exit 1
}

while [[ "$#" -gt 0 ]]; do
  case $1 in
    -e) recipient_email="$2"; shift ;;
    -f) file_to_encrypt="$2"; shift ;;
    -pk) public_key="$2"; shift ;;
    *) usage ;;
  esac
  shift
done

if [ -z "$recipient_email" ] || [ -z "$file_to_encrypt" ] || [ -z "$public_key" ]; then
  echo "Error: Missing required arguments."
  usage
fi

# Check if the public key file exists
if [ ! -f "$public_key" ]; then
  echo "Error: Public key file $public_key not found."
  exit 1
fi

# Check if the file to encrypt exists
if [ ! -f "$file_to_encrypt" ]; then
  echo "Error: File to encrypt $file_to_encrypt not found."
  exit 1
fi

# import the public key
echo "Importing public key from $public_key..."
gpg --import "$public_key"
if [ $? -ne 0 ]; then
  echo "Error: Failed to import public key."
  exit 1
fi

# encrypt the file
echo "Encrypting $file_to_encrypt for $recipient_email..."
gpg --encrypt --armor --recipient "$recipient_email" "$file_to_encrypt"
if [ $? -eq 0 ]; then
  if [ -f "$file_to_encrypt.asc" ]; then
    echo "File encrypted successfully! Encrypted file: $file_to_encrypt.asc"
  else
    echo "Error: Encryption process completed, but no encrypted file generated."
  fi
else
  echo "Error: Failed to encrypt the file."
  exit 1
fi
