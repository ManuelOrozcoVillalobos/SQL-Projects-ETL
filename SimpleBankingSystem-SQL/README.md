# SimpleBankingSystem-SQL

This script allows customers to create a new account in our banking system.

Once the program starts it prints the menu:

1. Create an account
2. Log into the account
0. Exit

If the customer chooses ‘Create an account’, the script generates a new card number that satisfies all the conditions described above. 
Then it should generate a PIN code that belongs to the generated card number. 
The PIN is a sequence of 4 digits; it should be generated in the range from 0000 to 9999.

If the customer chooses ‘Log into account’, the script asks to enter the card information.

After the information has been entered correctly, the script allows the user to check the account balance; after creating the account, the balance should be 0. 
It should also be possible to log out of the account and exit the program.

Create a database named card.s3db with a table titled card. IT has the following columns:
-id INTEGER
-number TEXT
-pin TEXT
-balance INTEGER DEFAULT 0
Pay attention: your database file should be created when the program starts if it hasn’t yet been created. And all created cards should be stored in the database from now.

The menu should look like this:
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit

If the user asks for Balance, the program reads the balance of the account from the database and output it into the console.

Add income item should allow us to deposit money to the account.

Do transfer item should allow transferring money to another account. 
Erros handled:
If the user tries to transfer more money than he/she has, output: Not enough money!
If the user tries to transfer money to the same account, output the following message: You can't transfer money to the same account!
If the receiver's card number doesn’t pass the Luhn algorithm, the script should output: Probably you made a mistake in the card number. Please try again!
If the receiver's card number doesn’t exist, the script should output: Such a card does not exist.
If there is no error, ask the user how much money they want to transfer and make the transaction.
If the user chooses the Close account item, the script should delete that account from the database.

Close account deletes the entry from the database and close the account.
