## AI Powered Flashcards creator

Convert your study materials into interactive flashcards effortlessly!

This Python-based tool is designed to transform lecture slides, summaries, and other study materials into flashcards, making learning more efficient and engaging. Ideal for students and educators alike, this project leverages AI to simplify your study process.

## Prerequisites

Before using the Study Material to Flashcards Converter, make sure you have the following installed:

- Anki: [Anki](https://apps.ankiweb.net/)
- AnkiConnect: [AnkiConnect](https://github.com/FooSoft/anki-connect)
- Python (version 3.x)
- Tesseract: [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

## Functionalities

- **AI-Powered Conversion**: Extracts key information from study materials using AI and formats it into flashcards.
- **Multiple Formats**: Choose to receive flashcards in JSON, CSV, or directly in Anki.
- **Anki Integration**: Directly create Anki decks for use within the Anki App.
- **User-Friendly GUI**: Easy-to-use interface built with Tkinter and Figma.
- **Drag and Drop**: Simplify file selection with a drag-and-drop feature. 

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/omar7l/FlashCards_Creator

2. Navigate to the project directory:

   ```bash
   cd FlashCards_Creator

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```
   If you encounter issues while installing any requirements, through the command line, you can try installing them directly in PyCharm:
      1. Open PyCharm and navigate to `File > Settings > Project: YourProjectName > Python Interpreter`.
      2. Click on the `+` button to open the package manager.
      3. Search for the package you need to install (e.g., `pymupdf`) and click on `Install Package`.
      4. After installation, verify the installation by attempting to import the package in your Python script.

5. Ensure prerequirements are met:

Ensure you have Anki with the AnkiConnect plugin setup as well as Python (version 3.x) and Tesseract (latest version) installed.

## How to use

1. Navigate to the project directory:

   ```bash
   cd FlashCards_Creator

2. Run the application like this:

   ```bash
   python3 main.py

3. Select your file:

   Select your file via the SELECT button or drag and drop your desired learning materials into the entry field.

4. Select the output format:

   Select which format you like to receive.

   - JSON: The flashcards will be saved as a JSON file in your local downloads folder.
   - CSV: The flashcards will be saved as a CSV file in your local downloads folder.
   - Anki: The flashcards will automatically be imported as a deck into Anki. Make sure to have the Anki App open when converting the file.

5. Create flashcards:

   Press the Convert button to create the flashcards.
   

   
