from DAO.data import salvar_dados
from resources.refresher import atualizar_lista
import datetime

def atualizar_resource(self, resource):
    nome = self.entrada_resource_nome.get()
    quantidade_str = self.entrada_resource_quantidade.get()
    preco_pago_str = self.entrada_resource_preco_pago.get().replace(",", ".")
    unidade_medida = self.combobox_unidade_medida.get()
    actual_date = datetime.date.today().isoformat()

    if nome and quantidade_str.isdigit() and preco_pago_str.replace(".", "").isdigit() and unidade_medida:
        quantidade = int(quantidade_str)
        preco_pago = float(preco_pago_str)
        preco_final = preco_pago / quantidade

        # Atualize os valores do resource
        resource["Name"] = nome
        resource["Quantity"] = quantidade
        resource["PaidAmount"] = preco_pago
        resource["UnitPrice"] = preco_final
        resource["UnitMeasure"] = unidade_medida
        resource["CreatedAt"] = resource.get("CreatedAt", actual_date)
        resource["UpdatedAt"] = actual_date

        # Atualize a lista de resources
        atualizar_lista(self, self.lista_resources, self.resources, 'resources')

        # Feche a janela de edição de resource
        self.limpar_campos_resources()
        salvar_dados(self, "resources")
        if nome.lower() == 'valor hora':
            self.system_config["WorkInfo"]["HourlyRate"] = preco_pago
            salvar_dados(self, "config")
    else:
        self.popup_erro("Por favor, preencha os campos corretamente.")

def atualizar_produto(self, produto):
    nome = self.entrada_produto_nome.get()
    margem_lucro_atacado_str = self.entrada_margem_lucro_atacado.get().replace("%","").replace(" ","")
    margem_lucro_varejo_str = self.entrada_margem_lucro_varejo.get().replace("%","").replace(" ","")
    resources = self.selected_resources
    calcula_tempo_str = self.combobox_calcula_tempo.get()
    tipo_str = self.combobox_tipo.get()
    actual_date = datetime.date.today().isoformat()

    if nome and resources:
        margem_lucro_atacado = int(margem_lucro_atacado_str)
        margem_lucro_varejo = int(margem_lucro_varejo_str)
        preco_custo = 0.0
        mao_de_obra_custo = 0.0
        valor_hora_exists = False
        for resource in resources:
            if resource["ResourceName"].lower() in ['m\u00e3o de obra', "mao de obra", "valor hora"] and self.product_type != 'Combo':
                mao_de_obra_custo += resource["SpentAmount"]
                valor_hora_exists = True
            elif self.product_type == 'Combo' or self.product_type == 'Servi\u00e7o':
                mao_de_obra_custo += resource["HourValue"]# * resource["UsedQuantity"]
                preco_custo += resource["SpentAmount"]
            else:
                preco_custo += resource["SpentAmount"]
            print(mao_de_obra_custo)
        preco_atacado = (preco_custo)*(1+(margem_lucro_atacado/100))+mao_de_obra_custo
        preco_varejo = (preco_custo)*(1+(margem_lucro_varejo/100))+mao_de_obra_custo
        if (valor_hora_exists == True or calcula_tempo_str == 'N\u00e3o'):
            if len(resources) >= 1 and (preco_atacado > 0 or preco_varejo > 0):
                # Atualize os valores do produto
                produto["Name"] = nome
                produto["WholesaleProfitMargin"] = margem_lucro_atacado
                produto["RetailProfitMargin"] = margem_lucro_varejo
                produto["CostPrice"] = preco_custo
                produto["WholesaleSuggestedPrice"] = preco_atacado
                produto["RetailSuggestedPrice"] = preco_varejo
                produto["CalculateTimeSpent"] = calcula_tempo_str
                produto["Type"] = tipo_str
                produto["CreatedAt"] = produto.get("CreatedAt", actual_date)
                produto["UpdatedAt"] = actual_date

                # Atualize a lista de produtos
                atualizar_lista(self, self.lista_produtos, self.produtos, 'produtos')

                # Feche a janela de edição de produto
                self.limpar_campos_produtos()
                salvar_dados(self, "products")
            else:
                self.popup_erro("O preço final do produto é inválido. Por favor, insira um recurso válido!")
        else:
            self.popup_erro("Por favor, Inclua o resource: 'Valor Hora'.")
            
    else:
        self.popup_erro("Por favor, preencha os campos corretamente.")