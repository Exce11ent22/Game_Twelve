import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QPushButton

from game import Game


def styles_from_file():
    styles = []
    with open("resources/styles.txt") as file:
        for line in file:
            styles.append(line)
    return styles


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.h = 700
        self.w = 500
        self.setWindowTitle("The Twelve game")
        self.setWindowIcon(QtGui.QIcon("resources/main_ico.png"))
        self.setFixedHeight(self.h)
        self.setFixedWidth(self.w)
        self.game = Game()
        self.grid = self.create_grid()
        self.styles = styles_from_file()

        self.info = QPushButton(self)
        self.info.move(10, 10)
        self.info.setIcon(QtGui.QIcon("resources/info.png"))
        self.info.setFixedHeight(40)
        self.info.setFixedWidth(40)
        self.info.clicked.connect(self.dialog_info)

        self.difficulty = QPushButton(self)
        self.difficulty.move(60, 10)
        self.difficulty.setFixedHeight(40)
        self.difficulty.setFixedWidth(40)
        self.difficulty.setIcon(QtGui.QIcon("resources/menu.png"))
        self.difficulty.clicked.connect(self.difficulty_dialog)

        self.score = QLabel(self)
        self.score.move(300, 155)
        self.score.setFixedWidth(200)
        self.score.setStyleSheet("color: red; font-size: 30px;")

        self.refresh_main_window()
        self.refresh_buttons()
        self.refresh_grid()
        self.refresh_score()

    def create_grid(self):
        grid = [[QPushButton(self) for j in range(self.game.get_size())] for i in range(self.game.get_size())]
        for i in range(self.game.get_size()):
            for j in range(self.game.get_size()):
                grid[i][j].move(j * int(self.w/self.game.get_size()), 200 + i * int(self.w/self.game.get_size()))
                grid[i][j].setFixedHeight(int(self.w/self.game.get_size()))
                grid[i][j].setFixedWidth(int(self.w/self.game.get_size()))
                grid[i][j].clicked.connect(lambda checked, i=i, j=j: self.request(i, j))
        return grid

    def request(self, i, j):
        self.game.select_cell(i, j)
        self.refresh_grid()
        if self.game.is_lose():
            self.dialog_lose()
            self.game.set_new_game()
            self.refresh_grid()
        if self.game.is_win():
            self.dialog_win()
        self.refresh_score()

    def dialog_win(self):
        dlg = QDialog(self)
        dlg.setFixedWidth(300)
        dlg.setFixedHeight(300)
        dlg.score = QLabel(dlg)
        dlg.score.setText(f"Score: {self.game.get_score()}")
        dlg.score.move(90, 200)
        dlg.setStyleSheet("background-image: url(resources/win_light.jpg)")
        dlg.score.setStyleSheet("color: red; font-size: 25px;")
        dlg.exec_()

    def dialog_lose(self):
        dlg = QDialog(self)
        dlg.setFixedWidth(300)
        dlg.setFixedHeight(300)
        dlg.score = QLabel(dlg)
        dlg.score.setText(f"Score: {self.game.get_score()}")
        dlg.score.move(90, 200)
        dlg.setStyleSheet("background-image: url(resources/game_over_light.jpg)")
        dlg.score.setStyleSheet("color: red; font-size: 25px;")
        dlg.exec_()

    def dialog_info(self):
        dlg = QDialog(self)
        dlg.setFixedWidth(300)
        dlg.setFixedHeight(300)
        dlg.setWindowTitle("Game rules")
        dlg.setStyleSheet("background-image: url(resources/rules_light.jpg)")
        dlg.exec_()

    def difficulty_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Difficulty selection")
        dlg.setFixedWidth(300)
        dlg.setFixedHeight(350)

        dlg.easy = QPushButton(dlg)
        dlg.easy.setText("easy")
        dlg.easy.move(50, 50)
        dlg.easy.setFixedWidth(200)
        dlg.easy.setFixedHeight(50)
        dlg.easy.clicked.connect(self.set_easy_game)
        dlg.easy.clicked.connect(dlg.done)

        dlg.medium = QPushButton(dlg)
        dlg.medium.setText("medium")
        dlg.medium.move(50, 150)
        dlg.medium.setFixedWidth(200)
        dlg.medium.setFixedHeight(50)
        dlg.medium.clicked.connect(self.set_medium_game)
        dlg.medium.clicked.connect(dlg.done)

        dlg.hard = QPushButton(dlg)
        dlg.hard.setText("hard")
        dlg.hard.move(50, 250)
        dlg.hard.setFixedWidth(200)
        dlg.hard.setFixedHeight(50)
        dlg.hard.clicked.connect(self.set_hard_game)
        dlg.hard.clicked.connect(dlg.done)

        dlg.setStyleSheet("background-color: white")
        dlg.easy.setStyleSheet("border-radius: 25px; background-color: red; font-size: 25px;")
        dlg.medium.setStyleSheet("border-radius: 25px; background-color: red; font-size: 25px;")
        dlg.hard.setStyleSheet("border-radius: 25px; background-color: red; font-size: 25px;")

        dlg.exec_()

    def set_easy_game(self):
        self.game.set_new_game(3)
        self.refresh_grid()
        self.refresh_score()

    def set_medium_game(self):
        self.game.set_new_game(10)
        self.refresh_grid()
        self.refresh_score()

    def set_hard_game(self):
        self.game.set_new_game(17)
        self.refresh_grid()
        self.refresh_score()

    def refresh_main_window(self):
        self.setStyleSheet("QMainWindow{background-image: url(resources/light.jpg)}")

    def refresh_buttons(self):
        self.info.setStyleSheet("background-color: red; border-radius: 20px;")
        self.difficulty.setStyleSheet("background-color: red; border-radius: 20px;")

    def refresh_grid(self):
        table = self.game.get_table()
        for i, row in enumerate(table):
            for j, el in enumerate(row):
                style = self.styles[12] if el > 12 else self.styles[el]
                if el == 0:
                    self.grid[i][j].setText("")
                else:
                    self.grid[i][j].setText(str(el))
                if self.game.is_selected(i, j):
                    style += "border-style: solid; border-color: red; border-width: 4px;"
                self.grid[i][j].setStyleSheet(style)

    def refresh_score(self):
        self.score.setText("Score: " + str(self.game.get_score()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

