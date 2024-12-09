import requests
from pystyle import Colors, Write, Center
from phonenumbers import geocoder, carrier, timezone
import phonenumbers
import whois
import os
from concurrent.futures import ThreadPoolExecutor

default_color = Colors.red  

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def restart():
    Write.Input("\nPress Enter to return to the main menu...", default_color, interval=0)
    clear()

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
        clear()
        Write.Print("\n[!] > Request timed out. Please try again later", default_color, interval = 0)
    except requests.exceptions.ConnectionError:
        clear()
        Write.Print("\n[!] > Connection error", default_color, interval = 0)
    except requests.exceptions.HTTPError as e:
        clear()
        Write.Print(f"\n[!] > HTTP error: {e.response.status_code}", default_color, interval = 0)
    except Exception:
        clear()
        Write.Print(f"\n[!] > Error", default_color, interval = 0)

    restart()

def username_search(nickname):
    def check_url(url):
        try:
            response = requests.get(url, timeout=10)
            status_code = response.status_code

            if status_code == 200:
                return f"[+] > {url:<50}|| Found"
            elif status_code == 404:
                return f"[-] > {url:<50}|| Not found"
            else:
                return f"[-] > {url:<50}|| Error: {status_code}"

        except requests.exceptions.Timeout:
            return f"[-] > {url:<50}|| Timeout"
        except requests.exceptions.ConnectionError:
            return f"[-] > {url:<50}|| Connection error"
        except requests.exceptions.RequestException:
            return f"[-] > {url:<50}|| Request error"
        except Exception:
            return f"[-] > {url:<50}|| Unexpected error"

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

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(check_url, urls))
    
    for result in results:
        search_results += f"| {result:<78} |\n"

    search_results += f"╰─{' '*78}─╯"

    Write.Print(Center.XCenter(search_results), Colors.white, interval=0)

    restart()

def phone_info(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        country = geocoder.country_name_for_number(parsed_number, "en")
        region = geocoder.description_for_number(parsed_number, "en")
        operator = carrier.name_for_number(parsed_number, "en")
        valid = phonenumbers.is_valid_number(parsed_number)
        validity = "Valid" if valid else "Invalid"
        phonetext = f"""
\n
╭─{" "*50}─╮
|{' '*17}Phone number info{' '*18}|
|{"="*52}|
| [+] > Number   || {phone_number: <33}|
| [+] > Country  || {country: <33}|
| [+] > Regiom   || {region: <33}|
| [+] > Operator || {operator: <33}|
| [+] > Validity || {validity: <33}|
╰─{" "*15}─╯╰─{" "*31}─╯\n"""

        Write.Print(Center.XCenter(phonetext), Colors.white, interval=0)
    
    except phonenumbers.phonenumberutil.NumberParseException:
        clear()
        Write.Print(f"\n[!] > Error: invalid phone number format", default_color, interval = 0)

    restart()

def domain_info(domain):

    def domain_date(date):
        if isinstance(date, list):
            date = date[0]
        return date.strftime("%Y-%m-%d") if date else "Unknown"

    try:
        domain_data = whois.whois(domain)
        domain_name = domain_data.domain_name
        domain_registrar = domain_data.registrar
        domain_creation_date = domain_date(domain_data.creation_date)
        domain_expiration_date = domain_date(domain_data.expiration_date)
        domain_updated_date = domain_date(domain_data.updated_date)
        registrant_name = domain_data.registrant_name if domain_data.registrant_name else "Private"
        registrant_email = domain_data.registrant_email if domain_data.registrant_email else "Private"

        domain_details = f"""
╭─{" "*78}─╮
|{' '*34} WHOIS Info {' '*34}|
|{"="*80}|
| [+] > Domain:           || {domain_name: <52}|
| [+] > Registrar:        || {domain_registrar: <52}|
| [+] > Creation Date:    || {domain_creation_date: <52}|
| [+] > Expiration Date:  || {domain_expiration_date: <52}|
| [+] > Last Updated:     || {domain_updated_date: <52}|
| [+] > Registrant Name:  || {registrant_name: <52}|
| [+] > Registrant Email: || {registrant_email: <52}|
╰─{" "*23}─╯╰─{" "*51}─╯
"""
        Write.Print(Center.XCenter(domain_details), Colors.white, interval=0)
    except Exception:
        Write.Print(f"[!] > Error", default_color, interval=0)

    restart()

def change_color():
    global default_color
    clear()
    color_menu = """
╭─    ─╮╭─                     ─╮
|  №   ||         Color         |
|======||=======================|
| [1]  || Red                   |
| [2]  || Blue                  |
| [3]  || Green                 |
| [4]  || Yellow                |
| [5]  || Cyan                  |
| [6]  || White                 |
|------||-----------------------|
| [0]  || Back to settings menu |
╰─    ─╯╰─                     ─╯
"""
    Write.Print(Center.XCenter(color_menu), Colors.white, interval=0)

    color_choice = Write.Input("\n\n[?] >  ", default_color, interval=0).strip()

    color = {"1": Colors.red,
        "2": Colors.blue,
        "3": Colors.green,
        "4": Colors.yellow,
        "5": Colors.cyan,
        "6": Colors.white}

    if color_choice in color:
        default_color = color[color_choice]
        clear()
        Write.Print("[!] > Color changed successfully.\n", default_color, interval=0)
    elif color_choice == "0":
        settings()
    else:
        clear()
        Write.Print("[!] > Invalid choice. Please choose a number from 1 to 6.\n", Colors.red, interval=0)
    restart()

def main():
    clear()
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

        menu = """\n\n                                   [ S.O.T ]\n
                               Simple OSINT Tools

╭─    ─╮╭─                   ─╮╭─                                             ─╮
|  №   ||      Function       ||                  Description                  |
|======||=====================||===============================================|
| [1]  || IP Info Search      || Search for information about an IP address    |
| [2]  || Username Search     || Search for profiles on social media platforms |
| [3]  || Phone Info Search   || Search for information about a phone number   |
| [4]  || Domain Info Search  || Search for information about a domain         |
|------||---------------------||-----------------------------------------------|
| [0]  || Exit                || Exit the program                              |
| [99] || Settings            || Set up this tool                              |
╰─    ─╯╰─                   ─╯╰─                                             ─╯\n\n\n"""

        Write.Print(Center.XCenter(menu_art), default_color, interval = 0)
        Write.Print(Center.XCenter(menu), Colors.white, interval = 0)

        choice = Write.Input("[?] >  ", default_color, interval = 0).strip()

        if choice == "1":
            clear()
            ip = Write.Input("[?] > IP-Adress: ", default_color, interval = 0)
            if not ip:
                clear()
                Write.Print("[!] > Please, enter IP Adress\n", default_color, interval = 0)
                continue
            ip_info(ip)

        elif choice == "2":
            clear()
            nickname = Write.Input("[?] > Username: ", default_color, interval = 0)
            Write.Print("[!] > Please wait, it may take some time...\n", default_color, interval = 0)
            if not nickname:
                clear()
                Write.Print("[!] > Please, enter username\n", default_color, interval = 0)
                continue
            username_search(nickname)

        elif choice == "3":
            clear()
            phone_number = Write.Input("[?] > Phone number: ", default_color, interval = 0)
            if not phone_number:
                clear()
                Write.Print("[!] > Please, enter phone number\n", default_color, interval = 0)
                continue
            phone_info(phone_number)
            
        elif choice == "4":
            clear()
            domain = Write.Input("[?] > URL: ", default_color, interval = 0)
            Write.Print("[!] > Please wait, it may take some time...\n", default_color, interval = 0)
            if not domain:
                clear()
                Write.Print("[!] > Please, enter URL\n", default_color, interval = 0)
                continue
            domain_info(domain)


        elif choice == "0":
            clear()
            Write.Print("\n[!] > Exiting...", default_color, interval = 0)
            exit()

        elif choice == "99":
            settings()

        else:
            clear()
            Write.Print("[!] > Invalid input.\n", default_color, interval = 0)
            continue

def settings():
    clear()
    while True:
        settings_menu_art = """\n   ▄████████  ▄██████▄      ███     
  ███    ███ ███    ███ ▀█████████▄ 
  ███    █▀  ███    ███    ▀███▀▀██ 
  ███        ███    ███     ███   ▀ 
▀███████████ ███    ███     ███     
         ███ ███    ███     ███     
   ▄█    ███ ███    ███     ███     
 ▄████████▀   ▀██████▀     ▄████▀   
\n"""

        settings_menu = """\n\n                                 [ S.O.T ]\n
                             Simple OSINT Tools
                                 Settings

╭─    ─╮╭─                   ─╮╭─                                         ─╮
|  №   ||       Setting       ||                Description                |
|======||=====================||===========================================|
| [1]  || Theme change        || Customize the SOT theme                   |
| [?]  || In development...   || ???                                       |
|------||---------------------||-------------------------------------------|
| [0]  || Back to menu        || Exit the settings                         |
╰─    ─╯╰─                   ─╯╰─                                         ─╯\n\n\n"""
        Write.Print(Center.XCenter(settings_menu_art), default_color, interval = 0)
        Write.Print(Center.XCenter(settings_menu), Colors.white, interval = 0)

        settings_choice = Write.Input("[?] >  ", default_color, interval = 0).strip()

        if settings_choice == "1":
            change_color()
        elif settings_choice == "0":
            main()
        else:
            clear()
            Write.Print("[!] > Invalid input.\n", default_color, interval = 0)
            continue

main()
