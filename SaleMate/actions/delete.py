from tkinter import messagebox
from DAO.data import salvar_dados
from resources.refresher import atualizar_lista
    
def excluir_resource(self, resource):
    nome_resource = resource["Name"]
    if nome_resource.lower() != "valor hora":
        confirmacao = messagebox.askyesno("Confirmação", "Tem certeza de que deseja excluir este resource?")
        if confirmacao:
            self.resources.remove(resource)
            atualizar_lista(self, self.lista_resources, self.resources, 'resources')
            self.limpar_campos_resources()
            salvar_dados(self, "resources")
    else:
        messagebox.showerror("Operação não permitida!", f"Não é possível excluir o resource: {nome_resource}")


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

def remove_resource_selecionado(self):
    # Pega o item selecionado na lista de resources
    selected_item = self.selected_resources_list.selection()
    if selected_item:
        # Pega o item_id do item selecionado
        item_id = self.selected_resources_list.item(selected_item)["values"][0]
        item_name = self.selected_resources_list.item(selected_item)["values"][1]
        item_quantity = self.selected_resources_list.item(selected_item)["values"][2]
        for i, selectedresource in enumerate(self.selected_resources):
            resource_id = selectedresource.get("ResourceId")
            resource_name = selectedresource.get("ResourceName")
            resource_qtt = float(selectedresource.get("UsedQuantity"))
            if (resource_id == item_id and 
                resource_name == item_name and 
                round(resource_qtt, 2) == round(float(item_quantity), 2)):
                self.selected_resources.pop(i)
                self.selected_resources_list.delete(selected_item)
                break  # Saia do loop após encontrar o item correspondente





