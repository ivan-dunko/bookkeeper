"""
Модель бюджета
"""
from dataclasses import dataclass


@dataclass
class Budget:
    """
    Бюджет хранит собственно бюджет, текущую сумму,
    срок и порядковый номер
    """
    budget: int = 0
    cur_sum: int = 0
    term: str = '-'
    pk: int = 0
