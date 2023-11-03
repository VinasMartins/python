import tkinter as tk

def create_main_menu(self):
    # Criando o menu principal
    menu_principal = tk.Menu(self.janela)
    self.janela.config(menu=menu_principal)

    # Criar um novo menu chamado "Configurações"
    main = tk.Menu(menu_principal, tearoff=0)
    help = tk.Menu(menu_principal, tearoff=0)
    menu_principal.add_cascade(label="Menu Principal", menu=main)
    menu_principal.add_cascade(label="Ajuda", menu=help)

    # Adicione opções de configurações ao menu
    help.add_command(label="Sobre o sistema", command=about_us)
    main.add_command(label="Configurações", command=self.show_config_window)
    main.add_command(label="Sair", command=self.janela.destroy)

def about_us():
    # Crie uma nova janela para a tela "Sobre Nós" apenas quando clicado
    janela_about_us = tk.Toplevel()
    janela_about_us.title("Sobre Nós")
    janela_about_us.iconbitmap('images/logo2.ico')

    # Adicione o conteúdo da tela "Sobre Nós"
    label_sobre_nos = tk.Label(janela_about_us, text="Bem-vindo ao SaleMate! \nEsta é uma aplicação para gerenciamento de vendas e produtos.")
    label_sobre_nos.pack(padx=20, pady=20)

    # Adicione informações de direitos autorais
    copyright_label = tk.Label(janela_about_us, text="\n\n\n© 2023 SaleMate. Todos os direitos reservados.")
    copyright_label.pack(padx=20, pady=5)

    # Botão para fechar a janela "Sobre Nós"
    botao_fechar = tk.Button(janela_about_us, text="Fechar", command=janela_about_us.destroy)
    botao_fechar.pack(padx=20, pady=10)

    # Centralize a janela na tela
    largura_janela = 400  # Defina a largura da janela conforme necessário
    altura_janela = 200  # Defina a altura da janela conforme necessário
    largura_tela = janela_about_us.winfo_screenwidth()
    altura_tela = janela_about_us.winfo_screenheight()
    x = (largura_tela - largura_janela) // 2
    y = (altura_tela - altura_janela) // 2
    janela_about_us.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")