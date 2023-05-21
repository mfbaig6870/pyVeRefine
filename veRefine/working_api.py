from flask import Flask, request
import subprocess
import sys
import flask

app = Flask(__name__)


@app.route('/my-endpoint', methods=['POST'])
def my_endpoint():
    # Extract data from the request
    # data = request.get_json()

    # Pass the data as arguments to the script
    # args = ['python', 'a_logTransientThrottleFilter.py', str(data)]
    args = ['python', 'a_logTransientThrottleFilter.py']

    # Execute the script and capture the output
    try:
        output = subprocess.check_output(args, stderr=subprocess.STDOUT, timeout=10)
    except subprocess.CalledProcessError as e:
        output = e.output
    except subprocess.TimeoutExpired as e:
        output = "The script took too long to execute."
    except Exception as e:
        output = str(e)

    # Add environment information to the output
    python_version = sys.version.split()[0]
    flask_version = flask.__version__
    werkzeug_version = request.environ.get('werkzeug.version')
    virtual_env = sys.prefix
    output_str = output.decode('utf-8')
    output_with_env = "{}\n\nEnvironment:\nVirtual Env: {}\nPython {}\nFlask {}\nWerkzeug {}".format(output_str,
                                                                                                     virtual_env,
                                                                                                     python_version,
                                                                                                     flask_version,
                                                                                                     werkzeug_version)

    # Return the output as JSON
    return {'output': output_with_env}


if __name__ == '__main__':
    app.run(debug=True)
