import random
import sqlite3

connection = sqlite3.connect('card.s3db')
cursor = connection.cursor()

card_table = """CREATE TABLE IF NOT EXISTS card
(id INTEGER PRIMARY KEY AUTOINCREMENT,
number VARCHAR(17) NOT NULL UNIQUE,
pin VARCHAR(5) NOT NULL,
balance INTEGER DEFAULT 0
);
"""

cursor.execute(card_table)
connection.commit()


def luhn_check(iterable):
    luhn_list = [int(x) for x in iterable]

    for y in range(1, 16):
        if y % 2 == 1:
            luhn_list[y - 1] *= 2
            if luhn_list[y - 1] > 9:
                luhn_list[y - 1] -= 9
    return sum(luhn_list) % 10


options = 1
while options in (1, 2):
    options = int(input("1.Create an account\n"
                        "2.Log into account\n"
                        "0.Exit\n"))
    if options == 1:
        card_digits = ['4', '0', '0', '0', '0', '0'] + [str(random.randint(0, 9)) for i in range(9)]
        PIN_numbers = [str(random.randint(0, 9)) for u in range(4)]

        control_number = luhn_check(card_digits)

        if control_number == 0:
            card_digits.append('0')
        else:
            card_digits.append(str(10 - control_number))

        card_number = "".join(card_digits)
        PIN_number = "".join(PIN_numbers)
        print('Your card has been created')
        print(f'Your card number:\n'
              f'{card_number}')
        print(f'Your card PIN:\n'
              f'{PIN_number}\n')

        add_values = """INSERT INTO card (id ,number, pin)
        VALUES(NULL, ?, ?)
        """
        cursor.execute(add_values, (card_number, PIN_number))
        connection.commit()

    if options == 2:
        cursor.execute("""SELECT * FROM card""")
        all_rows = cursor.fetchall()

        if len(all_rows) != 0:
            card_login = input('Enter your card number:\n')
            PIN_login = input('Enter your PIN\n')
            cursor.execute(f"""SELECT * FROM card WHERE number = {card_login} AND pin = {PIN_login};""")
            current_account = cursor.fetchone()

            if current_account is not None:
                print('You have successfully logged in!')
                logged_options = 1
                balance = current_account[3]
                while logged_options in (1, 2, 3, 4, 5):
                    logged_options = int(input("1.Balance\n"
                                               "2.Add income\n"
                                               "3.Do transfer\n"
                                               "4.Close account\n"
                                               "5.Log out\n"
                                               "0.Exit\n"))
                    if logged_options == 1:
                        print(f'Balance: {balance}')

                    elif logged_options == 2:
                        income = int(input('Enter income:\n'))
                        print('Income was added!')
                        balance += income
                        cursor.execute(f"""UPDATE card SET balance = {balance} WHERE id = {current_account[0]};""")
                        connection.commit()

                    elif logged_options == 3:
                        try:
                            transfer_account = input('Transfer\n'
                                                     'Enter card number:\n')
                            card_checksum = 10 - luhn_check(transfer_account[:-1])
                            cursor.execute(f"""SELECT id, number FROM card WHERE number = {transfer_account};""")
                            target_account = cursor.fetchone()

                            if transfer_account == current_account[1]:
                                print("You can't transfer money to the same account!")

                            elif int(transfer_account[-1]) != card_checksum:
                                print('Probably you made a mistake in the card number. Please try again!')

                            elif target_account is None:
                                print('Such a card does not exist')

                            else:
                                transfer_amount = int(input("Enter how much money you want to transfer:\n"))

                                if transfer_amount > balance:
                                    print("Not enough money!")

                                else:
                                    balance = balance - transfer_amount
                                    cursor.execute(f"""UPDATE card SET balance = {balance}
                                                    WHERE id = {current_account[0]}""")
                                    cursor.execute(f"""UPDATE card SET balance = balance + {transfer_amount} 
                                                    WHERE id = {target_account[0]}""")
                                    connection.commit()
                                    print("Success!")
                        except IndexError:
                            print('The length of your card is not correct')

                    elif logged_options == 4:
                        cursor.execute(f"""DELETE FROM card WHERE id = {current_account[0]}""")
                        connection.commit()
                        print("The account has been closed!")
                        break

                    elif logged_options == 0:
                        options = 0

            else:
                print('Wrong card number or PIN!')
        else:
            print('You have to create an account first')


print('Bye!')
cursor.close()
connection.close()

