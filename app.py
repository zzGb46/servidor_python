from flask import Flask, request, render_template, session

from flask_wtf import FlaskForm
# wtforms é o motor principal quando se cria formularios com Flask
from wtforms import  StringField, PasswordField, SubmitField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'abc123'

class RegisterForm(FlaskForm):
   first_name= StringField('primeiro nome')
   last_name = StringField('Sobrenome')
   email = StringField('E-mail')
   password = PasswordField('Senha')
   confirm =  PasswordField('Confirme a senha')
   submit = SubmitField('CADASTRAR')

@app.route('/register')
def register():
    form = RegisterForm()
    return render_template('register.html', form= form)
   

@app.route('/exemplo')
def exemplo():
   session['nome'] = 'gabriel'
   return f'o usuario é {session['nome']}'

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
   return render_template('index.html',  name= 'gabriel')


if __name__ == '__main__':
    app.run(debug=True, port=5152)