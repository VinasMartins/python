def limpar_campos_resources(self):
    try:
        self.janela_popup_resource.destroy()
    except AttributeError:
        pass

def limpar_campos_produtos(self):
    self.selected_resources = []
    try:
        self.janela_popup_produto.destroy()
    except AttributeError:
        pass