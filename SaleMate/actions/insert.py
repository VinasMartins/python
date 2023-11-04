from DAO.data import salvar_dados
import uuid
import datetime
from tkinter import messagebox
import tkinter as tk
from resources.refresher import atualizar_lista
from DAO.data import *
from actions.getter import *

def cadastrar_resource(self):
    nome = self.entrada_resource_nome.get()
    quantidade_str = self.entrada_resource_quantidade.get()
    preco_pago_str = self.entrada_resource_preco_pago.get().replace(",", ".")
    unidade_medida = self.combobox_unidade_medida.get()
    actual_date = datetime.date.today().isoformat()

    if nome and quantidade_str.isdigit() and preco_pago_str.replace(".", "").isdigit() and unidade_medida:
        quantidade = int(quantidade_str)
        preco_pago = float(preco_pago_str)
        preco_final = preco_pago / quantidade

        # Gera um UUID exclusivo para o resource
        resource_id = str(uuid.uuid4())

        self.resources.append(
            {"ID": resource_id, "Name": nome, "Quantity": quantidade, "PaidAmount": preco_pago, "UnitPrice": preco_final, "UnitMeasure": unidade_medida, "CreatedAt": actual_date, "UpdatedAt": actual_date}
        )

        atualizar_lista(self, self.lista_resources, self.resources, 'resources')

        self.limpar_campos_resources()

        salvar_dados(self,"resources")
    else:
        self.popup_erro("Por favor, preencha os campos corretamente.")

def cadastrar_valor_hora(self, hour_config_value=None):
    carregar_dados(self)
    exist_resource = self.verify_if_has_hour_value()
    actual_date = datetime.date.today().isoformat()

    if exist_resource == False:
        nome = "Valor Hora"
        quantidade_str = 60
        preco_pago_str = deep_get(self.system_config, "WorkInfo.HourlyRate", 25) #self.system_config["WorkInfo"]["HourlyRate"] if self.system_config else 25
        unidade_medida = "Minutos"

        quantidade = int(quantidade_str)
        preco_pago = float(preco_pago_str)
        preco_final = preco_pago / quantidade
        resource_id = str(uuid.uuid4())

        self.resources.append(
            {"ID": resource_id, "Name": nome, "Quantity": quantidade, "PaidAmount": preco_pago, "UnitPrice": preco_final, "UnitMeasure": unidade_medida, "CreatedAt": actual_date, "UpdatedAt": actual_date}
        )

        salvar_dados(self,"resources")
        atualizar_lista(self, self.lista_resources, self.resources, 'resources')
        messagebox.showinfo("Valor de Produção por Hora Cadastrado","Cadastramos um valor hora padrão nos seus recursos, você pode editar o valor desse recurso a qualquer momento.")
    else:
        for resource in self.resources:
            if resource["Name"].lower() == "valor hora" and hour_config_value:
                resource["PaidAmount"] = hour_config_value
                resource["UnitPrice"] = hour_config_value / resource["Quantity"]
                resource["CreatedAt"] = resource.get("CreatedAt", actual_date)
                resource["CreatedAt"] = resource.get("CreatedAt", actual_date)
                resource["UpdatedAt"] = actual_date
                # Atualize a lista de resources
                atualizar_lista(self, self.lista_resources, self.resources, 'resources')
                salvar_dados(self, "resources")
def cadastrar_produto(self):
    produto_nome = self.entrada_produto_nome.get()
    margem_lucro_atacado_str = self.entrada_margem_lucro_atacado.get().replace("%","").replace(" ","")
    margem_lucro_varejo_str = self.entrada_margem_lucro_varejo.get().replace("%","").replace(" ","")
    calcula_tempo_str = self.combobox_calcula_tempo.get()
    tipo_str = self.combobox_tipo.get()
    
    actual_date = datetime.date.today().isoformat()

    if produto_nome and self.selected_resources:
        margem_lucro_atacado = int(margem_lucro_atacado_str)
        margem_lucro_varejo = int(margem_lucro_varejo_str)
        preco_custo = 0.0
        mao_de_obra_custo = 0.0
        valor_hora_exists = False
        for resource in self.selected_resources:
            if resource["ResourceName"].lower() in ['m\u00e3o de obra', "mao de obra", "valor hora"] and self.product_type != 'Combo':
                mao_de_obra_custo += resource["SpentAmount"]
                valor_hora_exists = True
            elif self.product_type == 'Combo' or self.product_type == 'Servi\u00e7o':
                mao_de_obra_custo += resource["HourValue"]# * resource["UsedQuantity"]
                preco_custo += resource["SpentAmount"]
            else:
                preco_custo += resource["SpentAmount"]
        preco_atacado = (preco_custo)*(1+(margem_lucro_atacado/100))+mao_de_obra_custo
        preco_varejo = (preco_custo)*(1+(margem_lucro_varejo/100))+mao_de_obra_custo

        if preco_atacado <= 0 or preco_varejo <= 0:
            self.popup_erro("O preço final do produto é inválido. Por favor, insira um recurso  válido!")
        else:
            produto_id = str(uuid.uuid4())

            produto = {
                "ID": produto_id,
                "Name": produto_nome,
                "Resources": self.selected_resources,
                "CostPrice": preco_custo,
                "WholesaleProfitMargin": margem_lucro_atacado,
                "RetailProfitMargin": margem_lucro_varejo,
                "WholesaleSuggestedPrice": preco_atacado,
                "RetailSuggestedPrice": preco_varejo,
                "CalculateTimeSpent": calcula_tempo_str,
                "Type": tipo_str,
                "CreatedAt": actual_date,
                "UpdatedAt": actual_date
            }

            if (valor_hora_exists or calcula_tempo_str == 'N\u00e3o') and len(self.selected_resources) >= 1:
                self.produtos.append(produto)
                atualizar_lista(self, self.lista_produtos, self.produtos, 'produtos')
                self.entrada_produto_nome.delete(0, tk.END)
                self.selected_resources = []
                self.atualizar_selected_resources_list()
                self.limpar_campos_produtos()
                salvar_dados(self, "products")
            else:
                self.popup_erro("Por favor, Inclua o recurso: 'Valor Hora'.")
    else:
        self.popup_erro("Por favor, preencha os campos corretamente.")

def adicionar_resource(self):
    quantidade_utilizada_str = self.entrada_quantidade_utilizada.get()
    resource_selecionado = self.combobox_resources.get().split(" [")[0]
    if self.product_type == 'Combo':
        for produto in self.produtos:
            if produto["Name"] == resource_selecionado:
                if quantidade_utilizada_str.replace(".", "").isdigit():
                    quantidade_utilizada = float(quantidade_utilizada_str)
                    valor_hora = 0
                    for resource in produto["Resources"]:
                        if resource["ResourceName"].lower() in ['m\u00e3o de obra', "mao de obra", "valor hora"]:
                            valor_hora += resource["SpentAmount"] * quantidade_utilizada
                    valor_gasto = (quantidade_utilizada * produto["CostPrice"])
                    self.selected_resources.append({
                        "ResourceId": produto["ID"],
                        "ResourceName": produto["Name"],
                        "UnitMeasure": 'Unidades',
                        "UsedQuantity": quantidade_utilizada,
                        "SpentAmount": valor_gasto,
                        "HourValue": valor_hora
                    })
                    self.atualizar_selected_resources_list()
                    self.combobox_resources.set("")
                    self.entrada_quantidade_utilizada.delete(0, tk.END)
                    return
                else:
                    self.popup_erro("A quantidade utilizada deve ser um valor numérico.")
                    return
    elif self.product_type == 'Produto':
        for resource in self.resources:
            if resource["Name"] == resource_selecionado:
                if quantidade_utilizada_str.replace(".", "").isdigit():
                    quantidade_utilizada = float(quantidade_utilizada_str)
                    valor_gasto = quantidade_utilizada * resource["UnitPrice"]
                    self.selected_resources.append({
                        "ResourceId": resource["ID"],
                        "ResourceName": resource["Name"],
                        "UnitMeasure": resource["UnitMeasure"],
                        "UsedQuantity": quantidade_utilizada,
                        "SpentAmount": valor_gasto,
                        "HourValue": 0
                    })
                    self.atualizar_selected_resources_list()
                    self.combobox_resources.set("")
                    self.entrada_quantidade_utilizada.delete(0, tk.END)
                    return
                else:
                    self.popup_erro("A quantidade utilizada deve ser um valor numérico.")
                    return
    else:
        # Verifique em ambos os tipos de recursos (produtos e recursos)
        found = False
        for resource in self.resources:
            if resource["Name"] == resource_selecionado:
                if quantidade_utilizada_str.replace(".", "").isdigit():
                    quantidade_utilizada = float(quantidade_utilizada_str)
                    valor_gasto = quantidade_utilizada * resource["UnitPrice"]
                    self.selected_resources.append({
                        "ResourceId": resource["ID"],
                        "ResourceName": resource["Name"],
                        "UnitMeasure": resource["UnitMeasure"],
                        "UsedQuantity": quantidade_utilizada,
                        "SpentAmount": valor_gasto,
                        "HourValue": 0
                    })
                    self.atualizar_selected_resources_list()
                    self.combobox_resources.set("")
                    self.entrada_quantidade_utilizada.delete(0, tk.END)
                    found = True
                    break

        if not found:
            for produto in self.produtos:
                if produto["Name"] == resource_selecionado:
                    if quantidade_utilizada_str.replace(".", "").isdigit():
                        quantidade_utilizada = float(quantidade_utilizada_str)
                        valor_hora = 0
                        for resource in produto["Resources"]:
                            if resource["ResourceName"].lower() in ['m\u00e3o de obra', "mao de obra", "valor hora"]:
                                valor_hora += resource["SpentAmount"] * quantidade_utilizada
                            else:
                                valor_hora += resource["HourValue"] * quantidade_utilizada
                        valor_gasto = (quantidade_utilizada * produto["CostPrice"])
                        self.selected_resources.append({
                            "ResourceId": produto["ID"],
                            "ResourceName": produto["Name"],
                            "UnitMeasure": 'Unidades',
                            "UsedQuantity": quantidade_utilizada,
                            "SpentAmount": valor_gasto,
                            "HourValue": valor_hora
                        })
                        self.atualizar_selected_resources_list()
                        self.combobox_resources.set("")
                        self.entrada_quantidade_utilizada.delete(0, tk.END)
                        found = True
                        break

        if not found:
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
        "hourly_rate": self.entry_hourly_rate.get().replace(",", "."),
        "limit_time_in_days": self.entry_limit_time_in_days.get().replace(",", "."),
        "remind_update": self.remind_update_var.get()
    }

    try:
        required_fields = ["name", "street", "number", "city", "state", "cep", "neighborhood", "country", "company", "company_code", "hours", "hourly_rate"]
        numeric_fields = ["hours", "hourly_rate"]
        # Validando campos obrigatórios
        for field in required_fields:
            if not config_dict.get(field):
                self.popup_erro(f"O campo '{field}' é obrigatório e precisa estar preenchido corretamente.")
                return

        # Validando campos numéricos
        for field in numeric_fields:
            value = config_dict.get(field)
            if not value.replace(".", "").isdigit():
                self.popup_erro(f"O campo '{field}' deve conter apenas números.")
                return

        self.system_config = {
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
            },
            "SystemConfig": {
                "LimitTimeInDays": int(config_dict["limit_time_in_days"]) if config_dict["limit_time_in_days"] else 90,
                "RemindUpdate": config_dict["remind_update"]
            }
        }

        salvar_dados(self, "config")
      
        self.limpar_campos_config()
        self.show_default_screens()
        cadastrar_valor_hora(self, float(config_dict["hourly_rate"]))
    except Exception as e:
        self.popup_erro(f"Erro ao salvar dados. Erro: {e}")
