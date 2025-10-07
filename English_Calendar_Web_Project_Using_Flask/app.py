from flask import Flask, render_template, request
import calendar

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    cal_output = None
    year = month = None

    if request.method == 'POST':
        year = int(request.form['year'])
        month = int(request.form['month'])
        cal_output = calendar.month(year, month)

    return render_template('index.html', cal_output=cal_output, year=year, month=month)

if __name__ == '__main__':
    app.run(debug=True)
