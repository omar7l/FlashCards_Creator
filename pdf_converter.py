import concurrent.futures
import os
import fitz
import pytesseract
from PIL import Image


class PDFConverter:
    def __init__(self):
        pass


    '''
        This is the worker function that will be called by the thread pool executor
        It will render the PDF page at the given page number to an image and save it to the given image folder
    '''
    @staticmethod
    def render_pdf_worker(pdf_file, image_folder, page_number, dpi=300):
        pdf_document = fitz.open(pdf_file)
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
        pil_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        image_filename = f"{image_folder}/page_{page_number + 1}.png"
        pil_image.save(image_filename, dpi=(dpi, dpi))
        print(f"Page {page_number + 1} saved as {image_filename}")
        pdf_document.close()


    '''
        This is the worker function that will be called by the thread pool executor
        It will perform OCR on the image at the given path and return the text
    '''
    @staticmethod
    def ocr_worker(image_path):
        try:
            # check if the image exists
            if not os.path.isfile(image_path):
                print(f"Image at path {image_path} does not exist")
                return ""

            image = Image.open(image_path)

            #check if the image is valid
            if image is None:
                print(f"Image at path {image_path} is not valid")
                return ""

            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"Error processing image at path: {image_path}")
            print(f"Error message: {str(e)}")
            return ""

    def perform_ocr_and_render(self, pdf_file, image_folder, output_text_file, dpi=300, num_threads=1):
        with open(output_text_file, 'w', encoding='utf-8') as txt_file:
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                pdf_document = fitz.open(pdf_file)
                for page_number in range(pdf_document.page_count):
                    executor.submit(self.render_pdf_worker, pdf_file, image_folder, page_number, dpi)
                pdf_document.close()

            image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.png')]

            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                future_to_image = {executor.submit(self.ocr_worker, image_path): image_path for image_path in image_files}
                for future in concurrent.futures.as_completed(future_to_image):
                    image_path = future_to_image[future]
                    text = future.result()
                    page_number = image_files.index(image_path) + 1
                    txt_file.write(f'\r\nPage {page_number}:\n')
                    txt_file.write(f'{text }\r\n\r\n')
                    print(f'Extracted text from Page {page_number}')

            #open the file and remove recurring texts (future work)


    def serialize_data(self, tmp_output):
        with open(tmp_output, 'r', encoding='utf-8') as file:
            data = file.read().replace('\n', '')
            return data

    @staticmethod
    def delete_files(image_folder):
        for filename in os.listdir(image_folder):
            file_path = os.path.join(image_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
