
import locale

def atualizar_lista(self, lista_widget, lista_dados, tipo):
    lista_dados = sorted(lista_dados, key=lambda x: x["Nome"])
    for item in lista_widget.get_children():
        lista_widget.delete(item)

    if tipo == "materiais":
        for item in lista_dados:
            id = item.get("ID", "")
            nome = item.get("Nome", "")
            quantidade = item.get("Quantidade", "")
            preco_pago = locale.currency(item.get("Valor Pago", 0), grouping=True)
            preco_final = locale.currency(item.get("Preco Unit", 0), grouping=True)
            unidade_medida = item.get("Unidade de Medida", "")

            lista_widget.insert("", "end", values=(id, nome, quantidade, preco_pago, preco_final, unidade_medida))
    elif tipo == "produtos":
        for item in lista_dados:
            id = item.get("ID", "")
            nome = item.get("Nome", "")
            tipo = item.get("Tipo", "")
            materiais = ", ".join([material["Material"] for material in item.get("Materiais", [])])
            preco_custo = locale.currency(item.get("Preco de Custo", 0), grouping=True)
            margem_lucro_atacado = f'{item.get("Margem de Lucro Atacado", 0)}%'
            margem_lucro_varejo = f'{item.get("Margem de Lucro Varejo", 0)}%'
            preco_atacado = locale.currency(item.get("Preco Sugerido Atacado", 0), grouping=True)
            preco_varejo = locale.currency(item.get("Preco Sugerido Varejo", 0), grouping=True)

            lista_widget.insert("", "end", values=(id, nome, tipo, materiais, preco_custo, margem_lucro_atacado, margem_lucro_varejo, preco_atacado, preco_varejo))