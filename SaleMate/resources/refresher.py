
import locale

def atualizar_lista(self, lista_widget, lista_dados, tipo):
    lista_dados = sorted(lista_dados, key=lambda x: x["Name"])
    for item in lista_widget.get_children():
        lista_widget.delete(item)

    if tipo == "resources":
        for item in lista_dados:
            id = item.get("ID", "")
            nome = item.get("Name", "")
            quantidade = item.get("Quantity", "")
            preco_pago = locale.currency(item.get("PaidAmount", 0), grouping=True)
            preco_final = locale.currency(item.get("UnitPrice", 0), grouping=True)
            unidade_medida = item.get("UnitMeasure", "")

            lista_widget.insert("", "end", values=(id, nome, quantidade, preco_pago, preco_final, unidade_medida))
    elif tipo == "produtos":
        for item in lista_dados:
            id = item.get("ID", "")
            nome = item.get("Name", "")
            tipo = item.get("Type", "")
            resources = ", ".join([resource["ResourceName"] for resource in item.get("Resources", [])])
            preco_custo = locale.currency(item.get("CostPrice", 0), grouping=True)
            margem_lucro_atacado = f'{item.get("WholesaleProfitMargin", 0)}%'
            margem_lucro_varejo = f'{item.get("RetailProfitMargin", 0)}%'
            preco_atacado = locale.currency(item.get("WholesaleSuggestedPrice", 0), grouping=True)
            preco_varejo = locale.currency(item.get("RetailSuggestedPrice", 0), grouping=True)

            lista_widget.insert("", "end", values=(id, nome, tipo, resources, preco_custo, margem_lucro_atacado, margem_lucro_varejo, preco_atacado, preco_varejo))