import json
import requests
from pathlib import Path

class AnkiConverter:
    def __init__(self):
        self.anki_connect_url = "http://localhost:8765"
        self.deck_name_prefix = "anki_deck"
        self.note_type = "Basic"
        self.deck_count_file = Path("deck_count.txt")

        self.deck_count = int(self.deck_count_file.read_text())
        print(self.deck_count)

    def create_deck(self):
        self.deck_count += 1
        self.deck_name = f"{self.deck_name_prefix}_{self.deck_count}"

        payload = {
            "action": "createDeck",
            "version": 6,
            "params": {"deck": self.deck_name}
        }

        response = requests.post(self.anki_connect_url, json=payload)
        print(response.status_code, response.content)

        # Save the updated deck count to the file
        self.deck_count_file.write_text(str(self.deck_count))



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
        print(response.status_code, response.content)

    def convert_to_anki(self, json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as file:
            flashcards_data = json.load(file)

        for flashcard in flashcards_data.get('flashcards', []):
            front_content = flashcard.get('front', '')
            back_content = flashcard.get('back', '')
            self.add_flashcard(front_content, back_content)

        print("Flashcards created successfully! and saved in anki")

    # create a function called check_decks() that checks if there are any decks in Anki that start with the deck_name_prefix
    # if there are, then set the entry deck_count.txt file to the number of decks that start with the deck_name_prefix
    # if there aren't, then delete the deck_count.txt file
    def check_decks(self):
        payload = {
            "action": "deckNames",
            "version": 6,
            "params": {}
        }

        response = requests.post(self.anki_connect_url, json=payload)
        print(response.status_code, response.content)

        deck_names = response.json()['result']

        self.deck_count = 0

        for deck_name in deck_names:
            if deck_name.startswith(self.deck_name_prefix):
                self.deck_count += 1

        if self.deck_count == 0:
            self.deck_count_file.write_text("0")
        else:
            self.deck_count_file.write_text(str(self.deck_count))

        print(self.deck_count)

if __name__ == "__main__":
    # Example usage
    converter = AnkiConverter()

    converter.check_decks()

    converter.create_deck()

    # Add flashcards from JSON file
    converter.convert_to_anki('flashcard_test.json')
