from collections import Counter
import re
import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests

def occurrences_mots(texte):
    mots = re.findall(r'\b\w+\b', texte.lower())
    occurrences = Counter(mots)
    occurrences = occurrences.most_common()
    return occurrences

def supprimer_mots_parasites(occurrences, mots_parasites):
    mots_filtrés = [(mot, occ) for mot, occ in occurrences if mot not in mots_parasites]
    return mots_filtrés

def lire_mots_parasites(fichier_csv):
    with open(fichier_csv, 'r', newline='') as file:
        reader = csv.reader(file)
        mots_parasites = [mot[0] for mot in reader]
    return mots_parasites



def supprimer_balises_html(texte_html):
    soup = BeautifulSoup(texte_html, 'html.parser')
    texte_sans_balises = soup.get_text(separator=' ')
    return texte_sans_balises

def valeurs_attribut_html(texte_html, balise, attribut):
    soup = BeautifulSoup(texte_html, 'html.parser')
    valeurs = [element.get(attribut) for element in soup.find_all(balise)]
    return valeurs


def extraire_nom_domaine(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def filtrer_urls_par_domaine(nom_domaine, liste_urls):
    urls_domaine = []
    urls_hors_domaine = []

    for url in liste_urls:
        domaine_url = extraire_nom_domaine(url)
        if domaine_url == nom_domaine:
            urls_domaine.append(url)
        else:
            urls_hors_domaine.append(url)

    return urls_domaine, urls_hors_domaine

def recuperer_texte_html(url):
    try:
        reponse = requests.get(url)
        reponse.raise_for_status()
        return reponse.text
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération du texte HTML : {e}")
        return None

def audit_page():
    
    print("\n==> Début de l'analyse...")
    url_page = input("Veuillez entrer l'URL de la page à analyser : ")

    
    texte_html_page = recuperer_texte_html(url_page)

    if texte_html_page:
        
        texte_sans_balises = supprimer_balises_html(texte_html_page)

        
        occurrences = occurrences_mots(texte_sans_balises)

        
        mots_parasites = lire_mots_parasites("parasite.csv")

        
        mots_filtres = supprimer_mots_parasites(occurrences, mots_parasites)

        
        valeurs_alt_img = valeurs_attribut_html(texte_html_page, 'img', 'alt')

        
        nom_domaine = extraire_nom_domaine(url_page)

        
        liste_urls_test = [
            "https://www.example.com/page1.html",
            "https://www.example.com/page2.html",
            "https://www.anotherdomain.com/page3.html",
            "https://www.example.com/page4.html",
        ]

        
        urls_domaine, urls_hors_domaine = filtrer_urls_par_domaine(nom_domaine, liste_urls_test)

        ''
        print("\n=== Résultats de l'audit ===\n")
        print("Mots clefs les plus importants :", mots_filtres[:3])
        print("Nombre de liens entrants :", len(urls_domaine))
        print("Nombre de liens sortants :", len(urls_hors_domaine))
        print("Présence de balises alt pour les images :", valeurs_alt_img)
        print("\n====== Fin de l'audit ======\n")
    else:
        print("ERROR ! Impossible de récupérer le texte HTML de la page.")

audit_page()

#Test étapes 1-2-3

texte_a_analyser = """
    L'optimisation pour les moteurs de recherche, aussi connue sous le sigle SEO, inclut l'ensemble des techniques qui visent à améliorer le positionnement d'une page, d'un site ou d'une application web dans la page de résultats d'un moteur de recherche.
"""
occurrences = occurrences_mots(texte_a_analyser)

mots_parasites = lire_mots_parasites("parasite.csv")

mots_filtres = supprimer_mots_parasites(occurrences, mots_parasites)

print("\n=== Liste desccurrences de mots triées ===")
for mot, occ in occurrences:
    print(f"{mot}: {occ}")

print("\n=== Liste des mots parasites ===")
print(mots_parasites)

print("\n=== Liste des mots filtrés ===")
for mot, occ in mots_filtres:
    print(f"{mot}: {occ}")


#Test etapes 5-6-7

html_test_img_alt = """
    <img src='image1.jpg' alt="Description de l'image 1">
    <img src='image2.jpg' alt="Description de l'image 2">
    <img src='image3.jpg' alt="Description de l'image 3">
"""
valeurs_alt_img = valeurs_attribut_html(html_test_img_alt, 'img', 'alt')

print("\n=== Résultats pour les attributs alt des balises img ===")
for i, valeur in enumerate(valeurs_alt_img, start=1):
    print(f"Image {i}: {valeur}")

html_test_href = """
    <a href='lien1.html'>Lien 1</a>
    <a href='lien2.html'>Lien 2</a>
    <a href='lien3.html'>Lien 3</a>
"""
valeurs_href_a = valeurs_attribut_html(html_test_href, 'a', 'href')

print("\n=== Résultats pour les attributs href des balises a ===")
for i, valeur in enumerate(valeurs_href_a, start=1):
    print(f"Lien {i}: {valeur}")
