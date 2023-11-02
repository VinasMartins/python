import tkinter as tk
from tkinter import ttk
from actions.filter import filter_list

def criar_aba_produtos(self):
    frame_produtos = ttk.Frame(self.aba_produtos, style="Custom.TFrame")
    frame_produtos.pack(padx=10, pady=10, fill='both', expand=True)

    # Botão "Cadastrar Novo Produto"
    self.botao_novo_produto = ttk.Button(frame_produtos, text="Novo", command=self.mostrar_campos_produto, style='Green.TButton')
    self.botao_novo_produto.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    # Rótulo e caixa de entrada para o filtro
    filtro_label = ttk.Label(frame_produtos, text="Filtrar por Nome:")
    filtro_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

    filtro_entry = ttk.Entry(frame_produtos, width=70)
    filtro_entry.grid(row=1, column=0, padx=105, pady=5, sticky=tk.W)

    filtro_button = ttk.Button(frame_produtos, text="Filtrar", command=lambda: filter_list(self,filtro_entry.get(), 'products'))
    filtro_button.grid(row=1, column=0, padx=530, pady=5, sticky=tk.W)

    # Treeview
    self.lista_produtos = ttk.Treeview(frame_produtos, columns=("ID", "Nome", "Tipo", "Materiais", "Preço de Custo", "Margem de Lucro Atacado", "Margem de Lucro Varejo", "Preço Sugerido Atacado", "Preço Sugerido Varejo"))
    self.lista_produtos.heading("#1", text="ID", anchor=tk.W)
    self.lista_produtos.heading("#2", text="Nome")
    self.lista_produtos.heading("#3", text="Tipo")
    self.lista_produtos.heading("#4", text="Materiais")
    self.lista_produtos.heading("#5", text="Preço de Custo")
    self.lista_produtos.heading("#6", text="Margem de Lucro Atacado")
    self.lista_produtos.heading("#7", text="Margem de Lucro Varejo")
    self.lista_produtos.heading("#8", text="Preço Sugerido Atacado")
    self.lista_produtos.heading("#9", text="Preço Sugerido Varejo")
    self.lista_produtos.column("#0", width=0, stretch=tk.NO)
    self.lista_produtos.heading("#0", text="", anchor=tk.W)
    self.lista_produtos.column("#1", width=0, stretch=tk.NO)
    self.lista_produtos.column("#4", width=0, stretch=tk.NO)
    self.lista_produtos.column("#6", width=0, stretch=tk.NO)
    self.lista_produtos.column("#7", width=0, stretch=tk.NO)
    self.lista_produtos.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
    
    # Configuração da expansão da grade
    frame_produtos.grid_rowconfigure(2, weight=1)
    frame_produtos.grid_columnconfigure(0, weight=1)
    
    self.lista_produtos.bind("<Double-1>", self.editar_produto)
