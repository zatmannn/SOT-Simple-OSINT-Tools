clear
echo -e "\033[1;91m
  ▄████████  ▄██████▄      ███     
  ███    ███ ███    ███ ▀█████████▄ 
  ███    █▀  ███    ███    ▀███▀▀██ 
  ███        ███    ███     ███   ▀ 
▀███████████ ███    ███     ███     
         ███ ███    ███     ███     
   ▄█    ███ ███    ███     ███     
 ▄████████▀   ▀██████▀     ▄████▀"

echo -e "\033[1;91m[!]\033[1;97m Installing..."
apt update -y
apt upgrade -y
echo -e "\033[1;91m[!]\033[1;97m Installing Python..."
apt install python -y
echo -e "\033[1;91m[!]\033[1;97m Installing Requests..."
pip install requests
echo -e "\033[1;91m[!]\033[1;97m Installing Phonenumbers..."
pip install phonenumbers
echo -e "\033[1;91m[!]\033[1;97m Installing Pystyle..."
pip install pystyle
echo -e "\033[1;91m[!]\033[1;97m Installing Whois..."
pip install python-whois
clear
echo -e "\033[1;91m[!]\033[1;97m Installed successfully"
