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



class ProductService:

    def get_products(self) -> list[dict]:
        return db.get_product_list()
    
    def get_product_by_id(self, product_id: int) -> dict | None:
        for product in self.get_products():
            if product['id'] == product_id:
                return product
            
    def get_product_by_name(self, name: str) -> list[dict]:
        result = []
        for product in self.get_products():
            if name.lower() in product['name'].lower():
                result.append(product)

        return result


class CartService:
    def __init__(self):
        self.cart = self.load_cart()

    def load_cart(self):
        try:
            with open(DB_FILE, "r") as f:
                data = json.load(f)
                return data.get("cart", {})
        except Exception:
            return {}

    def save_cart(self):
        try:
            with open(DB_FILE, "r+") as f:
                data = json.load(f)
                data["cart"] = self.cart
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        except Exception:
            pass

    def add_to_cart(self, product_id, quantity=1):
        """ Savatga maxsulot qo'shish """
        if str(product_id) in self.cart:
            self.cart[str(product_id)] += quantity
        else:
            self.cart[str(product_id)] = quantity

        self.save_cart()
        return self.cart

    def remove_from_cart(self, product_id):
        """ Savatdan mahsulotni o'chirish """
        if str(product_id) in self.cart:
            del self.cart[str(product_id)]
            self.save_cart()
        return self.cart

    def clear_cart(self):
        """ Savatni bo'shatish """
        self.cart = {}
        self.save_cart()
        return self.cart

    def get_cart_items(self):
        """ Hozirgi savat """
        return self.cart


class OrderService:
    def __init__(self):
        self.orders = self.load_orders()

    def load_orders(self):
        try:
            with open(DB_FILE, "r") as f:
                data = json.load(f)
                return data.get("orders", [])
        except Exception:
            return []

    def save_orders(self):
        try:
            with open(DB_FILE, "r+") as f:
                data = json.load(f)
                data["orders"] = self.orders
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        except Exception:
            pass

    def create_order(self, customer_id, cart_items):
        """
        Buyurtma yaratish:
        - customer_id: mijoz identifikatori
        - cart_items: savatdagi mahsulotlar dict
        """
        order_id = len(self.orders) + 1
        new_order = {
            "order_id": order_id,
            "customer_id": customer_id,
            "items": cart_items,
            "status": "pending"
        }
        self.orders.append(new_order)
        self.save_orders()
        return new_order

    def get_all_orders(self):
        """ Barcha buyurtmalar """
        return self.orders

    def get_orders_by_customer(self, customer_id):
        """ Mijoz boyicha buyurtmalar """
        return [o for o in self.orders if o["customer_id"] == customer_id]

    def update_order_status(self, order_id, status):
        """
        Buyurtma statusini yangilash
        status: pending / confirmed / shipped / delivered
        """
        for order in self.orders:
            if order["order_id"] == order_id:
                order["status"] = status
                self.save_orders()
                return order
        return None

