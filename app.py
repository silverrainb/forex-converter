from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from forex_python.converter import CurrencyRates, CurrencyCodes
import requests
import json
import datetime

REQUESTS = requests.get('https://openexchangerates.org/api/currencies.json')

app = Flask(__name__)
app.config['SECRET_KEY'] = "thisismyfirstforexconverterapp"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def home():
    return redirect('/convert')


@app.route("/convert")
def convert_result():
    currencies = json.loads(REQUESTS.text)
    codes = currencies.keys()
    names = currencies.values()
    currentDT = datetime.datetime.now()
    return render_template("convert.html", currencies=currencies,
                           codes=codes, names=names, currentDT=currentDT)


@app.route("/convert/new", methods=['POST'])
def convert():
    amount = request.form["amount"]
    to = request.form["to"]
    from_code = request.form["from-code"]

    c = CurrencyRates()
    converted = c.convert(from_code, to, float(amount))

    symbol = CurrencyCodes()
    to_symbol = symbol.get_symbol(to)

    flash(
        f"{amount} {from_code} equals {to_symbol}{round(converted, 2)}({to})",
        'success')
    return redirect('/convert')

# @app.route('/movies/new', methods=["POST"])
# def add_movie():
#     title = request.form['title']
#     # add to Pretend DB
#     if title in MOVIES:
#         flash('MOVIE ALREADY EXIST', 'error')
#     else:
#         MOVIES.add(title)
#         flash("Added Movie Successfully", 'success')
#     return redirect('/movies')
