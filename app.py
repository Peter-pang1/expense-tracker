from flask import Flask, render_template, request, redirect, url_for
from services.database import init_db
from services.expense_service import add_expense, get_expenses, get_expenses_by_date
from services.report_service import get_summary_by_category, get_summary_by_month

app = Flask(__name__)

@app.route("/")
def index():
    category_summary = get_summary_by_category()
    month_summary = get_summary_by_month()
    expenses = get_expenses()
    return render_template("index.html",
                           category_summary=category_summary,
                           month_summary=month_summary,
                           expenses=expenses)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            category = request.form["category"]
            date = request.form["date"]
            note = request.form["note"]
            add_expense(amount, category, date, note)
        except Exception as e:
            print("Error adding expense:", e)
        return redirect(url_for("index"))
    return render_template("add_expense.html")

@app.route("/history")
def history():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if start_date and end_date:
        expenses = get_expenses_by_date(start_date, end_date)
    else:
        expenses = get_expenses()

    return render_template("history.html", 
                           expenses=expenses, 
                           start_date=start_date, 
                           end_date=end_date)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)