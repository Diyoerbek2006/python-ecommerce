def validate_username(username: str) -> bool:
    return username.isalnum()

def validate_password(password: str) -> bool:
    return len(password) >= 4

def validate_name(name: str) -> bool:
    return name.isalpha()
