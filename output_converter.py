import json
import csv
import shutil
from pathlib import Path
import os


class OutputConverter:



    def __init__(self):
        pass

# write a function convert_to_json() that takes in a JSON file path and data(which already is in JSON format) and writes the data to the JSON file
    def convert_to_json(self, json_file_path, data):   # data is JSON data
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Flashcards converted to json!")

    def convert_to_csv(self, csv_file_path, data):    # data is JSON data

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter='\t')
            for flashcard in data.get('flashcards', []):
                front = flashcard.get('front', '')
                back = flashcard.get('back', '')
                csv_writer.writerow([front, back])

        print("Flashcards converted to csv!")


    def download_file(self, file_path):
        try:
            # Get the downloads folder path
            downloads_folder = Path.home() / "Downloads"

            # Create the destination path in the downloads folder
            destination_path = downloads_folder / file_path.name

            # Copy the file to the downloads folder
            shutil.copy(file_path, destination_path)

            print(f"File saved to: {destination_path}")
        except Exception as e:
            print(f"Error saving file: {e}")

    # write a function delete_files() that takes in a folder path and deletes all files in that folder

    def delete_files(self, output_folder):
        for filename in os.listdir(output_folder):
            file_path = os.path.join(output_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)

            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

