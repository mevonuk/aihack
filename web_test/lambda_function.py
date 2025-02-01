#fonction sur aws lambda

import json
import boto3

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')

def lambda_handler(event, context):
    try:
        if 'message' in event:
            user_message = event['message']
        else:
            body = json.loads(event.get('body', '{}'))
            user_message = body.get('message')

        if not user_message:
            raise ValueError("No message provided in the request.")

        # Nouveau prompt renforcé
        formatted_prompt = (
            f"<s>[INST] Tu es un modèle d'analyse de sentiments. "
            f"Analyse le texte suivant et réponds uniquement par l’un des mots suivants, sans ajouter d'explications : "
            f"'positif', 'négatif', ou 'factuel'. "
            f"Voici des exemples pour t'aider :\n\n"
            f"Exemple 1 : \"De nombreuses coupures électriques ont également touché le territoire et il a fallu le renfort d'équipes Enedis, arrivées de Corrèze les jours suivants, pour remettre en état l'intégralité du réseau. Jusqu'au mois de mai, le palais des Sports de Berck est resté fermé en raison des dégâts\" → positif\n"
            f"Exemple 2 : \"L’agence Enedis pourrait quitter la ville d’Avesnes-sur-Helpe, cette année. Le directeur départemental parle de «concertations en cours» et promet un maintien des services aux consommateurs. Pour la CGT, les dés sont jetés et les clients pâtiront de ce départ. \" → négatif\n"
            f"Exemple 3 : \"Une équipe d’Énedis était sur place, tout comme une patrouille de la police nationale. Après une inspection des lieux, les pompiers ont pu déterminer l’origine des fumées.\" → factuel\n\n"
            f"Texte : \"{user_message}\" [/INST]"
        )

        payload = {
            "modelId": "mistral.mistral-7b-instruct-v0:2",
            "contentType": "application/json",
            "accept": "application/json",
            "body": json.dumps({
                "prompt": formatted_prompt,
                "max_tokens": 5,  # Suffisant pour un seul mot
                "temperature": 0.2,  # Réponse déterministe
                "top_p": 0.9,
                "top_k": 50
            })
        }

        response = bedrock_runtime.invoke_model(
            modelId=payload["modelId"],
            contentType=payload["contentType"],
            accept=payload["accept"],
            body=payload["body"]
        )

        response_body = json.loads(response['body'].read().decode('utf-8'))
        outputs = response_body.get('outputs', [])
        reply = outputs[0].get('text', '').strip().lower() if outputs else 'No response generated.'

        # Normalisation de la réponse (suppression des espaces, gestion des variations)
        reply = reply.replace(".", "").replace("\n", "").strip()

        # Vérification des réponses attendues
        if reply not in ['positif', 'négatif', 'factuel']:
            reply = 'analyse non concluante'

        return {
            'statusCode': 200,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps({ 'reply': reply })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({ 'error': str(e) })
        }
