import random
import string


def get_random_id(list_ids: list) -> str:
    while True:
        id = f"{random.choice(string.ascii_uppercase)}{random.randint(0, 9)}{random.randint(0, 9)}"
        if id not in list_ids:
            return id


print(get_random_id(["A89"]))
