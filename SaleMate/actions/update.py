from DAO.data import salvar_dados
from resources.refresher import atualizar_lista

def atualizar_material(self, material):
    nome = self.entrada_material_nome.get()
    quantidade_str = self.entrada_material_quantidade.get()
    preco_pago_str = self.entrada_material_preco_pago.get().replace(",", ".")
    unidade_medida = self.combobox_unidade_medida.get()

    if nome and quantidade_str.isdigit() and preco_pago_str.replace(".", "").isdigit() and unidade_medida:
        quantidade = int(quantidade_str)
        preco_pago = float(preco_pago_str)
        preco_final = preco_pago / quantidade

        # Atualize os valores do material
        material["Nome"] = nome
        material["Quantidade"] = quantidade
        material["Valor Pago"] = preco_pago
        material["Preco Unit"] = preco_final
        material["Unidade de Medida"] = unidade_medida

        # Atualize a lista de materiais
        atualizar_lista(self, self.lista_materiais, self.materiais, 'materiais')

        # Feche a janela de edição de material
        self.limpar_campos_materiais()
        salvar_dados(self, "materials")
    else:
        self.popup_erro("Por favor, preencha os campos corretamente.")

def atualizar_produto(self, produto):
    nome = self.entrada_produto_nome.get()
    margem_lucro_atacado_str = self.entrada_margem_lucro_atacado.get().replace("%","").replace(" ","")
    margem_lucro_varejo_str = self.entrada_margem_lucro_varejo.get().replace("%","").replace(" ","")
    materiais = self.materiais_selecionados
    calcula_tempo_str = self.combobox_calcula_tempo.get()
    tipo_str = self.combobox_tipo.get()

    if nome and materiais:
        margem_lucro_atacado = int(margem_lucro_atacado_str)
        margem_lucro_varejo = int(margem_lucro_varejo_str)
        preco_custo = 0.0
        mao_de_obra_custo = 0.0
        valor_hora_exists = False
        for material in materiais:
            
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
        if (valor_hora_exists == True or calcula_tempo_str == 'N\u00e3o'):
            if len(materiais) >= 1 and (preco_atacado > 0 or preco_varejo > 0):
                # Atualize os valores do produto
                produto["Nome"] = nome
                produto["Margem de Lucro Atacado"] = margem_lucro_atacado
                produto["Margem de Lucro Varejo"] = margem_lucro_varejo
                produto["Preco de Custo"] = preco_custo
                produto["Preco Sugerido Atacado"] = preco_atacado
                produto["Preco Sugerido Varejo"] = preco_varejo
                produto["Calcula Tempo Gasto"] = calcula_tempo_str
                produto["Tipo"] = tipo_str

                # Atualize a lista de produtos
                atualizar_lista(self, self.lista_produtos, self.produtos, 'produtos')

                # Feche a janela de edição de produto
                self.limpar_campos_produtos()
                salvar_dados(self, "products")
            else:
                self.popup_erro("O preço final do produto é inválido. Por favor, insira um recurso válido!")
        else:
            self.popup_erro("Por favor, Inclua o material: 'Valor Hora'.")
            
    else:
        self.popup_erro("Por favor, preencha os campos corretamente.")