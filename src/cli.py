import sys
from getpass import getpass

from termcolor import colored, cprint

from .utils import (
    validate_username, 
    validate_password, 
    validate_name,
)
from .serivices import UserService, ProductService


class CLI:
    
    def __init__(self):
        self.current_user = None
        self.user_service = UserService()
        self.product_service = ProductService()
    
    def run(self) -> None:
        while True:
            if not self.current_user:
                self.print_main_menu()

                choice = input(colored('> ', 'yellow'))
                if choice == '1':
                    self.show_products()
                elif choice == '2':
                    self.login()
                elif choice == '3':
                    self.register()
                elif choice == '0':
                    self.quit()
                else:
                    cprint('Bunday menu mavjud emas!', 'red')
            else:
                self.print_user_manu()

                choice = input(colored('> ', 'yellow'))
                if choice == '1':
                    self.show_products()
                elif choice == '2':
                    self.logout()
                elif choice == '0':
                    self.quit()
                else:
                    cprint('Bunday menu mavjud emas!', 'red')

    def logout(self):
        self.current_user = None

    def print_main_menu(self) -> None:
        print('----------------------Main Menu----------------------')
        print('1. Products')
        print('2. Login')
        print('3. Register')
        print('0. Quit')

    def print_user_manu(self) -> None:
        print('----------------------User Menu----------------------')
        print('1. Products')
        print('2. Logout')
        print('0. Quit')

    def show_products(self) -> None:
        print('----------------------Product List----------------------')
        products = self.product_service.get_products()

        if products:
            for product in products:
                print(f"{product['id']}. {product['name']}")

            self.search_product()
        else:
            print(colored('Hozirda birorta ham mahsulot mavjud emas!', 'yellow'))

    def search_product(self):
        self.print_product_detail_menu()

        choice = input(colored('> ', 'yellow'))
        if choice == '1':
            self.show_product_detail_by_id()
        elif choice == '2':
            self.search_products_by_name()
        elif choice == '0':
            return None
        
    def show_product_detail_by_id(self):
        product_id = int(input('Product ID: '))

        product = self.product_service.get_product_by_id(product_id)

        if product:
            self.print_product_detail(product)
        else:
            print(colored('Bunday ID ga ega product mavjud emas!', 'yellow'))

    def print_product_detail(self, product):
        print('Porudct haqida malumotlar')
        print(f'Nomi: {product["name"]}')
        print(f'Tavsif: {product["description"]}')
        print(f'Narxi: {product["price"]}')
        print(f'Chegirma foizi: {product["sale"]}')
        print(f'Soni: {product["stock"]}')

    def search_products_by_name(self):
        pass

    def print_product_detail_menu(self):
        print('Productni qidirish uchun qaysi usulni tanlaysiz?')
        print('1. Product IDsi boyicha')
        print('2. Product name boyicha')
        print('0. Bosh sahifaga qaytish')

    def login(self) -> None:
        while True:
            print('Login qilish uchun quyidagi malumotlarni kiriting')

            username = input('Username: ').strip()
            password = getpass('Password: ').strip()

            # Validation
            errors = 0
            if not validate_username(username):
                cprint('Yaroqli username kiriting!', 'red')
                errors += 1
            if not validate_password(password):
                cprint('Yaroqli password kiriting!', 'red')
                errors += 1

            user = self.user_service.authenticate(username, password)
            if user is None:
                cprint('Bunday user mavjud emas!', 'red')
                errors += 1

            if errors > 0:
                continue
            else:
                cprint("Siz muvaffaqiyatli tizimga kirdingiz!", "green")
                self.current_user = user

                return True

    def register(self) -> None:
        while True:
            print('Royxatdan otish uchun quyidagi malumotlarni kiriting')

            username = input('Username: ').strip()
            password = getpass('Password: ').strip()
            confirm = getpass('Confirm: ').strip()
            first_name = input('First Name: ').strip()
            last_name = input('Last Name: ').strip()

            # Validation
            errors = 0
            if not validate_username(username):
                cprint('Yaroqli username kiriting!', 'red')
                errors += 1
            if self.user_service.get_user_by_username(username) is not None:
                cprint('Boshqa username kiriting!', 'red')
                errors += 1
            if not validate_password(password):
                cprint('Yaroqli password kiriting!', 'red')
                errors += 1
            if not validate_name(first_name):
                cprint('Yaroqli firstname kiriting!', 'red')
                errors += 1
            if not validate_name(last_name):
                cprint('Yaroqli firstname kiriting!', 'red')
                errors += 1
            if password != confirm:
                cprint('password va confirm bir xil emas!', 'red')
                errors += 1

            if errors > 0:
                continue
            else:
                self.current_user = self.user_service.add_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )
                cprint("Siz muvaffaqiyatli royxatdan otdingiz!", "green")

                return True

    def quit(self) -> None:
        cprint('Hayr!', 'green')
        sys.exit()
