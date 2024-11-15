from dataclasses import dataclass
from uuid import UUID, uuid4
import re

@dataclass
class Person:
    """Информация о пользователе."""
    login: str
    password: str
    username: str
    metadata: str = ""

class PersonDB:
    def __init__(self) -> None:
        """Инициализирует базу данных."""
        self._database: dict[UUID, Person] = {}
        self._login_registry: dict[str, UUID] = {}

    def _validate_login(self, login: str) -> None:
        """Проверяет, что логин валиден."""
        if not login or not re.match(r'^[A-Za-z0-9]+$', login):
            raise ValueError("Логин не должен быть пустым и должен содержать только буквы и цифры.")
        if login in self._login_registry:
            raise ValueError("Логин должен быть уникальным.")

    def _validate_password(self, password: str) -> None:
        """Проверяет, что пароль валиден."""
        if (len(password) < 10 or
            not re.search(r'[A-Z]', password) or
            not re.search(r'[a-z]', password) or
            not re.search(r'[0-9]', password) or
            not re.match(r'^[A-Za-z0-9]+$', password)):
            raise ValueError("Пароль не соответствует требованиям.")

    def create_person(self, person: Person) -> UUID:
        """Создает новую запись о пользователе в базе данных."""
        self._validate_login(person.login)
        self._validate_password(person.password)
        
        person_id = uuid4()
        self._database[person_id] = person
        self._login_registry[person.login] = person_id
        
        return person_id
    
    def read_person_info(self, person_id: UUID) -> Person:
        """Читает данные пользователя из базы данных по его UUID."""
        if person_id not in self._database:
            raise KeyError("Пользователь не найден.")
        return self._database[person_id]

    def update_person_info(self, person_id: UUID, person_info_new: Person) -> None:
        """Обновляет данные о пользователе по его UUID."""
        if person_id not in self._database:
            raise KeyError("Пользователь не найден.")
        
        current_person = self._database[person_id]

        if person_info_new.login and person_info_new.login != current_person.login:
            self._validate_login(person_info_new.login)
            del self._login_registry[current_person.login]
            self._login_registry[person_info_new.login] = person_id
            current_person.login = person_info_new.login
        
        if person_info_new.password:
            self._validate_password(person_info_new.password)
            current_person.password = person_info_new.password
        
        if person_info_new.username:
            current_person.username = person_info_new.username
        
        if person_info_new.metadata:
            current_person.metadata = person_info_new.metadata

    def delete_person(self, person_id: UUID) -> None:
        """Удаляет запись о пользователе по его UUID."""
        if person_id not in self._database:
            raise KeyError("Пользователь не найден.")
        
        deleted_person = self._database.pop(person_id)
        del self._login_registry[deleted_person.login]

# Пример тестирования
if __name__ == "__main__":
    # Создаем пользователя и проверяем базу данных
    person1 = Person(
        password="Aa1Bb2Cc3Dd4",
        login="login1",
        username="user#1",
    )

    database = PersonDB()
    person1_id = database.create_person(person1)

    assert len(database._database) == 1
    assert len(database._login_registry) == 1
    assert person1_id in database._database
    assert person1.login in database._login_registry
    assert database._database[person1_id] == person1

    # Проверяем неправильные входные данные
    persons_wrong = {
        "no-login": Person(password="Aa1Bb2Cc3Dd4", login="", username="user#2"),
        "existed-login": Person(password="Aa1Bb2Cc3Dd4", login="login1", username="user#2"),
        "too-short-password": Person(password="12345", login="login2", username="user#2"),
        "no-lower": Person(password="A1B2C3D4E5F", login="login2", username="user#2"),
        "no-upper": Person(password="a1b2c3d4e5f", login="login2", username="user#2"),
        "no-digits": Person(password="aAbBcCdDeEf", login="login2", username="user#2"),
    }

    for test_name, wrong_person in persons_wrong.items():
        try:
            database.create_person(wrong_person)
            assert False, test_name
        except ValueError:
            assert True
            assert len(database._database) == 1
            assert len(database._login_registry) == 1

    # Чтение данных о пользователе
    person = database.read_person_info(person1_id)
    assert person1 == person
    assert len(database._database) == 1
    assert len(database._login_registry) == 1

    try:
        fake_id = uuid4()
        person = database.read_person_info(fake_id)
        assert False
    except KeyError:
        assert True
        assert len(database._database) == 1
        assert len(database._login_registry) == 1

    # Обновление данных о пользователе
    person2 = Person(password="AaBbcC1234Dd", login="login2", username="user#2")
    person2_id = database.create_person(person2)

    assert len(database._database) == 2
    assert len(database._login_registry) == 2
    assert person2_id in database._database
    assert person2.login in database._login_registry
    assert database._database[person2_id] == person2

    person2_update = Person(password="abcDEF123456", login="LOGIN2", username="")
    database.update_person_info(person2_id, person2_update)
    
    assert len(database._database) == 2
    assert len(database._login_registry) == 2
    assert person2_id in database._database
    assert person2.login not in database._login_registry
    assert "LOGIN2" in database._login_registry
    assert database._database[person2_id].login == "LOGIN2"

    # Удаление пользователя
    try:
        fake_id = uuid4()
        database.delete_person(fake_id)
        assert False
    except KeyError:
        assert True
        assert len(database._database) == 2
        assert len(database._login_registry) == 2

    database.delete_person(person2_id)
    assert len(database._database) == 1
    assert len(database._login_registry) == 1
    assert person2_id not in database._database
    assert "LOGIN2" not in database._login_registry