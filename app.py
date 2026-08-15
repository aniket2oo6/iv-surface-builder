from flask import Flask, render_template, request, jsonify
from data_fetcher import get_option_chain
from iv_solver import add_iv_column
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods = ['POST'])
def analyze():
    ticker = request.form.get('ticker')

    if not ticker:
        return jsonify({'error': 'No ticker provided'}), 400

    try:
        x = get_option_chain(ticker)
        df_with_column = add_iv_column(x)

        pivot = df_with_column.pivot_table(index = 'T', columns = 'strike', values = 'iv')
        pivot = pivot.interpolate(axis = 1, limit_direction = 'both')
        pivot = pivot.astype(object).where(pd.notnull(pivot), None)

        x = pivot.columns.tolist()
        y = pivot.index.tolist()
        z = pivot.values.tolist()

        return jsonify({'x': x, 'y': y, 'z': z})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug = True)

