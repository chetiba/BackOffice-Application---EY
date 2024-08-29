from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
import requests
import logging

# Set up logging
logger = logging.getLogger(__name__)

class ActionSearchCVByName(Action):
    def name(self) -> Text:
        return "action_search_cv_by_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        person_name = tracker.get_slot('Nom')
        competences = tracker.get_slot('competences')

        if person_name:
            query = person_name
        elif competences:
            query = competences
        else:
            dispatcher.utter_message(text="Je n'ai pas compris le nom ou les compétences. Pouvez-vous préciser davantage ?")
            return []

        logger.info(f"Recherche de CV pour : {query}")
        self.send_params_to_django(query, dispatcher)
        return []

    def send_params_to_django(self, query: str, dispatcher: CollectingDispatcher):
        url = f"http://localhost:8000/collaborateurs/search/?query={query}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if 'cvs' in data and data['cvs']:
            # Start with a friendly introduction
            if len(data['cvs']) == 1:
                intro_text = "Voici le CV que vous avez demandé :"
            else:
                intro_text = "Voici les CVs que vous avez demandés :"
            dispatcher.utter_message(text=intro_text)

            # List each CV
            for cv in data['cvs']:
                prenom = cv.get('prenom', 'Prénom non spécifié')
                nom = cv.get('nom', 'Nom non spécifié')
                cv_url = cv['url']
                cv_info = f"{prenom} {nom} - [Voir le CV]({cv_url})"
                dispatcher.utter_message(text=cv_info)
        else:
            dispatcher.utter_message(text="Aucun CV trouvé correspondant à la recherche.")
