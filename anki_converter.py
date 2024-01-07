import json
import requests
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class AnkiConverter:
    def __init__(self):
        self.anki_connect_url = "http://localhost:8765"
        self.deck_name_prefix = "anki_deck"
        self.note_type = "Basic"
        self.deck_count_file = Path("deck_count.txt")
        self.deck_count = int(self.deck_count_file.read_text())
        logging.debug(f"Deck count: {self.deck_count}")

    # This function creates a new deck in Anki
    def create_deck(self):
        self.deck_count += 1
        self.deck_name = f"{self.deck_name_prefix}_{self.deck_count}"

        payload = {
            "action": "createDeck",
            "version": 6,
            "params": {"deck": self.deck_name}
        }

        response = requests.post(self.anki_connect_url, json=payload)
        logging.debug(f"Response: {response.status_code}, {response.content}")

        # Save the updated deck count to the file
        self.deck_count_file.write_text(str(self.deck_count))

    # This function adds a flashcard to an Anki deck
    def add_flashcard(self, front, back):
        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": self.deck_name,
                    "modelName": self.note_type,
                    "fields": {"Front": front, "Back": back},
                    "options": {"allowDuplicate": True},
                    "tags": [],
                }
            }
        }

        response = requests.post(self.anki_connect_url, json=payload)
        logging.debug(f"Response: {response.status_code}, {response.content}")

    # This function reads the JSON file and adds the flashcards to Anki
    def convert_to_anki(self, json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as file:
            flashcards_data = json.load(file)

        for flashcard in flashcards_data.get('flashcards', []):
            front_content = flashcard.get('front', '')
            back_content = flashcard.get('back', '')
            self.add_flashcard(front_content, back_content)

        logging.info("Flashcards added to Anki!")

    # This function checks if a deck with the specified prefix exists in Anki
    # If it does not exist, it creates a new deck
    # If it exists, it increments the deck count and creates a new deck
    # It also saves the updated deck count to a file
    def check_decks(self):
        logging.debug("Checking existing decks in Anki")

        payload = {
            "action": "deckNames",
            "version": 6,
            "params": {}
        }

        response = requests.post(self.anki_connect_url, json=payload)
        logging.debug(f"Deck check response: {response.status_code} - {response.content}")

        deck_names = response.json().get('result', [])

        self.deck_count = 0

        for deck_name in deck_names:
            if deck_name.startswith(self.deck_name_prefix):
                self.deck_count += 1

        if self.deck_count == 0:
            self.deck_count_file.unlink(missing_ok=True)
            logging.debug("No matching decks found. deck_count.txt deleted")
        else:
            self.deck_count_file.write_text(str(self.deck_count))
            logging.debug(f"Updated deck count ({self.deck_count}) written to file")
