from flask import Flask  

app = Flask(__name__)


# definindo uma rota básica que responde a requisições GET
@app.route("/")
def root():
    return 'ola mundo'

if __name__ == '__main__':
    app.run(debug=True, port=5152)