from PyPDF2 import PdfReader
import re
import boto3
import openpyxl

session = boto3.Session()
bedrock = session.client(service_name='bedrock-runtime')

def pass_to_model(text):

    doc_message = {
      "role": "user",
      "content": [
          { "text": text }
      ]
    }

    response = bedrock.converse(
        modelId="mistral.mistral-large-2407-v1:0",
        messages=[doc_message],
        inferenceConfig={
            "maxTokens": 20,
            "temperature": 0.1,
            "topP": 0.2
        },
    )

    return response['output']['message']['content'][0]['text']



# this needs to be replaced with uploaded PDF
reader = PdfReader("Revue-Médias - DR Nord-Pas-de-Calais du 02012025.pdf")
number_of_pages = len(reader.pages)
page_num = 0

article_page = []
loop = 1
index_start = 0
while loop and page_num <= number_of_pages:
    page = reader.pages[page_num]
    text = page.extract_text()
    if "Page " in text:
        index_start = 1
        article_index1 = [m.start() for m in re.finditer('Page ', text)]
        for pp in article_index1:
            article_page.append(int(text[pp+5:pp+7:1]))
    elif index_start:
        loop = 0
    page_num = page_num + 1

# open excel file
wBook = openpyxl.Workbook()
sheet = wBook.active
col1 = 'ouput'
col2 = 'input'
sheet.append([col1,col2])

# have page numbers of all articles in article_page list
num_articles = len(article_page)
pp = 0
p1 = 0
while pp <= num_articles - 1:
    p1 = pp
    page = reader.pages[article_page[pp]]
    text = page.extract_text()
    while pp < num_articles - 1 and article_page[pp + 1] > article_page[p1] + 1:
        p1 = p1 + 1
        page = reader.pages[article_page[p1]]
        text = text + page.extract_text()

        formatted_prompt1 = (
            f"<s>[INST] Tu es un analyste de l'entreprise Enedis. "
            f"Analyse le texte suivant et décrit l'image d'Enedis dégagée avec un des mots suivants, sans ajouter d'explications : "
            f"'positif', 'négatif', factuel', 'factuel positif', 'factuel négatif', positif nuancé, négatif nuancé. La distribution des différents résultats est la suivante : 'factuel': 741/1000, 'factuel négatif': 23/1000, 'factuel positif': 53/1000, 'négatif': 47/1000, 'négatif nuancé': 19/1000, 'positif': 80/1000, 'positif nuancé': 37/1000."
            f"Voici des exemples pour t'aider :\n\n"
            f"Exemple 1 : \"De nombreuses coupures électriques ont également touché le territoire et il a fallu le renfort d'équipes Enedis, arrivées de Corrèze les jours suivants, pour remettre en état l'intégralité du réseau. Jusqu'au mois de mai, le palais des Sports de Berck est resté fermé en raison des dégâts\" → positif\n"
            f"Exemple 2 : \"L’agence Enedis pourrait quitter la ville d’Avesnes-sur-Helpe, cette année. Le directeur départemental parle de «concertations en cours» et promet un maintien des services aux consommateurs. Pour la CGT, les dés sont jetés et les clients pâtiront de ce départ. \" → négatif\n"
            f"Exemple 3 : \"Une équipe d’Énedis était sur place, tout comme une patrouille de la police nationale. Après une inspection des lieux, les pompiers ont pu déterminer l’origine des fumées.\" → factuel\n\n"
            f"Texte : \"{text}\" [/INST]"
        )
        predicted_output = pass_to_model(formatted_prompt1)
        sheet.append([predicted_output,text])
    pp = pp + 1

wBook.save('AIoutput.xlsx')