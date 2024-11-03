def signup_validator(data):
    error_exists = False
    print(data)
    if data.get('firstname') is None:
        print("fn")
        error_exists = True
    elif data.get('lastname') is None:
        print('ln')
        error_exists = True
    elif data.get('phonenumber') is None:
        print('pn')
        error_exists = True
    elif data.get('username') is None:
        print('un')
        error_exists = True
    elif data.get('password') is None:
        print('pwd')
        error_exists = True
    if error_exists:
        raise ValueError("Validation error")
    
def login_validator(data):
    error_exists = False
    print(data)
    if data.get("username") is None:
        print("un")
        error_exists = True
    elif data.get("password") is None:
        print("pwd")
        error_exists = True
    if error_exists:
        raise ValueError("Validation ")