from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/inicio')
def ola():
    lista = ['O Senhor dos Anéis', 'Dom Casmurro', 'O Alquimista','O Livro']
    return render_template('lista.html', titulo='Listagem de Livros - SENAI',lista_de_livros=lista)

@app.route('/curriculo')
def curriculo():
    return render_template('curriculo.html')

'''@app.route('/tabela')
def tab():
    base_tabela = 'tabela_livros.csv'
    df = pd.read_csv(base_tabela)
    return render_template('tabela_livro.html', titulo='Listagem de Livros',lista_de_livros=df)'''

@app.route('/tabela')
def tabela():
    df = pd.read_csv('tabela_livros.csv')
    dados = df.to_dict(orient='records')
    return render_template('tabela_livro.html', dados=dados)



app.run(debug=True)