from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from typing import Any


class Presenter:
    def __init__(self,
                 cat_repo: AbstractRepository[Category],
                 exp_repo: AbstractRepository[Expense],
                 budget_repo: AbstractRepository[Budget]) -> None:
        self._cat_repo = cat_repo
        self._exp_repo = exp_repo
        self._budget_repo = budget_repo

    def get_all_categories(self, where: dict[str, Any] | None = None) -> list[Category]:
        return self._cat_repo.get_all()

    def update_category(self, cat: Category) -> None:
        self._cat_repo.update(cat)

    def update_budget(self, budget: Budget) -> None:
        self._budget_repo.update(budget)

    def update_expense(self, exp: Expense) -> None:
        self._exp_repo.update(exp)

    def add_category(self, cat: Category) -> None:
        self._cat_repo.add(cat)

    def add_expense(self, exp: Expense) -> None:
        self._exp_repo.add(exp)
        # update budgets
        budgets = self.get_all_budgets()
        for bud in budgets:
            bud.cur_sum += exp.amount
            self._budget_repo.update(bud)

    def get_category(self, cat_id: int) -> Category:
        return self._cat_repo.get(cat_id)

    def get_all_expenses(self) -> list[Expense]:
        return self._exp_repo.get_all()

    def get_all_budgets(self) -> list[Budget]:
        return self._budget_repo.get_all()
