from PySide6 import QtWidgets
from bookkeeper.presenter import Presenter
from bookkeeper.models.budget import Budget
from PySide6 import QtCore


class BudgetTable(QtWidgets.QTableWidget):
    def __init__(self, rows: int, cols: int, presenter: Presenter) -> None:
        super().__init__(rows, cols)
        self._presenter = presenter
        """
        self.setHorizontalHeaderLabels(
            "Срок Сумма Бюджет".split())

        self.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        
        self.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        self.itemChanged.connect(self.item_changed)

        for budget in presenter.get_all_budgets():
            self.add_row(budget)
        """

    def add_row(self, budget: Budget) -> None:
        self.blockSignals(True)
        row = self.rowCount()
        self.insertRow(row)
        item = QtWidgets.QTableWidgetItem(budget.term)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.setItem(row, 0, item)

        item = QtWidgets.QTableWidgetItem(str(budget.cur_sum))
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.setItem(row, 1, item)

        item = QtWidgets.QTableWidgetItem(str(budget.budget))
        # item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.setItem(row, 2, item)
        self.blockSignals(False)

    def cell_changed(self, row: int, col: int) -> None:
        item = self.item(row, col)
        pk = row + 1
        term = self.item(row, 0).text()
        cur_sum = int(self.item(row, 1).text())
        new_budget = int(item.text())
        new_budget_obj = Budget(budget=new_budget, cur_sum=cur_sum, term=term, pk=pk)
        print(new_budget_obj)
        self._presenter.update_budget(new_budget_obj)
        """
        self.clear()
        for bud in self._presenter.get_all_budgets():
            self.add_row(bud)
        """
        print('Item changed')
