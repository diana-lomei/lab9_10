from src.database.repositories.user_repo import UserRepository

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def register_user(self, name, age):
        # Проста бізнес-логіка
        if not name:
            raise ValueError("Name is required")
        return self.repo.create(name, age)

    def get_user_info(self, user_id):
        return self.repo.get(user_id)
