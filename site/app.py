from flask import Flask, render_template, url_for, request, redirect, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # This is how you can pass in information for the jinja liquid syntax
    # return render_template('index.html', tasks=tasks)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
