import json
import time
import openai


class FlashcardCreator:



    def __init__(self, assistant_id, api_key):
        self.api_key = api_key
        self.assistant_id = assistant_id


    def ai_generate_flashcards(self, ocr_data):
        client = openai.Client(api_key=self.api_key)

        def wait_for_run_completion(thread_id):
            while True:
                runs = client.beta.threads.runs.list(thread_id=thread_id)
                if not runs.data or runs.data[-1].status in ["completed", "failed"]:
                    break
                time.sleep(1)

        print("Creating thread with OCR data...")
        thread = client.beta.threads.create(
            messages=[{
                "role": "user",
                "content": ocr_data
            }]
        )

        print("Creating run with assistant...")
        client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant_id
        )

        print("Waiting for OCR data run to complete...")
        wait_for_run_completion(thread.id)

        print("Fetching final response...")
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        for message in messages.data:
            if message.role == 'assistant':
                message_text = message.content[0].text.value
                print(f"Received message from assistant: {message_text}")
                try:
                    if message_text[0] != '{':
                        message_text = message_text[message_text.find('{'):]
                    if message_text[-1] != '}':
                        message_text = message_text[:message_text.rfind('}') + 1]
                    return json.loads(message_text)
                except json.JSONDecodeError:
                    continue

        return None







