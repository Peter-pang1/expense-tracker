from flask import Flask, render_template, request, redirect, url_for, session
from services.database import init_db
from services.expense_service import add_expense, get_expenses, get_expenses_by_date
from services.report_service import get_summary_by_category, get_summary_by_month
from services.user_service import register_user, get_user

app = Flask(__name__)
app.secret_key = "my_secret_key"  # คีย์สำหรับ session

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    category_summary = get_summary_by_category(user_id)
    month_summary = get_summary_by_month(user_id)
    expenses = get_expenses(user_id)
    return render_template("index.html",
                           category_summary=category_summary,
                           month_summary=month_summary,
                           expenses=expenses)

@app.route("/add", methods=["GET", "POST"])
def add():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        add_expense(session["user_id"],
                    float(request.form["amount"]),
                    request.form["category"],
                    request.form["date"],
                    request.form["note"])
        return redirect(url_for("index"))
    return render_template("add_expense.html")

@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    user_id = session["user_id"]

    if start_date and end_date:
        expenses = get_expenses_by_date(user_id, start_date, end_date)
    else:
        expenses = get_expenses(user_id)

    return render_template("history.html", expenses=expenses,
                           start_date=start_date, end_date=end_date)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = get_user(request.form["username"], request.form["password"])
        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect(url_for("index"))
        return render_template("login.html", error="ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            register_user(request.form["username"], request.form["password"])
            return redirect(url_for("login"))
        except:
            return render_template("register.html", error="มีผู้ใช้นี้อยู่แล้ว")
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)