"""
Table for budget handling
"""
from PySide6 import QtWidgets
from PySide6 import QtCore
from bookkeeper.presenter import Presenter
from bookkeeper.models.budget import Budget


class BudgetTable(QtWidgets.QTableWidget):
    """Table for budget handling"""
    def __init__(self, rows: int, cols: int, presenter: Presenter) -> None:
        super().__init__(rows, cols)
        self._presenter = presenter

    def add_row(self, budget: Budget) -> None:
        """Adds row to table"""
        self.blockSignals(True)
        row = self.rowCount()
        self.insertRow(row)
        item = QtWidgets.QTableWidgetItem(budget.term)
        item.setFlags(QtCore.Qt.ItemIsEnabled)  # type: ignore[attr-defined]
        self.setItem(row, 0, item)

        item = QtWidgets.QTableWidgetItem(str(budget.cur_sum))
        item.setFlags(QtCore.Qt.ItemIsEnabled)  # type: ignore[attr-defined]
        self.setItem(row, 1, item)

        item = QtWidgets.QTableWidgetItem(str(budget.budget))
        # item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.setItem(row, 2, item)
        self.blockSignals(False)

    def refresh(self) -> None:
        """Updates table"""
        self.clearContents()
        self.setRowCount(0)
        for bud in self._presenter.get_all_budgets():
            self.add_row(bud)

    def cell_changed(self, row: int, col: int) -> None:
        """Updates budget model"""
        item = self.item(row, col)
        pk = row + 1
        term = self.item(row, 0).text()
        cur_sum = int(self.item(row, 1).text())
        new_budget = int(item.text())
        new_budget_obj = Budget(budget=new_budget, cur_sum=cur_sum, term=term, pk=pk)
        print(new_budget_obj)
        self._presenter.update_budget(new_budget_obj)
        print('Item changed')
