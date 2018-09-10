import cs50

#This python program gives change.

def main():
    while True:
        print("Change owed: ", end = "")
        change = cs50.get_float()
        if change >= 0:
            break
    cents = int(100 * change)
    print(cash(cents))

def cash(cents):
    return cents//25 + (cents%25)//10 + (cents%25%10)/5 + (cents%25%10%5)


if __name__ == "__main__":
    main()
