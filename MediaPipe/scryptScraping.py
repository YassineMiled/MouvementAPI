import requests
from bs4 import BeautifulSoup
import json

# URL cible
url = "index.html"
css_selector = 'div.main-content'  # Sélecteur CSS de l'élément principal

# Lire le contenu HTML depuis le fichier
with open(url, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parser le contenu HTML avec BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Trouver l'élément principal avec le sélecteur CSS donné
element = soup.select_one(css_selector)

# Trouver toutes les balises <div> avec la classe 'markdown-content'
markdown_contents = soup.find_all('div', class_='markdown-content')

# Initialiser les listes pour stocker les données
data = []

# Vérifier et traiter les balises trouvées
if markdown_contents:
    for markdown_content in markdown_contents:
        heading_root = markdown_content.find('div', class_='anchor-heading-root')
        if heading_root:
            link_tag = heading_root.find('a', class_='anchor-heading-link')
            headingName = heading_root.find('h2', class_='anchor-heading')

            source = link_tag['href'] if link_tag else ''
            nomDuLangage = ''
            code_contents = []  # Liste pour maintenir l'ordre des segments de code
            seen_contents = set()  # Ensemble pour vérifier les doublons

            code_samples = markdown_content.find_all('div', class_='code-sample')
            for code_sample in code_samples:
                code_sample_body = code_sample.find('div', class_='code-sample-body')
                if code_sample_body:
                    pre_tags = code_sample_body.find_all('pre', class_='hljs syntax-highlighter dark-mode code-sample-pre')
                    for pre_tag in pre_tags:
                        code_content = pre_tag.get_text().strip()
                        
                        if code_content not in seen_contents:
                            seen_contents.add(code_content)
                            code_contents.append(code_content)

                code_tag = code_sample.find('code')
                if code_tag:
                    nomDuLangage = ' '.join(code_tag['class'])

            # Préparer un dictionnaire avec les informations nécessaires
            data_template = {
                'headingName': headingName.get_text(strip=True) if headingName else '',
                'source': source,
                'contenue': {
                    'nomDuLangage': nomDuLangage,
                    'contenue2': code_contents
                }
            }
            data.append(data_template)

# Sauvegarder les données dans des fichiers JSON
with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("fini")