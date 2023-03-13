"""
Простой тестовый скрипт для терминала
"""
import os

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SqliteRepository
from bookkeeper.utils import read_tree
from bookkeeper.presenter import Presenter
from bookkeeper.view.gui_view import GUIView

# cat_repo = MemoryRepository[Category]()
# exp_repo = MemoryRepository[Expense]()

os.remove('bookkeeper.db')
cat_repo = SqliteRepository[Category](Category, db_name='bookkeeper')
exp_repo = SqliteRepository[Expense](Expense, db_name='bookkeeper')
budget_repo = SqliteRepository[Budget](Budget, db_name='bookkeeper')

budget_repo.add(Budget(budget=1000, cur_sum=0, term='day'))
budget_repo.add(Budget(budget=32000, cur_sum=0, term='month'))
budget_repo.add(Budget(budget=500000, cur_sum=0, term='year'))

cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()

Category.create_from_tree(read_tree(cats), cat_repo)
exp = Expense(int(20), 1)
exp_repo.add(exp)
exp = Expense(int(30), 2)
exp_repo.add(exp)
presenter = Presenter(cat_repo, exp_repo, budget_repo)
gui = GUIView(presenter)
gui.get_app().exec()

"""
while True:
    try:
        cmd = input('$> ')
    except EOFError:
        break
    if not cmd:
        continue
    if cmd == 'категории':
        print(*cat_repo.get_all(), sep='\n')
    elif cmd == 'расходы':
        print(*exp_repo.get_all(), sep='\n')
    elif cmd[0].isdecimal():
        amount, name = cmd.split(maxsplit=1)
        try:
            cat = cat_repo.get_all({'name': name})[0]
        except IndexError:
            print(f'категория {name} не найдена')
            continue
        exp = Expense(int(amount), cat.pk)
        exp_repo.add(exp)
        print(exp)
"""
