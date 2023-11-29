import json
import requests

class AnkiConverter:
    def __init__(self, deck_name):
        self.anki_connect_url = "http://localhost:8765"
        self.deck_name = deck_name
        self.note_type = "Basic"

        # Create a new deck if it doesn't exist
        self.create_deck()

    def create_deck(self):
        payload = {
            "action": "createDeck",
            "version": 6,
            "params": {"deck": self.deck_name}
        }

        response = requests.post(self.anki_connect_url, json=payload)
        print(response.status_code, response.content)

    def rename_deck(self, new_name):
        if self.deck_id is not None:
            result = self._invoke("deckRename", deck=self.deck_id, name=new_name)
            return result["result"]
        else:
            return None

        response = requests.post(self.anki_connect_url, json=payload)
        print(response.status_code, response.content)

        # Update the local deck name
        self.deck_name = new_deck_name

    def add_flashcard(self, front, back):
        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": self.deck_name,
                    "modelName": self.note_type,
                    "fields": {"Front": front, "Back": back},
                    "options": {"allowDuplicate": False},
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

if __name__ == "__main__":
    # Example usage
    converter = AnkiConverter(deck_name="Flashcards")

    # Add flashcards from JSON file
    converter.convert_to_anki('flashcard_test.json')
