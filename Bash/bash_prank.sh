#! /bin/bash
# ░░░░░▄▄▄▄▀▀▀▀▀▀▀▀▄▄▄▄▄▄░░░░░░░
# ░░░░░█░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░▀▀▄░░░░
# ░░░░█░░░▒▒▒▒▒▒░░░░░░░░▒▒▒░░█░░░
# ░░░█░░░░░░▄██▀▄▄░░░░░▄▄▄░░░░█░░
# ░▄▀▒▄▄▄▒░█▀▀▀▀▄▄█░░░██▄▄█░░░░█░
# █░▒█▒▄░▀▄▄▄▀░░░░░░░░█░░░▒▒▒▒▒░█
# █░▒█░█▀▄▄░░░░░█▀░░░░▀▄░░▄▀▀▀▄▒█
# ░█░▀▄░█▄░█▀▄▄░▀░▀▀░▄▄▀░░░░█░░█░
# ░░█░░░▀▄▀█▄▄░█▀▀▀▄▄▄▄▀▀█▀██░█░░
# ░░░█░░░░██░░▀█▄▄▄█▄▄█▄████░█░░░
# ░░░░█░░░░▀▀▄░█░░░█░█▀██████░█░░
# ░░░░░▀▄░░░░░▀▀▄▄▄█▄█▄█▄█▄▀░░█░░
# ░░░░░░░▀▄▄░▒▒▒▒░░░░░░░░░░▒░░░█░
# ░░░░░░░░░░▀▀▄▄░▒▒▒▒▒▒▒▒▒▒░░░░█░
# ░░░░░░░░░░░░░░▀▄▄▄▄▄░░░░░░░░█░░

# Get current volume (Linux)
cur_vol=$(amixer get Master | grep -o '[0-9]*%' | head -n 1 | tr -d '%')

# To restore vol to current level
restore_vol=$(echo "${cur_vol}/100" | bc -l)

# Get bool if muted
mute_state=$(amixer get Master | grep -o '\[off\]' | wc -l)

# If system doesn't have shuf, not gonna work
if ! command -v shuf &> /dev/null; then
  exit; exit
fi

# Set vol to max
amixer set Master 100%

# Create temp dir
if [ -d ~/temp ]; then
  tempe=1
else
  tempe=0
  mkdir ~/temp
fi

# Create list of annoying things to say
curl -s https://raw.githubusercontent.com/libialany/DevOpsProject/refs/heads/main/Bash/jokes.txt > ~/temp/jokes

# Use shuf to generate random permutations
# Use -n1 to get a phrase from list
# Pipe it to espeak to transform text to speech (Linux)
shuf -n1 ~/temp/jokes | espeak -v en-us -s 150

# Restore volume 
amixer set Master "${restore_vol}%"
if [[ ${mute_state} -eq 1 ]]; then
  amixer set Master mute
fi

# Cleanup
if [[ ${tempe} -eq 0 ]]; then
  rm -Rf ~/temp
else
  rm -f ~/temp/jokes
fi