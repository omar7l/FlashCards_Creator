import re
from idlelib import tooltip
import tkinter as tk
from threading import Thread
from tkinter import Canvas, Button, PhotoImage, filedialog, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
from anki_converter import *
from flashcard_creator import *
from output_converter import *
from pdf_converter import *
from dotenv import load_dotenv
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.debug("Starting the program")
logging.debug("Loading the environment variables")
#Load the environment variables
load_dotenv("config.env")

API_KEY = os.getenv('API_KEY')
ASSISTANT_ID = os.getenv('ASSISTANT_ID')
TMP_FOLDER = os.getenv("TMP_FOLDER")
TMP_OUTPUT = os.getenv("TMP_OUTPUT")
DPI = int(os.getenv("DPI"))
NUM_THREADS = int(os.getenv("NUM_THREADS"))

logging.debug("Setting up the required paths")
MAIN_PATH = Path(__file__).parent
ASSETS_PATH = Path(__file__).parent / "build" / "assets" / "frame0"
OUTPUT_PATH = Path(__file__).parent / "output"

logging.debug("Checking if the required directories exist")


''' Init the required directories if they don't exist
./tmp
./output
'''
if not os.path.exists(MAIN_PATH / TMP_FOLDER):
    logging.debug("Creating the tmp folder")
    os.mkdir(MAIN_PATH / TMP_FOLDER)
if not os.path.exists(MAIN_PATH / "output"):
    logging.debug("Creating the output folder")
    os.mkdir(MAIN_PATH / "output")
#delete files if there are any in tmp

logging.debug("Checking if there are any files in the tmp folder")
for filename in os.listdir(MAIN_PATH / TMP_FOLDER):
    logging.debug("Deleting the file in the tmp folder")
    os.remove(MAIN_PATH / TMP_FOLDER / filename)

#I have added this specific line of code to make the program work on windows.
#This is because the program was not able to find the tcl and tk libraries.
#For the moment, this should work fine, but if you have any issues, please let me know.
if os.name == 'nt':
    logging.debug("Setting up the required environment variables for Windows")
    #get the appdata local path
    appdata_local = os.getenv('LOCALAPPDATA')
    #check if path exists "\\Programs\\Python\\Python310\\tcl\\tcl8.6"
    if os.path.exists(appdata_local + "\\Programs\\Python\\Python310\\tcl\\tcl8.6"):
        os.environ['TCL_LIBRARY'] = appdata_local + "\\Programs\\Python\\Python310\\tcl\\tcl8.6"
        os.environ['TK_LIBRARY'] = appdata_local + "\\Programs\\Python\\Python310\\tcl\\tk8.6"
    if os.path.exists(appdata_local + "\\Programs\\Python\\Python39\\tcl\\tcl8.6"):
        os.environ['TCL_LIBRARY'] = appdata_local + "\\Programs\\Python\\Python39\\tcl\\tcl8.6"
        os.environ['TK_LIBRARY'] = appdata_local + "\\Programs\\Python\\Python39\\tcl\\tk8.6"
    if os.path.exists(appdata_local + "\\Programs\\Python\\Python38\\tcl\\tcl8.6"):
        os.environ['TCL_LIBRARY'] = appdata_local + "\\Programs\\Python\\Python38\\tcl\\tcl8.6"
        os.environ['TK_LIBRARY'] = appdata_local + "\\Programs\\Python\\Python38\\tcl\\tk8.6"
    if os.path.exists(appdata_local + "\\Programs\\Python\\Python37\\tcl\\tcl8.6"):
        os.environ['TCL_LIBRARY'] = appdata_local + "\\Programs\\Python\\Python37\\tcl\\tcl8.6"
        os.environ['TK_LIBRARY'] = appdata_local + "\\Programs\\Python\\Python37\\tcl\\tk8.6"



# initialize global variables
selected_file = None
txt_select_1 = None
txt_select_2 = None
progress_bar = None



# function to get the path of the assets folder
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# function to get the path for the entire project
def relative_to_project(path: str) -> Path:
    return MAIN_PATH / Path(path)


def relative_to_output(path: str) -> Path:
    return OUTPUT_PATH / Path(path)


# create window
window = TkinterDnD.Tk()
window.geometry("604x830")
window.configure(bg="#DFDFDF")
window.title("AI Powered Flash Cards Creator")

# create outer canvas
main_canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=830,
    width=604,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
main_canvas.place(x=0, y=0)

center_x = 604 / 2
center_y = 25.0

# create Title
main_canvas.create_text(
    center_x,
    center_y,
    anchor="center",
    text="\nAI Powered Flashcards",
    fill="#000000",
    font=("Inter", 40 * -1)
)
# create Subtitle
main_canvas.create_text(
    85.0,
    122.0,
    anchor="nw",
    text="Convert your study material to flashcards",
    fill="#000000",
    font=("Inter", 25 * -1)
)
# create DnD field
dnd_field_img = PhotoImage(
    file=relative_to_assets("dnd_field.png"))
entry_bg_1 = main_canvas.create_image(
    302.0,
    411.0,
    image=dnd_field_img
)

dnd_canvas = Canvas(
    window,
    bd=0,
    bg="#F1F1F1",
    highlightthickness=0,
    height=380,
    width=380,
)
dnd_canvas.place(x=112.0, y=213.0)
dnd_canvas.drop_target_register(DND_FILES)
dnd_canvas.dnd_bind('<<Drop>>', lambda event: on_drop(event))

# create info box and set the text
info_box = Canvas(
    dnd_canvas,
    bd=0,
    bg="#F1F1F1",
    highlightthickness=0,
    height=50,
    width=380,
)
info_box.place(x=0, y=160)

txt_select_1 = info_box.create_text(
    70,
    0,
    anchor="nw",
    text="Select a file or drag and drop here",
    fill="#000000",
    font=("Inter", 15)
)

txt_select_2 = info_box.create_text(
    11,
    20.0,
    anchor="nw",
    text="PDF, filename must not contain any spaces or illegal characters",
    fill="#A0A0A0",
    font=("Inter", 12 * -1)
)
# create tooltip which display the illegal characters when hovering over the info box
tooltip = Canvas(
    window,
    bd=0,
    bg="#FFFFFF",
    highlightthickness=0,
    height=50,
    width=350,
)
info_text = tooltip.create_text(
    175,
    25.0,
    anchor="center",
    text="Illegal characters: !@#$%^&*()+=[]\\\';,./{}|\":<>?~",
    fill="Red",
    font=("Inter", 12 * -1)
)
tooltip.place_forget()
info_box.bind("<Enter>", lambda event: show_tooltip())
info_box.bind("<Leave>", lambda event: hide_tooltip())

# create buttons
img_select_clickable = PhotoImage(
    file=relative_to_assets("select_clickable.png"))
select_button = Button(
    image=img_select_clickable,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: select_file(),
    relief="flat"
)
select_button.place(
    x=327.0,
    y=530.0,
    width=150.0,
    height=50.0
)

img_convert_unclickable = PhotoImage(
    file=relative_to_assets("convert_unclickable.png"))
img_convert_clickable = PhotoImage(
    file=relative_to_assets("convert_clickable.png"))
convert_button = Button(
    image=img_convert_unclickable,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
convert_button.place(
    x=402.0,
    y=745.0,
    width=150.0,
    height=50.0
)

img_clear_unclickable = PhotoImage(
    file=relative_to_assets("clear_unclickable.png"))
img_clear_clickable = PhotoImage(
    file=relative_to_assets("clear_clickable.png"))
clear_button = Button(
    image=img_clear_unclickable,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: clear_selection(),
    relief="flat"
)
clear_button.place(
    x=126.0,
    y=530.0,
    width=150.0,
    height=50.0
)
# create file preview button and canvas to display the file name
img_file_prev = PhotoImage(
    file=relative_to_assets("file_preview.png"))
file_prev = Button(
    dnd_canvas,
    image=img_file_prev,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_file(),
    relief="flat",
)

name_canvas = Canvas(
    file_prev,
    bg="#FFFFFF",
    height=74,
    width=175,
    bd=0,
    highlightthickness=0,
)
name_canvas.place(x=70.0, y=5.0)

# create radio buttons and text
main_canvas.create_text(
    102.0,
    639.0,
    anchor="nw",
    text="Select your desired output data type: ",
    fill="#000000",
    font=("Inter", 15 * -1)
)

radio_var = tk.IntVar()
radio_btn_1 = tk.Radiobutton(
    main_canvas,
    text="JSON",
    bg="#FFFFFF",
    fg="#000000",
    variable=radio_var,
    value=1,
    command=lambda: on_radiobutton_selected(radio_var.get())
)
radio_btn_1.place(x=123.0, y=684.0)

radio_btn_2 = tk.Radiobutton(
    main_canvas,
    text="CSV",
    bg="#FFFFFF",
    fg="#000000",
    variable=radio_var,
    value=2,
    command=lambda: on_radiobutton_selected(radio_var.get())
)
radio_btn_2.place(x=273.0, y=684.0)

radio_btn_3 = tk.Radiobutton(
    main_canvas,
    text="Anki",
    bg="#FFFFFF",
    fg="#000000",
    variable=radio_var,
    value=3,
    command=lambda: on_radiobutton_selected(radio_var.get())
)
radio_btn_3.place(x=423.0, y=684.0)

# function to handle the drop event
def on_drop(event):
    file_path = event.data
    if(check_file(file_path) == False):
        return

    file_name = os.path.basename(file_path)
    file_name = file_name[:-4]

    global selected_file
    selected_file = file_path

    name_canvas.delete("all")
    info_box.delete(txt_select_1)
    info_box.delete(txt_select_2)

    file_prev.place(
        x=60.0,
        y=120.0,
        width=261.0,
        height=84.0
    )
    name_canvas.create_text(
        88.0,
        37.0,
        anchor="center",
        text=file_name,
        fill="#000000",
        font=("Inter", adjust_font_size() * -1)

    )
    clear_button.config(image=img_clear_clickable)
    convert_button.config(command=lambda: convert_file())

    logging.debug("File dropped")
    logging.debug(f"Main path: {MAIN_PATH}")
    logging.debug(f"Assets path: {ASSETS_PATH}")

# function to handle the file selection
def select_file():
    file_path = filedialog.askopenfilename(title="Select a file")

    #Check if the file selection is aborted
    if not file_path:
        logging.debug("File selection aborted")

    #Default file Check
    if(check_file(file_path) == False):
        return

    file_name = os.path.basename(file_path)
    file_name = file_name[:-4]

    global selected_file
    selected_file = file_path

    name_canvas.delete("all")
    info_box.delete(txt_select_1)
    info_box.delete(txt_select_2)

    file_prev.place(
        x=60.0,
        y=120.0,
        width=261.0,
        height=84.0
    )
    name_canvas.create_text(
        5.0,
        37.0,
        anchor="nw",
        text=file_name,
        fill="#000000",
        font=("Inter", adjust_font_size() * -1)
    )


    logging.debug(f"Selected file path: {file_path}")
    clear_button.config(image=img_clear_clickable)
    convert_button.config(command=lambda: convert_file())
    logging.debug("File selected from the file dialog")

# function to open the file from the file preview
def open_file():
    try:
        logging.debug("Opening the file")
        #check if file contains illegal characters
        if re.search(r'[!@#$%^&*()+=\[\]\\\'\';,./{}|\":<>?~]', selected_file):
            logging.debug("File contains illegal characters")
            return
        else:
            logging.debug("File does not contain illegal characters")
            logging.debug(f'Opening the file "{selected_file}"')
            os.system(f'open "{selected_file}"')
    except Exception as e:
        logging.error(f"Error opening file: {e}")

# function to check the file properties
def check_file(file_path):
    logging.debug("Checking if the file is a pdf file")

    if file_path is None:
        logging.debug("No file path provided")
        return False

    if not isinstance(file_path, str):
        logging.debug("File path is not a string")
        return False

    # Extract the filename from the file path
    filename = os.path.basename(file_path)

    # Check for illegal characters in the filename
    if re.search(r'[!@#$%^&*()+=\[\]{}|\\;:\'",<>?*]', filename):
        logging.debug("Filename contains illegal characters")
        return False

    if not file_path.lower().endswith(".pdf"):
        logging.debug("File is not a pdf file")
        return False

    if not os.path.exists(file_path):
        logging.debug("File does not exist")
        return False

    logging.debug("File is OK!")
    return True

# function to adjust the font size of the file name based on the length of the file name
def adjust_font_size():
    text_name = os.path.basename(selected_file)

    if len(text_name) > 40:
        font_size = int(min((int(175) + 150) / len(text_name), 19))
    elif len(text_name) > 16:
        font_size = int(min((int(175) + 150) / len(text_name), 19) - 1)
    else:
        font_size = 20

    return int(font_size)

# function to show the tooltip
def show_tooltip():
    while True:
        if selected_file is None:
            tooltip.place(x=127.0, y=420.0)
            break
        else:
            tooltip.place_forget()
            break

# function to hide the tooltip
def hide_tooltip():
    tooltip.place_forget()


# function to handle the radio button selection
def on_radiobutton_selected(value):
    logging.debug(f"Selected option: {value}")
    if value != 0:
        convert_button.config(image=img_convert_clickable)
    return value

# function to clear the selection
def clear_selection():
    global selected_file
    selected_file = None

    file_prev.place_forget()

    global txt_select_1
    txt_select_1 = info_box.create_text(
        70,
        0,
        anchor="nw",
        text="Select a file or drag and drop here",
        fill="#000000",
        font=("Inter", 15)
    )
    global txt_select_2
    txt_select_2 = info_box.create_text(
        11,
        20.0,
        anchor="nw",
        text="PDF, filename must not contain any spaces or illegal characters",
        fill="#A0A0A0",
        font=("Inter", 12 * -1)
    )
    clear_button.config(image=img_clear_unclickable)
    convert_button.config(image=img_convert_unclickable)

    radio_var.set(0)

# function to start the conversion process
def convert_file():

    if on_radiobutton_selected(radio_var.get()) == 0:
        logging.debug("No conversion option selected!")
        return

    # Initialize the progress bar and start it
    init_progress_bar()
    progress_bar.place(x=402, y=795)
    progress_bar.start()
    logging.debug("Starting the conversion process")

    # Start the conversion process in a separate thread
    conversion_thread = Thread(target=perform_conversion)
    conversion_thread.start()

# function to perform the conversion
def perform_conversion():

    try:

        pdf_convert = PDFConverter()
        flashcard_creator = FlashcardCreator(ASSISTANT_ID,
                                             API_KEY)

        pdf_convert.perform_ocr_and_render(selected_file, TMP_FOLDER, TMP_OUTPUT, DPI, NUM_THREADS)
        ocr_data = pdf_convert.serialize_data(TMP_OUTPUT)
        data = flashcard_creator.ai_generate_flashcards(ocr_data)

        output_converter = OutputConverter()
        output_converter.convert_to_json(relative_to_output("output.json"), data)

        # handle the different conversion options and download the file respectively
        if on_radiobutton_selected(radio_var.get()) == 1:
            logging.debug("Converting to JSON")
            output_converter.download_file(relative_to_output("output.json"))
        elif on_radiobutton_selected(radio_var.get()) == 2:
            logging.debug("Converting to CSV")
            output_converter.convert_to_csv(relative_to_output("output.csv"), data)
            output_converter.download_file(relative_to_output("output.csv"))
        elif on_radiobutton_selected(radio_var.get()) == 3:
            logging.debug("Converting to Anki")
            anki_converter = AnkiConverter()
            anki_converter.check_decks()
            anki_converter.create_deck()
            anki_converter.convert_to_anki(relative_to_output("output.json"))

        # Delete the files in the tmp and output folders
        pdf_convert.delete_files(TMP_FOLDER)
        output_converter.delete_files(OUTPUT_PATH)

        # Stop the progress bar
        progress_bar.stop()
        progress_bar.place_forget()
        logging.debug("Conversion process completed")

    except Exception as e:
        logging.error(f"Error performing conversion: {e}")


# function to check if the API key is set
def check_api_key():
    api_key = os.getenv('API_KEY')
    if api_key is None or api_key.strip() == "":
        # API key is not set, prompt the user to enter it
        logging.debug("API key not found. Prompting the user to enter it.")
        user_api_key = tk.simpledialog.askstring("API Key", "Please enter your API Key:")
        if user_api_key is not None and user_api_key.strip() != "":
            os.environ['API_KEY'] = user_api_key
        else:
            # If the user clicks Cancel or enters an empty API key, exit the application
            logging.debug("API key not provided. Exiting the application.")
            window.destroy()
            return False
    return True

# function to initialize the progress bar
def init_progress_bar():
    global progress_bar
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("TProgressbar",
                background='#5498FF',
                throughcolor="#000000",
                bordercolor='#FFFFFF',
                lightcolor='#B6D3FF',
                darkcolor='#3C64A0')

    progress_bar = ttk.Progressbar(window,
                                   mode="indeterminate",
                                   length=150,
                                   maximum=100,
                                   value=0,
                                   orient="horizontal",
                                   style="TProgressbar")
    logging.debug("Progress bar initialized")

# function to run the application
def run():

    if not check_api_key():
        return

    window.resizable(True, True)
    window.mainloop()

if __name__ == "__main__":
    run()