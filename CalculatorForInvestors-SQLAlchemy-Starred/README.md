# CalculatorForInvestors-SQLAlchemy

The script starts with a welcoming message: Welcome to the Investor Program!;

Display MAIN MENU
MAIN MENU
0 Exit
1 CRUD operations
2 Show top ten companies by criteria

Ask for an option

When CRUD MENU is selected, display the menu and ask for an option.
CRUD MENU
0 Back
1 Create a company
2 Read a company
3 Update a company
4 Delete a company
5 List all companies

-When Create a company is selected.
  Ask for related values.;
  Create a company in the companies table;
  Create the financial data in the financial table;
  Print Company created successfully!;
  Return to the main menu;
  
 
 -When Read a company is selected
  Ask for a name Enter company name;
  When no match is found, print Company not found! and return to the main menu;
  When a match is found, list the matching companies with indexes;
  Ask for a number Enter company number;
  Calculate the financial indicators with the given formulas below;
  Print them with the company name and ticker;
  Return to the main menu;
  
-When Update a company is selected;
  Ask for a name Enter company name:;
  When no match is found, print Company not found! and return to the main menu;
  When a match is found, list the matching companies with indexes;
  Ask for a number Enter company number:;
  Ask for the related values;
  Updates the values and print Company updated successfully!;
  Return to the main menu;
  
-When Delete a company is selected.
  Ask for a name: Enter company name:;
  When no match is found, print Company not found! and return to the main menu;
  When a match is found, list the matching companies with indexes;
  Ask for a number Enter company number:;
  Delete the company, print Company deleted successfully!;
  Return to the main menu;
  
-When List all companies is selected.
  Print COMPANY LIST as heading;
  Print the ticker, name, and industry ordered by ticker from the companies table;
  Return to the main menu;
  

When TOP TEN MENU is selected, display the menu and ask for an option:
1 List by ND/EBITDA
2 List by ROE
3 List by ROA

When a valid option is selected, calculate the indicator
Find the top ten values
Print a ticker and indicator in the heading
Print the top ten values

The code snippet below shows the formulas to calculate the rankings:
P/E = Market price / Net profit
P/S = Market price / Sales
P/B = Market price / Assets
ND/EBITDA = Net debt / EBITDA
ROE = Net profit / Equity
ROA = Net profit / Assets
L/A = Liabilities / Assets
.
