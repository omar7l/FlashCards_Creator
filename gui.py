from idlelib import tooltip
import tkinter as tk
from tkinter import Canvas, Button, PhotoImage, filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from anki_converter import *
from flashcard_creator import *
from output_converter import *
from pdf_converter import *

MAIN_PATH = Path(__file__).parent
ASSETS_PATH = Path(__file__).parent / "build" / "assets" / "frame0"
OUTPUT_PATH = Path(__file__).parent / "output"

#I have added this specific line of code to make the program work on windows.
#This is because the program was not able to find the tcl and tk libraries.
#For the moment, this should work fine, but if you have any issues, please let me know.
if os.name == 'nt':
    #get the appdata local path
    appdata_local = os.getenv('LOCALAPPDATA')
    os.environ['TCL_LIBRARY'] = appdata_local + "\\Programs\\Python\\Python310\\tcl\\tcl8.6"
    os.environ['TK_LIBRARY'] = appdata_local + "\\Programs\\Python\\Python310\\tcl\\tk8.6"
    os.environ['TCL_LIBRARY'] = appdata_local + "\\Programs\\Python\\Python39\\tcl\\tcl8.6"
    os.environ['TK_LIBRARY'] = appdata_local + "\\Programs\\Python\\Python39\\tcl\\tk8.6"



# initialize global variables
selected_file = None
txt_select_1 = None
txt_select_2 = None


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
window.configure(bg="#FFFFFF")
window.title("Jet")

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

main_canvas.create_text(
    261.0,
    6.0,
    anchor="nw",
    text="\nTitle",
    fill="#000000",
    font=("Inter", 40 * -1)
)
main_canvas.create_text(
    85.0,
    122.0,
    anchor="nw",
    text="Convert your study material to flashcards",
    fill="#000000",
    font=("Inter", 25 * -1)
)

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
    # command=lambda: upload_file(),
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

img_file_prev = PhotoImage(
    file=relative_to_assets("file_preview.png"))
file_prev = Button(
    dnd_canvas,
    image=img_file_prev,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: openFile(),
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


def on_drop(event):
    file_path = event.data
    file_name = os.path.basename(file_path)
    file_name = file_name[:-4]

    global selected_file
    selected_file = file_path
    print(selected_file)

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

    print(MAIN_PATH)
    print(ASSETS_PATH)


def select_file():
    file_path = filedialog.askopenfilename(title="Select a file")
    file_name = os.path.basename(file_path)
    file_name = file_name[:-4]

    global selected_file
    selected_file = file_path
    print(selected_file)

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
    clear_button.config(image=img_clear_clickable)
    convert_button.config(command=lambda: convert_file())


def openFile():
    try:
        os.system(f'open "{selected_file}"')
    except Exception as e:
        print(f"Error opening file: {e}")

    print(selected_file)


def adjust_font_size():
    text_name = os.path.basename(selected_file)
    print(text_name)

    if len(text_name) > 40:
        font_size = int(min((int(175) + 150) / len(text_name), 19))
    elif len(text_name) > 16:
        font_size = int(min((int(175) + 150) / len(text_name), 19) - 1)
    else:
        font_size = 20

    return int(font_size)


def show_tooltip():
    while True:
        if selected_file is None:
            tooltip.place(x=127.0, y=420.0)
            break
        else:
            tooltip.place_forget()
            break


def hide_tooltip():
    tooltip.place_forget()


def on_radiobutton_selected(value):
    print(f"Selected option: {value}")
    if value != 0:
        convert_button.config(image=img_convert_clickable)
    return value


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


def convert_file():
    pdf_convert = PDFConverter()
    flashcard_creator = FlashcardCreator("asst_7fMAud27Ph7NLaokksbuHcQC",
                                         "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")  # enter the assistant id and api key here
    tmp_folder = relative_to_project("tmp")
    tmp_output = relative_to_project("tmp/output.txt")
    dpi = 500
    num_threads = 8

    if on_radiobutton_selected(radio_var.get()) == 0:
        print("Please select an output data type")
        return

    pdf_convert.perform_ocr_and_render(selected_file, tmp_folder, tmp_output, dpi, num_threads)

    data = flashcard_creator.ai_generate_flashcards(pdf_convert.serialize_data(tmp_output))

    output_converter = OutputConverter()
    output_converter.convert_to_json(relative_to_output("output.json"), data)

    if on_radiobutton_selected(radio_var.get()) == 1:
        output_converter.download_file(relative_to_output("output.json"))
    elif on_radiobutton_selected(radio_var.get()) == 2:
        output_converter.convert_to_csv(relative_to_output("output.csv"), data)
        output_converter.download_file(relative_to_output("output.csv"))
    elif on_radiobutton_selected(radio_var.get()) == 3:
        anki_converter = AnkiConverter()
        anki_converter.check_decks()
        anki_converter.create_deck()
        anki_converter.convert_to_anki(relative_to_output("output.json"))

    pdf_convert.delete_files(tmp_folder)
    output_converter.delete_files(OUTPUT_PATH)


def run():
    window.resizable(False, False)
    window.mainloop()


if __name__ == "__main__":
    run()
