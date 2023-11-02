import tkinter as tk
from tkinter import ttk
from actions.filter import filter_list

def criar_aba_materiais(self):    
    frame_materiais = ttk.Frame(self.aba_materiais, style="Custom.TFrame")
    frame_materiais.pack(padx=10, pady=10, fill='both', expand=True)

    # Botão "Cadastrar Novo Material"
    self.botao_novo_material = ttk.Button(frame_materiais, text="Novo", command=self.mostrar_campos_material, style='Green.TButton')
    self.botao_novo_material.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    # Rótulo e caixa de entrada para o filtro
    filtro_label = ttk.Label(frame_materiais, text="Filtrar por Nome:")
    filtro_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

    filtro_entry = ttk.Entry(frame_materiais, width=70)
    filtro_entry.grid(row=1, column=0, padx=105, pady=5, sticky=tk.W)

    filtro_button = ttk.Button(frame_materiais, text="Filtrar", command=lambda: filter_list(self,filtro_entry.get(), 'materials'))
    filtro_button.grid(row=1, column=0, padx=530, pady=5, sticky=tk.W)

    
    # Treeview
    self.lista_materiais = ttk.Treeview(frame_materiais, columns=("ID", "Nome", "Quantidade", "Valor Pago", "Preço Unitário", "Unidade de Medida"))
    self.lista_materiais.heading("#1", text="ID", anchor=tk.W)
    self.lista_materiais.heading("#2", text="Nome")
    self.lista_materiais.heading("#3", text="Quantidade")
    self.lista_materiais.heading("#4", text="Valor Pago")
    self.lista_materiais.heading("#5", text="Preço Unitário")
    self.lista_materiais.heading("#6", text="Unidade de Medida")
    self.lista_materiais.heading("#0", text="", anchor=tk.W)
    self.lista_materiais.column("#0", width=0, stretch=tk.NO)
    self.lista_materiais.column("#1", width=0, stretch=tk.NO)
    self.lista_materiais.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
    
    # Configuração da expansão da grade
    frame_materiais.grid_rowconfigure(2, weight=1)
    frame_materiais.grid_columnconfigure(0, weight=1)

    self.lista_materiais.bind("<Double-1>", self.editar_material)
