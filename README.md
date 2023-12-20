# Study Material to Flashcards Converter

This project is a Python script that helps convert study material, such as lecture slides or summaries, into flashcards.

## Prerequisites

Before using the Study Material to Flashcards Converter, make sure you have the following installed:

- Anki: [Anki](https://apps.ankiweb.net/)
- AnkiConnect: [AnkiConnect](https://github.com/FooSoft/anki-connect)
- Python (version 3.x)
- Tesseract (Windows): https://github.com/UB-Mannheim/tesseract/wiki

Upon installing these prerequisites, make sure to update the config.env file with the correct path to your AnkiConnect plugin and Tesseract installation.

## Functionalities

- Convert study material into flashcards: The script reads in the study material and retrieves the provided information using AI, which is then converted into a flashcards format.
- Output in multiple data formats: the user can select in which format they like to receive the flashcards (JSON, CSV, Anki)
- Direct Connection to Anki: By selecting the Anki format option, the script automatically creates Anki flashcard desk, which can be used within the Anki App.
- GUI: A comprehensible GUI is created, to ensure easy usage for the program, using Tkinter and Figma.
- Drag and Drop feature: Drag and drop feature implemented in the GUI, using Tkinterdnd2, for increased usability. 

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/omar7l/Slides_to_Quiz

2. Navigate to the project directory:

   ```bash
   cd Slides_to_Quiz

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt

4. Ensure prerequirements are met:

Ensure you have Anki with the AnkiConnect plugin setup as well as Python (version 3.x) installed.

## How to use

1. Navigate to the project directory:

   ```bash
   cd Slides_to_Quiz

2. Run the application like this:

   ```bash
   python3 gui.py

3. Select your file:

   Select your file via the SELECT button or drag and drop your desired learning materials into the entry field.

4. Select the output format:

   Select which format you like to receive.

   - JSON: The flashcards will be saved as a JSON file in your local downloads folder.
   - CSV: The flashcards will be saved as a CSV file in your local downloads folder.
   - Anki: The flashcards will automatically be imported as a deck into Anki. Make sure to have the Anki App open when converting the file.

5. Create flashcards:

   Press the Convert button to create the flashcards.
   

   
