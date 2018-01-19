"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session
import jinja2

import melons

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")  # this notation IS passing melon_id
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print melon  # this prints TO THE TERMINAL. this could be scraped by server?
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    cart_list = []
    total_cost = 0.00

    if "cart" in session:
        cart_dict = session["cart"]
        for melon_id in cart_dict:
            melon = melons.get_by_id(melon_id)
            melon.quantity = cart_dict[melon_id]
            melon.total = melon.quantity * melon.price
            cart_list.append(melon)
            total_cost = total_cost + melon.total

    return render_template("cart.html", cart_list=cart_list, total_cost=total_cost)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    if "cart" not in session:
        session["cart"] = {}  # cart is the only session key so far. its value
                              # is a dictionary. In that dictionary, each melon-id
                              # that is added will be a key, its count as a value

    if melon_id not in session["cart"]:  # don't need .keys() because it will look through all the keys in the value!
        session["cart"][melon_id] = 1  # puts melon_id as a key to count of 1
    else:
        session["cart"][melon_id] += 1  # increments the count for that melon_id

    melon = melons.get_by_id(melon_id)
    flash(("{common_name} successfully added to cart!").format(
        common_name=melon.common_name))

    print session["cart"]
    return redirect("/cart")  # immediately goes to the view function path "/cart"


@app.route("/login", methods=["GET"])  # this route will only accept GET method requests
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    # The logic here should be something like:
    #
    # - get user-provided name and password from request.form
    # - use customers.get_by_email() to retrieve corresponding Customer
    #   object (if any)
    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    # - if they match, store the user's email in the session, flash a success
    #   message and redirect the user to the "/melons" route
    # - if they don't, flash a failure message and redirect back to "/login"
    # - do the same if a Customer with that email doesn't exist

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
