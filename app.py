import forex_python
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from forex_python.converter import CurrencyRates
import json
import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "thisismyfirstforexconverterapp"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

file_path = os.path.dirname(os.path.abspath(__file__))
with open(file_path + '/assets/currencies.json') as f:
    currency_data = json.loads(f.read())


@app.route("/")
def home():
    return redirect('/convert')


@app.route("/convert")
def convert_result():
    codes = [d['cc'] for d in currency_data]

    currentDT = datetime.datetime.now()
    return render_template("convert.html",
                           codes=codes, currentDT=currentDT)


@app.route("/convert/new", methods=['POST'])
def convert():
    try:
        # get data from form
        amount = request.form["amount"]
        to = request.form["to"]
        from_code = request.form["from-code"]

        # convert rates
        c = CurrencyRates()
        converted = c.convert(from_code, to, float(amount))

        # get currency name and symbol
        def get_name_symbol(code):
            return next((item for item in currency_data if item["cc"] == code),
                        None)

        from_name = get_name_symbol(from_code)['name']
        to_symb = get_name_symbol(to)['symbol']
        to_name = get_name_symbol(to)['name']

        # flash result message
        flash(
            f"{amount} {from_name} equals {to_symb}{round(converted, 2)} {to_name}",
            'success')
    except forex_python.converter.RatesNotAvailableError:
        flash(
            f"{from_code} to {to} conversion is currently not available.",
            'error')

    return redirect('/convert')

if __name__ == '__main__':
    app.run()