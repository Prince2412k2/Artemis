import random
import string
import bcrypt

def get_random_id(list_ids: list) -> str:
    while True:
        id = f"{random.choice(string.ascii_uppercase)}{random.randint(0, 9)}{random.randint(0, 9)}"
        if id not in list_ids:
            return id



def main():
    print(get_random_id([]))

if __name__=="__main__":
    main()