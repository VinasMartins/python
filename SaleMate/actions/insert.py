from DAO.data import salvar_dados
import uuid
import json
from tkinter import messagebox
import tkinter as tk
from resources.refresher import atualizar_lista
import json
import os
from DAO.data import *
from actions.getter import *

def cadastrar_material(self):
    nome = self.entrada_material_nome.get()
    quantidade_str = self.entrada_material_quantidade.get()
    preco_pago_str = self.entrada_material_preco_pago.get().replace(",", ".")
    unidade_medida = self.combobox_unidade_medida.get()

    if nome and quantidade_str.isdigit() and preco_pago_str.replace(".", "").isdigit() and unidade_medida:
        quantidade = int(quantidade_str)
        preco_pago = float(preco_pago_str)
        preco_final = preco_pago / quantidade

        # Gera um UUID exclusivo para o material
        material_id = str(uuid.uuid4())

        self.materiais.append(
            {"ID": material_id, "Nome": nome, "Quantidade": quantidade, "Valor Pago": preco_pago, "Preco Unit": preco_final, "Unidade de Medida": unidade_medida}
        )

        atualizar_lista(self, self.lista_materiais, self.materiais, 'materiais')

        self.limpar_campos_materiais()

        salvar_dados(self,"materials")
    else:
        self.popup_erro("Por favor, preencha os campos corretamente.")

def cadastrar_valor_hora(self):
    carregar_dados(self)
    exist_material = self.verify_if_has_hour_value()

    if exist_material == False:
        nome = "Valor Hora"
        quantidade_str = 60
        preco_pago_str = deep_get(self.system_config, "WorkInfo.HourlyRate", 25) #self.system_config["WorkInfo"]["HourlyRate"] if self.system_config else 25
        unidade_medida = "Minutos"

        quantidade = int(quantidade_str)
        preco_pago = float(preco_pago_str)
        preco_final = preco_pago / quantidade
        material_id = str(uuid.uuid4())

        self.materiais.append(
            {"ID": material_id, "Nome": nome, "Quantidade": quantidade, "Valor Pago": preco_pago, "Preco Unit": preco_final, "Unidade de Medida": unidade_medida}
        )

        salvar_dados(self,"materials")
        atualizar_lista(self, self.lista_materiais, self.materiais, 'materiais')
        messagebox.showinfo("Valor de Produção por Hora Cadastrado","Cadastramos um valor hora padrão nos seus recursos, você pode editar o valor desse recurso a qualquer momento.")

def cadastrar_produto(self):
    produto_nome = self.entrada_produto_nome.get()
    margem_lucro_atacado_str = self.entrada_margem_lucro_atacado.get().replace("%","").replace(" ","")
    margem_lucro_varejo_str = self.entrada_margem_lucro_varejo.get().replace("%","").replace(" ","")
    calcula_tempo_str = self.combobox_calcula_tempo.get()
    tipo_str = self.combobox_tipo.get()

    if produto_nome and self.materiais_selecionados:
        margem_lucro_atacado = int(margem_lucro_atacado_str)
        margem_lucro_varejo = int(margem_lucro_varejo_str)
        preco_custo = 0.0
        mao_de_obra_custo = 0.0
        valor_hora_exists = False
        for material in self.materiais_selecionados:
            
            if material["Material"].lower() in ['m\u00e3o de obra', "mao de obra", "valor hora"] and self.product_type != 'Combo':
                mao_de_obra_custo += material["Valor Gasto"]
                valor_hora_exists = True
            elif self.product_type == 'Combo':
                mao_de_obra_custo += material["Valor Hora"] * material["Quantidade Utilizada"]
                preco_custo += material["Valor Gasto"]
            else:
                preco_custo += material["Valor Gasto"]
        preco_atacado = (preco_custo)*(1+(margem_lucro_atacado/100))+mao_de_obra_custo
        preco_varejo = (preco_custo)*(1+(margem_lucro_varejo/100))+mao_de_obra_custo

        if preco_atacado <= 0 or preco_varejo <= 0:
            self.popup_erro("O preço final do produto é inválido. Por favor, insira um recurso  válido!")
        else:
            produto_id = str(uuid.uuid4())

            produto = {
                "ID": produto_id,
                "Nome": produto_nome,
                "Materiais": self.materiais_selecionados,
                "Preco de Custo": preco_custo,
                "Margem de Lucro Atacado": margem_lucro_atacado,
                "Margem de Lucro Varejo": margem_lucro_varejo,
                "Preco Sugerido Atacado": preco_atacado,
                "Preco Sugerido Varejo": preco_varejo,
                "Calcula Tempo Gasto": calcula_tempo_str,
                "Tipo": tipo_str
            }

            if (valor_hora_exists or calcula_tempo_str == 'N\u00e3o') and len(self.materiais_selecionados) >= 1:
                self.produtos.append(produto)
                atualizar_lista(self, self.lista_produtos, self.produtos, 'produtos')
                self.entrada_produto_nome.delete(0, tk.END)
                self.materiais_selecionados = []
                self.atualizar_lista_materiais_selecionados()
                self.limpar_campos_produtos()
                salvar_dados(self, "products")
            else:
                self.popup_erro("Por favor, Inclua o recurso: 'Valor Hora'.")
    else:
        self.popup_erro("Por favor, preencha os campos corretamente.")

def adicionar_material(self):
    quantidade_utilizada_str = self.entrada_quantidade_utilizada.get()
    material_selecionado = self.combobox_materiais.get().split(" [")[0]
    if self.product_type == 'Combo':
        for produto in self.produtos:
            if produto["Nome"] == material_selecionado:
                if quantidade_utilizada_str.replace(".", "").isdigit():
                    quantidade_utilizada = float(quantidade_utilizada_str)
                    valor_hora = 0
                    for material in produto["Materiais"]:
                        if material["Material"].lower() in ['m\u00e3o de obra', "mao de obra", "valor hora"]:
                            valor_hora += material["Valor Gasto"]
                    valor_gasto = (quantidade_utilizada * produto["Preco de Custo"])#+valor_hora
                    self.materiais_selecionados.append({
                        "Material ID": produto["ID"],
                        "Material": produto["Nome"],
                        "Unidade de Medida": 'Unidades',
                        "Quantidade Utilizada": quantidade_utilizada,
                        "Valor Gasto": valor_gasto,
                        "Valor Hora": valor_hora
                    })
                    self.atualizar_lista_materiais_selecionados()
                    self.combobox_materiais.set("")
                    self.entrada_quantidade_utilizada.delete(0, tk.END)
                    return
                else:
                    self.popup_erro("A quantidade utilizada deve ser um valor numérico.")
                    return
    else:
        for material in self.materiais:
            if material["Nome"] == material_selecionado:
                if quantidade_utilizada_str.replace(".", "").isdigit():
                    quantidade_utilizada = float(quantidade_utilizada_str)
                    valor_gasto = quantidade_utilizada * material["Preco Unit"]
                    self.materiais_selecionados.append({
                        "Material ID": material["ID"],
                        "Material": material["Nome"],
                        "Unidade de Medida": material["Unidade de Medida"],
                        "Quantidade Utilizada": quantidade_utilizada,
                        "Valor Gasto": valor_gasto
                    })
                    self.atualizar_lista_materiais_selecionados()
                    self.combobox_materiais.set("")
                    self.entrada_quantidade_utilizada.delete(0, tk.END)
                    return
                else:
                    self.popup_erro("A quantidade utilizada deve ser um valor numérico.")
                    return

    self.popup_erro("Selecione um recurso/produto válido.")

def save_config_to_json(self):
    config_dict = {
        "name": self.entry_name.get(),
        "email": self.entry_email.get(),
        "street": self.entry_street.get(),
        "number": self.entry_number.get(),
        "city": self.entry_city.get(),
        "state": self.entry_state.get(),
        "cep": self.entry_cep.get(),
        "neighborhood": self.entry_neighborhood.get(),
        "country": self.combo_country.get(),
        "company":self.entry_company_name.get(),
        "company_code":self.entry_company_code_cnpj_cpf.get(),
        "hours": self.entry_hours.get(),
        "hourly_rate": self.entry_hourly_rate.get().replace(",", ".")
    }

    __file_path = os.path.join(os.getcwd(), 'databases')
    

    try:
        required_fields = ["name", "street", "number", "city", "state", "cep", "neighborhood", "country", "company", "company_code", "hours", "hourly_rate"]
        numeric_fields = ["cep", "hours", "hourly_rate"]
        # Validando campos obrigatórios
        for field in required_fields:
            if not config_dict.get(field):
                self.popup_erro(f"O campo '{field}' é obrigatório e não pode estar vazio.")
                return

        # Validando campos numéricos
        for field in numeric_fields:
            value = config_dict.get(field)
            if not value.replace(".", "").isdigit():
                self.popup_erro(f"O campo '{field}' deve conter apenas números.")
                return

        config_data = {
            "Name": config_dict["name"],
            "Email": config_dict["email"],
            "Address": {
                "Street": config_dict["street"],
                "Number": config_dict["number"],
                "City": config_dict["city"],
                "State": config_dict["state"],
                "CEP": config_dict["cep"],
                "Neighborhood": config_dict["neighborhood"],
                "Country": config_dict["country"]
            },
            "WorkInfo": {
                "Company": config_dict["company"],
                "CompanyCode": config_dict["company_code"],
                "HoursPerDay": float(config_dict["hours"]),
                "HourlyRate": float(config_dict["hourly_rate"])
            }
        }
        
        with open(f'{__file_path}/config.json', 'w') as config_file:
            json.dump(config_data, config_file, indent=4)
        
      
        self.limpar_campos_config()
        self.show_default_screens()
        cadastrar_valor_hora(self)
    except Exception as e:
        self.popup_erro(f"Erro ao salvar dados. Erro: {e}")
