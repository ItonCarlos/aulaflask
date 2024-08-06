from flask import Flask, redirect, render_template, request, url_for
from asgiref.wsgi import WsgiToAsgi
import pandas as pd
import os

TITULO = os.getenv("TITULO")

app = Flask(__name__)

class Livro:
    def __init__(self, titulo, autor, categoria, ano, editora="Sem Editora"):
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.ano = ano
        self.editora = editora
        self.ativo = False

    def ativa_livro(self):
        self.ativo = not self.ativo

        if self.ligado:
            return "Ativo"
        else:
            return "Inativo"

   # def atualizar_editora(self, nova_editora):
      #  self.editora = nova_editora      
       

@app.route('/inicio')
def ola():
    livro1 = Livro("O Senhor dos Anéis", "J.R.R. Tolkien", "Fantasia", 1954)
    livro2 = Livro("Dom Casmurro", "Machado de Assis", "Romance", 1899, "Martin Claret")
    livro3 = Livro("O Alquimista", "Paulo Coelho", "Autoajuda", 1988, "Rocco")
    lista = [livro1,livro2, livro3]
    return render_template('lista.html', titulo='TITULO',lista_de_livros=lista)

@app.route('/tabela')
def listagem_de_livros():
    try:
        df = pd.read_csv('tabela_livros.csv')
    except FileNotFoundError:
        return "Arquivo não encontrado", 404
    except Exception as e:
        return str(e), 500

    # Lista para armazenar objetos Livro
    lista_livros = []

    # Percorre o DataFrame e cria objetos Livro
    for index, row in df.iterrows():
        livro = Livro(
            titulo=row['Titulo do Livro'],
            autor=row['Autor'],
            categoria=row['Categoria'],  # Incluindo a categoria se disponível
            ano=row['Ano de Publicação'],  # Incluindo o ano se disponível
            editora=row.get('Editora','Sem editora')  # Incluindo a editora se disponível
        )
        lista_livros.append(livro)
        
        
    # Renderiza o template com a lista de livros
    return render_template('lista_livro.html', livros=lista_livros)


#Rota para atualizar editora
@app.route('/atualizar_editora', methods=['GET', 'POST'])
def atualizar_editora():
    if request.method == 'POST':
        titulo = request.form['titulo']
        nova_editora = request.form['editora']
        
        # Carregar livros
        #livros = carregar_livros(): 

        # Atualizar editora
        for livro in livros:
            if livro.titulo == titulo:
                livro.atualizar_editora(nova_editora)
                break
        
        # Salvar livros atualizados no CSV
        df = pd.DataFrame([vars(livro) for livro in livros])
        df.to_csv('tabela_livros.csv', index=False)

        return redirect(url_for('listagem_de_livros'))
    
    return render_template('atualizar_editora.html')


@app.route('/home')
def tabela():
    df = pd.read_csv('tabela_livros.csv')
    dados = df.to_dict(orient='records')
    return render_template('tabela_livro.html', dados=dados)

@app.route('/curriculo')
def curriculo():
    return render_template('curriculo.html')
    




asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    app.run(debug=True)