# GPG stuff

A script to generate a message and sign it with GPG.
Apart from that, encryption can be applied to E-mails.

## Prerequisites

- GPG installed
- Make the scripts executable (`chmod +x encrypt.sh decrypt.sh`)

## Public Key 

```
gpg --generate-key 
gpg --list-keys
gpg --export -a demo123@example.com > public-key.asc
```

## Encrypt

The gpg-encrypt.sh script encrypts a file using the recipient's public key.

```bash
sh gpg-encrypt.sh -e demo123@example.com -f message.txt -pk public-key.asc
```

## Decrypt

```bash
sh gpg-decrypt.sh -f message.txt.asc
```
