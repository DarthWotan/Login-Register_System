import random

def encoding(word: str, indicator: int, available_symbols):
    new_word = []
    for i in list(word):
        if i != " ":
            new_word.append(available_symbols[available_symbols.index(i) - indicator])
        else:
            new_word.append(i)

    new_word = "".join(new_word)
    return new_word


def decoding(word: str, indicator: int, available_symbols:str):
    new_word = []
    for i in word:
        if i != " ":
            new_word.append(available_symbols[(available_symbols.index(i) - (len(available_symbols) - indicator))])

        else:
            new_word.append(i)

    new_word = "".join(new_word)
    return new_word


if __name__ == "__main__":

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    numbers = "1234567890"
    symbols = "!§$%&/()=?@€{[]}+*~#'-_.:,;<>|"


    available_symbols = (letters + numbers + symbols)

    print(len(available_symbols))
    n = 1
    x = 0
    for _ in range(len(available_symbols)):
        x = random.randint(1, len(available_symbols))
        word = "Wotan wotan@gmail.com 1234 Owner 10000"

        new_word = encoding(word, x, available_symbols)

        print(f"New word: {new_word}")

        old_word = decoding(new_word, x, available_symbols)

        print(f"Indicator: {x}")
        print(f"{n}. Old word: {old_word}\n")
        if old_word != "Testacc test@gmail.com 1234 Admin 10000":
            print("ERROR")
            break
        n += 1
    word = str(input("Word:"))
    ind = int(input("Indicator"))
    print(decoding(word,ind, available_symbols))