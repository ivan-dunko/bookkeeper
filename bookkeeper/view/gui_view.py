"""
Module defines GUI interface
"""

import sys
from PySide6 import QtWidgets


class GUIView:
    """
    Class that defines GUI interface.
    """
    def __init__(self) -> None:
        self._app = QtWidgets.QApplication(sys.argv)
        self._window = QtWidgets.QWidget()
        self._window.setWindowTitle('Bookkeeper')
        self._window.resize(300, 300)

        recent_expenses_label = QtWidgets.QLabel('Последние расходы')

        expenses_table = QtWidgets.QTableWidget(4, 20)
        expenses_table.setColumnCount(4)
        expenses_table.setRowCount(0)
        expenses_table.setHorizontalHeaderLabels(
            "Дата Сумма Категория Комментарий".split())
        header = expenses_table.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.ResizeMode.Stretch)

        budget_label = QtWidgets.QLabel('Бюджет')

        budget_table = QtWidgets.QTableWidget(3, 0)
        budget_table.setColumnCount(3)
        budget_table.setRowCount(0)
        budget_table.setHorizontalHeaderLabels(
            "Срок Сумма Бюджет".split())
        header = budget_table.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)

        hor_layout1 = QtWidgets.QHBoxLayout()
        sum_label = QtWidgets.QLabel('Сумма')
        sum_edit = QtWidgets.QLineEdit()
        hor_layout1.addWidget(sum_label)
        hor_layout1.addWidget(sum_edit)

        hor_layout2 = QtWidgets.QHBoxLayout()
        cat_label = QtWidgets.QLabel('Категория')
        cat_list = QtWidgets.QComboBox()
        edit_button = QtWidgets.QPushButton('Редактировать')
        hor_layout2.addWidget(cat_label)
        hor_layout2.addWidget(cat_list)
        hor_layout2.addWidget(edit_button)

        add_button = QtWidgets.QPushButton('Добавить')

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(recent_expenses_label)
        vertical_layout.addWidget(expenses_table)
        vertical_layout.addWidget(budget_label)
        vertical_layout.addWidget(budget_table)
        vertical_layout.addLayout(hor_layout1)
        vertical_layout.addLayout(hor_layout2)
        vertical_layout.addWidget(add_button)
        self._window.setLayout(vertical_layout)

        self._window.show()

    def get_window(self) -> QtWidgets.QWidget:
        """Return window"""
        return self._window

    def get_app(self) -> QtWidgets.QApplication:
        """Returns app instance"""
        return self._app


# GUIView().get_app().exec()
gui = GUIView()
gui.get_app().exec()
