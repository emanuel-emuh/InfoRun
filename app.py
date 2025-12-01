from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Função para conectar ao banco e criar a tabela se não existir
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS corridas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            atleta TEXT NOT NULL,
            km REAL NOT NULL,
            data_registro DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Rota Principal: Mostra o Ranking do Mês Atual
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Pega o ano e mês atual (Ex: '2023-11')
    mes_atual = datetime.now().strftime('%Y-%m')
    
    # Soma os KMs de cada atleta, mas SÓ as corridas deste mês
    query = '''
        SELECT atleta, SUM(km) as total_km
        FROM corridas
        WHERE strftime('%Y-%m', data_registro) = ?
        GROUP BY atleta
        ORDER BY total_km DESC
    '''
    cursor.execute(query, (mes_atual,))
    ranking = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', ranking=ranking)

# Rota para Registrar os KMs
@app.route('/registrar', methods=['POST'])
def registrar():
    atleta = request.form['atleta']
    km = request.form['km']
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO corridas (atleta, km, data_registro) VALUES (?, ?, ?)', (atleta, km, data_hoje))
    conn.commit()
    conn.close()
    
    return redirect('/')

if __name__ == '__main__':
    init_db() # Cria o banco ao iniciar
    app.run(debug=True)