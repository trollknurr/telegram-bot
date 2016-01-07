from pathlib import PurePath

from PIL import Image, ImageFont, ImageDraw

pieces = dict(zip("KQRBNPkqrbnp", "♔♕♖♗♘♙♚♛♜♝♞♟"))

root = PurePath(__file__).parent


def expand_digits(fen_string):
    new_string = ""
    for s in fen_string:
        if s.isdigit():
            new_string += " " * int(s)
        else:
            new_string += s
    return new_string


def chess_position_img(fen, font_size=40, sq_size=50):
    """
    Based on http://wordaligned.org/articles/drawing-chess-positions
    :param fen:
    :param font_size:
    :param sq_size:
    :return:
    """
    font = ImageFont.truetype(str(root / 'res' / 'chess_merida_unicode.ttf'), font_size)
    board = Image.open(str(root / 'res' / 'board.png'), 'r')
    put_piece = ImageDraw.Draw(board).text

    def point(i, j):
        if font_size != sq_size:
            centering_factor = (sq_size - font_size) / 2
        else:
            centering_factor = 0
        return i * sq_size + centering_factor, j * sq_size + centering_factor

    for row, row_str in enumerate(expand_digits(fen).split('/')):
        for col, c in enumerate(row_str):
            if c != ' ':
                put_piece(point(col, row), pieces[c], fill='black', font=font)
    return board


if __name__ == '__main__':
    chess_position_img('rnb1kbnr/pppp1ppp/4q3/4P3/4P3/8/PPP2PPP/RNBQKBNR', 40)
