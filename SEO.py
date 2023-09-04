import requests
from bs4 import BeautifulSoup
import re
import os

# Liste des bibliothèques nécessaires
required_libraries = []

# Vérifiez si chaque bibliothèque est installée
missing_libraries = [lib for lib in required_libraries if not subprocess.call(["pip", "show", lib]) == 0]

# Installez les bibliothèques manquantes
if missing_libraries:
    print("Installation des bibliothèques nécessaires...")
    for lib in missing_libraries:
        subprocess.call(["pip", "install", lib])

# Codes ANSI pour les couleurs
COLORS = {
    "h1": "\033[92m",   # Vert
    "h2": "\033[93m",   # Jaune
    "h3": "\033[94m",   # Bleu
    "h4": "\033[95m",   # Magenta
    "h5": "\033[96m",   # Cyan
    "h6": "\033[91m",   # Rouge
    "reset": "\033[0m"  # Réinitialisation des couleurs
}
logo = '''
   _____ ______ ____    _______          _       ____                 _    _          _______        _     
  / ____|  ____/ __ \  |__   __|        | |     |  _ \               | |  (_)        |__   __|      | |    
 | (___ | |__ | |  | |    | | ___   ___ | |___  | |_) |_ __ ___  __ _| | ___ _ __   __ _| | ___  ___| |__  
  \___ \|  __|| |  | |    | |/ _ \ / _ \| / __| |  _ <| '__/ _ \/ _` | |/ / | '_ \ / _` | |/ _ \/ __| '_ \ 
  ____) | |___| |__| |    | | (_) | (_) | \__ \ | |_) | | |  __/ (_| |   <| | | | | (_| | |  __/ (__| | | |
 |_____/|______\____/     |_|\___/ \___/|_|___/ |____/|_|  \___|\__,_|_|\_\_|_| |_|\__, |_|\___|\___|_| |_|
                                                                                    __/ | V1.0                  
                                                                                   |___/                                
'''
colored_logo = '\033[91m' + logo + '\033[0m' 
def main():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colored_logo)
        previous_url = None

        while True:
            print("\n\033[94mMenu:\033[0m")
            print("\033[32m--------------------------------------------------------------------")
            print(" 1 - Vérifier le statut de l'url")
            print(" 2 - Afficher Title, méta, url canonical...")
            print(" 3 - Afficher les Hn")
            print(" 4 - Analyser les backlinks")
            print(" 5 - Quitter")
            print("---------------------------------------------------------------------\033[0m")

            choice = input("\nEntrez votre choix : ")

            if choice == "1":
                previous_url = check_url_status(previous_url)
            elif choice == "2":
                previous_url = analyze_seo_data(previous_url)
            elif choice == "3":
                previous_url = display_headings(previous_url)
            elif choice == "4":
                previous_url = backlinks_submenu(previous_url)
            elif choice == "5":
                print("\nMerci d'avoir utilisé cet outil :)")
                break
            else:
                print("Choix invalide. Veuillez entrer un nouveau choix.")

    except KeyboardInterrupt:
        print("\nProgramme interrompu. Merci d'avoir utilisé cet outil :)")

def check_url_status(previous_url):
    try:
        if previous_url:
            use_previous = input("Voulez-vous utiliser l'URL précédente? '1' (oui) / '2' (non) : ").strip().lower()
            if use_previous == "1":
                url = previous_url
            else:
                url = input("\nEntrez l'url de la page : ")
        else:
            url = input("\nEntrez l'url de la page : ")

        if not re.match(r'^https?://', url):
            url = 'http://' + url

        response = requests.get(url)
        code = response.status_code

        print("\nLe code de réponse de la page est :\033[92m", code, "\033[0m", end="")

        if len(response.history) > 0:
            original_url = response.history[0].url
            final_url = response.url
            print("\n\033[31m URL d'origine (avant redirection) :\033[0m", original_url, end="")
            print("\n\033[31m URL de redirection :\033[0m", final_url)

        # Mettre à jour previous_url ici
        previous_url = url  # Mettez à jour previous_url avec la nouvelle URL

        return previous_url

    except requests.exceptions.RequestException as e:
        print("Une erreur de requête s'est produite:", e)
        return previous_url

def analyze_seo_data(previous_url):
    try:
        if previous_url:
            use_previous = input("Voulez-vous utiliser l'URL précédente? '1' (oui) / '2' (non) : ").strip().lower()
            if use_previous == "1":
                url = previous_url
            else:
                url = input("\nEntrez l'URL de la page : ")
        else:
            url = input("\nEntrez l'URL de la page : ")

        if not re.match(r'^https?://', url):
            url = 'http://' + url

        response = requests.get(url)
        code = response.status_code

        if code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            title = soup.title.text if soup.title else 'N/A'
            meta_description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else 'N/A'
            url_canonical = soup.find('link', attrs={'rel': 'canonical'})['href'] if soup.find('link', attrs={'rel': 'canonical'}) else 'N/A'
            image_og = soup.find('meta', attrs={'property': 'og:image'})['content'] if soup.find('meta', attrs={'property': 'og:image'}) else 'N/A'
            
            print(f"\n\033[31mTitre:\033[0m {title}")
            print(f"\033[31mMéta description:\033[0m {meta_description}")
            print(f"\033[31mUrl Canonical:\033[0m {url_canonical}")
            print(f"\033[31mImage OG:\033[0m {image_og}")
        else:
            print("La requête n'a pas abouti.")

        return url

    except requests.exceptions.RequestException as e:
        print("Une erreur de requête s'est produite:", e)
        return previous_url

def display_headings(previous_url):
    try:
        if previous_url:
            use_previous = input("Voulez-vous utiliser l'URL précédente ? '1' (oui) / '2' (non) : ").strip().lower()
            if use_previous == "1":
                url = previous_url
            else:
                url = input("\nEntrez l'URL de la page : ")
        else:
            url = input("\nEntrez l'URL de la page : ")

        if not re.match(r'^https?://', url):
            url = 'http://' + url

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
                heading_type = heading.name
                color = COLORS.get(heading_type, COLORS["reset"])
                print(f"{color}{heading_type}: {heading.text}{COLORS['reset']}")
        
        return url

    except requests.exceptions.RequestException as e:
        print("Une erreur de requête s'est produite :", e)
        return previous_url

def backlinks_submenu(previous_url):
    while True:
        print("\n\033[94mSous-Menu - Analyser les backlinks internes et externes:\033[0m")
        print("\033[95m--------------------------------------------------------------------")
        print(" 1 - Lister les backlinks internes et externes avec leur ancre")
        print(" 2 - Vérifier la présence de liens cassés")
        print(" 3 - Analyser les liens entrant en code 404 et 301")
        print(" 4 - Retourner au menu principal")
        print("---------------------------------------------------------------------\033[0m")

        sub_choice = input("\nEntrez votre choix : ")

        if sub_choice == "1":
            analyze_backlinks(previous_url)
        elif sub_choice == "2":
            previous_url = check_broken_links(previous_url)  # Call the function with one argument
        elif sub_choice == "3":
            previous_url = analyze_404_301_links(previous_url)
        elif sub_choice == "4":
            os.system('cls' if os.name == 'nt' else 'clear')
            return previous_url
        else:
            print("Choix invalide. Veuillez entrer un nouveau choix.")

def analyze_backlinks(previous_url):
    try:
        if previous_url:
            use_previous = input("Voulez-vous utiliser l'URL précédente? '1' (oui) / '2' (non) : ").strip().lower()
            if use_previous == "1":
                url = previous_url
            else:
                url = input("\nEntrez l'url de la page : ")
        else:
            url = input("\nEntrez l'url de la page : ")

        if not re.match(r'^https?://', url):
            url = 'http://' + url

        response = requests.get(url)
        code = response.status_code

        if code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all("a")

            internal_links = []
            external_links = []
            broken_links = []
            redirect_links = []

            for link in links:
                href = link.get("href")
                anchor = link.get_text().strip()

                if href:
                    if href.startswith("#"):
                        internal_links.append(anchor)
                    elif re.match(r'^(https?:)?//', href):
                        if url in href:
                            internal_links.append(anchor)
                        else:
                            external_links.append((anchor, href))
                    else:
                        internal_links.append(anchor)

            print("\n\033[92mLiens internes :\033[0m")
            for idx, anchor in enumerate(internal_links, start=1):
                print(f"{idx}. \033[92m{anchor}\033[0m -> {href}")

            print("\n\033[93mLiens externes :\033[0m")
            for idx, (anchor, href) in enumerate(external_links, start=1):
                print(f"{idx}. \033[93m{anchor}\033[0m -> {href}")

            print("\n\033[92mNombre total de liens internes\033[0m :", len(internal_links))
            print("\033[93mNombre total de liens externes\033[0m :", len(external_links))

        else:
            print("La requête n'a pas abouti.")

        return url

    except requests.exceptions.RequestException as e:
        print("Une erreur de requête s'est produite:", e)
        return previous_url

def check_broken_links(previous_url):
    try:
        if previous_url:
            use_previous = input("Voulez-vous utiliser l'URL précédente? '1' (oui) / '2' (non) : ").strip().lower()
            if use_previous == "1":
                url = previous_url
            else:
                url = input("\nEntrez l'URL de la page : ")
        else:
            url = input("\nEntrez l'URL de la page : ")

        if not re.match(r'^https?://', url):
            url = 'http://' + url

        response = requests.get(url)
        code = response.status_code

        if code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)
            broken_links_404 = []
            redirected_links_301 = []

            broken_links = []

            print("\nAnalyse des liens cassés...\n")

            for link in links:
                link_url = link['href']

                if link_url.startswith('/'):
                    link_url = url + link_url

                if link_url.startswith(('http://', 'https://')):
                    try:
                        link_response = requests.get(link_url)
                        link_code = link_response.status_code

                        if link_code == 404:
                            broken_links.append((link_url, link.text))
                    except requests.exceptions.RequestException as e:
                        print(f"Erreur lors de la requête pour {link_url}: {e}")
                else:
                    print(f"Le lien {link_url} a été ignoré car il n'utilise pas le schéma HTTP/HTTPS.")

            if broken_links:
                print("\n\033[91mLiens cassés\033[0m :")
                for link_url, anchor_text in broken_links:
                    print(f"{link_url} - Ancre : {anchor_text}")
            else:
                print("\nAucun lien cassé trouvé.")

        else:
            print("La requête n'a pas abouti.")

    except requests.exceptions.RequestException as e:
        print("Une erreur de requête s'est produite:", e)

    return previous_url

def analyze_404_301_links(previous_url):
    try:
        if previous_url:
            use_previous = input("Voulez-vous utiliser l'URL précédente? '1' (oui) / '2' (non) : ").strip().lower()
            if use_previous == "1":
                url = previous_url
            else:
                url = input("\nEntrez l'URL de la page : ")
        else:
            url = input("\nEntrez l'URL de la page : ")

        if not re.match(r'^https?://', url):
            url = 'http://' + url

        response = requests.get(url)
        code = response.status_code

        if code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)
            broken_links_404 = []
            redirected_links_301 = []

            print("\nAnalyse des liens entrant en code 404 et 301...\n")

            for link in links:
                link_url = link['href']

                if link_url.startswith('/'):
                    link_url = url + link_url

                # Ajoutez une vérification pour exclure les liens indésirables (comme 'tel:', 'mailto:', etc.)
                if not link_url.startswith(('http://', 'https://')):
                    continue

                link_response = requests.get(link_url)
                link_code = link_response.status_code

                if link_code == 404:
                    broken_links_404.append((link_url, link.text))
                elif link_code == 301:
                    redirected_links_301.append((link_url, link.text))

            if broken_links_404:
                print("\n\033[91mLiens en code 404 (non trouvés) :\033[0m")
                for link_url, anchor_text in broken_links_404:
                    print(f"{link_url} - Ancre : {anchor_text}")

            if redirected_links_301:
                print("\n\033[91mLiens en code 301 (redirigés) :\033[0m")
                for link_url, anchor_text in redirected_links_301:
                    print(f"{link_url} - Ancre : {anchor_text}")

            if not broken_links_404 and not redirected_links_301:
                print("\n\033[92mAucun lien en code 404 ou 301 trouvé.\033[0m")

        else:
            print("La requête n'a pas abouti.")

    except requests.exceptions.RequestException as e:
        print("Une erreur de requête s'est produite:", e)
        return previous_url

if __name__ == "__main__":
    main()