import csv
import pandas as pd
import datetime
from flask import Flask,render_template,url_for,request,redirect


app = Flask(__name__)
# import matplotlib.pyplot as plt


# Define the filename
filename = "expenses2.csv"

# Allowed categories and modes
ALLOWED_CATEGORIES = ["Shopping", "Groceries", "Travel", "Education", "Utilities", "Entertainment"]
ALLOWED_MODES = ["Online", "Offline"]

def validate_amount(amount):
    #amount needs to be positive
    amount = float(amount)
    if amount <=0:
        return False,"enter a positive amount"
    return True,amount

def validate_category(category):
    if category not in ALLOWED_CATEGORIES:
        return False,"invalid category chosen"
    return True,category

def validate_mode(mode):
    if mode not in ALLOWED_MODES:
        return False,"invalid mode chosen"
    return True,mode

with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    
    # Writing the header row
    writer.writerow(["Date", "Category", "Amount","Mode"])


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def add_new_data():
    #take user input and add an expense
    # ID = input("enter the payment id: ")#doubt
    # date = datetime.datetime.now().strftime("%d-%m-%Y")
    category = request.form.get("category")
    amount = request.form.get("amount")
    mode = request.form.get("mode")
    date = datetime.datetime.now().strftime("%d-%m-%Y")

    _, vamount=validate_amount(amount)
    _, vcategory=validate_category(category)
    _, vmode=validate_mode(mode)
    new_entery = [date,vcategory,vamount,vmode]
    with open(filename,mode="a",newline="") as file:
        writer = csv.writer(file)
        writer.writerow(new_entery)

    print(vcategory)
    print(vamount)
    print(vmode)
    print(date)
    
    


    return render_template("index.html")

@app.route("/update", methods=["GET"])
def update_form():
    return render_template("update.html")

@app.route("/update", methods=["POST"])
def update_expense():
    date = request.form.get("date")
    amount = request.form.get("amount")
    mode = request.form.get("mode")
    category = request.form.get("category")

    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        return "Error: expenses.csv not found.", 500

    # Validate inputs
    valid_amt, vamt = validate_amount(amount) if amount else (True, None)
    valid_cat, vcat = validate_category(category) if category else (True, None)
    valid_mode, vmode = validate_mode(mode) if mode else (True, None)

    if not (valid_amt and valid_cat and valid_mode):
        return "Invalid input", 400

    # Update only if the date exists and inputs are provided
    if date in df["Date"].values:
        if amount:
            df.loc[df["Date"] == date, "Amount"] = vamt
        if mode:
            df.loc[df["Date"] == date, "Mode"] = vmode
        if category:
            df.loc[df["Date"] == date, "Category"] = vcat

        # Save changes
        df.to_csv(filename, index=False)
        return "Record updated successfully!", 200
    else:
        return "No record found for the given date.", 404


if __name__ == "__main__":
    app.run(debug=True)

