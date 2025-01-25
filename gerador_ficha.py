import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
from fpdf import FPDF

# Função para gerar a ficha catalográfica
def gerar_ficha():
    titulo = entry_titulo.get()
    autor = entry_autor.get()
    ano = entry_ano.get()
    editora = entry_editora.get()

    if titulo and autor and ano and editora:
        ficha = f"""
        Ficha Catalográfica
        -------------------
        Título: {titulo}
        Autor: {autor}
        Ano: {ano}
        Editora: {editora}
        """
        text_ficha.delete(1.0, tk.END)
        text_ficha.insert(tk.END, ficha)
        salvar_ficha(titulo, autor, ano, editora)
    else:
        messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos.")

# Função para salvar a ficha no banco de dados
def salvar_ficha(titulo, autor, ano, editora):
    conn = sqlite3.connect('fichas_catalograficas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fichas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            autor TEXT,
            ano TEXT,
            editora TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO fichas (titulo, autor, ano, editora)
        VALUES (?, ?, ?, ?)
    ''', (titulo, autor, ano, editora))
    conn.commit()
    conn.close()

# Função para exportar a ficha para TXT
def exportar_txt():
    ficha = text_ficha.get(1.0, tk.END)
    if ficha.strip():
        arquivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt")])
        if arquivo:
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(ficha)
            messagebox.showinfo("Sucesso", "Ficha exportada para TXT com sucesso!")
    else:
        messagebox.showwarning("Ficha Vazia", "Nenhuma ficha para exportar.")

# Função para exportar a ficha para PDF
def exportar_pdf():
    ficha = text_ficha.get(1.0, tk.END)
    if ficha.strip():
        arquivo = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Arquivos PDF", "*.pdf")])
        if arquivo:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for linha in ficha.split('\n'):
                pdf.cell(200, 10, txt=linha, ln=True)
            pdf.output(arquivo)
            messagebox.showinfo("Sucesso", "Ficha exportada para PDF com sucesso!")
    else:
        messagebox.showwarning("Ficha Vazia", "Nenhuma ficha para exportar.")

# Interface gráfica
app = tk.Tk()
app.title("Gerador de Ficha Catalográfica")

# Campos de entrada
tk.Label(app, text="Título:").grid(row=0, column=0, padx=10, pady=5)
entry_titulo = tk.Entry(app, width=40)
entry_titulo.grid(row=0, column=1, padx=10, pady=5)

tk.Label(app, text="Autor:").grid(row=1, column=0, padx=10, pady=5)
entry_autor = tk.Entry(app, width=40)
entry_autor.grid(row=1, column=1, padx=10, pady=5)

tk.Label(app, text="Ano:").grid(row=2, column=0, padx=10, pady=5)
entry_ano = tk.Entry(app, width=40)
entry_ano.grid(row=2, column=1, padx=10, pady=5)

tk.Label(app, text="Editora:").grid(row=3, column=0, padx=10, pady=5)
entry_editora = tk.Entry(app, width=40)
entry_editora.grid(row=3, column=1, padx=10, pady=5)

# Botão para gerar ficha
btn_gerar = tk.Button(app, text="Gerar Ficha", command=gerar_ficha)
btn_gerar.grid(row=4, column=0, columnspan=2, pady=10)

# Área de texto para exibir a ficha
text_ficha = tk.Text(app, height=10, width=50)
text_ficha.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Botões para exportar
btn_exportar_txt = tk.Button(app, text="Exportar para TXT", command=exportar_txt)
btn_exportar_txt.grid(row=6, column=0, pady=10)

btn_exportar_pdf = tk.Button(app, text="Exportar para PDF", command=exportar_pdf)
btn_exportar_pdf.grid(row=6, column=1, pady=10)

# Rodar a aplicação
app.mainloop()