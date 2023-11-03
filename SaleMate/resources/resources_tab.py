import tkinter as tk
from tkinter import ttk
from actions.filter import filter_list

def create_resources_tab(self):    
    frame_resources = ttk.Frame(self.aba_resources, style="Custom.TFrame")
    frame_resources.pack(padx=10, pady=10, fill='both', expand=True)

    # Botão "Cadastrar Novo Material"
    self.botao_novo_resource = ttk.Button(frame_resources, text="Novo", command=self.mostrar_campos_resource, style='Green.TButton')
    self.botao_novo_resource.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    # Rótulo e caixa de entrada para o filtro
    filtro_label = ttk.Label(frame_resources, text="Filtrar por Nome:")
    filtro_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

    filtro_entry = ttk.Entry(frame_resources, width=70)
    filtro_entry.grid(row=1, column=0, padx=105, pady=5, sticky=tk.W)

    filtro_button = ttk.Button(frame_resources, text="Filtrar", command=lambda: filter_list(self,filtro_entry.get(), 'resources'))
    filtro_button.grid(row=1, column=0, padx=530, pady=5, sticky=tk.W)

    
    # Treeview
    self.lista_resources = ttk.Treeview(frame_resources, columns=("ID", "Name", "Quantity", "PaidAmount", "UnitPrice", "MeasureUnit"))
    self.lista_resources.heading("#1", text="ID", anchor=tk.W)
    self.lista_resources.heading("#2", text="Nome")
    self.lista_resources.heading("#3", text="Quantidade")
    self.lista_resources.heading("#4", text="Valor Pago")
    self.lista_resources.heading("#5", text="Preço Unitário")
    self.lista_resources.heading("#6", text="Unidade de Medida")
    self.lista_resources.heading("#0", text="", anchor=tk.W)
    self.lista_resources.column("#0", width=0, stretch=tk.NO)
    self.lista_resources.column("#1", width=0, stretch=tk.NO)
    self.lista_resources.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
    
    # Configuração da expansão da grade
    frame_resources.grid_rowconfigure(2, weight=1)
    frame_resources.grid_columnconfigure(0, weight=1)

    self.lista_resources.bind("<Double-1>", self.editar_resource)
