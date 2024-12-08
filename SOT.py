import requests
from pystyle import Colors, Write, Center
from phonenumbers import geocoder, carrier, timezone
import phonenumbers
import os

def ip_info(ip):
    url = f"https://ipinfo.io/{ip}/json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        response = response.json()
        ip_details = f"""
╭─{" "*78}─╮
|{' '*34} IP Details {' '*34}|
|{"="*80}|
| [+] > IP Address         || {response.get('ip', 'None'): <51}|
| [+] > City               || {response.get('city', 'None'): <51}|
| [+] > Region             || {response.get('region', 'None'): <51}|
| [+] > Country            || {response.get('country', 'None'): <51}|
| [+] > Postal code        || {response.get('postal', 'None'): <51}|
| [+] > ISP                || {response.get('org', 'None'): <51}|
| [+] > Latitude, Longitude|| {response.get('loc', 'None'): <51}|
| [+] > Timezone           || {response.get('timezone', 'None'): <51}|
| [+] > Google Maps        || https://www.google.com/maps?q={response.get('loc', 'None'): <21}|
╰─{" "*24}─╯╰─{" "*50}─╯
"""
        Write.Print(Center.XCenter(ip_details), Colors.white, interval=0)

    except requests.exceptions.Timeout:
        os.system('cls' if os.name == 'nt' else 'clear')
        Write.Print("\n[!] > Request timed out. Please try again later.", Colors.red, interval = 0)
    except requests.exceptions.ConnectionError:
        os.system('cls' if os.name == 'nt' else 'clear')
        Write.Print("\n[!] > Connection error.", Colors.red, interval = 0)
    except requests.exceptions.HTTPError as e:
        os.system('cls' if os.name == 'nt' else 'clear')
        Write.Print(f"\n[!] > HTTP error: {e.response.status_code}", Colors.red, interval = 0)
    except Exception as e:
        os.system('cls' if os.name == 'nt' else 'clear')
        Write.Print(f"\n[!] > An error occurred: {e}", Colors.red, interval = 0)

    Write.Input("\nPress Enter to return to the main menu...", Colors.red, interval=0)
    os.system('cls' if os.name == 'nt' else 'clear')

def username_search(nickname):
    urls = [f"https://www.instagram.com/{nickname}",
            f"https://www.tiktok.com/@{nickname}",
            f"https://www.x.com/{nickname}",
            f"https://www.facebook.com/{nickname}",
            f"https://www.youtube.com/@{nickname}",
            f"https://t.me/{nickname}",
            f"https://www.twitch.tv/{nickname}",
            f"https://open.spotify.com/user/{nickname}",
            f"https://www.pinterest.com/{nickname}",
            f"https://www.reddit.com/{nickname}",
            f"https://www.github.com/{nickname}",
            f"https://vk.com/{nickname}"]
    search_results = f"""
╭─{" "*78}─╮
|{' '*27}Social Media Search Results{' '*26}|
|{"="*80}|
"""

    for url in urls:
        try:
            response = requests.get(url)
            status_code = response.status_code
            
            if status_code == 200:
                result_text = f"[+] > {url:<50}|| Found"
            elif status_code == 404:
                result_text = f"[-] > {url:<50}|| Not found"
            else:
                result_text = f"[-] > {url:<50}|| Error: {status_code}"

            search_results += f"| {result_text:<78} |\n"
        
        except requests.exceptions.RequestException as e:
            result_text = f"[-] > {url:<50} || Error: {str(e)}"
            search_results += f"| {result_text:<78} |\n"

    search_results += f"╰─{' '*55}─╯╰─{' '*19}─╯"

    Write.Print(Center.XCenter(search_results), Colors.white, interval=0)
    Write.Input("\nPress Enter to return to the main menu...", Colors.red, interval=0)
    os.system('cls' if os.name == 'nt' else 'clear')

def phone_info(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        country = geocoder.country_name_for_number(parsed_number, "en")
        region = geocoder.description_for_number(parsed_number, "en")
        operator = carrier.name_for_number(parsed_number, "en")
        valid = phonenumbers.is_valid_number(parsed_number)
        validity_text = "Valid" if valid else "Invalid"
        phonetext = f"""
\n
╭─{" "*50}─╮
|{' '*17}Phone number info{' '*18}|
|{"="*52}|
| [+] > Number:   || {phone_number: <32}|
| [+] > Country:  || {country: <32}|
| [+] > Regiom:   || {region: <32}|
| [+] > Operator: || {operator: <32}|
| [+] > Validity: || {validity_text: <32}|
╰─{" "*15}─╯╰─{" "*31}─╯\n"""

        Write.Print(Center.XCenter(phonetext), Colors.white, interval=0)
    
    except phonenumbers.phonenumberutil.NumberParseException:
        os.system('cls' if os.name == 'nt' else 'clear')
        Write.Print(f"\n[!] > Error: invalid phone number format", Colors.red, interval = 0)

    Write.Input("\nPress Enter to return to the main menu...", Colors.red, interval=0)
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        menu_art = """\n   ▄████████  ▄██████▄      ███     
  ███    ███ ███    ███ ▀█████████▄ 
  ███    █▀  ███    ███    ▀███▀▀██ 
  ███        ███    ███     ███   ▀ 
▀███████████ ███    ███     ███     
         ███ ███    ███     ███     
   ▄█    ███ ███    ███     ███     
 ▄████████▀   ▀██████▀     ▄████▀   
\n"""

        menu = """\n\n                                 [ S.O.T ]\n
                            Simple OSINT Tools

╭─   ─╮╭─                 ─╮╭─                                             ─╮
|  №  ||     Function      ||                   Description                 |
|=====||===================||===============================================|
| [1] || IP info search    || Search information about an IP address        |
| [2] || Username search   || Search for profiles on social media platforms |
| [3] || Phone info search || Search information about a phone number       |
| [0] || Exit              || Exit the program                              |
╰─   ─╯╰─                 ─╯╰─                                             ─╯\n\n\n"""

        Write.Print(Center.XCenter(menu_art), Colors.red, interval = 0)
        Write.Print(Center.XCenter(menu), Colors.white, interval = 0)

        choice = Write.Input("[?] >  ", Colors.red, interval = 0).strip()
        if choice == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            ip = Write.Input("[?] > IP-Adress: ", Colors.red, interval = 0)
            if not ip:
                os.system('cls' if os.name == 'nt' else 'clear')
                Write.Print("[!] > Please, enter IP Adress\n", Colors.red, interval = 0)
                continue
            ip_info(ip)

        elif choice == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            nickname = Write.Input("[?] > Username: ", Colors.red, interval = 0)
            Write.Print("[!] > Please wait, it may take some time...\n", Colors.red, interval = 0)
            if not nickname:
                os.system('cls' if os.name == 'nt' else 'clear')
                Write.Print("[!] > Please, enter username\n", Colors.red, interval = 0)
                continue
            username_search(nickname)

        elif choice == "3":
            os.system('cls' if os.name == 'nt' else 'clear')
            phone_number = Write.Input("[?] > Phone number: ", Colors.red, interval = 0)
            if not phone_number:
                os.system('cls' if os.name == 'nt' else 'clear')
                Write.Print("[!] > Please, enter phone number\n", Colors.red, interval = 0)
                continue
            phone_info(phone_number)
            
        elif choice == "4":
            os.system('cls' if os.name == 'nt' else 'clear')
        
        elif choice == "0":
            Write.Print("\n[!] > Exiting...", Colors.red, interval = 0)
            exit()

        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            Write.Print("[!] > Invalid input. Please enter a number from 1 to 4\n", Colors.red, interval = 0)
            continue

main()
