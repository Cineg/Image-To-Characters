from PIL import Image
import math

CHARACTERS: str = "@%#*+=-:. "
MAX_WIDTH: int = 20
CHAR_STEP: float = 255 / len(CHARACTERS)

def main() -> None:
    image = Image.open("test_images/image2.jpg")
    width, height = image.size
    
    pixels = list(image.getdata())
    matrix_size: tuple[int, int] = get_character_matrix_size(width, height)
    matrix = get_pixel_matrix(pixels, width)
    matrix = get_cells(matrix,matrix_size)
    matrix = characterify(matrix)

    for row in matrix:
        string = ""
        for value in row:
            string += " " + value + " "
        
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

def characterify(matrix):
    temp_matrix = []
    for row in matrix:
        temp_row = []
        for cell in row:
            temp_row.append(get_value(cell))

        temp_matrix.append(temp_row)
    
    return temp_matrix


def get_value(rgb_array: list[tuple[int, int, int]]):
    length = len(rgb_array)

    red = 0
    green = 0
    blue = 0

    for item in rgb_array:
        red += item[0]
        green += item[1]
        blue += item[2]

    red /= length
    green /= length
    blue /= length

    avg: float = (red + green + blue) / 3

    index: int = round(avg/CHAR_STEP) - 1

    return CHARACTERS[index]

def get_cells(matrix, matrix_size: tuple[int, int]) -> list[list]:
    full_matrix: list[list] = []
    for row in range(matrix_size[1]):
        row_list: list[list] = []
        for col in range(matrix_size[0]):
            cell: list[tuple[int, int, int]] = _get_cell(matrix, row, col)
            row_list.append(cell)
        
        full_matrix.append(row_list)
    
    return full_matrix
    
def _get_cell(matrix: list, row: int, col: int, max_width: int = MAX_WIDTH) -> list[tuple[int, int, int]]:
    cell:list[tuple[int, int, int]] = []
    for r in range(max_width):
        for c in range(max_width):
            row_add: int = (max_width * row) - 1
            col_add: int = (max_width * col) - 1
            cell.append(matrix[r + row_add][c + col_add])
    
    return cell

if __name__ == "__main__":
    main()