import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_id = session["user_id"]

    # Query to retrieve stocks the user owns
    stocks = db.execute("""
        SELECT symbol, SUM(shares) AS total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, user_id)

    stock_data = []

    # Calculate total value of stocks
    total_value_of_stocks = 0

    # Look up current price for each stock and calculate total value
    for stock in stocks:
        stock_info = lookup(stock["symbol"])
        if stock_info:
            current_price = stock_info["price"]
            total_shares = stock["total_shares"]
            total_stock_value = total_shares * current_price
            total_value_of_stocks += total_stock_value
            stock_data.append({
                "symbol": stock["symbol"],
                "shares": total_shares,
                "price": usd(current_price),
                "total": usd(total_stock_value)
            })

    # Query to get user's current cash balance
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # Calculate grand total (cash + value of all stocks)
    grand_total = user_cash + total_value_of_stocks

    return render_template("index.html", stocks=stock_data, cash=usd(user_cash), total=usd(grand_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        # Ensure symbol is provided
        if not symbol:
            return apology("Missing symbol", 400)

        # Ensure shares are provided and a positive integer
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Invalid number of shares", 400)

        # Lookup stock price
        stock = lookup(symbol)
        if stock is None:
            return apology("Invalid symbol", 400)

        # Calculate total cost
        shares = int(shares)
        price_per_share = stock["price"]
        total_cost = shares * price_per_share

        user_id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        if total_cost > user_cash:
            return apology("Can't afford", 400)

        # Update user's cash and record transaction in transactions table
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id)

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, symbol, shares, price_per_share)

        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_id = session["user_id"]

    transactions = db.execute("""
        SELECT symbol, shares, price, timestamp as transacted
        FROM transactions
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, user_id)

    # Render the history page with transactions
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol")

        # Check if symbol is provided
        if not symbol:
            return apology("missing symbol", 400)

        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", stock=stock)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Get form inputs
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if username and password is provided
        if not username:
            return apology("missing username", 400)

        if not password:
            return apology("missing password", 400)

        # Check if password and confirmation are match
        elif password != confirmation:
            return apology("passwords don't match", 400)

        hash = generate_password_hash(password)

        try:
            new_user_id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username, hash
            )
        except ValueError:
            return apology("username already exists", 400)

        # Log in the new user automatically
        session["user_id"] = new_user_id

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure symbol was selected
        if not symbol:
            return apology("missing symbol", 400)

        if not shares:
            return apology("missing shares", 400)

        # Ensure shares are a positive integer
        if not shares.isdigit() or int(shares) <= 0:
            return apology("invalid shares", 400)

        shares = int(shares)

        # Check if user owns the stock and has enough shares
        stock = db.execute(
            "SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)
        if len(stock) != 1 or stock[0]["total_shares"] <= 0:
            return apology("symbol not owned", 400)

        user_shares = stock[0]["total_shares"]
        if shares > user_shares:
            return apology("too many shares", 400)

        # Lookup current price of the stock
        stock_info = lookup(symbol)
        if not stock_info:
            return apology("invalid symbol", 400)

        price_per_share = stock_info["price"]
        total_value = shares * price_per_share

        # Update user's cash and Record the sale in transactions (negative shares indicate a sale)
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_value, user_id)

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, symbol, -shares, price_per_share)

        # Redirect to home page
        return redirect("/")

    else:
        # Fetch the stocks the user owns for the select menu
        stocks = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)
        return render_template("sell.html", stocks=stocks)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change password"""

    user_id = session["user_id"]

    if request.method == "POST":
        # Get the form data
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not current_password:
            return apology("missing current password", 400)

        if not new_password:
            return apology("missing new password", 400)

        if new_password != confirm_password:
            return apology("passwords don't match", 400)

        user_data = db.execute("SELECT hash FROM users WHERE id = ?", user_id)
        if len(user_data) != 1:
            return apology("user not found", 404)

        # Check if the current password is correct
        if not check_password_hash(user_data[0]["hash"], current_password):
            return apology("current password incorrect", 400)

        new_password_hash = generate_password_hash(new_password)

        # Update the password in the database
        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_password_hash, user_id)

        # Flash a success message
        flash("Password updated successfully")

        # Redirect to the home page
        return redirect("/")

    # If method is GET, render the change_password form
    return render_template("change_password.html")


@app.route("/trade", methods=["POST"])
@login_required
def trade():
    """Buy or Sell shares of stock based on user action."""

    action = request.form.get("action")
    symbol = request.form.get("symbol").upper()
    shares = request.form.get("shares")

    # Ensure symbol is provided
    if not symbol:
        return apology("Missing symbol", 400)

    # Ensure shares are provided and a positive integer
    if not shares or not shares.isdigit() or int(shares) <= 0:
        return apology("Invalid number of shares", 400)

    # Lookup stock price
    stock = lookup(symbol)
    if stock is None:
        return apology("Invalid symbol", 400)

    shares = int(shares)
    price_per_share = stock["price"]

    user_id = session["user_id"]

    # Handle "buy" action
    if action == "buy":
        total_cost = shares * price_per_share

        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        if total_cost > user_cash:
            return apology("Can't afford", 400)

        # Update user's cash balance and record transaction
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, symbol, shares, price_per_share)

    # Handle "sell" action
    elif action == "sell":
        # Query user's current stock holdings
        stock_owned = db.execute(
            "SELECT SUM(shares) AS total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)

        if len(stock_owned) != 1 or stock_owned[0]["total_shares"] <= 0:
            return apology("You don't own this stock", 400)

        total_shares_owned = stock_owned[0]["total_shares"]

        if shares > total_shares_owned:
            return apology("Not enough shares", 400)

        total_sale_value = shares * price_per_share

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_sale_value, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, symbol, -shares, price_per_share)

    return redirect("/")
