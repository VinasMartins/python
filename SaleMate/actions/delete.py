from tkinter import messagebox
from DAO.data import salvar_dados
from resources.refresher import atualizar_lista
    
def excluir_material(self, material):
    nome_material = material["Nome"]
    if nome_material.lower() != "valor hora":
        confirmacao = messagebox.askyesno("Confirmação", "Tem certeza de que deseja excluir este material?")
        if confirmacao:
            self.materiais.remove(material)
            atualizar_lista(self, self.lista_materiais, self.materiais, 'materiais')
            self.limpar_campos_materiais()
            salvar_dados(self, "materials")
    else:
        messagebox.showerror("Operação não permitida!", f"Não é possível excluir o material: {nome_material}")


def excluir_produto(self, produto):
    confirmacao = messagebox.askyesno("Confirmação", "Tem certeza de que deseja excluir este produto?")
    if confirmacao:
        self.produtos.remove(produto)
        atualizar_lista(self, self.lista_produtos, self.produtos, 'produtos')
        self.limpar_campos_produtos()
        salvar_dados(self, "products")

# Função para abrir a janela de edição de um produto
def editar_produto(self, event):
    selected_item = self.lista_produtos.selection()
    if selected_item:
        item_id = self.lista_produtos.item(selected_item)["values"][0]
        produto = encontrar_produto_por_id(self, item_id)
        if produto:
            self.mostrar_campos_produto(produto)

def remove_material_selecionado(self):
    # Pega o item selecionado na lista de materiais
    selected_item = self.lista_materiais_selecionados.selection()
    if selected_item:
        # Pega o item_id do item selecionado
        item_id = self.lista_materiais_selecionados.item(selected_item)["values"][0]
        item_name = self.lista_materiais_selecionados.item(selected_item)["values"][1]
        item_quantity = self.lista_materiais_selecionados.item(selected_item)["values"][2]
        for i, selected_mat in enumerate(self.materiais_selecionados):
            material_id = selected_mat.get("Material ID")
            material_name = selected_mat.get("Material")
            material_qtt = float(selected_mat.get("Quantidade Utilizada"))
            if (material_id == item_id and 
                material_name == item_name and 
                round(material_qtt, 2) == round(float(item_quantity), 2)):
                self.materiais_selecionados.pop(i)
                self.lista_materiais_selecionados.delete(selected_item)
                break  # Saia do loop após encontrar o item correspondente





