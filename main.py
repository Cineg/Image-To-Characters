from PIL import Image, GifImagePlugin
import math

GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS

CHARACTERS: str = "@%#*+=-:. "
MAX_WIDTH: int = 1
CHAR_STEP: float = 255 / len(CHARACTERS)

def image_to_characters(characters: str, image_path: str) -> list[list]:
    characters_step: float = 255 / len(characters)

    image = Image.open(image_path)
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

        frame_data = []

        for frame in range(image.n_frames):
            image.seek(frame)
    
            pixels = list(image.getdata(None))
            
            matrix: list[list] = get_pixel_matrix(pixels, width)
            matrix = characterify(matrix, characters, characters_step)

            frame_data.append(matrix)

    return frame_data



def main() -> None:
    image = Image.open("test_images/image5.jpg")

    width, height = image.size
    width, height = resize(width, height, 100)
    image = image.resize((width, height))

    pixels = list(image.getdata())
    matrix = get_pixel_matrix(pixels, width)
    matrix = characterify(matrix)

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