import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    # get symbols of stocks bought by user.
    stock_symbols = db.execute("SELECT symbol, name, shares, price, total FROM portfolio WHERE id = :id", \
                               id=session["user_id"])

    total_cash = 0

    for stock_symbol in stock_symbols:
        symbol = stock_symbol["symbol"]
        name = stock_symbol["name"]
        shares = stock_symbol["shares"]
        stock = lookup(symbol)
        price = stock["price"]
        total = stock["price"] * shares
        total_cash += total
        db.execute("UPDATE portfolio set price = :price, \
                   total = :total WHERE id = :id and symbol = :symbol", \
                   price = usd(stock["price"]), total = usd(total), \
                   id = session["user_id"], symbol = symbol)

    # update cash.
    updated_cash = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])

    # update total cash.
    total_cash += updated_cash[0]["cash"]

    # Bring portfolio into the home page.
    updated_portfolio = db.execute("SELECT symbol, name, shares, price, total from portfolio \
                                   WHERE id = :id", name = stock["name"], symbol = stock["symbol"], \
                                   shares = shares, price = usd(stock["price"]), total = total, id = session["user_id"])

    return render_template("index.html", stocks = updated_portfolio, cash = usd(updated_cash[0]['cash']), total = usd(total_cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid symbol")

        try:
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("Shares must be a positive integer")

        except:
            return apology ("Enter Input")

        #select user's cash
        cashOnHand = db.execute("SELECT cash FROM users WHERE id = :id", \
                           id = session["user_id"])
        cashOnHand = int(cashOnHand[0]["cash"])

        total = usd(shares * stock["price"])

        if total > cashOnHand:
            return ("You're broke")


        # update cash
        db.execute("UPDATE users SET cash = cash -:total_price WHERE id=:user_id;", \
                   total_price = shares * stock['price'], \
                   user_id = session["user_id"])


        #insert the stock into the portfolio database
        db.execute("INSERT INTO portfolio (name, symbol, shares, price, total, id) \
                   VALUES (:name, :symbol, :shares, :price, :total, :id)", \
                   name = stock["name"], symbol = stock["symbol"], shares = shares, \
                   price = usd(stock["price"]), total = total, id = session["user_id"])

        #update portfolio
        db.execute("UPDATE portfolio SET shares = :shares \
                   WHERE id = :id AND symbol = :symbol", \
                   shares = shares, symbol = stock["symbol"], id = session["user_id"])

        # Insert into history database
        db.execute("INSERT INTO history (symbol, shares, price, id) \
                   VALUES (:symbol, :shares, :price, :id)", \
                   symbol = stock["symbol"], shares = shares, \
                   price = usd(stock["price"]), id = session["user_id"])


        # select user shares of that symbol
        user_shares = db.execute("SELECT shares FROM portfolio WHERE id = :id AND symbol = :symbol",
                                 id = session["user_id"], symbol = stock["symbol"])

        return redirect("/")

@app.route("/history")
@login_required
def history():
    """Show history of portfolio."""
    histories = db.execute("SELECT symbol, shares, price, transacted FROM history WHERE id=:id", id=session["user_id"])

    return render_template("history.html", histories=histories)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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
    return redirect("login.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("Stock not found :(")
        else:
            quote['price'] = usd(quote['price'])
            return render_template("quote.html", quote = quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # if the user reached the route via POST
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")

        # ensure password was submitted
        if not request.form.get("password"):
            return apology("Must provide password")

        # ensure password confirmation was submitted
        if not request.form.get("confirmation"):
            return apology("Must provide password confirmation")

        # ensure passwords match
        if request.form.get("confirmation") != request.form.get("password"):
            return apology("Passwords dd not match")

        # adding user into the database
        result = db.execute("INSERT INTO users (username, hash) \
                            VALUES (:username, :hash)", \
                            username = request.form.get("username"), \
                            hash = generate_password_hash(request.form.get("password")))

        # username must be unique
        if not result:
            return apology("Username is already taken.")

        session["user_id"] = result

        # redirect the user to home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell a stock"""
    if request.method == "POST":
        # check if valid input
        try:
            stock = lookup(request.form.get("symbol"))
            shares = int(request.form.get("shares"))
        except:
            return apology("enter some input")

        # if symbol is empty return apology
        if not stock:
            return apology("enter a valid symbol")

        # if shares is empty
        if not shares or shares <= 0:
            return apology("enter the shares of shares")

        # is the stock in the portfolio?
        stocks_held = db.execute("SELECT SUM(shares) FROM portfolio WHERE id=:id AND symbol=:symbol;", \
        id=session['user_id'], symbol = stock['symbol'])
        if not stocks_held[0]['SUM(shares)'] :
            return apology("you don't own this stock")

        # is shares less or = to the stocks held?
        if shares > stocks_held[0]['SUM(shares)']:
            return apology("you don't own that many stocks")

        # enter a new transaction in portfolio
            # ensure a sale is a negative number
        db.execute("INSERT INTO portfolio (symbol, shares, price, id) VALUES (:symbol, :shares, :price, :id);", \
        symbol = stock['symbol'], shares=-shares, price = stock['price'], id=session["user_id"])

        # update cash
        db.execute("UPDATE users SET cash = cash + :total_price WHERE id = :user_id;", total_price = shares * stock['price'], \
        user_id=session["user_id"])

        #update history
        db.execute("INSERT INTO history (symbol, shares, price, transacted, id \
                   VALUES (:symbol, :shares, :price, :transacted, :id)", \
                   symbol = stock["symbol"], shares = shares, \
                   price = usd(stock["price"]), transacted = stock["transacted"], \
                   id = session["user_id"])

        return redirect("/")

    else:
        return render_template("sell.html")




def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
