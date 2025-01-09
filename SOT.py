import requests
from pystyle import Colors, Write, Center, Box, System
from phonenumbers import parse, is_valid_number, number_type, PhoneNumberType, geocoder, carrier, format_number, PhoneNumberFormat
import phonenumbers
import whois
import os
from concurrent.futures import ThreadPoolExecutor
import re
import base64
import zlib
from googlesearch import search
from bs4 import BeautifulSoup
import json

default_color = Colors.red  

menu_art = """
\n
   ▄████████  ▄██████▄      ███     
  ███    ███ ███    ███ ▀█████████▄ 
  ███    █▀  ███    ███    ▀███▀▀██ 
  ███        ███    ███     ███   ▀ 
▀███████████ ███    ███     ███     
         ███ ███    ███     ███     
   ▄█    ███ ███    ███     ███     
 ▄████████▀   ▀██████▀     ▄████▀   
\n"""


def restart():
    Write.Input("\n\n(@SOT)─[!] > Press Enter to return...", default_color, interval=0)
    System.Clear()

def ip_info(ip, ip_choice):
    if ip_choice == "1" :
        url = f"https://ipinfo.io/json"

    elif ip_choice == "2":
        url = f"https://ipinfo.io/{ip}/json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        response = response.json()
        ip_address = response.get('ip')
        city = response.get('city') or "None"
        region = response.get('region') or "None"
        country = response.get('country') or "None"
        postal = response.get('postal') or "None"
        isp = response.get('org') or "None"
        lat_long = response.get('loc') or "None"
        timezone = response.get('timezone') or "None"

        ip_details = f"""
╔════════════════════════════════════════════╗
                [ IP Details ]
    ======================================
   [+] > IP Address          : {ip_address}
   [+] > City                : {city}
   [+] > Region              : {region}
   [+] > Country             : {country}
   [+] > Postal code         : {postal}
   [+] > ISP                 : {isp}
   [+] > Latitude, Longitude : {lat_long}
   [+] > Timezone            : {timezone}
   [+] > Google Maps         : https://www.google.com/maps?q={lat_long}
    ======================================
╚════════════════════════════════════════════╝
"""
        Write.Print(ip_details, Colors.white, interval=0)
        restart()

    except requests.exceptions.Timeout:
        System.Clear()
        Write.Print("\n[!] > Request timed out. Please try again later", default_color, interval = 0)
        restart()
    except requests.exceptions.ConnectionError:
        System.Clear()
        Write.Print("\n[!] > Connection error", default_color, interval = 0)
        restart()
    except requests.exceptions.HTTPError as e:
        System.Clear()    
        Write.Print(f"\n[!] > HTTP error: {e.response.status_code}", default_color, interval = 0)
        restart()
    except Exception as e:
        System.Clear()
        Write.Print(f"\n[!] > Error: {e}", default_color, interval = 0)
        restart()


def username_search(nickname):
    def check_url(url):

        try:
            response = requests.get(url, timeout=10)
            status_code = response.status_code

            if status_code == 200:
                return f"   [+] > {url:<35} : Found"
            elif status_code == 404:
                return f"   [-] > {url:<35} : Not found"
            else:
                return f"   [-] > {url:<35} : Error: {status_code}"

        except requests.exceptions.Timeout:
            return f"   [-] > {url:<35} : Timeout"
        except requests.exceptions.ConnectionError:
            return f"   [-] > {url:<35} : Connection error"
        except requests.exceptions.RequestException:
            return f"   [-] > {url:<35} : Request error"
        except Exception:
            return f"   [-] > {url:<35} : Unexpected error"

    urls = [f"https://www.instagram.com/{nickname}",
            f"https://www.tiktok.com/@{nickname}",
            f"https://www.x.com/{nickname}",
            f"https://www.facebook.com/{nickname}",
            f"https://www.youtube.com/@{nickname}",
            f"https://t.me/{nickname}",
            f"https://www.twitch.tv/{nickname}",
            f"https://open.spotify.com/user/{nickname}",
            f"https://www.reddit.com/user/{nickname}",
            f"https://www.github.com/{nickname}",
            f"https://vk.com/{nickname}"]

    search_results = f"""
╔════════════════════════════════════════════╗
       [ Social Media Search Results ]
    ======================================
"""

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(check_url, urls))
    
    for result in results:
        search_results += f"{result}\n"

    search_results += f"    ======================================\n╚════════════════════════════════════════════╝\n"

    Write.Print(search_results, Colors.white, interval=0)

    restart()

def phone_info(phone_number):
    try:
        parsed_number = parse(phone_number)
        country = geocoder.country_name_for_number(parsed_number, "en") or "Unknown"
        region = geocoder.description_for_number(parsed_number, "en") or "Unknown"
        operator = carrier.name_for_number(parsed_number, "en") or "Unknown"
        valid = is_valid_number(parsed_number)
        validity = "Valid" if valid else "Invalid"
        number_type_code = number_type(parsed_number)
        number_type_str = {PhoneNumberType.MOBILE: "Mobile",
        PhoneNumberType.FIXED_LINE: "Fixed Line",
        PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed or Mobile",
        PhoneNumberType.VOIP: "VoIP",
        PhoneNumberType.TOLL_FREE: "Toll-Free",
        PhoneNumberType.PREMIUM_RATE: "Premium Rate",
        }.get(number_type_code) or "Unknown"
        intl_format = format_number(parsed_number, PhoneNumberFormat.INTERNATIONAL)
        national_format = format_number(parsed_number, PhoneNumberFormat.NATIONAL)
        e164_format = format_number(parsed_number, PhoneNumberFormat.E164)
        phonetext = f"""
\n
╔════════════════════════════════════════════╗
             [ Phone Number Info ]
    ======================================
   [+] > Number          : {phone_number}
   [+] > Country         : {country}
   [+] > Region          : {region}
   [+] > Operator        : {operator}
   [+] > Validity        : {validity}
   [+] > Type            : {number_type_str}
   [+] > Intl. Format    : {intl_format}
   [+] > National Format : {national_format}
   [+] > E.164 Format    : {e164_format}
    ======================================
╚════════════════════════════════════════════╝\n"""

        Write.Print(phonetext, Colors.white, interval=0)
        restart()
    except phonenumbers.phonenumberutil.NumberParseException:
        System.Clear()
        Write.Print(f"(@SOT)─[!] > Error: invalid phone number format", default_color, interval = 0)
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
        registrant_name = domain_data.registrant_name or "Private"
        registrant_email = domain_data.registrant_email or "Private"

        domain_details = f"""
╔════════════════════════════════════════════╗
                 [ WHOIS Info ]
    ======================================
   [+] > Domain           : {domain_name}
   [+] > Registrar        : {domain_registrar}
   [+] > Creation Date    : {domain_creation_date}
   [+] > Expiration Date  : {domain_expiration_date}
   [+] > Last Updated     : {domain_updated_date}
   [+] > Registrant Name  : {registrant_name}
   [+] > Registrant Email : {registrant_email}
    ======================================
╚════════════════════════════════════════════╝
"""
        Write.Print(domain_details, Colors.white, interval=0)
        restart()
    except Exception as e:
        Write.Print(f"\n(@SOT)─[!] > Error: {e}", default_color, interval=0)
        restart()

def server_lookup(invite_link):

    try:
        response = requests.get(f"https://discord.com/api/v10/invites/{invite_link}")
        response.raise_for_status()
    except requests.exceptions.RequestException:
        Write.Print("\n(@SOT)─[-] > Request failed. Either Discord servers are down, or the link is invalid.\n", default_color, interval=0)
        restart()

    except Exception as e:
        Write.Print(f"\n(@SOT)─[-] > Error: {str(e)}\n", default_color, interval=0)
        restart()


    if response.status_code == 200:
        discord = response.json()
        inviter = discord.get('inviter', {})
        username = inviter.get('username') or 'Unknown'
        userid = inviter.get('id') or 'Unknown'
        guild = discord.get('guild', {})
        code = discord.get('code')
        date = discord.get('expires_at') or 'Never'
        serverid = guild.get('id') or 'Unknown'
        verification = guild.get('verification_level') or 'Unknown'
        channel = discord.get('channel', {}).get('name') or 'Unknown'
        servername = guild.get('name') or 'Unknown'
        results = f"""
╔════════════════════════════════════════════╗
              [ Invite Details ]
    ======================================
   [+] > Invite Link     : https://discord.gg/{code}
   [+] > Target Channel  : {channel}
   [+] > Expiration Date : {date}
    ======================================
              [ Inviter Details ]
    ======================================
   [+] > Username : {username}
   [+] > User ID  : {userid}
    ======================================
              [ Server Details ]
    ======================================
   [+] > Server Name        : {servername}
   [+] > Server ID          : {serverid}
   [+] > Verification Level : {verification}
    ======================================
╚════════════════════════════════════════════╝
"""
        Write.Print(results, Colors.white, interval=0)
        restart()


def token_info(token):

    headers = {'Authorization': token,
               'Content-Type': 'application/json'}

    try:
        response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        Write.Print(f"\n(@SOT)─[-] > HTTP Error: {http_err.response.status_code}\n", default_color, interval=0)
        restart()

    except requests.exceptions.RequestException:
        Write.Print("\n(@SOT)─[-] > Request failed. Either Discord servers are down, or the token is invalid.\n", default_color, interval=0)
        restart()
    except Exception as e:
        Write.Print(f"\n(@SOT)─[-] > Error: {str(e)}\n", default_color, interval=0)
        restart()


    if response.status_code == 200:

        discord = response.json()
        nickname = discord["username"]
        userid = discord["id"]
        token_email = discord["email"] or "Unknown"
        phonenumber = discord["phone"] or "Unknown"
        mfa = discord['mfa_enabled'] or "None"
        nitro_status = discord['premium_type']
        nitro = "Yes" if nitro_status else "No"
        verify = discord['verified']
        verified = "Yes" if verify else "No"
        results = f"""
╔════════════════════════════════════════════╗
               [ Token Details ]
    ======================================
   [+] > Username       : {nickname}
   [+] > User ID        : {userid}
   [+] > Email          : {token_email}
   [+] > Phone number   : {phonenumber}
   [+] > Nitro          : {nitro}
   [+] > MFA            : {mfa}
   [+] > Email verified : {verified}
    ======================================
╚════════════════════════════════════════════╝
"""
        Write.Print(results, Colors.white, interval=0)
        restart()


def obfuscate_code(path):
    def read_file(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()

        except UnicodeDecodeError:
            Write.Print(f"(@SOT)─[!] > Encoding error while reading file {file_path}", default_color, interval = 0)
            restart()

        except FileNotFoundError:
            Write.Print(f"(@SOT)─[!] > File {file_path} not found", default_color, interval = 0)
            restart()


    def write_obfuscated_code(obfuscated_code, output_path):
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(obfuscated_code)
    
    python_code = read_file(path)
    if python_code is None:
        return

    base64_encoded = base64.b64encode(python_code.encode('utf-8')).decode('utf-8')

    zlib_encoded = zlib.compress(base64_encoded .encode('utf-8'))

    zlib_encoded_base64 = base64.b64encode(zlib_encoded).decode('utf-8')

    reversed_encoded = zlib_encoded_base64[::-1]

    output_file = os.path.splitext(path)[0] + "_enc.py"

    code = f'''import base64
import zlib
encoded_code = "{reversed_encoded}"
exec(base64.b64decode(zlib.decompress(base64.b64decode(encoded_code[::-1]))).decode('utf-8'))'''

    write_obfuscated_code(code, output_file)
        
    Write.Print(f"(@SOT)─[+] > File successfully saved as: {output_file}", default_color, interval = 0)

    restart()

def check_proxy(proxy, url):
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    try:
        response = requests.get(url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            print(f"\n(@SOT)─[+] > {proxy} valid")
            return proxy
        else:
            print(f"\n(@SOT)─[-] > {proxy} is not valid or the server is not accessible at the moment")
    except requests.RequestException:
        print(f"\n(@SOT)─[-] > {proxy} not valid")
    return None

def google_dork_search(num_results, dork):
    System.Clear()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    Write.Print("(@SOT)─[!] > Please wait, it may take some time...\n", default_color, interval = 0)
    try:
        urls = []
        for url in search(dork, num_results=num_results):
            try:    
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                urls.append(url)
                print(f"\n(@SOT)─[+] > Found (Accessible)\nURL: {url}\n")
            except requests.RequestException:
                print(f"\n(@SOT)─[+] > Found (Inaccessible)\nURL: {url}\n")
                continue
        if not urls:
            print("(@SOT)─[!] > No results found")
        else:
            Write.Print(f"(@SOT)─[!] > Found {len(urls)}/{num_results}", default_color, interval=0)

            create_file = Write.Input("\n(@SOT)─[?] > Do you want to create a file with results? (y/n): ", default_color, interval=0).strip().lower()
            
            if create_file == "y":
                with open("google_dork.txt", "w", encoding="utf-8") as file:
                    file.write(f"Search Results:\n\n")
                    for url in urls:
                        file.write(f"{url}\n\n")
                Write.Print(f'\n(@SOT)─[+] > Results saved to "google_dork.txt"', default_color, interval=0)
            elif create_file == "n":
                Write.Print("\n(@SOT)─[+] > Results not saved", default_color, interval=0)
            else:
                Write.Print("(@SOT)─[!] > Invalid input. Results not saved", default_color, interval=0)

    except Exception as e:
        print(f"(@SOT)─[!] > Error: {e}")

    restart()

def tiktok_parser(username):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
    }

    url = f'https://www.tiktok.com/@{username}'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        Write.Print(f"\n(@SOT)─[!] > Error: {e}", default_color, interval=0)
        restart()

    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find('script', id='__UNIVERSAL_DATA_FOR_REHYDRATION__', type='application/json')

    try:
        json_data = json.loads(script_tag.string)
        user_data = json_data['__DEFAULT_SCOPE__']['webapp.user-detail']
        user_info = user_data['userInfo']['user']
        stats = user_data['userInfo']['stats']
        share_meta = user_data['shareMeta']
        id = user_info['id']
        uniqueid = user_info['uniqueId']
        nickname = user_info['nickname']
        bio = user_info['signature'].replace('\n', ' ')
        privacy = user_info['privateAccount']
        region = user_info['region']
        language = user_info['language']
        desc = share_meta['desc']
        title = share_meta['title']
        vidcount = stats['videoCount']
        likecount = stats['heartCount']
        followcount = stats['followingCount']
        followercount = stats['followerCount']
        results = f"""
╔════════════════════════════════════════════╗
             [ Token Parser Info ]
    ======================================
   [+] > Username        : {username}
   [+] > ID              : {id}
   [+] > Unique ID       : {uniqueid}
   [+] > Region          : {region}
   [+] > Language        : {language}
   [+] > Bio             : {bio}
   [+] > Description     : {desc}
   [+] > Title           : {title}
   [+] > Video Count     : {vidcount}
   [+] > Like Count      : {likecount}
   [+] > Following Count : {followcount}
   [+] > Follower Count  : {followercount}
   [+] > Private Account : {privacy}
    ======================================
╚════════════════════════════════════════════╝"""
        Write.Print(results, Colors.white, interval=0)
        restart()

    except (json.JSONDecodeError, KeyError):
        Write.Print(f"\n(@SOT)─[!] > Error. This profile does not exist", default_color, interval=0)
        restart()


def change_color():
    global default_color
    System.Clear()
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
| [99] || Choose a gradient     |
╰─    ─╯╰─                     ─╯
"""
    Write.Print(Center.XCenter(color_menu), Colors.white, interval=0)

    color_choice = Write.Input("\n\n(@SOT)─[?] >  ", default_color, interval=0).strip()

    color = {"1": Colors.red,
        "2": Colors.blue,
        "3": Colors.green,
        "4": Colors.yellow,
        "5": Colors.cyan,
        "6": Colors.white}

    if color_choice in color:
        default_color = color[color_choice]
        System.Clear()
        Write.Print("(@SOT)─[!] > Color changed successfully.\n", default_color, interval=0)

    elif color_choice == "99":
        gradient()

    elif color_choice == "0":
        System.Clear()
        return
    else:
        System.Clear()
        Write.Print("(@SOT)─[!] > Invalid input\n", default_color, interval=0)

def gradient():
    global default_color
    System.Clear()
    gradient_menu = """
╭─    ─╮╭─                     ─╮
|  №   ||        Gradient       |
|======||=======================|
| [1]  || Red to yellow         |
| [2]  || Blue to cyan          |
| [3]  || Green to white        |
| [4]  || Red to purple         |
| [5]  || Cyan to green         |
| [6]  || White to blue         |
|------||-----------------------|
| [0]  || Back to settings menu |
| [99] || Choose a colour       |
╰─    ─╯╰─                     ─╯
"""
    Write.Print(Center.XCenter(gradient_menu), Colors.white, interval=0)

    gradient_choice = Write.Input("\n\n(@SOT)─[?] >  ", default_color, interval=0).strip()

    gradient = {"1": Colors.red_to_yellow,
        "2": Colors.blue_to_cyan,
        "3": Colors.green_to_white,
        "4": Colors.red_to_purple,
        "5": Colors.cyan_to_green,
        "6": Colors.white_to_blue}
    
    if gradient_choice in gradient:
        default_color = gradient[gradient_choice]
        System.Clear()
        Write.Print("(@SOT)─[!] > Color changed successfully.\n", default_color, interval=0)

    elif gradient_choice == "99":
        change_color()

    elif gradient_choice == "0":
        System.Clear()
        return
    else:
        System.Clear()
        Write.Print("(@SOT)─[!] > Invalid input\n", default_color, interval=0)


def main():
    System.Clear()
    while True:
        menu = """\n\n                                   [ S.O.T ]\n
                               Simple OSINT Tools

╭─    ─╮╭─                     ─╮╭─                                             ─╮
|  №   ||         Tools         ||                  Description                  |
|======||=======================||===============================================|
| [1]  || Lookup tools          || Analyze data like IP, domain, phone, etc      |
| [2]  || Social Media tools    || Analyze data from social networks             |
| [3]  || Other tools           || Additional utilities                          |
|------||-----------------------||-----------------------------------------------|
| [0]  || Exit                  || Exit the program                              |
| [99] || Settings              || Customize configurations                      |
╰─    ─╯╰─                     ─╯╰─                                             ─╯\n\n\n"""

        Write.Print(Center.XCenter(menu_art), default_color, interval = 0)
        Write.Print(Center.XCenter(menu), Colors.white, interval = 0)

        choice = Write.Input("(@SOT)─[?] > ", default_color, interval = 0)

        if choice == "1":
            lookup()
        
        elif choice == "2":
            socialmedia()

        elif choice == "3":
            other()

        elif choice == "0":
            System.Clear()
            Write.Print("\n(@SOT)─[!] > Exiting the program...\n", default_color, interval = 0)
            exit()

        elif choice == "99":
            settings()

        else:
            System.Clear()
            Write.Print("(@SOT)─[!] > Invalid input\n", default_color, interval = 0)
            continue



def lookup():
    System.Clear()
    while True:
        menu = """\n\n                                  [ S.O.T ]\n
                              Simple OSINT Tools
                                 Lookup Tools

╭─    ─╮╭─                     ─╮╭─                                            ─╮
|  №   ||       Function        ||                  Description                 |
|======||=======================||==============================================|
| [1]  || IP Info Search        || Find details about an IP address             |
| [2]  || Phone Info Search     || Look up information linked to a phone number |
| [3]  || Domain Info Search    || Gather information related to a domain name  |
| [4]  || Google dork search    || Find more information with Google Dorks      |
| [?]  || In development...     || ???                                          |
|------||-----------------------||----------------------------------------------|
| [0]  || Back to menu          || Return to the main menu                      |
╰─    ─╯╰─                     ─╯╰─                                            ─╯\n\n\n"""
        Write.Print(Center.XCenter(menu_art), default_color, interval = 0)
        Write.Print(Center.XCenter(menu), Colors.white, interval = 0)

        choice = Write.Input("(@SOT)─[?] > ", default_color, interval = 0)

        if choice == "1":
            System.Clear()
            Write.Print("[1] > Check your IP Address\n[2] > Check other IP Address\n", Colors.white, interval = 0)

            ip_choice = Write.Input("\n(@SOT)─[?] > ", default_color, interval = 0)
            if ip_choice == "1":
                System.Clear()
                ip_info(None, ip_choice)
            elif ip_choice == "2":
                System.Clear()
                ip = Write.Input("(@SOT)─[?] > IP-Adress: ", default_color, interval = 0)
                if not ip:
                    System.Clear()
                    Write.Print("(@SOT)─[!] > Please, enter IP Adress\n", default_color, interval = 0)
                    continue
                ip_info(ip, ip_choice)
            else:
                System.Clear()
                Write.Print("(@SOT)─[!] > Invalid input\n", default_color, interval = 0)
                continue

        elif choice == "2":
            System.Clear()
            phone_number = Write.Input("(@SOT)─[?] > Phone number: ", default_color, interval = 0)
            if not phone_number:
                System.Clear()
                Write.Print("(@SOT)─[!] > Please, enter phone number\n", default_color, interval = 0)
                continue
            phone_info(phone_number)

        elif choice == "3":
            System.Clear()
            domain = Write.Input("(@SOT)─[?] > URL: ", default_color, interval = 0)
            Write.Print("(@SOT)─[!] > Please wait, it may take some time...\n", default_color, interval = 0)
            if not domain:
                System.Clear()
                Write.Print("(@SOT)─[!] > Please, enter URL\n", default_color, interval = 0)
                continue
            domain_info(domain)

        elif choice == "4":
            System.Clear()
            dork = Write.Input(f"(@SOT)─[?] > Enter the search query: ", default_color, interval=0).strip()
            num_results = int(Write.Input("(@SOT)─[?] > Number of results: ", default_color, interval=0))
            google_dork_search(num_results, dork)
            if not dork or not num_results:
                System.Clear()
                Write.Print("(@SOT)─[!] > Please, enter search query and number of results\n", default_color, interval = 0)
                continue

        elif choice == "0":
            main()

        else:
            System.Clear()
            Write.Print("(@SOT)─[!] > Invalid input\n", default_color, interval = 0)
            continue
                

def socialmedia():
    System.Clear()
    while True:
        menu = """\n\n                                 [ S.O.T ]\n
                             Simple OSINT Tools
                             Social Media Tools

╭─    ─╮╭─                     ─╮╭─                                           ─╮
|  №   ||       Function        ||                  Description                |
|======||=======================||=============================================|
| [1]  || Social media search   || Find profiles across social media platforms |
| [2]  || Discord invite lookup || Get details about a Discord invite link     |
| [3]  || Discord token info    || Get information related to a Discord token  |
| [4]  || TikTok profile parser || Parse information from TikTok profile       |
| [?]  || In development...     || ???                                         |
|------||-----------------------||---------------------------------------------|
| [0]  || Back to menu          || Return to the main menu                     |
╰─    ─╯╰─                     ─╯╰─                                           ─╯\n\n\n"""
        Write.Print(Center.XCenter(menu_art), default_color, interval = 0)
        Write.Print(Center.XCenter(menu), Colors.white, interval = 0)

        choice = Write.Input("(@SOT)─[?] > ", default_color, interval = 0)

        if choice == "1":
            System.Clear()
            nickname = Write.Input("(@SOT)─[?] > Username: ", default_color, interval = 0)
            Write.Print("(@SOT)─[!] > Please wait, it may take some time...\n", default_color, interval = 0)
            if not nickname:
                System.Clear()
                Write.Print("(@SOT)─[!] > Please, enter username\n", default_color, interval = 0)
                continue
            username_search(nickname)

        elif choice == "2":
            System.Clear()
            invite_link = Write.Input("(@SOT)─[?] > Invite code: ", default_color, interval = 0)
            if not invite_link:
                System.Clear()
                Write.Print("(@SOT)─[!] > Please, enter invite code\n", default_color, interval = 0)
                continue
            server_lookup(invite_link)

        elif choice == "3":
            System.Clear()
            token = Write.Input("(@SOT)─[?] > Token: ", default_color, interval = 0)
            if not token:
                System.Clear()
                Write.Print("(@SOT)─[!] > Please, enter token\n", default_color, interval = 0)
                continue
            token_info(token)

        elif choice == "4":
            System.Clear()
            username = Write.Input("(@SOT)─[?] > Username (without @): ", default_color, interval = 0)
            if not username:
                System.Clear()
                Write.Print("(@SOT)─[!] > Please, enter username\n", default_color, interval = 0)
                continue
            tiktok_parser(username)

        elif choice == "0":
            main()

        else:
            System.Clear()
            Write.Print("(@SOT)─[!] > Invalid input\n", default_color, interval = 0)
            continue
        
def other():
    System.Clear()
    while True:
        menu = """\n\n                                  [ S.O.T ]\n
                              Simple OSINT Tools
                                  Other tools

╭─    ─╮╭─                     ─╮╭─                                           ─╮
|  №   ||       Function        ||                 Description                 |
|======||=======================||=============================================|
| [1]  || Python Code Obfuscate || Obfuscate Python code using base64 and zlib |
| [2]  || Proxy Checker         || Simple HTTP/HTTPS proxy checker             |
| [?]  || In development...     || ???                                         |
|------||-----------------------||---------------------------------------------|
| [0]  || Back to menu          || Exit the settings                           |
╰─    ─╯╰─                     ─╯╰─                                           ─╯\n\n\n"""
        Write.Print(Center.XCenter(menu_art), default_color, interval = 0)
        Write.Print(Center.XCenter(menu), Colors.white, interval = 0)

        choice = Write.Input("(@SOT)─[?] > ", default_color, interval = 0)
        if choice == "1":
            System.Clear()
            path = Write.Input("(@SOT)─[?] > File Path: ", default_color, interval = 0)
            if not path:
                System.Clear()
                Write.Print("(@SOT)─[!] > Please, enter path to file\n", default_color, interval = 0)
                continue
            obfuscate_code(path)

        elif choice == "2":
            System.Clear()
            input_file = Write.Input("(@SOT)─[?] > Path to txt file with proxies: ", default_color, interval = 0)
            url = Write.Input("(@SOT)─[?] > URL to test proxies: ", default_color, interval = 0)
            if not input_file or not url:
                System.Clear()
                Write.Print("(@SOT)─[!] > Please, enter path to file and url\n", default_color, interval = 0)
                continue
            try:
                with open(input_file, "r") as file:
                    proxies = [line.strip() for line in file.readlines()]
            except FileNotFoundError:
                System.Clear()
                Write.Print(f'(@SOT)─[!] > File "{input_file}" not found', default_color, interval = 0)
                return

            valid = []

            for proxy in proxies:
                result = check_proxy(proxy, url)
                if result:
                    valid.append(result)
                    
            if valid:
                create_file = Write.Input("\n(@SOT)─[?] > Do you want to create a file with valid proxies? (y/n): ", default_color, interval=0).strip().lower()
                if create_file == "y":
                    with open("valid_proxies.txt", "w", encoding="utf-8") as file:
                        file.write("\n".join(valid))
                    Write.Print(f'\n\n(@SOT)─[+] > Proxy check completed. Valid proxies saved to "valid_proxies.txt"', default_color, interval = 0)
                elif create_file == "n":
                    Write.Print("\n(@SOT)─[+] > Results not saved", default_color, interval=0)
                else:
                    Write.Print("(@SOT)─[!] > Invalid input. Results not saved", default_color, interval=0)

            else:
                Write.Print("\n\n(@SOT)─[-] > No valid proxies found")
            restart()

        elif choice == "0":
            main()

        else:
            System.Clear()
            Write.Print("(@SOT)─[!] > Invalid input.\n", default_color, interval = 0)
            continue

def settings():
    System.Clear()
    while True:
        menu = """\n\n                                [ S.O.T ]\n
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
        Write.Print(Center.XCenter(menu_art), default_color, interval = 0)
        Write.Print(Center.XCenter(menu), Colors.white, interval = 0)

        settings_choice = Write.Input("(@SOT)─[?] >  ", default_color, interval = 0).strip()

        if settings_choice == "1":
            change_color()

        elif settings_choice == "0":
            main() 
        else:
            System.Clear()
            Write.Print("(@SOT)─[!] > Invalid input.\n", default_color, interval = 0)
            continue

main()
