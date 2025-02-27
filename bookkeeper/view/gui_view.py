"""
Module defines GUI interface
"""

import sys
from typing import Optional
from PySide6 import QtWidgets
from PySide6 import QtCore
from bookkeeper.presenter import Presenter
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.view.budget_table import BudgetTable


class EditCategoryDialog(QtWidgets.QDialog):
    """
    Dialog for editing/adding categories
    """

    def __init__(self, cat_list: list[Category], to_edit: Category | None = None) -> None:
        super().__init__()

        self._to_edit = to_edit
        self.setWindowTitle('Изменить категорию')

        buttons = QtWidgets.QDialogButtonBox.StandardButton.Ok | \
            QtWidgets.QDialogButtonBox.StandardButton.Cancel

        self.button_box = QtWidgets.QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)  # type: ignore[attr-defined]
        self.button_box.rejected.connect(self.reject)  # type: ignore[attr-defined]

        self._layout = QtWidgets.QVBoxLayout()
        # message = QtWidgets.QLabel("Something happened, is that OK?")
        name_label = QtWidgets.QLabel('Название')
        self._name_line = QtWidgets.QLineEdit()
        name_layout = QtWidgets.QHBoxLayout()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self._name_line)

        parent_label = QtWidgets.QLabel('Родительская подкатегория')
        self._parent_combo_box = QtWidgets.QComboBox()
        for cat in cat_list:
            self._parent_combo_box.addItem(cat.name, userData=cat)
        parent_layout = QtWidgets.QHBoxLayout()
        parent_layout.addWidget(parent_label)
        parent_layout.addWidget(self._parent_combo_box)

        self._layout.addLayout(name_layout)
        self._layout.addLayout(parent_layout)
        # self.layout.addWidget(message)
        self._layout.addWidget(self.button_box)
        self.setLayout(self._layout)

        self._res_obj: Optional[Category] = None

    def accept(self) -> None:
        """OK pressed action"""
        # print('OK')
        new_name = self._name_line.text()
        new_parent = self._parent_combo_box.itemData(
            self._parent_combo_box.currentIndex()).pk
        print(new_parent)
        if self._to_edit is not None:
            self._to_edit.name = new_name
            self._to_edit.parent = new_parent
            self._res_obj = self._to_edit
        else:
            self._res_obj = Category(name=new_name, parent=new_parent)
        self.done(QtWidgets.QDialog.DialogCode.Accepted)

    def reject(self) -> None:
        """Cancel pressed action"""
        print('Reject')
        # return 0
        self.done(QtWidgets.QDialog.DialogCode.Rejected)

    def get_res_obj(self) -> Category | None:
        """Resulting object"""
        return self._res_obj


class ExpenseDialog(QtWidgets.QDialog):
    """
        Dialog for adding expenses
    """

    def __init__(self, cat_list: list[Category], to_edit: Expense | None = None) -> None:
        super().__init__()

        self._to_edit = to_edit
        if to_edit is not None:
            self.setWindowTitle('Редактировать расходы')
        else:
            self.setWindowTitle('Новые расходы')

        buttons = QtWidgets.QDialogButtonBox.StandardButton.Ok \
            | QtWidgets.QDialogButtonBox.StandardButton.Cancel

        self.button_box = QtWidgets.QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)  # type: ignore[attr-defined]
        self.button_box.rejected.connect(self.reject)  # type: ignore[attr-defined]

        self._layout = QtWidgets.QVBoxLayout()
        # message = QtWidgets.QLabel("Something happened, is that OK?")
        sum_label = QtWidgets.QLabel('Сумма')
        self._sum_line = QtWidgets.QLineEdit()
        name_layout = QtWidgets.QHBoxLayout()
        name_layout.addWidget(sum_label)
        name_layout.addWidget(self._sum_line)

        cat_label = QtWidgets.QLabel('Категория')
        self._cat_combo_box = QtWidgets.QComboBox()
        for cat in cat_list:
            self._cat_combo_box.addItem(cat.name, userData=cat)
        cat_layout = QtWidgets.QHBoxLayout()
        cat_layout.addWidget(cat_label)
        cat_layout.addWidget(self._cat_combo_box)

        comment_label = QtWidgets.QLabel('Комментарий')
        self._comment_line = QtWidgets.QLineEdit()
        comment_layout = QtWidgets.QHBoxLayout()
        comment_layout.addWidget(comment_label)
        comment_layout.addWidget(self._comment_line)

        self._layout.addLayout(name_layout)
        self._layout.addLayout(cat_layout)
        self._layout.addLayout(comment_layout)
        # self.layout.addWidget(message)
        self._layout.addWidget(self.button_box)
        self.setLayout(self._layout)

        self._res_obj: Optional[Expense] = None

    def accept(self) -> None:
        """OK pressed action"""
        # print('OK')
        new_sum = int(self._sum_line.text())
        new_cat = self._cat_combo_box.itemData(
            self._cat_combo_box.currentIndex()).pk
        new_comment = self._comment_line.text()
        if self._to_edit is not None:
            self._to_edit.amount = new_sum
            self._to_edit.category = new_cat
            self._to_edit.comment = new_comment
            self._res_obj = self._to_edit
        else:
            self._res_obj = Expense(amount=new_sum, category=new_cat, comment=new_comment)
        self.done(QtWidgets.QDialog.DialogCode.Accepted)

    def reject(self) -> None:
        """Cancel button pressed action"""
        print('Reject')
        # return 0
        self.done(QtWidgets.QDialog.DialogCode.Rejected)

    def get_res_obj(self) -> Expense | None:
        """Returns result object"""
        return self._res_obj


class GUIView:
    """
    Class that defines GUI interface.
    """

    def __init__(self, presenter: Presenter) -> None:
        self._presenter = presenter
        self._app = QtWidgets.QApplication(sys.argv)
        self._window = QtWidgets.QWidget()
        self._window.setWindowTitle('Bookkeeper')
        self._window.resize(300, 300)

        recent_expenses_label = QtWidgets.QLabel('Последние расходы')

        self._expenses_table = QtWidgets.QTableWidget(4, 20)
        self.init_expense_table()

        budget_label = QtWidgets.QLabel('Бюджет')

        hor_layout1 = QtWidgets.QHBoxLayout()
        sum_label = QtWidgets.QLabel('Сумма')
        sum_edit = QtWidgets.QLineEdit()
        hor_layout1.addWidget(sum_label)
        hor_layout1.addWidget(sum_edit)

        hor_layout2 = QtWidgets.QHBoxLayout()
        cat_label = QtWidgets.QLabel('Категория')
        self._cat_combo_box = QtWidgets.QComboBox()
        for cat in self._presenter.get_all_categories():
            self._cat_combo_box.addItem(cat.name, userData=cat)
        edit_button = QtWidgets.QPushButton('Редактировать')
        edit_button.\
            clicked.connect(self.edit_category)  # type: ignore[attr-defined]
        add_cat_button = QtWidgets.QPushButton('Добавить')
        add_cat_button.\
            clicked.connect(self.add_category)  # type: ignore[attr-defined]
        # self._del_cat_button = QtWidgets.QPushButton('Удалить')

        hor_layout2.addWidget(cat_label)
        hor_layout2.addWidget(self._cat_combo_box)
        hor_layout2.addWidget(edit_button)
        hor_layout2.addWidget(add_cat_button)
        # self._hor_layout2.addWidget(self._del_cat_button)

        add_exp_button = QtWidgets.QPushButton('Добавить')
        add_exp_button.\
            clicked.connect(self.add_expense)  # type: ignore[attr-defined]

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(recent_expenses_label)
        vertical_layout.addWidget(self._expenses_table)
        vertical_layout.addWidget(budget_label)
        # self._vertical_layout.addWidget(self._budget_table)
        self._budget_table = BudgetTable(0, 3, self._presenter)
        self.init_budget_table()

        vertical_layout.addWidget(self._budget_table)
        vertical_layout.addLayout(hor_layout1)
        vertical_layout.addLayout(hor_layout2)
        vertical_layout.addWidget(add_exp_button)
        self._window.setLayout(vertical_layout)

        self._window.show()

        # dialog = EditCategoryDialog([Category(name='A', parent=2)])

    def init_expense_table(self) -> None:
        """inits expense table"""
        self._expenses_table.setColumnCount(4)
        self._expenses_table.setRowCount(0)
        self._expenses_table.setHorizontalHeaderLabels(
            "Дата Сумма Категория Комментарий".split())
        self._header = self._expenses_table.horizontalHeader()
        self._header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self._header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self._header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self._header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.ResizeMode.Stretch)

        for exp in self._presenter.get_all_expenses():
            self.add_to_expenses_table(exp)

    def init_budget_table(self) -> None:
        """inits budget table"""
        self._budget_table.setColumnCount(3)
        self._budget_table.setRowCount(0)
        self._budget_table.setHorizontalHeaderLabels(
            "Срок Сумма Бюджет".split())
        _header = self._budget_table.horizontalHeader()
        _header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        _header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        _header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)

        for bud in self._presenter.get_all_budgets():
            self.add_to_budget_table(bud)

    def get_window(self) -> QtWidgets.QWidget:
        """Return window"""
        return self._window

    def get_app(self) -> QtWidgets.QApplication:
        """Returns app instance"""
        return self._app

    def edit_category(self) -> None:
        """action edits category"""
        cat = self._cat_combo_box.itemData(self._cat_combo_box.currentIndex())
        dialog = EditCategoryDialog(self._presenter.get_all_categories(), cat)
        dialog.show()
        dial_res = dialog.exec()
        print(dial_res)
        if dial_res == QtWidgets.QDialog.DialogCode.Accepted:
            print('Edit accepted')
            res_obj = dialog.get_res_obj()
            if res_obj is not None:
                self._presenter.update_category(res_obj)
            self._cat_combo_box.clear()
            for cat in self._presenter.get_all_categories():
                self._cat_combo_box.addItem(cat.name, userData=cat)

    def add_category(self) -> None:
        """action adds category"""
        dialog = EditCategoryDialog(self._presenter.get_all_categories())
        dialog.show()
        dial_res = dialog.exec()
        print(dial_res)
        if dial_res == QtWidgets.QDialog.DialogCode.Accepted:
            print('Add accepted')
            res_obj = dialog.get_res_obj()
            if res_obj is not None:
                self._presenter.add_category(res_obj)
            self._cat_combo_box.clear()
            for cat in self._presenter.get_all_categories():
                self._cat_combo_box.addItem(cat.name, userData=cat)

    def add_to_expenses_table(self, exp: Expense) -> None:
        """action adds expense"""
        row = self._expenses_table.rowCount()
        self._expenses_table.insertRow(row)
        item = QtWidgets.QTableWidgetItem(str(exp.expense_date))
        item.setFlags(QtCore.Qt.ItemIsEnabled)  # type: ignore[attr-defined]
        self._expenses_table.setItem(row, 0, item)

        item = QtWidgets.QTableWidgetItem(str(exp.amount))
        item.setFlags(QtCore.Qt.ItemIsEnabled)  # type: ignore[attr-defined]
        self._expenses_table.setItem(row, 1, item)

        cat = self._presenter.get_category(exp.category)
        item = QtWidgets.QTableWidgetItem(cat.name if cat is not None else '-')
        item.setFlags(QtCore.Qt.ItemIsEnabled)  # type: ignore[attr-defined]
        self._expenses_table.setItem(row, 2, item)

        item = QtWidgets.QTableWidgetItem(exp.comment)
        item.setFlags(QtCore.Qt.ItemIsEnabled)  # type: ignore[attr-defined]
        self._expenses_table.setItem(row, 3, item)

    def add_to_budget_table(self, budget: Budget) -> None:
        """adds record to budget table"""
        row = self._budget_table.rowCount()
        self._budget_table.insertRow(row)
        item = QtWidgets.QTableWidgetItem(budget.term)
        item.setFlags(QtCore.Qt.ItemIsEnabled)  # type: ignore[attr-defined]
        self._budget_table.setItem(row, 0, item)

        item = QtWidgets.QTableWidgetItem(str(budget.cur_sum))
        item.setFlags(QtCore.Qt.ItemIsEnabled)  # type: ignore[attr-defined]
        self._budget_table.setItem(row, 1, item)

        item = QtWidgets.QTableWidgetItem(str(budget.budget))
        item.setFlags(QtCore.Qt.ItemIsEnabled)  # type: ignore[attr-defined]
        self._budget_table.setItem(row, 2, item)

    def add_expense(self) -> None:
        """adds expense"""
        dialog = ExpenseDialog(self._presenter.get_all_categories())
        dial_res = dialog.exec()
        if dial_res == QtWidgets.QDialog.DialogCode.Accepted:
            new_exp = dialog.get_res_obj()
            print('new_exp', new_exp)
            if new_exp is not None:
                self._presenter.add_expense(new_exp)
            self._expenses_table.clearContents()
            self._expenses_table.setRowCount(0)
            for exp in self._presenter.get_all_expenses():
                self.add_to_expenses_table(exp)

            # update budgets
            self._budget_table.refresh()
