from django.shortcuts import render

# Create your views here.
import csv
import random
from datetime import datetime
import os


class AccountingSystem:
    """writing class"""

    def __init__(self, name_accno: str):
        """constructor"""
        

    def ledger(self, date, category, description, debit, credit, mode_of_payment):
        """function to add data to the ledger file"""
        file_name = self.current_path + "/ledger.csv"
        if not os.path.exists(file_name):
            with open(file_name, "w", encoding="utf8") as f:
                csv_writer = csv.writer(f)
                current_balance = 0
        else:
            with open(file_name, "r", encoding="utf8") as f:
                csv_reader = csv.DictReader(f)
                data = list(csv_reader)
                if f.tell() == 0:
                    current_balance = 0
                else:
                    latest_data = data[-1]
                    current_balance = latest_data["Balance"]
        if debit:
            current_balance = int(current_balance) - debit
        if credit:
            current_balance = int(current_balance) + credit

        data = {
            "Date": date,
            "Category": category,
            "Description": description,
            "Debit": debit,
            "Credit": credit,
            "Balance": current_balance,
            "Mode of Payment": mode_of_payment,
        }
        headers = list(data.keys())

        with open(file_name, "a", encoding="utf8", newline="\n") as f:
            csv_writer = csv.DictWriter(f, fieldnames=headers)
            if f.tell() == 0:
                csv_writer.writeheader()
            csv_writer.writerow(data)
        return current_balance

    def credit(self, date, amount, category, description, mode_of_payment):
        """function to add data of credited amount"""
        return self.ledger(date, category, description, 0, amount, mode_of_payment)

    def debit(self, date, amount, category, description, mode_of_payment):
        """function to add data of debited amount"""
        return self.ledger(date, category, description, amount, 0, mode_of_payment)

    def transaction(
        self, date, amount, category, description, mode_of_payment, credit=True
    ):
        """function to add credited or debited transaction"""
        if credit:
            return "Credited " + str(
                (self.ledger(date, category, description, 0, amount, mode_of_payment))
            )
        return "Debited " + str(
            (self.ledger(date, category, description, amount, 0, mode_of_payment))
        )

    def generate_category_report(self):
        """function to generate category report"""
        ledger_filename = self.current_path + "/ledger.csv"
        with open(ledger_filename, "r", encoding="utf8") as f:
            csv_reader = csv.DictReader(f)
            main_data = list(csv_reader)

        category_fieldnames = ["Date", "Category", "Debit", "Credit"]
        category_data = [
            {key: value for key, value in x.items() if key in category_fieldnames}
            for x in main_data
        ]
        category_filename = self.current_path + "/category.csv"
        with open(category_filename, "w", encoding="utf8", newline="\n") as f:
            category_writer = csv.DictWriter(f, fieldnames=category_fieldnames)
            category_writer.writeheader()
            category_writer.writerows(category_data)

    def generate_payment_report(
        self,
    ):
        """function to generate mode_of_payment report"""
        ledger_filename = self.current_path + "/ledger.csv"
        with open(ledger_filename, "r", encoding="utf8") as f:
            csv_reader = csv.DictReader(f)
            main_data = list(csv_reader)

        category_fieldnames = ["Date", "Debit", "Credit", "Mode of Payment"]
        category_data = [
            {key: value for key, value in x.items() if key in category_fieldnames}
            for x in main_data
        ]
        payment_filename = self.current_path + "/mode_of_payment.csv"
        with open(payment_filename, "w", encoding="utf8", newline="\n") as f:
            category_writer = csv.DictWriter(f, fieldnames=category_fieldnames)
            category_writer.writeheader()
            category_writer.writerows(category_data)

    def print_report(self):
        """function to print report"""
        ledger_filename = self.current_path + "/ledger.csv"
        with open(ledger_filename, "r", encoding="utf8") as f:
            csv_reader = csv.DictReader(f)
            data = list(csv_reader)
        header = [
            "Category",
            "Year",
            "Jan",
            "Feb",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "Sept",
            "Oct",
            "Nov",
            "Dec",
            "Total Debit",
            "Total Credit",
            "Final Balance",
        ]
        month_list = [
            "Jan",
            "Feb",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "Sept",
            "Oct",
            "Nov",
            "Dec",
        ]

        aggregate_data = {}
        for x in data:
            date_object = x["Date"]
            year = int(date_object[:4])
            if date_object[6] == "-":
                month = int(date_object[5:6])
            else:
                month = int(date_object[5:7])
            key = (x["Category"], year, month_list[month - 1])

            if key not in aggregate_data:
                aggregate_data[key] = {"Debit": [0] * 12, "Credit": [0] * 12}

            aggregate_data[key]["Debit"][month - 1] += float(x["Debit"])
            aggregate_data[key]["Credit"][month - 1] += float(x["Credit"])

        report_filename = self.current_path + "/report.csv"
        with open(report_filename, "w", encoding="utf8", newline="\n") as f:
            csv_writer = csv.DictWriter(f, fieldnames=header)
            csv_writer.writeheader()

            for key, value in aggregate_data.items():
                category, year, _ = key
                row_data = {"Category": category, "Year": year}

                for i, month in enumerate(month_list):
                    row_data[month] = value["Credit"][i] - value["Debit"][i]

                row_data["Total Debit"] = sum(value["Debit"])
                row_data["Total Credit"] = sum(value["Credit"])
                row_data["Final Balance"] = (
                    row_data["Total Credit"] - row_data["Total Debit"]
                )
                csv_writer.writerow(row_data)

        with open(report_filename, "r", encoding="utf8") as f:
            report_reader = csv.reader(f)
            for x in report_reader:
                print(x)

    def generate_txt(self):
        """function to generate text file of report generated"""
        report_filename = self.current_path + "/report.csv"
        text_filename = self.current_path + "/report.txt"
        self.print_report()
        with open(report_filename, "r", encoding="utf8") as f1, open(
            text_filename, "w", encoding="utf8"
        ) as f2:
            report_reader = csv.reader(f1)
            for x in report_reader:
                temp = ""
                print(x)
                for index, i in enumerate(x):
                    if index in range(1, 14):
                        temp += f"{i:10}"
                    else:
                        temp += f"{i:14}"
                temp += "\n"
                f2.write(temp)

    def generate_random_data(self, n):
        """function to generate random data"""
        current_year = datetime.now().year
        start_year = current_year - n - 1
        date_list = []
        date_list = [
            str(random.randint(start_year, current_year - 1))
            + "-"
            + str(random.randint(1, 12))
            + "-"
            + str(random.randint(1, 28))
            for i in range(100)
        ]

        date_list = sorted(date_list)
        categories = ["Food", "Rent", "Arcade", "Movies", "Travel", "Petrol", "EMI"]
        descriptions = ["Groceries", "Restaurant", "Internet", "Movie", "Flight"]
        modes_of_payment = [
            "Credit Card",
            "Debit Card",
            "Cash",
            "G-pay",
            "Paytm",
            "Amazon-pay",
            "Phone-pay",
        ]

        category_list = random.choices(categories, k=100)
        description_list = random.choices(descriptions, k=100)
        mode_of_payment_list = random.choices(modes_of_payment, k=100)
        print(category_list)
        debit_list, credit_list = [], []
        for i in range(100):
            debit_or_credit = random.randint(0, 2)
            if debit_or_credit:
                debit_list.append(0)
                credit_list.append(random.randint(500, 100000))
            else:
                debit_list.append(random.randint(500, 100000))
                credit_list.append(0)
            self.ledger(
                date_list[i],
                category_list[i],
                description_list[i],
                debit_list[i],
                credit_list[i],
                mode_of_payment_list[i],
            )


if __name__ == "__main__":
    gaurav = AccountingSystem("Gaurav007")
    gaurav.generate_random_data(10)
    # gaurav.generate_category_report()
    # gaurav.generate_payment_report()
    # gaurav.generate_txt()

    # akash = AccountingSystem('Akash197')
    # akash.generate_random_data(10)
    # akash.generate_category_report()
    # akash.generate_payment_report()
    # akash.generate_txt()
    gaurav.print_report()