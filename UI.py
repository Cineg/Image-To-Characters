from time import sleep
import PySimpleGUI as sg
from main import image_to_characters

def main():

    sg.theme('DarkBlue')
    layout = [  
                [sg.Text('Charactes grading: '), sg.InputText("@%#*+=-:. ")],
                [sg.Text('Image path: '), sg.InputText(""), sg.FileBrowse("Pick Image")],
                [sg.Button('Ok'), sg.Button('Cancel'), sg.Button('Clear')],
                [sg.Checkbox("Loop gif?", False, key="isGifLooped"), sg.Text("Frame time: ") ,sg.Spin(key="FrameTime", values=[0.03, 0.05, 0.1, 0.15, 0.2, 0.3,], initial_value=0.05)],
                [sg.Text(text="", key="Characterify", font="Consolas", auto_size_text=True)], 
                ] 

    window = sg.Window('Picture to Charactes', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        
        if event == "Clear":
            window["Characterify"].update("")

        if event == "Ok":
            matrix = image_to_characters(values[0], values[1])
            if values[1][-4:] != ".gif":
                print_static_image(matrix, window, True)
            else:
                
                print_gif(matrix, window, window["FrameTime"].get())
                if window["isGifLooped"].get():
                    while window["isGifLooped"].get():
                        sleep(0.5)
                        print_gif(matrix, window, window["FrameTime"].get())

            window.refresh()

    window.close()

def print_gif(matrix: list[list[list]], window, frame_time: float):
    for frame in matrix:
        print_static_image(frame, window, False)
        sleep(frame_time)
        window.refresh()

def print_static_image(matrix: list[list], window, refresh: bool) -> None:
    total_string: str = ""
    for row in matrix:
        string: str = ""
        for item in row:
            string += "" + item + ""

        total_string += string + "\n"
        window["Characterify"].update(total_string)

        if refresh: 
            window.refresh()

if __name__ == "__main__":
    main()