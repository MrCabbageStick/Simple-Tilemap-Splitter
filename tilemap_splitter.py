from sys import argv
from pathlib import Path
from enum import Enum
from PIL import Image

class SplitterOutput(Enum):
    SPLITTED: str = "Successfuly splitted"
    NOT_A_DIRECTORY: str = "Output path is not a directory"
    FILE_DOES_NOT_EXISTS: str = "File does not exist"

    INCORRECT_TILE_SIZE: str = "Tile width or height does not meet the criteria: 0 < size"


def split(file_path: Path, output_path: Path, tile_width: int, tile_height: int, tile_name: str = "tile_{0}.png") -> SplitterOutput:

    # Path checks
    if not file_path.exists():
        return SplitterOutput.FILE_DOES_NOT_EXISTS

    if not output_path.exists():
        output_path.mkdir(parents=True)

    elif not output_path.is_dir():
        return SplitterOutput.NOT_A_DIRECTORY
    
    # Parameter checks
    if tile_height <= 0 or tile_width <= 0:
        return SplitterOutput.INCORRECT_TILE_SIZE
    
    
    # Splitting
    image = Image.open(file_path)

    n_columns = int(image.width / tile_width)
    n_rows = int(image.height / tile_height)


    for tile_row in range(n_rows):
        for tile_column in range(n_columns):

            tile_start = (tile_column * tile_width, tile_row * tile_height)
            tile_end = ((tile_column + 1) * tile_width, (tile_row + 1) * tile_height)

            tile = image.crop((*tile_start, *tile_end))

            tile.save(output_path.joinpath(tile_name.format(tile_column + tile_row * n_columns)))


    return SplitterOutput.SPLITTED



def main():

    if len(argv) < 5:
        print(r"""Usage: %s <input_file> <output_dir> <tile_width> <tile_height> [optional: <tile_name>]
            Parameters:
            -> file_name: formatted as 'file_name_{0}.ext'""".replace("    ", "") % argv[0])
        exit(1)
        
    input_file = Path(argv[1])
    output_dir = Path(argv[2])

    try:
        tile_width = int(argv[3])
    except ValueError:
        print(f"Unable to parse tile_width: '{argv[3]}' to int")
        exit(1)

    try:
        tile_height = int(argv[4])
    except ValueError:
        print(f"Unable to parse tile_height: '{argv[4]}' to int")
        exit(1)

    tile_name = "tile_{0}.png" if len(argv) < 6 else argv[5]

    result = split(input_file, output_dir, tile_width, tile_height, tile_name)

    if result == SplitterOutput.SPLITTED:
        print(f"Succesfully splitted the tile map")
        exit(0)

    print(f"Unable to split the tilemap: {result.value}")
    exit(1)


if __name__ == "__main__":
    main()