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
    data = json.loads(json_data)

    # Open a CSV file for writing
    with open(csv_file, 'w', newline='') as csvfile:
        # Create a CSV writer
        csv_writer = csv.writer(csvfile)

        # Iterate through the flashcards and write each front and back to a row
        for flashcard in data['flashcards']:
            front = flashcard['front']
            back = flashcard['back']
            csv_writer.writerow([front, back])



def ai_generate_flashcards(prompt, assistant_id, api_key2):
    client = openai.Client(api_key=api_key2)

    # Create a Thread with an initial user message
    print("Creating thread...")
    thread = client.beta.threads.create(
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    # Create a Run with the specified assistant
    print("Creating run with assistant...")
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # Spinner for loading animation
    spinner = ["-", "\\", "|", "/"]
    spin_index = 0

    # Polling for Run completion with timeout
    print("Waiting for response...")
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > 60:  # 60 seconds timeout
            print("Timeout reached. No response within 60 seconds.")
            return None

        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status
        if run_status in ["completed", "failed"]:
            break

        # Print loading spinner
        print(spinner[spin_index % 4], end="\r")
        spin_index += 1
        time.sleep(0.1)

    if run_status == "failed":
        print("Run failed to complete.")
        return None

    # Retrieve the Assistant's messages after Run completion
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for message in messages.data:
        if message.role == 'assistant':
            print("New message from assistant:", message.content)
            try:
                content_json = json.loads(message.content)
                if 'acknowledged' in content_json.values():
                    print("Acknowledged received in JSON format.")
                    return content_json
            except json.JSONDecodeError:
                continue

    return None


if __name__ == "__main__":
    pdf_file = "./input/10_Gaddis Python_Lecture_ppt_ch10.pdf"  # Replace with your PDF file path
    tmp_folder = "./tmp"  # Replace with the folder where you want to save the images
    dpi = 500
    num_threads = 8
    # openai params
    assistant_id = "asst_7fMAud27Ph7NLaokksbuHcQC"
    api_key = "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"

    #perform_ocr_and_render(pdf_file, tmp_folder, 'output.txt', dpi, num_threads)

    #get the text from the output.txt file (utf-8)
    with open('output.txt', 'r', encoding='utf-8') as file:
        data = file.read().replace('\n', '')


    #print out data
    #print(data)
    #generate flashcards
    response = ai_generate_flashcards(data + "\n presto123!", assistant_id, api_key)

    #print out response
    print(response)

    #save the response to a json file
    with open('sample.json', 'w') as outfile:
        json.dump(response, outfile)

    #convert json to csv
    convert_json_to_csv(response, 'output.csv')

    delete_files(tmp_folder)