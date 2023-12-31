from time import sleep
from PIL import Image, GifImagePlugin
import subprocess
import math

GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS

CHARACTERS: str = "@%#*+=-:. "
MAX_WIDTH: int = 1
CHAR_STEP: float = 255 / len(CHARACTERS)

def image_to_characters(characters: str, image_path: str) -> list[list]:
    characters_step: float = 255 / len(characters)
    try:
        image = Image.open(image_path)
    except:
        print("Can't open image.")
        return []

    width, height = image.size
    width, height = resize(width, height, 100)

    if image_path[-4:] != ".gif":
        image = image.resize((width,height))
        image.convert("RGB")

        pixels = list(image.getdata(None))
    
        matrix: list[list] = get_pixel_matrix(pixels, width)
        matrix = characterify(matrix, characters, characters_step)

        return matrix


    if image_path[-4:] == ".gif":
        frames = resize_gif(image_path, width, height)
        frame_data = []

        for frame in frames:
            pixels = list(frame.getdata(None))
            
            matrix: list[list] = get_pixel_matrix(pixels, width)
            matrix = characterify(matrix, characters, characters_step)

            frame_data.append(matrix)

    return frame_data


def resize_gif(image_path: str, width: int, height: int):
    if image_path[-4:] != ".gif":
        return
    
    image = Image.open(image_path)
    
    image_array = []
    for frame in range(image.n_frames):
        image.seek(frame)
        temp_image = image.copy()
        temp_image = temp_image.resize((width, height))
        image_array.append(temp_image)

    return image_array    


def main() -> None:
    image_path: str = input("Please input image path: ")
    characters_gradient: str = input("Please input image gradient. Default = @%#*+=-:. ")

    if len(characters_gradient) < 2:
        print("Using default characters scheme")
        characters_gradient = CHARACTERS
    
    image = image_to_characters(characters_gradient, image_path)
    
    if image_path[-4:] == ".gif":
        for frame in image:
            sleep(0.05)
            subprocess.run("cls", shell=True)
            print_image(frame)
    
    else:
        print_image(image)

def print_image(matrix):
    for row in matrix:
        string = ""
        for value in row:
            string += value

        print(string)


def get_character_matrix_size(width_px: int, height_px: int, max_width: int = MAX_WIDTH) -> tuple[int, int]:
    columns: int = math.floor(width_px / max_width)
    rows: int = math.floor(height_px / max_width)
    return columns, rows

def get_pixel_matrix(pixels, width: int) -> list[list[tuple[int, int, int]]]:
    matrix: list[list] = []
    
    row: list[tuple[int, int, int]] = []
    for index, pixel in enumerate(pixels):
        if index % width == 0 and index != 0:
            matrix.append(row)
            row = []
        row.append(pixel)
        
    return matrix

def characterify(matrix, characters_list: str = CHARACTERS, character_step:float = CHAR_STEP) -> list[list[str]]:
    temp_matrix: list[list[str]] = []
    for row in matrix:
        temp_row: list[str] = []
        for cell in row:
            temp_row.append(get_value(cell, characters_list, character_step))

        temp_matrix.append(temp_row)
    
    return temp_matrix

def resize(width: int, height: int, target_character_size: int = 100) -> tuple[int, int]:
    divide_by: float = max(width/target_character_size, height/target_character_size)

    #height should be divided by 2, because of printing
    w: int = round(width/divide_by)
    h: int = round((height/divide_by) / 2)
    return w, h

def get_value(rgb: tuple[int, int, int], character_list, characters_step: float ):
    red, green, blue = rgb

    avg: float = (red + green + blue) / 3

    index: int = round(avg/characters_step) - 1

    return character_list[index]

if __name__ == "__main__":
    main()