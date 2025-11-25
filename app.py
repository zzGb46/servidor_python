from flask import Flask, request, render_template

app = Flask(__name__)


# definindo uma rota básica que responde a requisições GET
@app.route("/")
def root():
    return 'ola mundo'


@app.route('/submit', methods= ['GET', 'POST'])
def submit():
    if request.method == 'POST':
    #  pega os dados do formulario via POST
     data = request.form['name']
     return f'Voce enviou:{data}'
    return '''
    <form method="POST">
    Nome: <input type="text" name= "name">
    <input type="submit" value="enviar"> 
    </form>
    '''
# INTERAGINDO COM OS DADOS PELA PRÓPRIA LINHA DE COMANDO
# import requests 
# response =requests.post('http://localhost:5152/submit', data = {'name':'Programador Aventureiro'})
# print(response.text)


@app.route('/template')
def template():
   return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5152)