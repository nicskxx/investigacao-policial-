from email import message
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask import Flask, request, jsonify, render_template, redirect, url_for
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

from database import criar_conexao

app = Flask(__name__)


app.secret_key = 'uma_chave_super_secreta_e_unica_aqui'

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


@app.route('/novo-caso')
def pagina_registrar_caso():
    return render_template('registrar_caso.html')


@app.route('/registrar-caso', methods=['POST'])
def salvar_caso():

    titulo = request.form['titulo']
    tipo = request.form['tipo']
    data_abertura = request.form['data_abertura']
    local = request.form['local']
    descricao = request.form['descricao']
    status = request.form['status']

    conn = criar_conexao()
    cursor = conn.cursor()

    try:
        cursor.execute(
            '''
            INSERT INTO casos (
                titulo,
                tipo,
                data_abertura,
                local,
                descricao,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ''',
            (
                titulo,
                tipo,
                data_abertura,
                local,
                descricao,
                status
            )
        )

        conn.commit()

        print("Caso cadastrado com sucesso!")

    except Exception as e:
        conn.rollback()
        print(f"Erro ao cadastrar caso: {e}")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('home'))

@app.route('/nova-evidencia')
def pagina_registrar_evidencia():
    return render_template('adicionar_evidencia.html')

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


@app.route('/adicionar-informacoes')
def pagina_adicionar_informacoes():
    return render_template('adicionar_informacoes.html')

@app.route('/inve-s', methods=['POST'])
def cadastrar_testemunhas():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    print(f"Nova testemunha: {dados}")

    conn = criar_conexao()
    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO testemunhas(nome, telefone, endereco,depoimento, caso_id) 
        VALUES(%s, %s, %s, %s, %s)
        RETURNING id;
        ''',
        (dados['nome'], dados['telefone'], dados['endereco'],
         dados['depoimento'], dados['caso_id'])
    )

    novo_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    return jsonify({
        'message': 'Suspeito cadastrado com sucesso!',
        'id': novo_id,
        'suspeito': dados
    }), 201

@app.route('/nova-testemunha', methods=['GET'])
def pagina_cadastrar_testemunha():
    return render_template('cadastrar_testemunha.html')

@app.route('/cadastrar-testemunha', methods=['POST'])
def salvar_testemunha():
    nome = request.form['nome']
    telefone = request.form['telefone']
    endereco = request.form['endereco']
    depoimento = request.form['depoimento']
    caso_id = request.form['caso_id']

    conn = criar_conexao()
    cursor = conn.cursor()

    try:
        cursor.execute(
            '''
            INSERT INTO testemunhas (nome, telefone, endereco, depoimento, caso_id) 
            VALUES (%s, %s, %s, %s, %s)
            ''',
            (nome, telefone, endereco, depoimento, caso_id)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erro ao cadastrar testemunha: {e}")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('home'))




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        conn = criar_conexao()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                (email, hashed_password)
            )
            conn.commit()
            flash('Conta criada com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            print(f"Erro ao registar: {e}")
            flash('Este e-mail já pode estar registado.', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = criar_conexao()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT id, email, password_hash FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            flash('Login efetuado com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('E-mail ou palavra-passe incorretos.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    flash('Terminou a sessão com sucesso.', 'success')
    return redirect(url_for('login'))






if __name__ == '__main__':
    app.run(debug=True)


