import os
# Define distracting blog for you (this is my case)
distracting_blog = "jewelrymakingjournal.com"
# Get the IP address of the study site
distracting_blog_ip = os.popen(f" dig +short {distracting_blog} | head -n1").read().strip()
# Add IP Tables rules for deny that distracting site
os.system(f"sudo ufw deny out to  {distracting_blog_ip}")
# Enable ufw
os.system(f"sudo ufw enable")