from flask import Flask, request, g, render_template, jsonify, make_response, redirect, request, url_for, abort, session, flash
import ast
import requests
app = Flask(__name__)


@app.route('/report', methods=['GET', 'POST'])
def index():
    return render_template('report_index.html')


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
