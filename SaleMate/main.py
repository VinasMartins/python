import tkinter as tk
from tkinter import ttk, messagebox
import locale
import datetime
from resources.catalog_tab import create_catalog_tab
from resources.resources_tab import create_resources_tab
from resources.main_menu import create_main_menu
from resources.refresher import *
from DAO.data import *
from actions.delete import *
from actions.filter import *
from actions.insert import *
from actions.update import *

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

        self.actual_date = datetime.date.today()

        self.resources = []
        self.produtos = []
        self.selected_resources = []
        self.selected_resources_list = None
        self.system_config = None
        self.has_default_screen = False
        self.remind_update_var = tk.BooleanVar()
        
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
        # Verifique se já existe um resource com o nome "Valor Hora"
        value = False
        for resource in self.resources:
            if resource["Name"].lower() == "valor hora":
                value = True
        return value


    def show_default_screens(self):

        if not self.has_default_screen:
            self.abas = ttk.Notebook(self.janela)
            self.aba_resources = ttk.Frame(self.abas)
            self.aba_produtos = ttk.Frame(self.abas)

            create_main_menu(self)
            self.abas.add(self.aba_resources, text="Recursos")
            self.abas.add(self.aba_produtos, text="Catálogo")

            self.abas.pack(fill='both', expand=True)

            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

            create_resources_tab(self)
            create_catalog_tab(self)

            atualizar_lista(self, self.lista_resources, self.resources, 'resources')
            atualizar_lista(self, self.lista_produtos, self.produtos, 'produtos')

            self.has_default_screen = True
    
    def mostrar_campos_resource(self, resource=None):
        self.limpar_campos_resources()
        print(resource)

        # Cria uma janela popup para a edição de resources
        self.janela_popup_resource = tk.Toplevel(self.aba_resources)
        self.janela_popup_resource.title("Cadastro de Recurso")
        self.janela_popup_resource.iconbitmap('images/logo2.ico')

        self.define_screen_size(self.janela_popup_resource, 580,180)

        frame_popup_resource = ttk.Frame(self.janela_popup_resource)
        frame_popup_resource.pack(padx=10, pady=10, fill='both', expand=True)

        self.label_resource_nome = ttk.Label(frame_popup_resource, text="Nome:")
        self.entrada_resource_nome = ttk.Entry(frame_popup_resource, width=70)

        self.label_resource_quantidade = ttk.Label(frame_popup_resource, text="Quantidade:")
        self.entrada_resource_quantidade = ttk.Entry(frame_popup_resource, width=70)

        self.label_resource_preco_pago = ttk.Label(frame_popup_resource, text="Valor (R$):")
        self.entrada_resource_preco_pago = ttk.Entry(frame_popup_resource, width=70)

        self.label_resource_unidade_medida = ttk.Label(frame_popup_resource, text="Unidade de Medida:")
        self.combobox_unidade_medida = ttk.Combobox(frame_popup_resource, values=self.unidades_medida, width=67)
        self.botao_cancelar_resource = ttk.Button(frame_popup_resource, text="Cancelar", command=self.limpar_campos_resources, style='Red.TButton')

        if resource:
            self.entrada_resource_nome.insert(0, resource["Name"])  # Preencha com o nome atual do resource
            self.entrada_resource_quantidade.insert(0, str(resource["Quantity"]))  # Preencha com a quantidade atual do resource
            self.entrada_resource_preco_pago.insert(0, str(resource["PaidAmount"]))  # Preencha com o valor pago atual do resource
            self.combobox_unidade_medida.set(resource["UnitMeasure"])  # Selecione a unidade de medida atual do resource
            self.entrada_resource_nome.config(state='disabled')
            self.combobox_unidade_medida.config(state='disabled')
            self.botao_atualizar_resource = ttk.Button(frame_popup_resource, text="Salvar Edição", command=lambda: atualizar_resource(self, resource), style='Blue.TButton')
            self.botao_excluir_resource = ttk.Button(frame_popup_resource, text="Excluir", command=lambda: excluir_resource(self, resource), style='Orange.TButton')
            # Verifica se o nome do resource é "Valor Hora" para desabilitar todos os campos
            if resource["Name"].lower() == "valor hora":
                self.entrada_resource_quantidade.config(state='disabled')
                self.entrada_resource_preco_pago.config(state='enabled')
            else:
                self.botao_excluir_resource.grid(row=4, column=1, padx=100, pady=5, columnspan=2, sticky=tk.E)
        else:
            self.botao_atualizar_resource = ttk.Button(frame_popup_resource, text="Salvar", command=lambda: cadastrar_resource(self), style='Green.TButton')

        self.label_resource_nome.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entrada_resource_nome.grid(row=0, column=1, padx=5, pady=5)
        self.label_resource_unidade_medida.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.combobox_unidade_medida.grid(row=1, column=1, padx=5, pady=5)
        self.label_resource_quantidade.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.entrada_resource_quantidade.grid(row=2, column=1, padx=5, pady=5)
        self.label_resource_preco_pago.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.entrada_resource_preco_pago.grid(row=3, column=1, padx=5, pady=5)
        self.botao_atualizar_resource.grid(row=4, column=0, padx=5, pady=5, columnspan=2, sticky=tk.W)
        self.botao_cancelar_resource.grid(row=4, column=1, padx=5, pady=5, columnspan=2, sticky=tk.E)
    
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
        self.combobox_tipo.bind("<<ComboboxSelected>>", lambda event: update_combobox_resources(self))
        
        self.label_calcula_tempo = ttk.Label(frame_popup_produto, text="Calcular Valor Hora?")
        self.combobox_calcula_tempo = ttk.Combobox(frame_popup_produto, values=self.boolean_values, width=67)

        self.label_product_resources = ttk.Label(frame_popup_produto, text="Recursos Utilizados (selecione):")
        self.var_filtro_resources = tk.StringVar() 
        self.combobox_resources = ttk.Combobox(frame_popup_produto, textvariable=self.var_filtro_resources, width=67)
        self.label_quantidade_utilizada = ttk.Label(frame_popup_produto, text="Quantidade Utilizada:")
        self.entrada_quantidade_utilizada = ttk.Entry(frame_popup_produto, width=50)
        self.botao_adicionar_resource = ttk.Button(frame_popup_produto, text="Adicionar Recurso", command=lambda: adicionar_resource(self), style='Blue.TButton')

        self.botao_cancelar_produto = ttk.Button(frame_popup_produto, text="Cancelar", command=self.limpar_campos_produtos, style='Red.TButton')
        
        # Vincula a função de filtro ao Combobox
        self.var_filtro_resources.trace_add('write', lambda *args: update_combobox_resources(self, is_filter=True))

        self.selected_resources_list = ttk.Treeview(frame_popup_produto, columns=("ResourceId", "ResourceName", "UsedQuantity", "SpentAmount"))
        self.selected_resources_list.heading("#0", text="", anchor=tk.W)
        self.selected_resources_list.heading("#1", text="ID", anchor=tk.W)
        self.selected_resources_list.heading("#2", text="Nome do Recurso")
        self.selected_resources_list.heading("#3", text="Quantidade Utilizada")
        self.selected_resources_list.heading("#4", text="Valor Gasto")
        self.selected_resources_list.column("#0", width=0, stretch=tk.NO)
        self.selected_resources_list.column("#1", width=0, stretch=tk.NO)
        self.selected_resources_list.bind("<Double-1>", lambda event: remove_resource_selecionado(self))

        if produto:
            self.selected_resources = produto["Resources"]
            self.entrada_produto_nome.insert(0, produto["Name"])  # Preencha com o nome atual do produto
            self.entrada_margem_lucro_atacado.insert(0, produto["WholesaleProfitMargin"])  # Preencha com a margem de lucro atual do produto
            self.entrada_margem_lucro_varejo.insert(0, produto["RetailProfitMargin"])  # Preencha com a margem de lucro atual do produto
            self.combobox_tipo.insert(0, produto["Type"])  # Preencha com o tipo do produto
            self.combobox_calcula_tempo.insert(0, produto["CalculateTimeSpent"])  # Preencha com o booleano se calcula ou nao o tempo gasto
            self.atualizar_selected_resources_list()
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
        self.label_product_resources.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.combobox_resources.grid(row=5, column=1, padx=5, pady=5)
        self.label_quantidade_utilizada.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.entrada_quantidade_utilizada.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        self.botao_adicionar_resource.grid(row=6, column=0, padx=5, pady=5, columnspan=2, sticky=tk.E)
        self.selected_resources_list.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
        self.botao_atualizar_produto.grid(row=8, column=0, padx=5, pady=5, columnspan=2, sticky=tk.W)
        self.botao_cancelar_produto.grid(row=8, column=1, padx=5, pady=5, columnspan=2, sticky=tk.E)

        update_combobox_resources(self, True)

    def show_config_window(self):

        carregar_dados(self)

        self.window_configs = tk.Toplevel()
        self.window_configs.title("Configurações")
        self.window_configs.iconbitmap('images/logo2.ico')

        self.frame_popup_config = ttk.Frame(self.window_configs)
        self.frame_popup_config.pack(padx=10, pady=10, fill='both', expand=True)

        self.define_screen_size(self.window_configs, 830,410)

        # Informações pessoais
        self.label_personal_info = ttk.Label(self.frame_popup_config, text="Dados Pessoais do Usuário", font=("TkDefaultFont", 12, "bold"))
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
        self.label_work_info = ttk.Label(self.frame_popup_config, text="Informações da Empresa", font=("TkDefaultFont", 12, "bold"))
        self.label_work_info.grid(row=10, column=0, columnspan=4, padx=5, pady=5, sticky="w")

        self.label_company_name = ttk.Label(self.frame_popup_config, text="Nome da Empresa:")
        self.entry_company_name = ttk.Entry(self.frame_popup_config, width=40)
        self.label_company_code_cnpj_cpf = ttk.Label(self.frame_popup_config, text="CNPJ/CPF:")
        self.entry_company_code_cnpj_cpf = ttk.Entry(self.frame_popup_config, width=40)
        self.label_hours = ttk.Label(self.frame_popup_config, text="Horas de Trabalho p/ dia:")
        self.entry_hours = ttk.Entry(self.frame_popup_config, width=10)
        self.label_hourly_rate = ttk.Label(self.frame_popup_config, text="Valor da Hora:")
        self.entry_hourly_rate = ttk.Entry(self.frame_popup_config, width=10)

        # Campos de sistema
        self.label_work_info = ttk.Label(self.frame_popup_config, text="Configurações do Sistema", font=("TkDefaultFont", 12, "bold"))
        self.label_work_info.grid(row=13, column=0, columnspan=4, padx=5, pady=5, sticky="w")

        self.label_limit_time_in_days = ttk.Label(self.frame_popup_config, text="Dias para Atualização:")
        self.entry_limit_time_in_days = ttk.Entry(self.frame_popup_config, width=40)

        self.label_remind_update = ttk.Label(self.frame_popup_config, text="Lembrete de Atualização:")
        self.checkbox_remind_update = tk.Checkbutton(self.frame_popup_config, variable=self.remind_update_var)

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

        self.label_limit_time_in_days.grid(row=14, column=0, columnspan=4, padx=5, pady=5, sticky="w")
        self.entry_limit_time_in_days.grid(row=14, column=1, columnspan=4, padx=5, pady=5, sticky="w")
        self.label_remind_update.grid(row=14, column=2, padx=5, pady=5, sticky="w")
        self.checkbox_remind_update.grid(row=14, column=3, padx=5, pady=5, sticky="w")

        self.save_config_button = ttk.Button(self.frame_popup_config, text="Salvar", command=lambda: save_config_to_json(self),style='Green.TButton')
        self.cancel_config_button = ttk.Button(self.frame_popup_config, text="Cancelar", command=self.limpar_campos_config, style='Red.TButton')

        self.save_config_button.grid(row=15, column=0, padx=5, pady=5, columnspan=2, sticky="w")
        self.cancel_config_button.grid(row=15, column=2, padx=5, pady=5, columnspan=2, sticky="e")

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
            self.entry_limit_time_in_days.insert(0, self.system_config["SystemConfig"]["LimitTimeInDays"])
            if self.system_config and "SystemConfig" in self.system_config and "RemindUpdate" in self.system_config["SystemConfig"]:
                remind_update = self.system_config["SystemConfig"]["RemindUpdate"]
                if remind_update:
                    self.checkbox_remind_update.select()
                else:
                    self.checkbox_remind_update.deselect()
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

    def limpar_campos_resources(self):
        try:
            self.janela_popup_resource.destroy()
        except AttributeError:
            pass

    def limpar_campos_produtos(self):
        self.selected_resources = []
        try:
            self.janela_popup_produto.destroy()
        except AttributeError:
            pass

    def atualizar_selected_resources_list(self):
        
        for item in self.selected_resources_list.get_children():
            self.selected_resources_list.delete(item)

        for resource in self.selected_resources:
            self.selected_resources_list.insert("", "end", values=(resource["ResourceId"], resource["ResourceName"], resource["UsedQuantity"], locale.currency(resource["SpentAmount"], grouping=True)))

    def popup_erro(self, mensagem):
        popup_erro = tk.Toplevel()
        popup_erro.title("Erro")
        popup_erro.grab_set()

        label_erro = tk.Label(popup_erro, text=mensagem)
        label_erro.pack()

        botao_fechar_erro = tk.Button(popup_erro, text="Fechar", command=popup_erro.destroy)
        botao_fechar_erro.pack()

        self.define_screen_size(popup_erro, 500,60)
    
    # Função para abrir a janela de edição de um resource
    def editar_resource(self, event):
        selected_item = self.lista_resources.selection()
        if selected_item:
            item_id = self.lista_resources.item(selected_item)["values"][0]
            resource = encontrar_resource_por_id(self, item_id)
            if resource:
                self.mostrar_campos_resource(resource)

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
