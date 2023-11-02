import tkinter as tk
from tkinter import ttk, IntVar, messagebox
import locale
import uuid
from resources.create_materials_tab import criar_aba_materiais
from resources.create_products_tab import criar_aba_produtos
from DAO.data import *
from actions.delete import *
from actions.update import *
from actions.insert import *
from actions.filter import *
from resources.refresher import *
from resources.config_menu import create_main_menu

class SaleMate:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("SaleMate v0.0.02")
        # largura_tela = self.janela.winfo_screenwidth()
        # altura_tela = self.janela.winfo_screenheight()
        # self.janela.geometry(f"{largura_tela-500}x{altura_tela-500}")
        self.define_screen_size(self.janela)
        self.janela.iconbitmap('images/logo2.ico')

        # Configurar o estilo do tema ttk
        self.estilo = ttk.Style()
        self.estilo.configure('TFrame', background='#f0f0f0')
        self.estilo.configure('TLabel', background='#f0f0f0')
        self.estilo.configure('TRadiobutton', background='#f0f0f0')
        self.estilo.configure('TEntry', background='#ffffff')

        # Botão Azul
        self.estilo.configure('Blue.TButton', background='#007acc')
        self.estilo.map('Blue.TButton', background=[('active', '#0055a4')])

        # Botão Vermelho
        self.estilo.configure('Red.TButton', background='#FF0000')
        self.estilo.map('Red.TButton', background=[('active', '#FF4444')])

        # Botão Laranja
        self.estilo.configure('Orange.TButton', background='#FFA500')
        self.estilo.map('Orange.TButton', background=[('active', '#FFD700')])

        # Botão Verde
        self.estilo.configure('Green.TButton', background='#00FF00')
        self.estilo.map('Green.TButton', background=[('active', '#33FF33')])

        self.materiais = []
        self.produtos = []
        self.materiais_selecionados = []
        self.lista_materiais_selecionados = None
        self.system_config = None
        self.has_default_screen = False
        
        self.product_type = 'Produto'

        self.unidades_medida = ["Centímetros", "cm²", "Gramas", "Mililitros", "Minutos", "Unidades"]
        self.product_types = ['Produto', 'Serviço', 'Combo']
        self.boolean_values = ['Sim','Não']

        try:
            carregar_dados(self)
        except Exception as e:
            messagebox.showinfo("É bom ter você aqui!", f"Você ainda não tem nenhum produto cadastrado!\nVamos começar?")

        if self.system_config:
            self.show_default_screens()
            cadastrar_valor_hora(self)
        else:
            self.show_config_window()

    def define_screen_size(self, screen, window_width=None,window_height=None):
        screen_width = screen.winfo_screenwidth()
        screen_height = screen.winfo_screenheight()
        window_width = screen_width - 500 if window_width is None else window_width
        window_height = screen_height - 500 if window_height is None else window_height
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        screen.geometry(f"{window_width}x{window_height}+{x}+{y}")


    def verify_if_has_hour_value(self):
        # Verifique se já existe um material com o nome "Valor Hora"
        value = False
        for material in self.materiais:
            if material["Nome"].lower() == "valor hora":
                value = True
        return value


    def show_default_screens(self):

        if not self.has_default_screen:
            self.abas = ttk.Notebook(self.janela)
            self.aba_materiais = ttk.Frame(self.abas)
            self.aba_produtos = ttk.Frame(self.abas)

            create_main_menu(self)
            self.abas.add(self.aba_materiais, text="Recursos")
            self.abas.add(self.aba_produtos, text="Catálogo")

            self.abas.pack(fill='both', expand=True)

            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

            criar_aba_materiais(self)
            criar_aba_produtos(self)

            atualizar_lista(self, self.lista_materiais, self.materiais, 'materiais')
            atualizar_lista(self, self.lista_produtos, self.produtos, 'produtos')

            self.has_default_screen = True
    
    def mostrar_campos_material(self, material=None):
        self.limpar_campos_materiais()

        # Cria uma janela popup para a edição de materiais
        self.janela_popup_material = tk.Toplevel(self.aba_materiais)
        self.janela_popup_material.title("Edição de Recurso")
        self.janela_popup_material.iconbitmap('images/logo2.ico')

        self.define_screen_size(self.janela_popup_material, 580,180)

        frame_popup_material = ttk.Frame(self.janela_popup_material)
        frame_popup_material.pack(padx=10, pady=10, fill='both', expand=True)

        self.label_material_nome = ttk.Label(frame_popup_material, text="Nome:")
        self.entrada_material_nome = ttk.Entry(frame_popup_material, width=70)

        self.label_material_quantidade = ttk.Label(frame_popup_material, text="Quantidade:")
        self.entrada_material_quantidade = ttk.Entry(frame_popup_material, width=70)

        self.label_material_preco_pago = ttk.Label(frame_popup_material, text="Valor (R$):")
        self.entrada_material_preco_pago = ttk.Entry(frame_popup_material, width=70)

        self.label_material_unidade_medida = ttk.Label(frame_popup_material, text="Unidade de Medida:")
        self.combobox_unidade_medida = ttk.Combobox(frame_popup_material, values=self.unidades_medida, width=67)
        self.botao_cancelar_material = ttk.Button(frame_popup_material, text="Cancelar", command=self.limpar_campos_materiais, style='Red.TButton')

        if material:
            self.entrada_material_nome.insert(0, material["Nome"])  # Preencha com o nome atual do material
            self.entrada_material_quantidade.insert(0, str(material["Quantidade"]))  # Preencha com a quantidade atual do material
            self.entrada_material_preco_pago.insert(0, str(material["Valor Pago"]))  # Preencha com o valor pago atual do material
            self.combobox_unidade_medida.set(material["Unidade de Medida"])  # Selecione a unidade de medida atual do material
            self.entrada_material_nome.config(state='disabled')
            self.combobox_unidade_medida.config(state='disabled')
            self.botao_atualizar_material = ttk.Button(frame_popup_material, text="Salvar Edição", command=lambda: atualizar_material(self, material), style='Blue.TButton')
            self.botao_excluir_material = ttk.Button(frame_popup_material, text="Excluir", command=lambda: excluir_material(self, material), style='Orange.TButton')
            # Verifica se o nome do material é "Valor Hora" para desabilitar todos os campos
            if material["Nome"].lower() == "valor hora":
                self.entrada_material_quantidade.config(state='disabled')
                self.entrada_material_preco_pago.config(state='enabled')
            else:
                self.botao_excluir_material.grid(row=4, column=1, padx=100, pady=5, columnspan=2, sticky=tk.E)
        else:
            self.botao_atualizar_material = ttk.Button(frame_popup_material, text="Salvar", command=lambda: cadastrar_material(self), style='Green.TButton')

        self.label_material_nome.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entrada_material_nome.grid(row=0, column=1, padx=5, pady=5)
        self.label_material_unidade_medida.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.combobox_unidade_medida.grid(row=1, column=1, padx=5, pady=5)
        self.label_material_quantidade.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.entrada_material_quantidade.grid(row=2, column=1, padx=5, pady=5)
        self.label_material_preco_pago.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.entrada_material_preco_pago.grid(row=3, column=1, padx=5, pady=5)
        self.botao_atualizar_material.grid(row=4, column=0, padx=5, pady=5, columnspan=2, sticky=tk.W)
        self.botao_cancelar_material.grid(row=4, column=1, padx=5, pady=5, columnspan=2, sticky=tk.E)
    
    def mostrar_campos_produto(self, produto=None):
        
        self.limpar_campos_produtos()

        # Crie uma janela popup para a edição de produtos
        self.janela_popup_produto = tk.Toplevel(self.aba_produtos)
        self.janela_popup_produto.title("Edição de Produto Final")
        self.janela_popup_produto.iconbitmap('images/logo2.ico')

        self.define_screen_size(self.janela_popup_produto, 635,510)

        frame_popup_produto = ttk.Frame(self.janela_popup_produto)
        frame_popup_produto.pack(padx=10, pady=10, fill='both', expand=True)

        self.label_produto_nome = ttk.Label(frame_popup_produto, text="Nome:")
        self.entrada_produto_nome = ttk.Entry(frame_popup_produto, width=70)

        self.label_margem_lucro_atacado = ttk.Label(frame_popup_produto, text="Margem de Lucro Atacado (%):")
        self.entrada_margem_lucro_atacado = ttk.Entry(frame_popup_produto, width=70)

        self.label_margem_lucro_varejo = ttk.Label(frame_popup_produto, text="Margem de Lucro Varejo (%):")
        self.entrada_margem_lucro_varejo = ttk.Entry(frame_popup_produto, width=70)

        self.label_tipo = ttk.Label(frame_popup_produto, text="Tipo:")
        self.combobox_tipo = ttk.Combobox(frame_popup_produto, values=self.product_types, width=67)
        self.combobox_tipo.bind("<<ComboboxSelected>>", lambda event: atualizar_combobox_materiais(self))
        
        self.label_calcula_tempo = ttk.Label(frame_popup_produto, text="Calcular Valor Hora?")
        self.combobox_calcula_tempo = ttk.Combobox(frame_popup_produto, values=self.boolean_values, width=67)

        self.label_produto_materiais = ttk.Label(frame_popup_produto, text="Recursos Utilizados (selecione):")
        self.var_filtro_materiais = tk.StringVar() 
        self.combobox_materiais = ttk.Combobox(frame_popup_produto, textvariable=self.var_filtro_materiais, width=67)
        self.label_quantidade_utilizada = ttk.Label(frame_popup_produto, text="Quantidade Utilizada:")
        self.entrada_quantidade_utilizada = ttk.Entry(frame_popup_produto, width=50)
        self.botao_adicionar_material = ttk.Button(frame_popup_produto, text="Adicionar Insumo", command=lambda: adicionar_material(self), style='Blue.TButton')

        self.botao_cancelar_produto = ttk.Button(frame_popup_produto, text="Cancelar", command=self.limpar_campos_produtos, style='Red.TButton')
        
        # Vincula a função de filtro ao Combobox
        self.var_filtro_materiais.trace_add('write', lambda *args: atualizar_combobox_materiais(self, is_filter=True))

        self.lista_materiais_selecionados = ttk.Treeview(frame_popup_produto, columns=("Material ID", "Material", "Quantidade Utilizada", "Valor Gasto"))
        self.lista_materiais_selecionados.heading("#0", text="", anchor=tk.W)
        self.lista_materiais_selecionados.heading("#1", text="Material ID", anchor=tk.W)
        self.lista_materiais_selecionados.heading("#2", text="Material")
        self.lista_materiais_selecionados.heading("#3", text="Quantidade Utilizada")
        self.lista_materiais_selecionados.heading("#4", text="Valor Gasto")
        self.lista_materiais_selecionados.column("#0", width=0, stretch=tk.NO)
        self.lista_materiais_selecionados.column("#1", width=0, stretch=tk.NO)
        self.lista_materiais_selecionados.bind("<Double-1>", lambda event: remove_material_selecionado(self))

        if produto:
            self.materiais_selecionados = produto["Materiais"]
            self.entrada_produto_nome.insert(0, produto["Nome"])  # Preencha com o nome atual do produto
            self.entrada_margem_lucro_atacado.insert(0, produto["Margem de Lucro Atacado"])  # Preencha com a margem de lucro atual do produto
            self.entrada_margem_lucro_varejo.insert(0, produto["Margem de Lucro Varejo"])  # Preencha com a margem de lucro atual do produto
            self.combobox_tipo.insert(0, produto["Tipo"])  # Preencha com o tipo do produto
            self.combobox_calcula_tempo.insert(0, produto["Calcula Tempo Gasto"])  # Preencha com o booleano se calcula ou nao o tempo gasto
            self.atualizar_lista_materiais_selecionados()
            self.entrada_produto_nome.config(state='disable')
            self.combobox_tipo.config(state='disable')
            self.botao_atualizar_produto = ttk.Button(frame_popup_produto, text="Salvar Edição", command=lambda: atualizar_produto(self, produto), style='Green.TButton', state='enabled')
            self.botao_excluir_produto = ttk.Button(frame_popup_produto, text="Excluir", command=lambda: excluir_produto(self, produto), style='Orange.TButton')
            self.botao_excluir_produto.grid(row=8, column=1, padx=100, pady=5, columnspan=2, sticky=tk.E)
        else:
            self.botao_atualizar_produto = ttk.Button(frame_popup_produto, text="Salvar", command=lambda: cadastrar_produto(self), style='Green.TButton')

        self.label_produto_nome.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entrada_produto_nome.grid(row=0, column=1, padx=5, pady=5)
        self.label_tipo.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.combobox_tipo.grid(row=1, column=1, padx=5, pady=5)
        self.label_margem_lucro_atacado.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.entrada_margem_lucro_atacado.grid(row=2, column=1, padx=5, pady=5)
        self.label_margem_lucro_varejo.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.entrada_margem_lucro_varejo.grid(row=3, column=1, padx=5, pady=5)
        self.label_calcula_tempo.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.combobox_calcula_tempo.grid(row=4, column=1, padx=5, pady=5)
        self.label_produto_materiais.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.combobox_materiais.grid(row=5, column=1, padx=5, pady=5)
        self.label_quantidade_utilizada.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.entrada_quantidade_utilizada.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        self.botao_adicionar_material.grid(row=6, column=0, padx=5, pady=5, columnspan=2, sticky=tk.E)
        self.lista_materiais_selecionados.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
        self.botao_atualizar_produto.grid(row=8, column=0, padx=5, pady=5, columnspan=2, sticky=tk.W)
        self.botao_cancelar_produto.grid(row=8, column=1, padx=5, pady=5, columnspan=2, sticky=tk.E)

        atualizar_combobox_materiais(self, True)

    def show_config_window(self):

        carregar_dados(self)

        self.window_configs = tk.Toplevel()
        self.window_configs.title("Configurações")
        self.window_configs.iconbitmap('images/logo2.ico')

        self.frame_popup_config = ttk.Frame(self.window_configs)
        self.frame_popup_config.pack(padx=10, pady=10, fill='both', expand=True)

        self.define_screen_size(self.window_configs, 770,340)

        # Informações pessoais
        self.label_personal_info = ttk.Label(self.frame_popup_config, text="INFORMAÇÕES PESSOAIS", font=("TkDefaultFont", 12, "bold"))
        self.label_personal_info.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="w")

        self.label_name = ttk.Label(self.frame_popup_config, text="Nome Completo:")
        self.entry_name = ttk.Entry(self.frame_popup_config, width=40)
        self.label_email = ttk.Label(self.frame_popup_config, text="E-mail:")
        self.entry_email = ttk.Entry(self.frame_popup_config, width=40)
        self.label_address = ttk.Label(self.frame_popup_config, text="Endereço:")
        self.entry_street = ttk.Entry(self.frame_popup_config, width=40)
        self.label_number = ttk.Label(self.frame_popup_config, text="Número:")
        self.entry_number = ttk.Entry(self.frame_popup_config, width=10)
        self.label_city = ttk.Label(self.frame_popup_config, text="Cidade:")
        self.entry_city = ttk.Entry(self.frame_popup_config, width=40)
        self.label_state = ttk.Label(self.frame_popup_config, text="Estado:")
        self.entry_state = ttk.Entry(self.frame_popup_config, width=10)
        self.label_cep = ttk.Label(self.frame_popup_config, text="CEP:")
        self.entry_cep = ttk.Entry(self.frame_popup_config, width=20)
        self.label_neighborhood = ttk.Label(self.frame_popup_config, text="Bairro:")
        self.entry_neighborhood = ttk.Entry(self.frame_popup_config, width=40)
        self.label_country = ttk.Label(self.frame_popup_config, text="País:")

        # Lista de países para o combobox
        self.countries = ["Brasil", "Estados Unidos", "Canadá", "Reino Unido", "Outro"]

        # Combobox para seleção de país
        self.combo_country = ttk.Combobox(self.frame_popup_config, values=self.countries, width=37)

        # Campos de trabalho
        self.label_work_info = ttk.Label(self.frame_popup_config, text="INFORMAÇÕES DE TRABALHO", font=("TkDefaultFont", 12, "bold"))
        self.label_work_info.grid(row=10, column=0, columnspan=4, padx=5, pady=5, sticky="w")

        self.label_company_name = ttk.Label(self.frame_popup_config, text="Nome da Empresa:")
        self.entry_company_name = ttk.Entry(self.frame_popup_config, width=40)
        self.label_company_code_cnpj_cpf = ttk.Label(self.frame_popup_config, text="CNPJ/CPF:")
        self.entry_company_code_cnpj_cpf = ttk.Entry(self.frame_popup_config, width=40)
        self.label_hours = ttk.Label(self.frame_popup_config, text="Horas de Trabalho p/ dia:")
        self.entry_hours = ttk.Entry(self.frame_popup_config, width=10)
        self.label_hourly_rate = ttk.Label(self.frame_popup_config, text="Valor da Hora:")
        self.entry_hourly_rate = ttk.Entry(self.frame_popup_config, width=10)

        # Organize os rótulos e campos em várias colunas
        self.label_name.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_name.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.label_email.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.entry_email.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        self.label_address.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_street.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.label_number.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.entry_number.grid(row=3, column=3, padx=5, pady=5, sticky="w")
        self.label_city.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_city.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.label_state.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.entry_state.grid(row=4, column=3, padx=5, pady=5, sticky="w")
        self.label_cep.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entry_cep.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        self.label_neighborhood.grid(row=5, column=2, padx=5, pady=5, sticky="w")
        self.entry_neighborhood.grid(row=5, column=3, padx=5, pady=5, sticky="w")
        self.label_country.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.combo_country.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        self.label_company_name.grid(row=11, column=0, padx=5, pady=5, sticky="w")
        self.entry_company_name.grid(row=11, column=1, padx=5, pady=5, sticky="w")
        self.label_company_code_cnpj_cpf.grid(row=11, column=2, padx=5, pady=5, sticky="w")
        self.entry_company_code_cnpj_cpf.grid(row=11, column=3, padx=5, pady=5, sticky="w")
        self.label_hours.grid(row=12, column=0, padx=5, pady=5, sticky="w")
        self.entry_hours.grid(row=12, column=1, padx=5, pady=5, sticky="w")
        self.label_hourly_rate.grid(row=12, column=2, padx=5, pady=5, sticky="w")
        self.entry_hourly_rate.grid(row=12, column=3, padx=5, pady=5, sticky="w")

        self.save_config_button = ttk.Button(self.frame_popup_config, text="Salvar", command=lambda: save_config_to_json(self),style='Green.TButton')
        self.cancel_config_button = ttk.Button(self.frame_popup_config, text="Cancelar", command=self.limpar_campos_config, style='Red.TButton')

        self.save_config_button.grid(row=13, column=0, padx=5, pady=5, columnspan=2, sticky="w")
        self.cancel_config_button.grid(row=13, column=2, padx=5, pady=5, columnspan=2, sticky="e")

        if self.system_config:
            self.entry_name.insert(0, self.system_config["Name"])
            self.entry_email.insert(0, self.system_config["Email"])
            self.entry_street.insert(0, self.system_config["Address"]["Street"])
            self.entry_number.insert(0, self.system_config["Address"]["Number"])
            self.entry_city.insert(0, self.system_config["Address"]["City"])
            self.entry_state.insert(0, self.system_config["Address"]["State"])
            self.entry_cep.insert(0, self.system_config["Address"]["CEP"])
            self.entry_neighborhood.insert(0, self.system_config["Address"]["Neighborhood"])
            self.combo_country.set(self.system_config["Address"]["Country"] if self.system_config["Address"]["Country"] else "")
            self.entry_company_name.insert(0, self.system_config["WorkInfo"]["Company"])
            self.entry_company_code_cnpj_cpf.insert(0, self.system_config["WorkInfo"]["CompanyCode"])
            self.entry_hours.insert(0, self.system_config["WorkInfo"]["HoursPerDay"])
            self.entry_hourly_rate.insert(0, self.system_config["WorkInfo"]["HourlyRate"])
        else:
            self.window_configs.protocol("WM_DELETE_WINDOW", self.on_config_window_close)
            self.cancel_config_button.config(state='disable')
    
    def on_config_window_close(self):
        result = messagebox.askquestion("Sair", "Você não pode fechar a janela de configuração. Deseja sair do SaleMate?")
        if result == 'yes':
            self.janela.destroy()
        else:
            self.window_configs.destroy()
            self.show_config_window()

    def limpar_campos_config(self):
        try:
            self.window_configs.destroy()
        except AttributeError:
            pass

    def limpar_campos_materiais(self):
        try:
            self.janela_popup_material.destroy()
        except AttributeError:
            pass

    def limpar_campos_produtos(self):
        self.materiais_selecionados = []
        try:
            self.janela_popup_produto.destroy()
        except AttributeError:
            pass

    def atualizar_lista_materiais_selecionados(self):
        
        for item in self.lista_materiais_selecionados.get_children():
            self.lista_materiais_selecionados.delete(item)

        for material in self.materiais_selecionados:
            self.lista_materiais_selecionados.insert("", "end", values=(material["Material ID"], material["Material"], material["Quantidade Utilizada"], locale.currency(material["Valor Gasto"], grouping=True)))

    def popup_erro(self, mensagem):
        popup_erro = tk.Toplevel()
        popup_erro.title("Erro")
        popup_erro.grab_set()

        label_erro = tk.Label(popup_erro, text=mensagem)
        label_erro.pack()

        botao_fechar_erro = tk.Button(popup_erro, text="Fechar", command=popup_erro.destroy)
        botao_fechar_erro.pack()

        self.define_screen_size(popup_erro, 300,60)
    
    # Função para abrir a janela de edição de um material
    def editar_material(self, event):
        selected_item = self.lista_materiais.selection()
        if selected_item:
            item_id = self.lista_materiais.item(selected_item)["values"][0]
            material = encontrar_material_por_id(self, item_id)
            if material:
                self.mostrar_campos_material(material)

    # Função para abrir a janela de edição de um produto
    def editar_produto(self, event):
        carregar_dados(self)
        selected_item = self.lista_produtos.selection()
        if selected_item:
            item_id = self.lista_produtos.item(selected_item)["values"][0]
            produto = encontrar_produto_por_id(self, item_id)
            if produto:
                self.mostrar_campos_produto(produto)

if __name__ == "__main__":
    root = tk.Tk()
    app = SaleMate(root)
    root.mainloop()
