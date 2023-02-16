import time


def delay_decorator(function):
    def wrapper_function():
        time.sleep(2)
        function()
    return wrapper_function()


@delay_decorator
def say_hello():
    return("Hello")


@delay_decorator
def say_bye():
    print("Bye")


@delay_decorator
def say_greeting():
    print("How are you?")


# say_hello()
# say_greeting()
# say_bye()

def uppercase_decorator(function):
    def wrapper():
        func = function()
        make_uppercase = f"<b> {func.upper()} </b>"
        return make_uppercase

    return wrapper

def say_hi():
    return 'hello there'

decorate = uppercase_decorator(say_hi)
print(decorate())
