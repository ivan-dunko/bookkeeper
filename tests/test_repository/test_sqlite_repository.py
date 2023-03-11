from bookkeeper.repository.sqlite_repository import SqliteRepository

import pytest
import os
from dataclasses import dataclass

@pytest.fixture
def custom_class():
    @dataclass
    class Custom():
        pk: int = 0
        name: str = 'A'

    return Custom


@pytest.fixture
def repo(custom_class):
    return SqliteRepository(custom_class().__class__, db_name=':memory:')


def test_init_name_db(custom_class):
    repo = SqliteRepository[custom_class().__class__](custom_class().__class__)
    del repo
    os.remove(custom_class().__class__.__name__ + '.db')

    repo = SqliteRepository[custom_class().__class__](custom_class().__class__, db_name='A')
    repo.add(custom_class())
    del repo

    repo = SqliteRepository[custom_class().__class__](custom_class().__class__, db_name='A')
    del repo
    os.remove('A.db')


def test_get_fields_as_string(repo, custom_class):
    s = SqliteRepository.get_fields_as_string(custom_class().__class__)
    assert s == 'pk,name'

def test_crud(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_can_delete_unexistent(repo):
    repo.delete(1)


def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_all(repo, custom_class):
    objects = [custom_class() for i in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects


def test_get_all_with_condition(repo, custom_class):
    objects = []
    for i in range(5):
        o = custom_class()
        o.name = str(i)
        #o.test = 'test'
        repo.add(o)
        objects.append(o)
    assert repo.get_all({'name': '0'}) == [objects[0]]
    #assert repo.get_all({'test': 'test'}) == objects
