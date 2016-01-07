from string import ascii_lowercase
from PIL import Image, ImageDraw, ImageFont


class ChessBoardDrawer(object):
    def __init__(self, field_size=400, cell_num=8, light_color=(245, 209, 166), dark_color=(165, 117, 81)):
        self.img = Image.new('RGBA', (field_size, field_size), color=(255, 255, 255, 0))
        self.draw = ImageDraw.Draw(self.img)
        self.cell_size = field_size / cell_num
        self.cell_num = cell_num
        self.light_color = light_color
        self.dark_color = dark_color

    def draw_board(self):
        for row in range(0, self.cell_num):
            row_start_color = row % 2
            for col in range(0, self.cell_num):
                col_color = (col + row_start_color) % 2
                color = self.light_color if col_color == 0 else self.dark_color
                self.draw.rectangle((col * self.cell_size, row * self.cell_size,
                             (col * self.cell_size) + self.cell_size, (row * self.cell_size) + self.cell_size),
                            color)

        fnt = ImageFont.load_default()

        for row in range(0, self.cell_num):
            self.draw.text((0, row * self.cell_size),
                           str(8 - row),
                           self.light_color if row % 2 else self.dark_color,
                           font=fnt)

        for col in range(0, self.cell_num):
            self.draw.text(((col + 0.75) * self.cell_size, self.cell_num * self.cell_size - 0.25 * self.cell_size),
                           ascii_lowercase[col],
                           self.dark_color if col % 2 else self.light_color,
                           font=fnt)
        return self.img

    def show(self):
        self.img.show()

    def save(self):
        self.img.save('res/board.png', 'PNG')


if __name__ == '__main__':
    dd = ChessBoardDrawer()
    dd.draw_board()
    dd.save()
