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




if __name__ == '__main__':
    app.run(debug=True)


