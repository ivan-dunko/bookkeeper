"""
Module containing Presenter class
"""
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget


class Presenter:
    """
    Presenter class defines business logic of application.
    It has methods for getting data from model to be shown
    in view
    """
    def __init__(self,
                 cat_repo: AbstractRepository[Category],
                 exp_repo: AbstractRepository[Expense],
                 budget_repo: AbstractRepository[Budget]) -> None:
        self._cat_repo = cat_repo
        self._exp_repo = exp_repo
        self._budget_repo = budget_repo

    def get_all_categories(self) -> list[Category]:
        """returns all categories"""
        return self._cat_repo.get_all()

    def update_category(self, cat: Category) -> None:
        """updates category"""
        self._cat_repo.update(cat)

    def update_budget(self, budget: Budget) -> None:
        """updates budget"""
        self._budget_repo.update(budget)

    def update_expense(self, exp: Expense) -> None:
        """updates expense"""
        self._exp_repo.update(exp)

    def add_category(self, cat: Category) -> None:
        """adds category"""
        self._cat_repo.add(cat)

    def add_expense(self, exp: Expense) -> None:
        """adds expense"""
        self._exp_repo.add(exp)
        # update budgets
        budgets = self.get_all_budgets()
        for bud in budgets:
            bud.cur_sum += exp.amount
            self._budget_repo.update(bud)

    def get_category(self, cat_id: int) -> Category | None:
        """gets category"""
        return self._cat_repo.get(cat_id)

    def get_all_expenses(self) -> list[Expense]:
        """gets all expenses"""
        return self._exp_repo.get_all()

    def get_all_budgets(self) -> list[Budget]:
        """gets all budgets"""
        return self._budget_repo.get_all()
