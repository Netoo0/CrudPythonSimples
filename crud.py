import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

class CRUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD App")
        
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)
        
        self.label_id = tk.Label(self.frame, text="ID:")
        self.label_id.grid(row=0, column=0)
        self.entry_id = tk.Entry(self.frame)
        self.entry_id.grid(row=0, column=1)
        
        self.label_nome = tk.Label(self.frame, text="Nome:")
        self.label_nome.grid(row=1, column=0)
        self.entry_nome = tk.Entry(self.frame)
        self.entry_nome.grid(row=1, column=1)
        
        self.label_endereco = tk.Label(self.frame, text="Endereço:")
        self.label_endereco.grid(row=2, column=0)
        self.entry_endereco = tk.Entry(self.frame)
        self.entry_endereco.grid(row=2, column=1)
        
        self.label_sexo = tk.Label(self.frame, text="Sexo:")
        self.label_sexo.grid(row=3, column=0)
        self.entry_sexo = tk.Entry(self.frame)
        self.entry_sexo.grid(row=3, column=1)
        
        self.btn_create = tk.Button(root, text="Create", command=self.create_data)
        self.btn_create.pack(pady=10)
        
        self.btn_read = tk.Button(root, text="Read", command=self.read_data)
        self.btn_read.pack(pady=10)
        
        self.btn_update = tk.Button(root, text="Update", command=self.update_data)
        self.btn_update.pack(pady=10)
        
        self.btn_delete = tk.Button(root, text="Delete", command=self.delete_data)
        self.btn_delete.pack(pady=10)
        
        self.db_connection = sqlite3.connect('data.db')
        self.create_table()
        
    def create_table(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dados'")
            table_exists = len(cursor.fetchall()) > 0
            
            if not table_exists:
                cursor.execute("CREATE TABLE dados (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, endereco TEXT, sexo TEXT)")
                self.db_connection.commit()
                messagebox.showinfo("Sucesso", "Tabela 'dados' criada com sucesso!")

            # Criação do arquivo data.db
            if not os.path.exists("data.db"):
                open("data.db", "w").close()
                
        except sqlite3.Error as error:
            messagebox.showerror("Erro", f"Erro ao criar tabela: {error}")
        
    def create_data(self):
        nome = self.entry_nome.get()
        endereco = self.entry_endereco.get()
        sexo = self.entry_sexo.get()
        
        if nome and endereco and sexo:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("INSERT INTO dados (nome, endereco, sexo) VALUES (?, ?, ?)", (nome, endereco, sexo))
                self.db_connection.commit()
                messagebox.showinfo("Sucesso", "Dados criados com sucesso!")
                self.entry_id.delete(0, tk.END)
                self.entry_nome.delete(0, tk.END)
                self.entry_endereco.delete(0, tk.END)
                self.entry_sexo.delete(0, tk.END)
            except sqlite3.Error as error:
                messagebox.showerror("Erro", f"Erro ao criar dados: {error}")
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            
    def read_data(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM dados")
            rows = cursor.fetchall()
            
            if rows:
                messagebox.showinfo("Dados", "\n".join([f"ID: {row[0]}, Nome: {row[1]}, Endereço: {row[2]}, Sexo: {row[3]}" for row in rows]))
            else:
                messagebox.showinfo("Dados", "Nenhum dado encontrado!")
        except sqlite3.Error as error:
            messagebox.showerror("Erro", f"Erro ao ler dados: {error}")
        
    def update_data(self):
        id = self.entry_id.get()
        nome = self.entry_nome.get()
        endereco = self.entry_endereco.get()
        sexo = self.entry_sexo.get()
        
        if id and nome and endereco and sexo:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("UPDATE dados SET nome=?, endereco=?, sexo=? WHERE id=?", (nome, endereco, sexo, id))
                self.db_connection.commit()
                messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
                self.entry_id.delete(0, tk.END)
                self.entry_nome.delete(0, tk.END)
                self.entry_endereco.delete(0, tk.END)
                self.entry_sexo.delete(0, tk.END)
            except sqlite3.Error as error:
                messagebox.showerror("Erro", f"Erro ao atualizar dados: {error}")
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
        
    def delete_data(self):
        id = self.entry_id.get()
        
        if id:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("DELETE FROM dados WHERE id=?", (id,))
                self.db_connection.commit()
                messagebox.showinfo("Sucesso", "Dados excluídos com sucesso!")
                self.entry_id.delete(0, tk.END)
                self.entry_nome.delete(0, tk.END)
                self.entry_endereco.delete(0, tk.END)
                self.entry_sexo.delete(0, tk.END)
            except sqlite3.Error as error:
                messagebox.showerror("Erro", f"Erro ao excluir dados: {error}")
        else:
            messagebox.showwarning("Aviso", "Insira um ID!")
        

if __name__ == '__main__':
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()
