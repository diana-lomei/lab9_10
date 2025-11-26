import pytest
from src.services.user_service import UserService

@pytest.fixture
def service():
    return UserService()

def test_register_user(service):
    user = service.register_user("Alice", 25)
    assert user["name"] == "Alice"
    assert user["age"] == 25

def test_register_user_without_name(service):
    import pytest
    with pytest.raises(ValueError):
        service.register_user("", 20)

def test_get_user_info(service):
    user = service.register_user("Bob", 30)
    fetched = service.get_user_info(user["id"])
    assert fetched["name"] == "Bob"
