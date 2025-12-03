from conexao import get_connection
from flask import Flask, render_template, request, redirect, url_for, flash
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

# ABAIXO MOSTRO A ROTA DE CADASTRO

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

        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for('register'))
        


    return render_template('register.html', form=form)




    
   #  ROTA PARA VER OS DADOS CADASTRADOS

@app.route("/listar")
def listar():
    con = get_connection()
    cursor = con.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tb_cliente")
    clientes = cursor.fetchall()

    # *** CÁLCULOS ***
    total = len(clientes)

    # idade média
    if total > 0:
        soma_idades = sum(int(c["idade"]) for c in clientes)
        idade_media = soma_idades / total
    else:
        idade_media = 0

    # mais novo
    if total > 0:
        mais_novo = min(clientes, key=lambda c: int(c["idade"]))
        mais_velho = max(clientes, key=lambda c: int(c["idade"]))
    else:
        mais_novo = None
        mais_velho = None

    cursor.close()
    con.close()

    return render_template(
        "tabela.html",
        clientes=clientes,
        total=total,
        idade_media=idade_media,
        mais_novo=mais_novo,
        mais_velho=mais_velho
    )


    # ABAIXO ROTA DE EXCLUSÃO DE ELEMENTOS DA LISTA


@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    con = get_connection()
    cursor = con.cursor()

    cursor.execute("DELETE FROM tb_cliente WHERE id_cliente = %s", (id,))
    con.commit()

    cursor.close()
    con.close()

    return redirect("/listar")


# BARRA DE PESQUISA
@app.route("/buscar")
def buscar():
    nome = request.args.get("nome")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tb_cliente WHERE nome LIKE %s", (f"%{nome}%",))
    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    # se quiser pode mostrar mensagem se não encontrar
    if not resultados:
        return render_template("tabela.html",
                               clientes=[],
                               mensagem="Nenhum paciente encontrado.",
                               total=0,
                               idade_media=0,
                               mais_novo=None,
                               mais_velho=None)

    # Agora as estatísticas
    idades = [r["idade"] for r in resultados]
    total = len(resultados)
    idade_media = sum(idades) / total

    mais_novo = min(resultados, key=lambda x: x["idade"])
    mais_velho = max(resultados, key=lambda x: x["idade"])

    return render_template("tabela.html",
                           clientes=resultados,
                           total=total,
                           idade_media=idade_media,
                           mais_novo=mais_novo,
                           mais_velho=mais_velho)
   

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
    app.run(debug=True, port=5151)