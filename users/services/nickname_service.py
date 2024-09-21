import random
from time import localtime, strftime, time


class TemporaryNickNameService:

    @staticmethod
    def generate_nickname() -> str:
        front_num = strftime("%H%M%S", localtime(time()))
        back_num = random.randint(1000, 9999)

        return f"U{front_num}-{back_num}"
