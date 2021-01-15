from flask import Flask

app = Flask(__name__)


@app.route("/metrics", methods=['GET'])
def get_file():
    try:
        with open("/home/app/mount/metrics", "r+") as f:
            data = f.read()
        return data, 200
    except FileNotFoundError:
        return '', 200
    except Exception as e:
        return str(e), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
