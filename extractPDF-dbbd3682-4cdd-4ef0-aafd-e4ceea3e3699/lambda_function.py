from PyPDF2 import PdfReader
import re
import boto3
import json
import urllib.request  # ✅ Remplace requests

def extract_articles(pdf_file):
    articles = []
    reader = PdfReader(pdf_file)
    number_of_pages = len(reader.pages)
    page_num = 0

    article_pages = []
    index_start = 0
    loop = 1

    while loop and page_num < number_of_pages:
        page = reader.pages[page_num]
        text = page.extract_text()

        if "Page " in text:
            index_start = 1
            article_indexes = [m.start() for m in re.finditer('Page ', text)]
            for idx in article_indexes:
                try:
                    page_number = int(text[idx + 5: idx + 7].strip())
                    article_pages.append(page_number)
                except ValueError:
                    continue
        elif index_start:
            loop = 0

        page_num += 1

    for i in range(len(article_pages)):
        start_page = article_pages[i]
        end_page = article_pages[i + 1] if i + 1 < len(article_pages) else number_of_pages

        article_text = ""
        for page_num in range(start_page, end_page):
            page = reader.pages[page_num]
            article_text += page.extract_text()

        articles.append(article_text.strip())

    return articles

def lambda_handler(event, context):
    s3_client = boto3.client('s3')

    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    print(f"Fichier détecté : {key} dans le bucket : {bucket}")

    pdf_object = s3_client.get_object(Bucket=bucket, Key=key)
    pdf_data = pdf_object['Body'].read()

    articles = extract_articles(pdf_data)

    IA_API_URL = "https://6n9kl3vvv8.execute-api.us-west-2.amazonaws.com/dev"
    results = []

    for article in articles:
        try:
            # ✅ Utilisation d'urllib.request au lieu de requests
            data = json.dumps({'text': article}).encode('utf-8')
            req = urllib.request.Request(
                IA_API_URL,
                data=data,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib.request.urlopen(req) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                results.append(response_data)

        except urllib.error.HTTPError as e:
            results.append({'error': f"Erreur HTTP : {e.code}, {e.reason}"})

        except urllib.error.URLError as e:
            results.append({'error': f"Erreur réseau : {e.reason}"})

    return {
        'statusCode': 200,
        'body': json.dumps({
            'fichier': key,
            'articles_extraits': len(articles),
            'analyses': results
        })
    }
