from hashlib import sha256

from .models import User
from .db import DB

db = DB()

class UserService:
    
    def add_user(self, username: str, password: str, first_name: str, last_name: str) -> User:
        user = User(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        db.create_user(
            id=user.id,
            username=user.username,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name
        )
        return user

    def get_user_by_username(self, username: str) -> User | None:
       user_data = db.get_user_by_username(username)

       if user_data is not None:
           return User.from_dict(user_data) 
       else:
           return None

    def get_user_by_id(self, id: str) -> User | None:
        pass

    def authenticate(self, username: str, password: str) -> User | None:
        user_data = db.get_user_by_username(username)

        if user_data is None:
            return None
        else:
            if user_data['password'] != str(sha256(password.encode()).hexdigest()):
                return None
            else:
                return User(
                    username=user_data['username'],
                    password=user_data['password'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )


class CartService:
    pass


class OrderService:
    pass
