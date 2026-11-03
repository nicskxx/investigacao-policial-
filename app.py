from email import message

from flask import Flask, request, jsonify, render_template, redirect, url_for
from psycopg2.extras import RealDictCursor

from database import criar_conexao

app = Flask(__name__)

@app.route('/inve', methods=['GET'])
def mostrar_ivestigadores():
    conn = criar_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM investigadores")
    resultado = cursor.fetchall()

    conn.close()
    return jsonify(resultado), 200


@app.route('/inve-s', methods=['POST'])
def cadastrar_suspeito():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    print(f"Novo suspeito: {dados}")

    conn = criar_conexao()
    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO suspeitos(nome, data_nascimento, cpf, endereco, caso_id) 
        VALUES(%s, %s, %s, %s, %s)
        RETURNING id;
        ''',
        (dados['nome'], dados['data_nascimento'], dados['cpf'],
         dados['endereco'], dados['caso_id'])
    )

    novo_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    return jsonify({
        'message': 'Suspeito cadastrado com sucesso!',
        'id': novo_id,
        'suspeito': dados
    }), 201

from flask import render_template

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/novo-suspeito', methods=['GET'])
def pagina_cadastrar_suspeito():
    return render_template('cadastrar_suspeito.html')

@app.route('/cadastrar-suspeito', methods=['POST'])
def salvar_suspeito():

    nome = request.form['nome']
    data_nascimento = request.form['data_nascimento']
    cpf = request.form['cpf']
    endereco = request.form['endereco']
    caso_id = request.form['caso_id']

    conn = criar_conexao()
    cursor = conn.cursor()

    try:
        cursor.execute(
            '''
            INSERT INTO suspeitos (nome, data_nascimento, cpf, endereco, caso_id) 
            VALUES (%s, %s, %s, %s, %s)
            ''',
            (nome, data_nascimento, cpf, endereco, caso_id)
        )
        conn.commit()
    except Exception as e:
        print(f"Erro ao cadastrar: {e}")
    finally:
        conn.close()
    return redirect(url_for('home'))


@app.route('/suspeitos')
def mostrar_suspeitos():
    conn = criar_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM suspeitos")
    lista_suspeitos = cursor.fetchall()

    conn.close()

    # Envia os dados do banco para o arquivo HTML que acabamos de criar
    return render_template('mostrar_suspeitos.html', suspeitos=lista_suspeitos)


@app.route('/casos')
def mostrar_casos():
    conn = criar_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM casos")
    lista_casos = cursor.fetchall()

    conn.close()

    return render_template('mostrar_casos.html', casos=lista_casos)


@app.route('/investigadores')
def mostrar_investigadores():
    conn = criar_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM investigadores")
    lista_investigadores = cursor.fetchall()

    conn.close()

    return render_template('mostrar_investigadores.html', investigadores=lista_investigadores)






if __name__ == '__main__':
    app.run(debug=True)


