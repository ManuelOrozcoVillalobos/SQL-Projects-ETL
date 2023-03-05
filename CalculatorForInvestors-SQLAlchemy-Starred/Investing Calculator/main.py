import csv
import sqlite3
from sqlalchemy import Column, String, Float, create_engine, asc
from sqlalchemy.orm import sessionmaker, declarative_base

connection = sqlite3.connect('investor.db')
Base = declarative_base()


class Company(Base):
    __tablename__ = "companies"

    ticker = Column(String, primary_key=True)
    name = Column(String)
    sector = Column(String)


class Finance(Base):
    __tablename__ = "financial"

    ticker = Column(String, primary_key=True)
    ebitda = Column(Float)
    sales = Column(Float)
    net_profit = Column(Float)
    market_price = Column(Float)
    net_debt = Column(Float)
    assets = Column(Float)
    equity = Column(Float)
    cash_equivalents = Column(Float)
    liabilities = Column(Float)


engine = create_engine("sqlite:///investor.db", echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
query_c = session.query(Company)
query_f = session.query(Finance)

company_numbers = len(query_c.all())
finance_numbers = len(query_f.all())

if company_numbers == 0 and finance_numbers == 0:
    with open("companies.csv", newline='') as company, open("financial.csv", newline='') as finance:
        company_reader = csv.reader(company, delimiter=",")
        finance_reader = csv.reader(finance, delimiter=",")
        company_list = [[item if item != "" else None for item in row] for row in company_reader]
        finance_list = [[item if item != "" else None for item in row] for row in finance_reader]
        company_size = len(company_list)
        finance_size = len(finance_list)

        for c in range(1, company_size):
            company_entry = Company(ticker=company_list[c][0], name=company_list[c][1], sector=company_list[c][2])
            session.add(company_entry)
            session.commit()

        for f in range(1, finance_size):
            try:
                finance_entry = Finance(ticker=finance_list[f][0], ebitda=finance_list[f][1],
                                        sales=finance_list[f][2], net_profit=finance_list[f][3],
                                        market_price=finance_list[f][4], net_debt=finance_list[f][5],
                                        assets=finance_list[f][6], equity=finance_list[f][7],
                                        cash_equivalents=finance_list[f][8], liabilities=finance_list[f][9])
                session.add(finance_entry)
                session.commit()
            except ValueError:
                pass


main_menu = 1

print('Welcome to the Investor Program!\n')

while main_menu != 0:
    try:
        main_menu = int(input("MAIN MENU\n"
                              "0 Exit\n"
                              "1 CRUD operations\n"
                              "2 Show top ten companies by criteria\n"
                              "\nEnter an option:\n"))
        if main_menu == 0:
            print('Have a nice day!')

        elif main_menu == 1:
            crud_menu = 1
            while crud_menu in (0, 1, 2, 3, 4, 5):
                crud_menu = int(input("CRUD MENU\n"
                                      "0 Back\n"
                                      "1 Create a company\n"
                                      "2 Read a company\n"
                                      "3 Update a company\n"
                                      "4 Delete a company\n"
                                      "5 List all companies\n"
                                      "\nEnter an option:\n"))
                if crud_menu == 0:
                    break

                elif crud_menu == 1:
                    ticker = input("Enter ticker (in the format 'MOON'):\n")
                    company_name = input("Enter company (in the format 'Moon Corp'):\n")
                    industry = input("Enter industries(in the format 'Technology'):\n")
                    ebitda = input("Enter ebitda (in the format '987654321'):\n")
                    sales = input("Enter sales (in the format '987654321'):\n")
                    net_profit = input("Enter net profit (in the format '987654321'):\n")
                    market_price = input("Enter market price (in the format '987654321'):\n")
                    net_debt = input("Enter net debt (in the format '987654321'):\n")
                    assets = input("Enter assets (in the format '987654321'):\n")
                    equity = input("Enter equity (in the format '987654321'):\n")
                    cash_equivalents = input("Enter cash equivalents (in the format '987654321'):\n")
                    liabilities = input("Enter liabilities (in the format '987654321'):\n")

                    try:

                        session.add(Company(ticker=ticker, name=company_name, sector=industry))
                        session.add(Finance(ticker=ticker, ebitda=ebitda, sales=sales, net_profit=net_profit,
                                            market_price=market_price, net_debt=net_debt, assets=assets, equity=equity,
                                            cash_equivalents=cash_equivalents, liabilities=liabilities))
                        session.commit()
                        print('Company created successfully!')
                        break
                    except ValueError:
                        print('You input a value with the wrong format')
                        break

                elif crud_menu == 2:
                    search_name = input("Enter company name:\n")
                    counter = 0
                    search_query = query_c.filter(Company.name.like(f"%{search_name}%"))
                    comp_fnd = [comp for comp in search_query]

                    if len(comp_fnd) == 0:
                        print("Company not found!")
                        break
                    else:
                        for row in search_query:
                            print(counter,  row.name)
                            counter += 1

                        comp_num = int(input("Enter company number:\n"))
                        if 0 <= comp_num <= len(comp_fnd):
                            finance_query = query_f.filter(Finance.ticker == comp_fnd[comp_num].ticker)
                            item = finance_query[0]

                            try:
                                PE = round(item.market_price / item.net_profit, 2)
                            except TypeError:
                                PE = None
                            try:
                                PS = round(item.market_price / item.sales, 2)
                            except TypeError:
                                PS = None
                            try:
                                PB = round(item.market_price / item.assets, 2)
                            except TypeError:
                                PB = None
                            try:
                                ND_EBITDA = round(item.net_debt / item.ebitda, 2)
                            except TypeError:
                                ND_EBITDA = None
                            try:
                                ROE = round(item.net_profit / item.equity, 2)
                            except TypeError:
                                ROE = None
                            try:
                                ROA = round(item.net_profit / item.assets, 2)
                            except TypeError:
                                ROA = None
                            try:
                                LA = round(item.liabilities / item.assets, 2)
                            except TypeError:
                                LA = None

                            print(f"{item.ticker} {comp_fnd[comp_num].name}\n"
                                  f"P/E = {PE}\n"
                                  f"P/S = {PS}\n"
                                  f"P/B = {PB}\n"
                                  f"ND/EBITDA = {ND_EBITDA}\n"
                                  f"ROE = {ROE}\n"
                                  f"ROA = {ROA}\n"
                                  f"L/A = {LA}\n")
                            break

                        else:
                            print("The number is invalid from the listed companies!")
                            break

                elif crud_menu == 3:
                    search_name = input("Enter company name:\n")
                    counter = 0
                    search_query = query_c.filter(Company.name.like(f"%{search_name}%"))
                    comp_fnd = [comp for comp in search_query]

                    if len(comp_fnd) == 0:
                        print("Company not found!")
                        break
                    else:
                        for row in search_query:
                            print(counter, row.name)
                            counter += 1

                        comp_num = int(input("Enter company number:\n"))
                        if 0 <= comp_num <= len(comp_fnd):
                            ebitda = input("Enter ebitda (in the format '987654321'):\n")
                            sales = input("Enter sales (in the format '987654321'):\n")
                            net_profit = input("Enter net profit (in the format '987654321'):\n")
                            market_price = input("Enter market price (in the format '987654321'):\n")
                            net_debt = input("Enter net debt (in the format '987654321'):\n")
                            assets = input("Enter assets (in the format '987654321'):\n")
                            equity = input("Enter equity (in the format '987654321'):\n")
                            cash_equivalents = input("Enter cash equivalents (in the format '987654321'):\n")
                            liabilities = input("Enter liabilities (in the format '987654321'):\n")

                            finance_query = query_f.filter(Finance.ticker == comp_fnd[comp_num].ticker)
                            finance_query.update({
                                "ebitda":  ebitda,
                                "sales": sales,
                                "net_profit": net_profit,
                                "market_price": market_price,
                                "net_debt": net_debt,
                                "assets": assets,
                                "equity": equity,
                                "cash_equivalents": cash_equivalents,
                                "liabilities": liabilities
                            })
                            session.commit()
                            print("Company updated successfully!")
                            break

                elif crud_menu == 4:
                    search_name = input("Enter company name:\n")
                    counter = 0
                    search_query = query_c.filter(Company.name.like(f"%{search_name}%"))
                    comp_fnd = [comp for comp in search_query]

                    if len(comp_fnd) == 0:
                        print("Company not found!")
                        break
                    else:
                        for row in search_query:
                            print(counter, row.name)
                            counter += 1

                        comp_num = int(input("Enter company number:\n"))
                        if 0 <= comp_num <= len(comp_fnd):
                            query_f.filter(Finance.ticker == comp_fnd[comp_num].ticker).delete()
                            query_c.filter(Company.ticker == comp_fnd[comp_num].ticker).delete()
                            session.commit()
                            print("Company deleted successfully!")
                            break

                elif crud_menu == 5:
                    list_query = query_c.order_by(asc(Company.ticker))
                    print("COMPANY LIST")
                    for companies in list_query:
                        print(companies.ticker, companies.name, companies.sector)
                    break

                else:
                    print('Invalid option!\n')

        elif main_menu == 2:
            top_ten_menu = 1
            while top_ten_menu in (0, 1, 2, 3):
                top_ten_menu = int(input("TOP TEN MENU\n"
                                         "0 Back\n"
                                         "1 List by ND/EBITDA\n"
                                         "2 List by ROE\n"
                                         "3 List by ROA\n"
                                         "\nEnter an option:\n"))
                if top_ten_menu == 0:
                    break

                elif top_ten_menu == 1:
                    NDE_dict = {}
                    for NDE in query_f.all():
                        try:
                            NDE_dict[NDE.ticker] = round(NDE.net_debt / NDE.ebitda, 2)
                        except TypeError:
                            continue

                    sorted_NDE_dict = sorted(NDE_dict.items(), key=lambda x: -x[1])
                    print("TICKER ND/EBITDA")
                    for i in range(10):
                        print(sorted_NDE_dict[i][0], sorted_NDE_dict[i][1])
                    print("")
                    break

                elif top_ten_menu == 2:
                    ROE_dict = {}
                    for ROE in query_f.all():
                        try:
                            ROE_dict[ROE.ticker] = round(ROE.net_profit / ROE.equity, 2)
                        except TypeError:
                            continue

                    sorted_ROE_dict = sorted(ROE_dict.items(), key=lambda x: -x[1])
                    print("TICKER ROE")
                    for i in range(10):
                        print(sorted_ROE_dict[i][0], sorted_ROE_dict[i][1])
                    print("")
                    break

                elif top_ten_menu == 3:
                    ROA_dict = {}
                    for ROA in query_f.all():
                        try:
                            ROA_dict[ROA.ticker] = round(ROA.net_profit / ROA.assets, 2)
                        except TypeError:
                            continue

                    sorted_ROA_dict = sorted(ROA_dict.items(), key=lambda x: -x[1])
                    print("TICKER ROA")
                    for i in range(10):
                        print(sorted_ROA_dict[i][0], sorted_ROA_dict[i][1])
                    print("")
                    break

                else:
                    print('Invalid option!\n')

        else:
            print('Invalid option!\n')

    except ValueError:
        print('Invalid option!\n')