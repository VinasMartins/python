def encontrar_material_por_id(self, material_id):
    for material in self.materiais:
        if material.get("ID") == material_id:
            return material
    return None

# Função para encontrar um produto pelo ID
def encontrar_produto_por_id(self, produto_id):
    for produto in self.produtos:
        if produto.get("ID") == produto_id:
            return produto
    return None

def filter_list(self, filter_by, entity):
    if entity == 'materials':
        for item in self.lista_materiais.get_children():
            valores = self.lista_materiais.item(item, 'values')
            nome = valores[1]
            if filter_by.lower() in nome.lower():
                self.lista_materiais.selection_set(item)
            else:
                self.lista_materiais.selection_remove(item)
    
    if entity == 'products':
        for item in self.lista_produtos.get_children():
            valores = self.lista_produtos.item(item, 'values')
            nome = valores[1]
            if filter_by.lower() in nome.lower():
                self.lista_produtos.selection_set(item)
            else:
                self.lista_produtos.selection_remove(item)

def atualizar_combobox_materiais(self, *args, is_filter=False):
    tipo_produto = self.combobox_tipo.get()
    self.product_type = tipo_produto
    
    texto_pesquisa = self.var_filtro_materiais.get()

    self.combobox_calcula_tempo.config(state='enable')
    self.combobox_calcula_tempo.set("Sim")
    self.janela_popup_produto.title(f"Cadastro de {self.product_type if self.product_type else 'Produto'}")

    if tipo_produto == "Combo":
        self.combobox_calcula_tempo.set("N\u00e3o")
        products = [produto['Nome'] for produto in sorted(self.produtos, key=lambda x: x["Nome"]) if produto["Tipo"] != 'Combo']
        _update_combobox(self, is_filter, texto_pesquisa, products)
    elif tipo_produto == 'Serviço':
        self.combobox_calcula_tempo.set("N\u00e3o")
        combined_list = [f"{produto['Nome']}" for produto in sorted(self.produtos, key=lambda x: x["Nome"])]
        combined_list.extend([f"{material['Nome']} [{material['Unidade de Medida']}]" for material in sorted(self.materiais, key=lambda x: x["Nome"])])
        _update_combobox(self, is_filter, texto_pesquisa, combined_list)
    else:
        self.combobox_tipo.set("Produto")
        materials = [f"{material['Nome']} [{material['Unidade de Medida']}]" for material in sorted(self.materiais, key=lambda x: x["Nome"])]
        _update_combobox(self, is_filter, texto_pesquisa, materials)

def _update_combobox(self, is_filter, texto_pesquisa, items):
    if is_filter:
        self.combobox_materiais['values'] = [item for item in items if texto_pesquisa.lower() in item.lower()]
    else:
        self.combobox_materiais['values'] = items
        