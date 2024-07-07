import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import webbrowser
from tkinter import messagebox, ttk
from datetime import datetime



conn = sqlite3.connect('luxury_wheels.db')


conn.execute('''CREATE TABLE IF NOT EXISTS veiculos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                ano_do_veiculo TEXT,
                categoria TEXT NOT NULL,
                transmissao TEXT NOT NULL,
                tipo TEXT NOT NULL,
                capacidade INTEGER NOT NULL,
                diaria REAL NOT NULL,
                ultima_manutencao TEXT,
                proxima_manutencao TEXT,
                ultima_inspecao TEXT,
                proxima_inspecao TEXT,
                imagem TEXT,
                status TEXT DEFAULT 'disponivel'
                )''')

conn.execute('''CREATE TABLE IF NOT EXISTS clientes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL
                )''')

conn.execute('''CREATE TABLE IF NOT EXISTS reservas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_veiculo INTEGER NOT NULL,
                id_cliente INTEGER NOT NULL,
                inicio_diaria TEXT NOT NULL,
                fim_diaria TEXT NOT NULL,
                pagamento TEXT NOT NULL,
                FOREIGN KEY (id_veiculo) REFERENCES veiculos(id),
                FOREIGN KEY (id_cliente) REFERENCES clientes(id)
                )''')

conn.execute('''CREATE TABLE IF NOT EXISTS pagamento(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metodo TEXT NOT NULL
                )''')

conn.execute('''CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL)
                ''')
conn.commit()

#Janela principal

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title('Login')
        self.root.geometry('200x200')
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text='Nome de Usuário').grid(row=0, column=0)
        self.usuario_entry = tk.Entry(self.root)
        self.usuario_entry.grid(row=0, column=1)

        tk.Label(self.root, text='Senha').grid(row=1, column=0)
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.root, text='Login', command=self.login).grid(row=2, column=0, columnspan=2)
        tk.Button(self.root, text='Registe-se', command=self.register).grid(row=3, column=0, columnspan=2)
        tk.Button(self.root, text='Atualizar Senha', command=self.update_password).grid(row=4, column=0, columnspan=2)


    def login(self):
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()

        cursor = conn.execute('SELECT * FROM users WHERE usuario=? AND password=?', (usuario, password))
        if cursor.fetchone():
            self.root.destroy()
            main_app()
        else:
            messagebox.showerror('Erro', 'Nome de usuário ou senha incorretos.')

    def register(self):
        RegisterWindow(self.root)

    def update_password(self):
        Updatepassword(self.root)

class RegisterWindow:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title('Registar - se')
        self.root.geometry('200x200')
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text='Usuário').grid(row=0, column=0)
        self.usuario_entry = tk.Entry(self.root)
        self.usuario_entry.grid(row=0, column=1)

        tk.Label(self.root, text='Senha').grid(row=1, column=0)
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.root, text='Registar', command=self.register).grid(row=2, column=0, columnspan=2)

    def register(self):
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()

        conn.execute('INSERT INTO users (usuario, password) VALUES (?, ?)', (usuario, password))
        conn.commit()

        messagebox.showinfo('Sucesso', 'Usuario registado com sucesso.')
        self.root.destroy()

class Updatepassword:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title('Atualizar Senha')
        self.root.geometry('300x200')
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text='Nome de Usuário').grid(row=0, column=0, padx=10, pady=10)
        self.usuario_entry = tk.Entry(self.root)
        self.usuario_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text='Senha Atual').grid(row=1, column=0, padx=10, pady=10)
        self.current_password_entry = tk.Entry(self.root, show='*')
        self.current_password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text='Nova Senha').grid(row=2, column=0, padx=10, pady=10)
        self.new_password_entry = tk.Entry(self.root, show='*')
        self.new_password_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.root, text='Atualizar', command=self.update_password).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def update_password(self):
        usuario = self.usuario_entry.get()
        password_atual = self.current_password_entry.get()
        password_nova = self.new_password_entry.get()


        cursor = conn.execute('SELECT * FROM users WHERE usuario=? AND password=?', (usuario, password_atual))
        result = cursor.fetchone()

        if result:

            conn.execute('UPDATE users SET password=? WHERE usuario=?', (password_nova, usuario))
            conn.commit()
            messagebox.showinfo('Sucesso', 'Senha atualizada com sucesso.')
            self.root.destroy()
        else:
            messagebox.showerror('Erro', 'Nome de usuário ou senha atual incorretos.')
            self.root.destroy()

def main_app():
    root = tk.Tk()
    app = LuxuryWheelsApp(root)
    root.mainloop()

class LuxuryWheelsApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Sistema de Gerenciamento Luxury Wheels')
        self.root.geometry('800x600')
        self.tab_control = ttk.Notebook(root)
        self.dashboard_tab = ttk.Frame(self.tab_control)
        self.veiculos_tab = ttk.Frame(self.tab_control)
        self.clientes_tab = ttk.Frame(self.tab_control)
        self.reservas_tab = ttk.Frame(self.tab_control)
        self.pagamentos_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.dashboard_tab, text='Dashboard')
        self.tab_control.add(self.veiculos_tab, text='Veiculos')
        self.tab_control.add(self.clientes_tab, text='Clientes')
        self.tab_control.add(self.reservas_tab, text='Reservas')
        self.tab_control.add(self.pagamentos_tab, text='Pagamento')
        self.tab_control.pack(expand=1, fill='both')

        self.tree_veiculos = None

        self.conn = sqlite3.connect('luxury_wheels.db')


        self.create_widgets()
        self.reservas_para_expirar()
        self.reservas_expiradas()

    def create_widgets(self):
        self.setup_dashboard_tab()
        self.setup_veiculos_tab()
        self.setup_clientes_tab()
        self.setup_reservas_tab()
        self.setup_pagamentos_tab()

    def setup_dashboard_tab(self):
        Dashboardwindow(self.dashboard_tab)

    def reservas_para_expirar(self):
        query = '''
        SELECT id, id_cliente, id_veiculo, fim_diaria
        FROM reservas
        WHERE julianday(fim_diaria) - julianday('now') <= 3 '''

        cursor = self.conn.execute(query)
        for row in cursor:
            id_reserva, id_cliente, id_veiculo, fim_diaria = row
            messagebox.showwarning('Alerta de Reserva', f'A reserva {id_reserva} para o veículo {id_veiculo} do cliente {id_cliente} está próxima ao vencimento ({fim_diaria}).')

    def reservas_expiradas(self):
        query = '''
        DELETE FROM reservas
        WHERE julianday(fim_diaria) < julianday('now')'''

        self.conn.execute(query)
        self.conn.commit()

        self.populate_tree_reservas_tab()

        self.root.after(86400000, self.reservas_expiradas)

    #Aba_veiculo
    def setup_veiculos_tab(self):
        tk.Label(self.veiculos_tab, text='Gerenciamento de Veículos', font=('Arial', 24)).pack(pady=10)

        button_frame = tk.Frame(self.veiculos_tab)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text='Adicionar Veículo', command=self.add_veiculo, height=5, width=20).grid(row=0,column=0, padx=10, pady=5)
        tk.Button(button_frame, text='Listar Veículos', command=self.listar_veiculos, height=5, width=20).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(button_frame, text='Indicar Manutenção', command=self.indicar_manutencao, height=5, width=20, bg='red', fg='white').grid(row=1, column=0, padx=10, pady=5)
        tk.Button(button_frame, text='Disponibilizar Veículo', command=self.alterar_status_veiculos, height=5, width=20).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(button_frame, text='Exportar para Excel', command=self.exportar_para_excel_veiculos, height=5, width=20).grid(row=2, column=0,padx=10, pady=20)
        tk.Button(button_frame, text='Atualizar Veículo', command=self.atualizar_veiculo, height=5, width=20).grid(row=2, column=1, columnspan=2, padx=10, pady=5)
        tk.Button(button_frame, text='Excluir Veículo', command=self.excluir_veiculo, height=5, width=20).grid(row=3, column=0, columnspan=2, padx=10, pady=5)



        self.tree_veiculos = ttk.Treeview(self.veiculos_tab, columns=('id', 'marca', 'modelo','imagem', 'status'), show='headings')
        self.tree_veiculos.heading('id', text='ID')
        self.tree_veiculos.heading('marca', text='Marca')
        self.tree_veiculos.heading('modelo', text='Modelo')
        self.tree_veiculos.heading('imagem', text='URL da Imagem')
        self.tree_veiculos.heading('status', text='Status')
        self.tree_veiculos.pack(fill='both', expand=True)


        self.tree_veiculos.tag_configure('indisponivel', background='light coral')
        self.tree_veiculos.tag_configure('alugado', background='lightblue')

        self.tree_veiculos.bind('<Button-1>', self.on_tree_click)

        self.populate_tree_veiculos_tab()

    def on_tree_click(self, event):
        regiao = self.tree_veiculos.identify_region(event.x, event.y)
        if regiao == 'cell':
            column = self.tree_veiculos.identify_column(event.x)
            if column =='#4':
                item = self.tree_veiculos.identify_row(event.y)
                url = self.tree_veiculos.item(item, 'values')[3]
                webbrowser.open(url)

    def add_veiculo(self):
        Addveiculowindow(self.root, self.populate_tree_veiculos_tab)

    def listar_veiculos(self):
        Listveiculoswindow(self.root)

    def atualizar_veiculo(self):
        item_selecionado = self.tree_veiculos.selection()
        if not item_selecionado:
            messagebox.showerror('Erro', 'Selecione um veículo para atualizar.')
            return

        id_veiculo = self.tree_veiculos.item(item_selecionado)['values'][0]
        atualizar_window = tk.Toplevel(self.root)
        atualizar_window.title('Atualizar Veículo')

        campos = ['Marca', 'Modelo', 'Ano do Veículo', 'Categoria', 'Transmissão', 'Tipo', 'Capacidade', 'Valor da Diária', 'Última Revisão', 'Próxima Revisão', 'Última Inspeção', 'Próxima Inspeção', 'imagem']
        entradas = {}

        for i, campo in enumerate(campos):
            tk.Label(atualizar_window, text=campo).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(atualizar_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entradas[campo] = entry

        query = 'SELECT marca, modelo, ano_do_veiculo, categoria, transmissao, tipo, capacidade, diaria, ultima_manutencao, proxima_manutencao, ultima_inspecao, proxima_inspecao, imagem FROM veiculos WHERE id=?'
        cursor = conn.execute(query, (id_veiculo,))
        veiculo = cursor.fetchone()

        for i, campo in enumerate(campos):
            entradas[campo].insert(0, str(veiculo[i]))

        def save_updates():
            values = {campo: entradas[campo].get() for campo in campos}
            query = '''
            UPDATE veiculos
            SET marca=?, modelo=?, ano_do_veiculo=?, categoria=?, transmissao=?, tipo=?, capacidade=?, diaria=?, ultima_manutencao=?, proxima_manutencao=?, ultima_inspecao=?, proxima_inspecao=?, imagem=?
            WHERE id=?
            '''

            try:
                conn.execute(query, (values['Marca'], values['Modelo'], values['Ano do Veículo'], values['Categoria'], values['Transmissão'], values['Tipo'], values['Capacidade'], values['Valor da Diária'],
                values['Última Revisão'], values['Próxima Revisão'], values['Última Inspeção'], values['Próxima Inspeção'],values['imagem'], id_veiculo))
                conn.commit()
                messagebox.showinfo('Sucesso', 'Veículo atualizado com sucesso.')
                atualizar_window.destroy()
                self.populate_tree_veiculos_tab()
            except Exception as e:
                messagebox.showerror('Erro', str(e))

        tk.Button(atualizar_window, text='Salvar', command=save_updates).grid(row=len(campos), column=0, columnspan=2, pady=10)

    def excluir_veiculo(self):
        item_selecionado = self.tree_veiculos.selection()
        if not item_selecionado:
            messagebox.showerror('Erro', 'Selecione um veículo para excluir.')
            return

        id_veiculo = self.tree_veiculos.item(item_selecionado)['values'][0]

        try:
            conn.execute('DELETE FROM veiculos WHERE id=?', (id_veiculo,))
            conn.commit()
            messagebox.showinfo('Sucesso', 'Veículo excluído com sucesso.')
            self.populate_tree_veiculos_tab()
        except Exception as e:
            messagebox.showerror('Erro', str(e))
    def populate_tree_veiculos_tab(self):

        for item in self.tree_veiculos.get_children():
            self.tree_veiculos.delete(item)


        query = 'SELECT id, marca, modelo, imagem, status FROM veiculos'
        cursor = conn.execute(query)
        for row in cursor:
            if row[4] == 'indisponivel':
                self.tree_veiculos.insert('', tk.END, values=row, tags=('indisponivel',))
            elif row[4] == 'alugado':
                self.tree_veiculos.insert('', tk.END, values=row, tags=('alugado', ))
            else:
                self.tree_veiculos.insert('', tk.END, values=row)



    #Aba_clientes
    def setup_clientes_tab(self):
        tk.Label(self.clientes_tab, text='Gerenciamento de Clientes', font=('Arial', 24)).pack(pady=10)

        button_frame = tk.Frame(self.clientes_tab)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text='Adicionar Clientes', command=self.add_cliente, height=5, width=25).grid(row=0,column=0, padx=10, pady=5)
        tk.Button(button_frame, text='Listar Clientes', command=self.listar_clientes, height=5, width=25).grid(row=0,column=1, padx=10, pady=5)
        tk.Button(button_frame, text='Exportar Clientes para o Excel', command=self.exportar_para_excel_clientes, height=5, width=25).grid(row=1,column=0, padx=10, pady=5)
        tk.Button(button_frame, text='Atualizar Cliente', command=self.atualizar_cliente, height=5, width=25).grid(row=1,column=1, padx=10, pady=5)
        tk.Button(button_frame, text='Excluir Cliente', command=self.excluir_cliente, height=5, width=25).grid(row=2,column=0, columnspan=2, padx=10, pady=5)


        columns = ('ID', 'Nome', 'Email', 'Telefone')
        self.tree_clientes = ttk.Treeview(self.clientes_tab, columns=columns, show='headings')

        for col in columns:
            self.tree_clientes.heading(col, text=col)
            self.tree_clientes.column(col, minwidth=0, width=100)

        self.tree_clientes.pack(fill='both', expand=True)

        self.populate_tree_clientes_tab()

    def add_cliente(self):
        Addclientewindow(self.root, self.populate_tree_clientes_tab)


    def listar_clientes(self):
        Listarclienteswindow(self.root)

    def atualizar_cliente(self):
        item_selecionado = self.tree_clientes.selection()
        if not item_selecionado:
            messagebox.showerror('Erro', 'Selecione um cliente para atualizar.')
            return

        id_cliente = self.tree_clientes.item(item_selecionado)['values'][0]

        atualizar_window = tk.Toplevel(self.root)
        atualizar_window.title('Atualizar Cliente')

        query = 'SELECT nome, email, telefone FROM clientes WHERE id=?'
        cursor = conn.execute(query, (id_cliente, ))
        cliente = cursor.fetchone()

        tk.Label(atualizar_window, text='Nome').grid(row=0, column=0, padx=10, pady=5)
        nome_entry= tk.Entry(atualizar_window)
        nome_entry.grid(row=0, column=1, padx=10, pady=5)
        nome_entry.insert(0, cliente[0])

        tk.Label(atualizar_window, text='Email').grid(row=1, column=0, padx=10, pady=5)
        email_entry = tk.Entry(atualizar_window)
        email_entry.grid(row=1, column=1, padx=10, pady=5)
        email_entry.insert(0, cliente[1])

        tk.Label(atualizar_window, text='Telefone').grid(row=2, column=0, padx=10, pady=5)
        telefone_entry = tk.Entry(atualizar_window)
        telefone_entry.grid(row=2, column=1, padx=10, pady=5)
        telefone_entry.insert(0, cliente[2])

        def save_updates():
            novo_nome = nome_entry.get()
            novo_email = email_entry.get()
            novo_telefone = telefone_entry.get()

            query = 'UPDATE clientes SET nome=?, email=?, telefone=? WHERE id=?'
            try:
                conn.execute(query, (novo_nome, novo_email, novo_telefone, id_cliente))
                conn.commit()
                messagebox.showinfo('Sucesso', 'Cliente atualizado com sucesso')
                atualizar_window.destroy()
                self.populate_tree_clientes_tab()
            except Exception as e:
                messagebox.showerror('Erro', str(e))

        tk.Button(atualizar_window, text='Salvar', command=save_updates).grid(row=3, column=0, columnspan=2, pady=10)

    def populate_tree_clientes_tab(self):

        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)


        query = 'SELECT id, nome, email, telefone FROM clientes'
        cursor = conn.execute(query)
        for row in cursor:
            self.tree_clientes.insert('', tk.END, values=row)

    def excluir_cliente(self):
        item_selecionado = self.tree_clientes.selection()
        if not item_selecionado:
            messagebox.showerror('Erro', 'Selecione um cliente para excluir.')
            return
        id_cliente = self.tree_clientes.item(item_selecionado)['values'][0]

        confirmar = messagebox.askyesno('Confirmar', 'Tem certeza de que deseja excluir este cliente?')
        if confirmar:
            try:
                conn.execute('DELETE FROM clientes WHERE id=?', (id_cliente,))
                conn.commit()
                messagebox.showinfo('Sucesso', 'Cliente excluído com sucesso.')
                self.populate_tree_clientes_tab()
            except Exception as e:
                messagebox.showerror('Erro', str(e))

    #Aba_reservas
    def setup_reservas_tab(self):
        tk.Label(self.reservas_tab, text='Gerenciamento de Reservas', font=('Arial', 24)).pack(pady=10)

        button_frame = tk.Frame(self.reservas_tab)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text='Adicionar Reserva', command=self.add_reserva, height=5, width=25).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(button_frame, text='Listar Reservas', command=self.listar_reservas, height=5, width=25).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(button_frame, text='Exportar Reservas para o Excel', command=self.exportar_para_excel_reservas, height=5, width=25).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(button_frame, text='Atualizar Reserva', command=self.atualizar_reserva, height=5, width=25).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(button_frame, text='Excluir Reserva', command=self.excluir_reserva, height=5, width=25).grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        columns = ('Id', 'Cliente', 'Veículo', 'Data de Início', 'Data do Fim', 'Forma de pagamento')
        self.tree_reservas = ttk.Treeview(self.reservas_tab, columns=columns, show='headings')

        for col in columns:
            self.tree_reservas.heading(col, text=col)
            self.tree_reservas.column(col, minwidth=0, width=100)

        self.tree_reservas.pack(fill='both', expand=True)

        self.populate_tree_reservas_tab()

    def populate_tree_reservas_tab(self):
        for item in self.tree_reservas.get_children():
            self.tree_reservas.delete(item)

        query = '''
            SELECT reservas.id, clientes.nome, veiculos.modelo, reservas.inicio_diaria, reservas.fim_diaria, reservas.pagamento
            FROM reservas
            JOIN clientes ON reservas.id_cliente = clientes.id
            JOIN veiculos ON reservas.id_veiculo = veiculos.id
            '''
        cursor = conn.execute(query)
        for row in cursor:
            self.tree_reservas.insert("", tk.END, values=row)

    def add_reserva(self):
        Addreservawindow(self.root, self.populate_tree_reservas_tab, self.populate_tree_reservas_tab, self.populate_tree_veiculos_tab)

    def listar_reservas(self):
        Listarreservaswindow(self.root)

    def atualizar_reserva(self):
        item_selecionado = self.tree_reservas.selection()
        if not item_selecionado:
            messagebox.showerror('Erro', 'Selecione uma reserva para atualizar.')
            return

        id_reserva = self.tree_reservas.item(item_selecionado)['values'][0]

        atualizar_window = tk.Toplevel(self.root)
        atualizar_window.title('Atualizar Reserva')

        query = '''SELECT id_veiculo, id_cliente, inicio_diaria, fim_diaria, pagamento 
        FROM reservas 
        JOIN clientes ON reservas.id_cliente = clientes.id
        WHERE reservas.id=?'''
        cursor = conn.execute(query, (id_reserva,))
        reserva = cursor.fetchone()

        tk.Label(atualizar_window, text='ID Veículo').grid(row=0, column=0, padx=10, pady=5)
        id_veiculo_entry = tk.Entry(atualizar_window)
        id_veiculo_entry.grid(row=0, column=1, padx=10, pady=5)
        id_veiculo_entry.insert(0, reserva[0])

        tk.Label(atualizar_window, text='ID Cliente').grid(row=1, column=0, padx=10, pady=5)
        id_cliente_entry = tk.Entry(atualizar_window)
        id_cliente_entry.grid(row=1, column=1, padx=10, pady=5)
        id_cliente_entry.insert(0, reserva[1])

        tk.Label(atualizar_window, text='Início Diária').grid(row=2, column=0, padx=10, pady=5)
        inicio_diaria_entry = tk.Entry(atualizar_window)
        inicio_diaria_entry.grid(row=2, column=1, padx=10, pady=5)
        inicio_diaria_entry.insert(0, reserva[2])

        tk.Label(atualizar_window, text='Fim Diária').grid(row=3, column=0, padx=10, pady=5)
        fim_diaria_entry = tk.Entry(atualizar_window)
        fim_diaria_entry.grid(row=3, column=1, padx=10, pady=5)
        fim_diaria_entry.insert(0, reserva[3])

        tk.Label(atualizar_window, text='Pagamento').grid(row=4, column=0, padx=10, pady=5)
        pagamento_entry = tk.Entry(atualizar_window)
        pagamento_entry.grid(row=4, column=1, padx=10, pady=5)
        pagamento_entry.insert(0, reserva[4])

        def save_updates():
            novo_id_veiculo = id_veiculo_entry.get()
            novo_id_cliente = id_cliente_entry.get()
            novo_inicio_diaria = inicio_diaria_entry.get()
            novo_fim_diaria = fim_diaria_entry.get()
            novo_pagamento = pagamento_entry.get()

            query = 'UPDATE reservas SET id_veiculo=?, id_cliente=?, inicio_diaria=?, fim_diaria=?, pagamento=? WHERE id=?'
            try:
                conn.execute(query, (novo_id_veiculo, novo_id_cliente, novo_inicio_diaria, novo_fim_diaria, novo_pagamento, id_reserva))
                conn.commit()
                messagebox.showinfo('Sucesso', 'Reserva atualizada com sucesso')
                atualizar_window.destroy()
                self.populate_tree_reservas_tab()
            except Exception as e:
                messagebox.showerror('Erro', str(e))

        tk.Button(atualizar_window, text='Salvar', command=save_updates).grid(row=5, column=0, columnspan=2, pady=10)

    def excluir_reserva(self):
        item_selecionado = self.tree_reservas.selection()
        if not item_selecionado:
            messagebox.showerror('Erro', 'Selecione uma reserva para excluir.')
            return

        id_reserva = self.tree_reservas.item(item_selecionado)['values'][0]

        confirm = messagebox.askyesno('Confirmar', 'Tem certeza que deseja excluir esta reserva?')
        if confirm:
            try:

                query_veiculo = 'SELECT id_veiculo FROM reservas WHERE id=?'
                cursor = conn.execute(query_veiculo, (id_reserva,))
                id_veiculo = cursor.fetchone()[0]


                query_delete_reserva = 'DELETE FROM reservas WHERE id=?'
                conn.execute(query_delete_reserva, (id_reserva,))
                conn.commit()


                query_update_veiculo = 'UPDATE veiculos SET status="disponivel" WHERE id=?'
                conn.execute(query_update_veiculo, (id_veiculo,))
                conn.commit()

                messagebox.showinfo('Sucesso', 'Reserva excluída com sucesso')
                self.populate_tree_reservas_tab()
                self.populate_tree_veiculos_tab()  # Atualizar a árvore de veículos

            except Exception as e:
                messagebox.showerror('Erro', str(e))


    #Aba_pagamentos
    def setup_pagamentos_tab(self):
        tk.Label(self.pagamentos_tab, text='Gerenciamento de Formas Pagamentos', font=('Arial', 24)).pack(pady=10)
        tk.Button(self.pagamentos_tab, text='Adicionar Forma de Pagamento', command=self.add_pagamento, height=5, width=25).pack(pady=5)
        tk.Button(self.pagamentos_tab, text='Listar Formas de Pagamento', command=self.listar_pagamentos, height=5, width=25).pack(pady=5)

    def add_pagamento(self):
        AddFormaPgtowindow(self.root)

    def listar_pagamentos(self):
        ListarFormaPgtowindow(self.root)

    # Funções adicionais
    def indicar_manutencao(self):
        try:
            item_selecionado = self.tree_veiculos.selection()[0]
            if not item_selecionado:
                messagebox.showerror('Erro', 'Selecione um veículo para marcar como em manutenção.')
                return

            veiculo_id = self.tree_veiculos.item(item_selecionado)['values'][0]

            conn.execute('UPDATE veiculos SET status = ? WHERE id = ?', ('indisponivel', veiculo_id))
            conn.commit()
            messagebox.showinfo('Sucesso', 'Veículo marcado como em manutenção.')
            self.populate_tree_veiculos_tab()
        except Exception as e:
            messagebox.showerror('Erro', str(e))

    def populate_tree(self):
        for item in self.tree_veiculos.get_children():
            self.tree_veiculos.delete(item)

        query = 'SELECT id, marca, modelo, status FROM veiculos'
        cursor = conn.execute(query)
        for row in cursor:
            if row[3] == 'indisponivel':
                self.tree_veiculos.insert('', tk.END, values=row, tags=('indisponivel',))
            else:
                self.tree_veiculos.insert('', tk.END, values=row)


    def exportar_para_excel_veiculos(self):
        try:
            query = 'SELECT * FROM veiculos'
            df = pd.read_sql_query(query, conn)

            df.to_excel('veiculos.xlsx', index=False)
            messagebox.showinfo('Sucesso', 'Dados exportados para veiculos.xlsx com sucesso.')
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao exportar dados: {str(e)}')

    def exportar_para_excel_clientes(self):
        try:
            query = 'SELECT * FROM clientes'
            df = pd.read_sql_query(query, conn)

            df.to_excel('clientes.xlsx', index=False)
            messagebox.showinfo('Sucesso', 'Dados exportados para clientes.xlsx com sucesso.')
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao exportar dados: {str(e)}')

    def exportar_para_excel_reservas(self):
        try:
            query = 'SELECT * FROM reservas'
            df = pd.read_sql_query(query, conn)

            df.to_excel('reservas.xlsx', index=False)
            messagebox.showinfo('Sucesso', 'Dados exportados para reservas.xlsx com sucesso.')
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao exportar dados: {str(e)}')

    def alterar_status_veiculos(self):
        try:
            item_selecionado = self.tree_veiculos.selection()[0]
            id_veiculo = self.tree_veiculos.item(item_selecionado, 'values')[0]

            print(f"Selecionado veículo ID: {id_veiculo}")

            cursor = conn.execute('SELECT status FROM veiculos WHERE id=?', (id_veiculo,))
            status_atual = cursor.fetchone()[0]

            print(f"Status atual: {status_atual}")

            if status_atual == 'indisponivel':
                novo_status = 'disponivel'
                conn.execute('UPDATE veiculos SET status=? WHERE id=?', (novo_status, id_veiculo))
                conn.commit()

                cursor = conn.execute('SELECT status FROM veiculos WHERE id=?', (id_veiculo,))
                status_atualizado = cursor.fetchone()[0]

                print(f"Status atualizado: {status_atualizado}")

                if status_atualizado == novo_status:
                    messagebox.showinfo('Sucesso', f'Status do veículo alterado para {novo_status}')
                else:
                    messagebox.showerror('Erro', 'Falha ao atualizar o status do veículo no banco de dados.')
            elif status_atual == 'alugado':
                novo_status = 'disponivel'
                conn.execute('UPDATE veiculos SET status=? WHERE id=?', (novo_status, id_veiculo))
                conn.commit()

                cursor = conn.execute('SELECT status FROM veiculos WHERE id=?', (id_veiculo,))
                status_atualizado = cursor.fetchone()[0]

                print(f"Status atualizado: {status_atualizado}")

                if status_atualizado == novo_status:
                    messagebox.showinfo('Sucesso', f'Status do veículo alterado para {novo_status}')
                else:
                    messagebox.showerror('Erro', 'Falha ao atualizar o status do veículo no banco de dados.')
            else:
                messagebox.showinfo('Info', 'O status do veículo já está "disponível".')


            self.populate_tree_veiculos_tab()

        except IndexError:
            messagebox.showwarning('Aviso', 'Por favor, selecione um veículo para alterar o status')
        except Exception as e:
            messagebox.showerror('Erro', str(e))

class Dashboardwindow:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.frame.pack(expand=True, fill='both', padx=10, pady=10)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.frame, text='Dashboard', font=('Arial', 24)).pack(pady=10)


        first_row_frame = ttk.Frame(self.frame)
        first_row_frame.pack(side='top', pady=10)

        tk.Button(first_row_frame, text='Veículos Alugados', command=self.mostrar_veiculos_alugados, height=5, width=25).pack(side='left', padx=10)
        tk.Button(first_row_frame, text='Últimos Clientes Registrados', command=self.mostrar_clientes_recentes, height=5, width=25).pack(side='left', padx=10)


        second_row_frame = ttk.Frame(self.frame)
        second_row_frame.pack(side='top', pady=10)

        tk.Button(second_row_frame, text='Veículos Disponíveis', command=self.plot_veiculos_disponiveis, height=5, width=25).pack(side='left', padx=10)
        tk.Button(second_row_frame, text='Reservas do Mês', command=self.mostrar_reservas_mensais, height=5, width=25).pack(side='left', padx=10)

        
        third_row_frame = ttk.Frame(self.frame)
        third_row_frame.pack(side='top', pady=10)

        tk.Button(third_row_frame, text='Próximas Inspeções', command=self.mostrar_proxima_inspecao, height=5, width=25).pack(side='left', padx=10)
        tk.Button(third_row_frame, text='Próximas Revisões', command=self.mostrar_proxima_manutencao, height=5, width=25).pack(side='left', padx=10)
    def mostrar_veiculos_alugados(self):
        query = '''
        SELECT veiculos.marca, veiculos.modelo, reservas.fim_diaria
        FROM reservas
        JOIN veiculos ON reservas.id_veiculo = veiculos.id
        WHERE julianday(reservas.fim_diaria) >= julianday('now')
        '''
        df = pd.read_sql_query(query, conn)

        if not df.empty:
            print(df)
            messagebox.showinfo('Veículos Alugados', df.to_string())
        else:
            messagebox.showinfo('Informação', 'Nenhum veículo alugado no momento.')

    def plot_veiculos_alugados(self):
        query = '''
        SELECT veiculos.marca, veiculos.modelo, reservas.fim_diaria, julianday(reservas.fim_diaria) - julianday('now') AS dias_restantes
        FROM reservas
        JOIN veiculos ON reservas.id_veiculo = id_veiculo
        WHERE julianday(reservas.fim_diaria) > julianday('now')
        '''
        df = pd.read_sql_query(query, conn)
        if not df.empty:
            df.plot(kind='bar', x='moodelo', y='dias_restantes', title='Veículos Alugados e dias Restantes',
                    fingsize=(10, 6))
            plt.xlabel('Modelo do Veículo')
            plt.ylabel('Dias Restantes')
            plt.show()
        else:
            messagebox.showinfo('Informação', 'Nnehum veículo alugado no momento.')

    def mostrar_clientes_recentes(self):
        query = '''
        SELECT nome, email, telefone
        FROM clientes
        ORDER BY id DESC
        LIMIT 5
        '''
        df = pd.read_sql_query(query, conn)

        if not df.empty:
            print(df)
            messagebox.showinfo('Últimos Clientes Registrados', df.to_string())
        else:
            messagebox.showinfo('Informação', 'Nenhum cliente registrado recentemente.')

    def plot_veiculos_disponiveis(self):
        query = '''
        SELECT tipo, categoria, COUNT(*) as count
        FROM veiculos
        WHERE id NOT IN (
            SELECT id_veiculo
            FROM reservas
            WHERE julianday(fim_diaria) >= julianday('now')
        )
        GROUP BY tipo, categoria
        '''

        df = pd.read_sql_query(query, conn)

        if not df.empty:
            df_pivot = df.pivot(index='categoria', columns='tipo', values='count')
            df_pivot.plot(kind='bar', stacked=True, title='Quantidade de Veículos Disponíveis', figsize=(10, 6))
            plt.xlabel('Categoria')
            plt.ylabel('Quantidade')
            plt.show()
        else:
            messagebox.showinfo('Informação', 'Nenhum veículo disponível no momento.')

    def mostrar_reservas_mensais(self):
        query = '''
        SELECT COUNT(*) AS count, SUM(veiculos.diaria * (julianday(fim_diaria) - julianday(inicio_diaria))) AS total_receita
        FROM reservas
        JOIN veiculos ON reservas.id_veiculo = veiculos.id
        WHERE strftime('%Y-%m', inicio_diaria) = strftime('%Y-%m', 'now')
        '''

        df = pd.read_sql_query(query, conn)

        if not df.empty and df['count'][0] is not None and df['total_receita'][0] is not None:
            messagebox.showinfo('Reservas do Mês',
                                f"Total de Reservas: {df['count'][0]}\nTotal Financeiro: {df['total_receita'][0]:.2f}€")
        else:
            messagebox.showinfo('Informação', 'Nenhuma reserva no mês atual.')

    def mostrar_proxima_inspecao(self):
        query = '''
        SELECT marca, modelo, proxima_inspecao
        FROM veiculos
        WHERE julianday(proxima_inspecao) - julianday('now') <= 15
        '''
        df = pd.read_sql_query(query, conn)

        if not df.empty:
            hoje = datetime.now().date()
            df_alerta = pd.DataFrame(columns=['marca', 'modelo', 'proxima_inspecao'])  # DataFrame para os alertas

            for index, row in df.iterrows():
                proxima_inspecao = datetime.strptime(row['proxima_inspecao'], '%Y-%m-%d').date()
                dias_para_inspecao = (proxima_inspecao - hoje).days

                if dias_para_inspecao == 5:
                    messagebox.showwarning('Alerta', f'A inspeção do veículo {row["marca"]} {row["modelo"]} está a 5 dias de distância.')
                    df_alerta = pd.concat(
                        [df_alerta, pd.DataFrame([row], columns=['marca', 'modelo', 'proxima_inspecao'])])
                elif dias_para_inspecao == 4:
                    messagebox.showwarning('Alerta', f'A inspeção do veículo {row["marca"]} {row["modelo"]} está a 4 dias de distância.')
                    df_alerta = pd.concat(
                        [df_alerta, pd.DataFrame([row], columns=['marca', 'modelo', 'proxima_inspecao'])])
                elif dias_para_inspecao == 3:
                    messagebox.showwarning('Alerta', f'A inspeção do veículo {row["marca"]} {row["modelo"]} está a 3 dias de distância.')
                    df_alerta = pd.concat(
                        [df_alerta, pd.DataFrame([row], columns=['marca', 'modelo', 'proxima_inspecao'])])
                elif dias_para_inspecao == 2:
                    messagebox.showwarning('Alerta', f'A inspeção do veículo {row["marca"]} {row["modelo"]} está a 2 dias de distância.')
                    df_alerta = pd.concat(
                        [df_alerta, pd.DataFrame([row], columns=['marca', 'modelo', 'proxima_inspecao'])])
                elif dias_para_inspecao == 1:
                    messagebox.showwarning('Alerta', f'A inspeção do veículo {row["marca"]} {row["modelo"]} está a 1 dia de distância.')
                    df_alerta = pd.concat(
                        [df_alerta, pd.DataFrame([row], columns=['marca', 'modelo', 'proxima_inspecao'])])
                elif dias_para_inspecao == 0:
                    messagebox.showwarning('Alerta', f'A inspeção do veículo {row["marca"]} {row["modelo"]} expira hoje!')
                    df_alerta = pd.concat(
                        [df_alerta, pd.DataFrame([row], columns=['marca', 'modelo', 'proxima_inspecao'])])

            if not df_alerta.empty:
                messagebox.showinfo('Próximas Inspeções:', df_alerta.to_string(index=False))
            else:
                messagebox.showinfo('Informação', 'Nenhum veículo com inspeção a expirar nos próximos 15 dias.')
        else:
            messagebox.showinfo('Informação', 'Nenhum veículo com inspeção a expirar.')

    def mostrar_proxima_manutencao(self):
        query = '''
        SELECT marca, modelo, proxima_manutencao
        FROM veiculos
        WHERE julianday(proxima_manutencao) - julianday('now') <= 15
        '''
        df = pd.read_sql_query(query, conn)

        if not df.empty:
            hoje = datetime.now().date()
            df_alerta = pd.DataFrame(columns=['marca', 'modelo', 'proxima_manutencao'])  # DataFrame para os alertas

            for index, row in df.iterrows():
                proxima_manutencao = datetime.strptime(row['proxima_manutencao'], '%Y-%m-%d').date()
                dias_para_manutencao = (proxima_manutencao - hoje).days

                if dias_para_manutencao == 5:
                    messagebox.showwarning('Alerta',
                                           f'A revisão do veículo {row["marca"]} {row["modelo"]} está a 5 dias de distância.')
                    df_alerta = pd.concat(
                        [df_alerta, pd.DataFrame([row], columns=['marca', 'modelo', 'proxima_manutencao'])])
                elif dias_para_manutencao == 4:
                    messagebox.showwarning('Alerta',
                                           f'A revisão do veículo {row["marca"]} {row["modelo"]} está a 4 dias de distância.')
                    df_alerta = pd.concat(
                        [df_alerta, pd.DataFrame([row], columns=['marca', 'modelo', 'proxima_manutencao'])])
                elif dias_para_manutencao == 3:
                    messagebox.showwarning('Alerta',
                                           f'A revisão do veículo {row["marca"]} {row["modelo"]} está a 3 dias de distância.')
                    df_alerta = pd.concat(
                        [df_alerta, pd.DataFrame([row], columns=['marca', 'modelo', 'proxima_manutencao'])])
                elif dias_para_manutencao == 2:
                    messagebox.showwarning('Alerta',
                                           f'A revisão do veículo {row["marca"]} {row["modelo"]} está a 2 dias de distância.')
                    df_alerta = pd.concat(
                        [df_alerta, pd.DataFrame([row], columns=['marca', 'modelo', 'proxima_manutencao'])])
                elif dias_para_manutencao == 1:
                    messagebox.showwarning('Alerta',
                                           f'A revisão do veículo {row["marca"]} {row["modelo"]} está a 1 dia de distância.')
                    df_alerta = pd.concat(
                        [df_alerta, pd.DataFrame([row], columns=['marca', 'modelo', 'proxima_manutencao'])])
                elif dias_para_manutencao == 0:
                    messagebox.showwarning('Alerta',
                                           f'A revisão do veículo {row["marca"]} {row["modelo"]} expira hoje!')
                    df_alerta = pd.concat(
                        [df_alerta, pd.DataFrame([row], columns=['marca', 'modelo', 'proxima_manutencao'])])

            if not df_alerta.empty:
                messagebox.showinfo('Próximas Revisões:', df_alerta.to_string(index=False))
            else:
                messagebox.showinfo('Informação', 'Nenhum veículo com revisão a expirar nos próximos 15 dias.')
        else:
            messagebox.showinfo('Informação', 'Nenhum veículo com revisão a expirar.')

class Addveiculowindow:
    def __init__(self, root, update_callback):
        self.root = root
        self.root = tk.Toplevel(root)
        self.root.title('Adicionar Veículo')
        self.update_callback = update_callback
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text='Marca').grid(row=0, column=0)
        self.marca_entry = tk.Entry(self.root)
        self.marca_entry.grid(row=0, column=1)

        tk.Label(self.root, text='Modelo').grid(row=1, column=0)
        self.modelo_entry = tk.Entry(self.root)
        self.modelo_entry.grid(row=1, column=1)

        tk.Label(self.root, text='Ano do veiculo').grid(row=2, column=0)
        self.ano_do_veiculo_entry = tk.Entry(self.root)
        self.ano_do_veiculo_entry.grid(row=2, column=1)

        tk.Label(self.root, text='Categoria').grid(row=3, column=0)
        self.categoria_entry = tk.Entry(self.root)
        self.categoria_entry.grid(row=3, column=1)

        tk.Label(self.root, text='Transmissão').grid(row=4, column=0)
        self.transmissao_entry = tk.Entry(self.root)
        self.transmissao_entry.grid(row=4, column=1)

        tk.Label(self.root, text='Tipo de Veículo').grid(row=5, column=0)
        self.tipo_entry = tk.Entry(self.root)
        self.tipo_entry.grid(row=5, column=1)

        tk.Label(self.root, text='Quantidade de Pessoas').grid(row=6, column=0)
        self.capacidade_entry = tk.Entry(self.root)
        self.capacidade_entry.grid(row=6, column=1)

        tk.Label(self.root, text='Valor da Diária').grid(row=7, column=0)
        self.diaria_entry = tk.Entry(self.root)
        self.diaria_entry.grid(row=7, column=1)

        tk.Label(self.root, text='Última Revisão').grid(row=8, column=0)
        self.ultima_manutencao_entry = tk.Entry(self.root)
        self.ultima_manutencao_entry.grid(row=8, column=1)

        tk.Label(self.root, text='Próxima Revisão').grid(row=9, column=0)
        self.proxima_manutencao_entry = tk.Entry(self.root)
        self.proxima_manutencao_entry.grid(row=9, column=1)

        tk.Label(self.root, text='Última Inspeção Obrigatória').grid(row=10, column=0)
        self.ultima_inspecao_entry = tk.Entry(self.root)
        self.ultima_inspecao_entry.grid(row=10, column=1)

        tk.Label(self.root, text='Próxima Inspeção Obrigatória').grid(row=11, column=0)
        self.proxima_inspecao_entry = tk.Entry(self.root)
        self.proxima_inspecao_entry.grid(row=11, column=1)

        tk.Label(self.root, text='Imagem').grid(row=12, column=0)
        self.imagem_entry = tk.Entry(self.root)
        self.imagem_entry.grid(row=12, column=1)

        tk.Button(self.root, text='Adicionar', command=self.add_veiculo).grid(row=13, column=0, columnspan=2)

    def add_veiculo(self):
        marca = self.marca_entry.get().upper()
        modelo = self.modelo_entry.get().title()
        ano_do_veiculo = self.ano_do_veiculo_entry.get()
        categoria = self.categoria_entry.get().upper()
        transmissao = self.transmissao_entry.get().title()
        tipo = self.tipo_entry.get().title()
        capacidade = self.capacidade_entry.get()
        diaria = self.diaria_entry.get()
        ultima_manutencao = self.ultima_manutencao_entry.get()
        proxima_manutencao = self.proxima_manutencao_entry.get()
        ultima_inspecao = self.ultima_inspecao_entry.get()
        proxima_inspecao = self.proxima_inspecao_entry.get()
        imagem = self.imagem_entry.get()

        try:
            conn.execute('''INSERT INTO veiculos(marca, modelo, ano_do_veiculo,  categoria, transmissao, tipo, capacidade, 
                                diaria, ultima_manutencao, proxima_manutencao, ultima_inspecao, proxima_inspecao, imagem, status)
                            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,  'disponivel');''', (
                marca, modelo, ano_do_veiculo, categoria, transmissao, tipo, capacidade, diaria,
                ultima_manutencao, proxima_manutencao, ultima_inspecao, proxima_inspecao, imagem))
            conn.commit()
            messagebox.showinfo('Sucesso', 'Veículo adicionado com sucesso.')
            self.update_callback()
        except Exception as e:
            messagebox.showerror('Erro', str(e))
        self.root.destroy()

class Listveiculoswindow:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title('Listar Veículos')
        self.create_widgets()

    def create_widgets(self):
        columns = (
        'ID', 'Marca', 'Modelo', 'Ano do veiculo', 'Categoria', 'Transmissão', 'Tipo', 'Capacidade', 'Valor da Diária', 'Última Revisão',
        'Próxima Revisão', 'Última Inspeção Obrigatória', 'Próxima Inspeção Obrigatória', 'imagem',  'status')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=0, width=100)

        self.tree.pack(fill='both', expand=True)

        self.populate_tree()


    def populate_tree(self):
        query = 'SELECT * FROM veiculos'
        cursor = conn.execute(query)
        for row in cursor:
            self.tree.insert("", tk.END, values=row)

class Addclientewindow:
    def __init__(self, root, populate_tree_clientes_tab):
        self.root = root
        self.root = tk.Toplevel(root)
        self.root.title('Adicionar Clientes')
        self.populate_tree_clientes_tab = populate_tree_clientes_tab
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text='Nome').grid(row=0, column=0)
        self.nome_entry = tk.Entry(self.root)
        self.nome_entry.grid(row=0, column=1)

        tk.Label(self.root, text='Email').grid(row=1, column=0)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=1, column=1)

        tk.Label(self.root, text='Telefone').grid(row=2, column=0)
        self.telefone_entry = tk.Entry(self.root)
        self.telefone_entry.grid(row=2, column=1)

        tk.Button(self.root, text='Adicionar', command=self.add_cliente).grid(row=3, column=0, columnspan=2)

    def add_cliente(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        telefone = self.telefone_entry.get()

        conn.execute('''INSERT INTO clientes (nome, email, telefone)
                            VALUES(?, ?, ?)''', (nome, email, telefone))
        conn.commit()
        messagebox.showinfo('Sucesso', 'Cliente adicionada com sucesso.')
        self.root.destroy()
        self.populate_tree_clientes_tab()


class Listarclienteswindow:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title('Listar Clientes')
        self.create_widgets()

    def create_widgets(self):
        columns = ('Id', 'Nome', 'Email', 'Telefone')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=0, width=100)
        self.tree.pack(fill='both', expand=True)

        self.populate_tree()

    def populate_tree(self):
        query = 'SELECT * FROM clientes'
        cursor = conn.execute(query)
        for row in cursor:
            self.tree.insert("", tk.END, values=row)

    def export_to_excel(self):

        data = [self.tree.item(item)['values'] for item in self.tree.get_children()]


        df = pd.DataFrame(data, columns=['Nome', 'Email', 'Telefone'])


        df.to_excel("clientes.xlsx", index=False)
        messagebox.showinfo('Sucesso', 'Dados exportados para clientes.xlsx')


class Addreservawindow:
    def __init__(self, root, update_callback, populate_tree_reserva_tab, populate_tree_veiculos_tab):
        self.root = tk.Toplevel(root)
        self.root.title('Adicionar Reserva')
        self.update_callback = update_callback
        self.populate_tree_reserva_tab = populate_tree_reserva_tab
        self.populate_tree_veiculos_tab = populate_tree_veiculos_tab
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text='Id do Cliente').grid(row=0, column=0)
        self.id_cliente_entry = tk.Entry(self.root)
        self.id_cliente_entry.grid(row=0, column=1)

        tk.Label(self.root, text='Id do Carro').grid(row=1, column=0)
        self.id_carro_entry = tk.Entry(self.root)
        self.id_carro_entry.grid(row=1, column=1)

        tk.Label(self.root, text='Data de Início (YYYY-MM-DD)').grid(row=2, column=0)
        self.inicio_diaria_entry = tk.Entry(self.root)
        self.inicio_diaria_entry.grid(row=2, column=1)

        tk.Label(self.root, text='Data do Fim (YYYY-MM-DD)').grid(row=3, column=0)
        self.fim_diaria_entry = tk.Entry(self.root)
        self.fim_diaria_entry.grid(row=3, column=1)

        tk.Label(self.root, text='Forma de Pagamento').grid(row=4, column=0)
        self.pagamento_entry = tk.Entry(self.root)
        self.pagamento_entry.grid(row=4, column=1)

        tk.Button(self.root, text='Adicionar', command=self.add_reservas).grid(row=5, column=0, columnspan=2)

    def add_reservas(self):
        id_cliente = self.id_cliente_entry.get()
        id_carro = self.id_carro_entry.get()
        inicio_diaria = self.inicio_diaria_entry.get()
        fim_diaria = self.fim_diaria_entry.get()
        pagamento = self.pagamento_entry.get().upper()

        try:
            conn.execute('''INSERT INTO reservas (id_veiculo, id_cliente, inicio_diaria, fim_diaria, pagamento)
                                VALUES(?, ?, ?, ?, ?)''', (id_carro, id_cliente, inicio_diaria, fim_diaria, pagamento))
            conn.commit()

            conn.execute('UPDATE veiculos SET status=? WHERE id=?', ('alugado', id_carro))
            conn.commit()

            messagebox.showinfo('Sucesso', 'Reserva adicionada com sucesso.')
            self.update_callback()
            self.populate_tree_reserva_tab()
            self.populate_tree_veiculos_tab()
            self.root.destroy()
        except Exception as e:
            messagebox.showerror('Erro', str(e))

class Listarreservaswindow:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title('Listar Reservas')
        self.create_widgets()

    def create_widgets(self):
        columns = ('Id', 'Id do Cliente', 'Id do Veículo', 'Data de Início', 'Data de Término', 'Forma de Pagamento')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=0, width=100)

        self.tree.pack(fill='both', expand=True)

        self.populate_tree()

    def populate_tree(self):
        query = 'SELECT * FROM reservas'
        cursor = conn.execute(query)
        for row in cursor:
            self.tree.insert('', tk.END, values=row)

class AddFormaPgtowindow:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title('Adicionar Forma de Pagamento')
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text='Metodo').grid(row=0, column=0)
        self.metodo_entry = tk.Entry(self.root)
        self.metodo_entry.grid(row=0, column=1)

        tk.Button(self.root, text='Adicionar', command=self.add_metodo).grid(row=1, column=0, columnspan=2)

    def add_metodo(self):
        metodo = self.metodo_entry.get().upper()

        conn.execute('''INSERT INTO pagamento(metodo) VALUES(?)''', (metodo,))
        conn.commit()

        messagebox.showinfo('Sucesso', 'Forma de Pagamento adicionada com sucesso')
        self.root.destroy()

class ListarFormaPgtowindow:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title('Listar Forma de Pagamento')
        self.root.geometry('600x400')
        self.create_widgets()

    def create_widgets(self):
        columns = ('Id','Metodo',)
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=0, width=100)

        self.tree.pack(fill='both', expand=True)
        self.populate_tree()

    def populate_tree(self):
        query = 'SELECT * FROM pagamento'
        cursor = conn.execute(query)
        for row in cursor:
            self.tree.insert('', tk.END, values=row)


def main():
    root = tk.Tk()
    Login(root)
    root.mainloop()


if __name__ == '__main__':
    main()
