from src.database.repositories.user_repo import UserRepository

class UserController:
    def __init__(self):
        self.repo = UserRepository()

    def create_user(self, data):
        return self.repo.create(data["name"], data.get("age"))

    def get_user(self, user_id):
        return self.repo.get(user_id)

    def update_user(self, user_id, data):
        return self.repo.update(user_id, data.get("name"), data.get("age"))

    def delete_user(self, user_id):
        return self.repo.delete(user_id)
