import sys
from getpass import getpass

from termcolor import colored, cprint

from .utils import (
    validate_username, 
    validate_password, 
    validate_name,
)
from .serivices import UserService


class CLI:
    
    def __init__(self):
        self.current_user = None
        self.user_service = UserService()
    
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
