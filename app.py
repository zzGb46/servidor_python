from conexao import get_connection
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc123'

class RegisterForm(FlaskForm):
    nome = StringField('primeiro nome', validators=[DataRequired()])
    idade = StringField('idade', validators=[DataRequired()])
    telefone = StringField('telefone', validators=[DataRequired()])
    submit = SubmitField('CADASTRAR')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        nome = form.nome.data
        idade = form.idade.data
        telefone = form.telefone.data

        con = get_connection()
        cursor = con.cursor()

        sql = "INSERT INTO tb_cliente (nome, idade, telefone) VALUES (%s, %s, %s)"
        valores = (nome, idade, telefone)

        cursor.execute(sql, valores)
        con.commit()

        cursor.close()
        con.close()

        return "Usuário cadastrado com sucesso!"

    return render_template('register.html', form=form)




    
    
   

# @app.route('/exemplo')
# def exemplo():
#    session['nome'] = 'gabriel'
#    return f'o usuario é {session['nome']}'

# # definindo uma rota básica que responde a requisições GET
# @app.route("/")
# def root():
#     return 'ola mundo'


# @app.route('/submit', methods= ['GET', 'POST'])
# def submit():
#     if request.method == 'POST':
#     #  pega os dados do formulario via POST
#      data = request.form['name']
#      return f'Voce enviou:{data}'
#     return '''
#     <form method="POST">
#     Nome: <input type="text" name= "name">
#     <input type="submit" value="enviar"> 
#     </form>
#     '''
# # INTERAGINDO COM OS DADOS PELA PRÓPRIA LINHA DE COMANDO
# # import requests 
# # response =requests.post('http://localhost:5152/submit', data = {'name':'Programador Aventureiro'})
# # print(response.text)


# @app.route('/template')
# def template():
#    return render_template('index.html',  name= 'gabriel')


if __name__ == '__main__':
    app.run(debug=True, port=5152)