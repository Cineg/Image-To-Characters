from time import sleep
import PySimpleGUI as sg
from main import image_to_characters

def main():

    sg.theme('DarkBlue')
    layout = [  
                [sg.Text('Charactes grading: '), sg.InputText("@%#*+=-:. ")],
                [sg.Text('Image path: '), sg.InputText(""), sg.FileBrowse("Pick Image")],
                [sg.Button('Ok'), sg.Button('Cancel'), sg.Button('Clear')],
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
            total_string: str = ""
            for row in matrix:
                string: str = ""
                for item in row:
                    string += "" + item + ""

                total_string += string + "\n"
                window["Characterify"].update(total_string)
                window.refresh()
            
            #window["Characterify"].update(total_string)

    window.close()

if __name__ == "__main__":
    main()