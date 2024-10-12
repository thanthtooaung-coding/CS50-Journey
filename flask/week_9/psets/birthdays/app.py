import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        birthday_id = request.form.get("id")

        # Validate the form inputs
        if not name or not month or not day:
            return redirect("/")

        try:
            month = int(month)
            day = int(day)
        except ValueError:
            return redirect("/")

        if month < 1 or month > 12 or day < 1 or day > 31:
            return redirect("/")

        # If birthday ID exists, update the existing birthday entry
        if birthday_id:
            db.execute("UPDATE birthdays SET name = ?, month = ?, day = ? WHERE id = ?",
                       name, month, day, birthday_id)
        else:
            # Insert new birthday into the database
            db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays")

        editing = False
        birthday = None
        # Render the index.html template with the birthdays data
        return render_template("index.html", birthdays=birthdays, editing=editing, birthday=birthday)


@app.route("/edit/<int:id>", methods=["GET"])
def edit(id):
    # Fetch the birthday data to edit
    birthday = db.execute("SELECT * FROM birthdays WHERE id = ?", id)
    if len(birthday) != 1:
        return redirect("/")

    birthdays = db.execute("SELECT * FROM birthdays")
    return render_template("index.html", birthdays=birthdays, editing=True, birthday=birthday[0])


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    db.execute("DELETE FROM birthdays WHERE id = ?", id)
    return redirect("/")
