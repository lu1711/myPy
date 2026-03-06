from tkinter import ttk
from tkinter import *
import sqlite3



class Produto:

    def __init__(self, root):
        self.janela = root
        self.janela.title("App Gestor de Produtos")
        self.janela.resizable(1,1)
        self.janela.wm_iconbitmap('recursos/M6_P2_icon.ico')

        frame = LabelFrame(self.janela, text = "Registar um novo produto", font=('Calibri', 16, 'bold'))
        frame.grid(row=0, column = 0, columnspan = 3, pady = 20)

        self.etiqueta_nome = Label(frame, text = "Nome:", font=('Calibri', 13))
        self.etiqueta_nome.grid(row=1, column=0)
        self.nome = Entry(frame, font=('Calibri', 13))
        self.nome.focus()
        self.nome.grid(row=1, column=1)

        self.etiqueta_preco = Label(frame, text="Preço: ", font=('Calibri', 13))
        self.etiqueta_preco.grid(row=2, column=0)
        self.preco = Entry(frame, font=('Calibri', 13))
        self.preco.grid(row=2, column=1)

        self.janela.resizable(1,1)
        root.geometry("400x200")

        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.botao_adicionar = ttk.Button(frame, text="Guardar Produto", command=self.add_produto, style='my.TButton')
        self.botao_adicionar.grid(row=3, columnspan=2, sticky=W + E)

        #tabela de produtos

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        self.tabela = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.tabela.grid(row=4, column=0, columnspan=2)
        self.tabela.heading('#0', text='Nome', anchor=CENTER)
        self.tabela.heading('#1', text='Preço', anchor=CENTER)

        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        botao_eliminar = ttk.Button(text='ELIMINAR', command=self.del_produto,
                                    style='my.TButton')
        botao_eliminar.grid(row=5, column=0, sticky=W + E)
        botao_editar = ttk.Button(text='EDITAR', command=self.edit_produto,
                                  style='my.TButton')
        botao_editar.grid(row=5, column=1, sticky=W + E)

        self.get_produtos()

        self.mensagem = Label(text = '', fg = 'red')
        self.mensagem.grid(row=3, column=0, columnspan=2, sticky= W+E)


    db = 'database/produtos.db'


    def db_consulta(self, consulta, parametros =()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado



    def get_produtos(self):
        registos_tabela = self.tabela.get_children()
        for linha in registos_tabela:
            self.tabela.delete(linha)

        query = 'SELECT * FROM produto ORDER BY nome DESC'
        registos_db = self.db_consulta(query)

        for linha in registos_db:
            print(linha)
            self.tabela.insert('', 'end', text=linha[1], values = (linha[2],))

    def validacao_nome(self):
        nome_introduzido = self.nome.get()
        return len(nome_introduzido) != 0

    def validacao_preco(self):
        preco_introduzido = self.preco.get()
        return len(preco_introduzido) != 0

    def add_produto(self):
        if self.validacao_nome() and self.validacao_preco():
            query = "INSERT INTO produto VALUES(NULL, ?, ?)"
            parametros = (self.nome.get(),self.preco.get())
            self.db_consulta(query, parametros)
            self.mensagem['text'] = 'Produto {} adicionado com êxito'.format(self.nome.get())

            self.nome.delete(0, END)
            self.preco.delete(0, END)

            #print(self.nome.get())
            #print(self.preco.get())
        elif self.validacao_nome() and self.validacao_preco() == False:
            print("Preço obrigatório!")
            self.mensagem['text'] = 'O preço é obrigatório'
        elif self.validacao_nome() == False and self.validacao_preco():
            print("Nome é obrigatório!")
            self.mensagem['text'] = 'O nome é obrigatório'
        else:
            print ("Nome e preço são obrigatórios!")
            self.mensagem['text'] = 'O nome e o preço são obrigatórios'

        self.get_produtos()

    def del_produto(self):
        #debug
        #print(self.tabela.item(self.tabela.selection()))

        #print(self.tabela.item(self.tabela.selection()))
        #print(self.tabela.item(self.tabela.selection())['text'])
        #print(self.tabela.item(self.tabela.selection())['values'])
        #print(self.tabela.item(self.tabela.selection())['values'][0])

        self.mensagem['text'] = ''
        try:
            self.tabela.item(self.tabela.selection())['text'][0]
        except IndexError as e:
            self.mensagem['text'] = 'Por favor, seleccione um produto'
            return

        self.mensagem['text'] = ''
        nome = self.tabela.item(self.tabela.selection())['text']
        query = "DELETE FROM produto WHERE nome = ?"
        self.db_consulta(query,(nome,))
        self.mensagem['text'] = 'Produto {} eliminado com êxito.'.format(nome)
        self.get_produtos()

    def edit_produto(self):
        self.mensagem ['text']=''
        try:
            self.tabela.item(self.tabela.selection())['text'][0]
        except IndexError as e:
            self.mensagem['text'] = 'Por favor seleccione um produto'
            return
        #obter dados actuais
        nome=self.tabela.item(self.tabela.selection())['text']
        old_preco = self.tabela.item(self.tabela.selection()) ['values'][0]

        #criar janela edição
        self.janela_editar = Toplevel()
        self.janela_editar.title("Editar Produto")
        self.janela_editar.resizable(1,1)
        self.janela_editar.wm_iconbitmap('recursos/M6_P2_icon.ico')

        titulo = Label(self.janela_editar, text='Edição de Produtos',
                       font=('Calibri', 50, 'bold'))
        titulo.grid(column=0, row=0)

        # Frame
        frame_ep = LabelFrame(self.janela_editar, text="Editar o seguinte Produto", font=('Calibri', 16, 'bold'))
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # label nome antigo
        self.etiqueta_nome_antigo = Label(frame_ep, text="Nome antigo: ", font=('Calibri', 13))
        self.etiqueta_nome_antigo.grid(row=2, column=0)
        self.input_nome_antigo = Entry(frame_ep, textvariable=StringVar(self.janela_editar, value=nome), state='readonly', font=('Calibri', 13))
        self.input_nome_antigo.grid(row=2, column=1)

        # Label Nome novo
        self.etiqueta_nome_novo = Label(frame_ep, text="Nome novo: ", font=('Calibri', 13))
        self.etiqueta_nome_novo.grid(row=3, column=0)

        self.input_nome_novo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nome_novo.grid(row=3, column=1)
        self.input_nome_novo.focus()

        # Label Preço antigo
        self.etiqueta_preco_antigo = Label(frame_ep, text="Preço antigo: ", font=('Calibri', 13))
        self.etiqueta_preco_antigo.grid(row=4, column=0)
        self.input_preco_antigo = Entry(frame_ep, textvariable=StringVar(self.janela_editar, value=old_preco), state='readonly', font=('Calibri', 13))
        self.input_preco_antigo.grid(row=4, column=1)

        #label preço novo
        self.etiqueta_preco_novo = Label(frame_ep, text="Preço novo: ",font=('Calibri', 13))
        self.etiqueta_preco_novo.grid(row=5, column=0)
        self.input_preco_novo = Entry(frame_ep,font=('Calibri', 13))
        self.input_preco_novo.grid(row=5, column=1)

        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.botao_atualizar = ttk.Button(frame_ep, text="Atualizar Produto", style='my.TButton', command=lambda:
                                          self.atualizar_produtos(self.input_nome_novo.get(),
                                          self.input_nome_antigo.get(),
                                          self.input_preco_novo.get(),
                                          self.input_preco_antigo.get()))
        self.botao_atualizar.grid(row=6, columnspan=2, sticky=W + E)

    def atualizar_produtos(self, novo_nome, antigo_nome, novo_preco, antigo_preco):
        produto_modificado = False
        query = 'UPDATE produto SET nome = ?, preco = ? WHERE nome = ? AND preco = ?'
        if novo_nome != '' and novo_preco != '':
            parametros = (novo_nome, novo_preco, antigo_nome, antigo_preco)
            produto_modificado = True
        elif novo_nome != '' and novo_preco == '':
            parametros = (novo_nome, antigo_preco, antigo_nome, antigo_preco)
            produto_modificado = True
        elif novo_nome == '' and novo_preco != '':
            parametros = (antigo_nome, novo_preco, antigo_nome, antigo_preco)
            produto_modificado = True

        if (produto_modificado):
            self.db_consulta(query, parametros)
            self.janela_editar.destroy()
            self.mensagem['text'] = 'O produto {} foi atualizado com êxito'.format(antigo_nome)
            self.get_produtos()
        else:
            self.janela_editar.destroy()
            nsagem['text'] = 'O produto {} NÃO foi atualizado'.format(antigo_nome)


if __name__ == '__main__':
    root = Tk()
    app = Produto(root)
    root.mainloop()