def encontrar_resource_por_id(self, resource_id):
    for resource in self.resources:
        if resource.get("ID") == resource_id:
            return resource
    return None

# Função para encontrar um produto pelo ID
def encontrar_produto_por_id(self, produto_id):
    for produto in self.produtos:
        if produto.get("ID") == produto_id:
            return produto
    return None

def filter_list(self, filter_by, entity):
    if entity == 'resources':
        for item in self.lista_resources.get_children():
            valores = self.lista_resources.item(item, 'values')
            nome = valores[1]
            if filter_by.lower() in nome.lower():
                self.lista_resources.selection_set(item)
            else:
                self.lista_resources.selection_remove(item)
    
    if entity == 'products':
        for item in self.lista_produtos.get_children():
            valores = self.lista_produtos.item(item, 'values')
            nome = valores[1]
            if filter_by.lower() in nome.lower():
                self.lista_produtos.selection_set(item)
            else:
                self.lista_produtos.selection_remove(item)

def update_combobox_resources(self, *args, is_filter=False):
    tipo_produto = self.combobox_tipo.get()
    self.product_type = tipo_produto
    
    texto_pesquisa = self.var_filtro_resources.get()

    self.combobox_calcula_tempo.config(state='enable')
    self.combobox_calcula_tempo.set("Sim")
    self.janela_popup_produto.title(f"Cadastro de {self.product_type if self.product_type else 'Produto'}")

    if tipo_produto == "Combo":
        self.combobox_calcula_tempo.set("N\u00e3o")
        products = [produto['Name'] for produto in sorted(self.produtos, key=lambda x: x["Name"]) if produto["Type"] != 'Combo']
        _update_combobox(self, is_filter, texto_pesquisa, products)
    elif tipo_produto == 'Serviço':
        self.combobox_calcula_tempo.set("N\u00e3o")
        combined_list = [f"{produto['Name']}" for produto in sorted(self.produtos, key=lambda x: x["Name"])]
        combined_list.extend([f"{resource['Name']} [{resource['UnitMeasure']}]" for resource in sorted(self.resources, key=lambda x: x["Name"])])
        _update_combobox(self, is_filter, texto_pesquisa, combined_list)
    else:
        self.combobox_tipo.set("Produto")
        resources = [f"{resource['Name']} [{resource['UnitMeasure']}]" for resource in sorted(self.resources, key=lambda x: x["Name"])]
        _update_combobox(self, is_filter, texto_pesquisa, resources)

def _update_combobox(self, is_filter, texto_pesquisa, items):
    if is_filter:
        self.combobox_resources['values'] = [item for item in items if texto_pesquisa.lower() in item.lower()]
    else:
        self.combobox_resources['values'] = items
        