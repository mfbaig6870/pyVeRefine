from flask import Flask, render_template
import subprocess

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run_script')
def run_script():
    subprocess.run(['python', './veRefineViz/veTable3d.py'])
    return 'Script executed successfully!'


if __name__ == '__main__':
    app.run(debug=True)
