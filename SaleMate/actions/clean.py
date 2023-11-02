def limpar_campos_materiais(self):
    try:
        self.janela_popup_material.destroy()
    except AttributeError:
        pass

def limpar_campos_produtos(self):
    self.materiais_selecionados = []
    try:
        self.janela_popup_produto.destroy()
    except AttributeError:
        pass