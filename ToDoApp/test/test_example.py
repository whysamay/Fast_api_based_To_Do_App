import pytest


def test_equal_or_not_equal():
    assert 3 == 3


def test_is_instance():
    assert isinstance("this is string", str)
    assert not isinstance("10", int)


def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'world') is False


def test_type():
    assert type('Hello' is str)
    assert type("issi" is not int)


def test_greater_and_less_than():
    assert 7>3
    assert 4<10


def test_list():
    num_list = [1,2,3,4,5]
    any_list = [False, False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)

class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


def test_person_initialisation():
    p = Student('John', 'Doe', 'Computer Sci', 3)
    assert p.first_name == 'John', 'First name should be john'
    assert p.last_name == "Doe", "last name should be doe"
    assert p.major == 'Computer Sci'
    assert p.years == 3


@pytest.fixture
def default_employee():
    return Student('John', 'Doe', 'Computer Sci', 3)


def default_initialisation(default_employee):
    assert default_employee.first_name == 'John', 'First name should be john'
    assert default_employee.last_name == "Doe", "last name should be doe"
    assert default_employee.major == 'Computer Sci'
    assert default_employee.years == 3