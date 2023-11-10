import os
import fitz  # PyMuPDF
import pytesseract
import concurrent.futures
from PIL import Image
import openai
import time

import csv
import json


def render_pdf_worker(pdf_file, image_folder, page_number, dpi=300):
    # Open the PDF file using PyMuPDF (Fitz)
    pdf_document = fitz.open(pdf_file)

    # Get the page
    page = pdf_document.load_page(page_number)

    # Convert the page to a Pillow (PIL) image with the specified DPI
    pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
    pil_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Save the image to the specified folder
    image_filename = f"{image_folder}/page_{page_number + 1}.png"
    pil_image.save(image_filename, dpi=(dpi, dpi))

    print(f"Page {page_number + 1} saved as {image_filename}")

    # Close the PDF document
    pdf_document.close()


def ocr_worker(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


def perform_ocr_and_render(pdf_file, image_folder, output_text_file, dpi=300, num_threads=1):
    with open(output_text_file, 'w', encoding='utf-8') as txt_file:
        # Create a ThreadPoolExecutor with the specified number of threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Submit PDF rendering tasks for each page
            pdf_document = fitz.open(pdf_file)
            for page_number in range(pdf_document.page_count):
                executor.submit(render_pdf_worker, pdf_file, image_folder, page_number, dpi)

            # Close the PDF document after all rendering tasks are submitted
            pdf_document.close()

        # List image files in the folder
        image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.png')]

        # Create a ThreadPoolExecutor with the specified number of threads for OCR
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Submit OCR tasks for each image
            future_to_image = {executor.submit(ocr_worker, image_path): image_path for image_path in image_files}

            for future in concurrent.futures.as_completed(future_to_image):
                image_path = future_to_image[future]
                text = future.result()

                # Write the extracted text to the text file
                page_number = image_files.index(image_path) + 1
                txt_file.write(f'Page {page_number}:\n')
                txt_file.write(f'{text}\n\n')
                print(f'Extracted text from Page {page_number}')


def ai_generate_flashcards(ocr_data, assistant_id, api_key2):
    client = openai.Client(api_key=api_key2)

    # Function to wait for the run to complete
    def wait_for_run_completion(thread_id):
        while True:
            runs = client.beta.threads.runs.list(thread_id=thread_id)
            if not runs.data or runs.data[-1].status in ["completed", "failed"]:
                break
            time.sleep(1)

    # Create a Thread with the OCR data as the initial user message
    print("Creating thread with OCR data...")
    thread = client.beta.threads.create(
        messages=[{
            "role": "user",
            "content": ocr_data
        }]
    )

    # Create a Run with the specified assistant
    print("Creating run with assistant...")
    client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # Wait for the OCR data run to complete
    print("Waiting for OCR data run to complete...")
    wait_for_run_completion(thread.id)

    # Fetch and process the final JSON response
    print("Fetching final response...")
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for message in messages.data:
        if message.role == 'assistant':
            message_text = message.content[0].text.value
            print(f"Received message from assistant: {message_text}")
            try:
                #Code cleanup
                #if message text first character is not a { then remove everything before the first {
                if message_text[0] != '{':
                    message_text = message_text[message_text.find('{'):]
                #if the last character is not a } then remove everything after the last }
                if message_text[-1] != '}':
                    message_text = message_text[:message_text.rfind('}') + 1]
                return json.loads(message_text)
            except json.JSONDecodeError:
                continue

    return None


def delete_files(image_folder):
    for filename in os.listdir(image_folder):
        file_path = os.path.join(image_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)

        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def convert_json_to_csv(json_data, csv_file):
    # Load JSON data
    data = json_data  # Remove json.loads since json_data is already a JSON object

    # Open a CSV file for writing
    with open(csv_file, 'w', newline='') as csvfile:
        # Create a CSV writer
        csv_writer = csv.writer(csvfile, delimiter='\t')

        # Iterate through the flashcards and write each front and back to a row
        for flashcard in data['flashcards']:
            front = flashcard['front']
            back = flashcard['back']
            csv_writer.writerow([front, back])



if __name__ == "__main__":
    pdf_file = "./input/10_Gaddis Python_Lecture_ppt_ch10.pdf"  # Replace with your PDF file path
    tmp_folder = "./tmp"  # Replace with the folder where you want to save the images
    dpi = 500
    num_threads = 8
    # openai params
    assistant_id = "asst_7fMAud27Ph7NLaokksbuHcQC"
    api_key = "your_api_key_here"

    perform_ocr_and_render(pdf_file, tmp_folder, './tmp/output.txt', dpi, num_threads)

    #get the text from the output.txt file (utf-8)
    with open('./tmp/output.txt', 'r', encoding='utf-8') as file:
        data = file.read().replace('\n', '')


    #print out data
    #print(data)
    #generate flashcards
    response = ai_generate_flashcards(data, assistant_id, api_key)

    #print out response
    print(response)

    #convert json to csv
    convert_json_to_csv(response, 'output.csv')

    delete_files(tmp_folder)