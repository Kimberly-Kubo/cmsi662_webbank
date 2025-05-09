import os
from flask import Flask, request, make_response, redirect, render_template, g, abort, flash
from flask_wtf.csrf import CSRFProtect
from user_service import get_user_with_credentials, logged_in, login_required
from account_service import get_balance, do_transfer, get_accounts_for_email

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

csrf = CSRFProtect(app)

# Template system handles XSS by excaping user input and calling functions
# to safely render HTML.


@app.route("/", methods=['GET'])
def home():
    if not logged_in():
        return render_template("login.html")
    return redirect('/dashboard')


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = get_user_with_credentials(email, password)
    if not user:
        return render_template("login.html", error="Invalid credentials")
    response = make_response(redirect("/dashboard"))
    response.set_cookie("auth_token", user["token"])
    return response, 303


@app.route("/logout", methods=['GET'])
def logout():
    response = make_response(redirect("/dashboard"))
    response.delete_cookie('auth_token')
    return response, 303


@app.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    accounts = get_accounts_for_email(g.user)
    return render_template("dashboard.html", email=g.user, accounts=accounts)


@app.route("/details", methods=['GET'])
@login_required
def details():
    account_number = request.args['account']

    # Get all accounts for the user to check ownership
    accounts = get_accounts_for_email(g.user)
    account_ids = [str(account['id']) for account in accounts]

    # Check if the requested account belongs to the user. If not, redirect to dashboard
    # and show an error message that does not reveal the existence of the account.
    if account_number not in account_ids:
        flash("You don't have permission to access this account", "error")
        return redirect('/dashboard')

    return render_template(
        "details.html",
        user=g.user,
        account_number=account_number,
        balance=get_balance(account_number, g.user))


@app.route("/transfer", methods=["GET"])
@login_required
def show_transfer_form():
    return render_template("transfer.html")


@app.route("/transfer", methods=["POST"])
@login_required
def transfer():
    source = request.form.get("from")
    target = request.form.get("to")
    amount = int(request.form.get("amount"))

    # A series of checks to validate the transfer request
    # Valid transfers are from the user's own accounts to any other account
    # owned by the user or to any other account in the system.
    if amount < 0:
        flash("You can't transfer negative LEGO bricks", "error")
        return redirect("/dashboard")
    if amount > 1000:
        flash("You can't transfer more than 1000 LEGO bricks at once", "error")
        return redirect("/dashboard")

    available_balance = get_balance(source, g.user)
    if available_balance is None:
        flash("Account #{} not found".format(source), "error")
        return redirect("/dashboard")
    if amount > available_balance:
        flash("You don't have enough LEGO bricks", "error")
        return redirect("/dashboard")
    if do_transfer(source, target, amount):
        flash("Transfer successful", "success")
    else:
        flash("Something bad happened", "error")
        return redirect("/dashboard")

    response = make_response(redirect("/dashboard"))
    return response, 303
