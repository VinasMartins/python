from .score import crawler
resultados = crawler.jogos_ao_vivo()
for resultado in resultados:
	print(f"\nResultado: {resultado} \n")