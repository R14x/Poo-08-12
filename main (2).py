from datetime import date

# Classe base (HERANÇA)
class Entidade:
    def __init__(self, id):
        self.id = id

# Classe Passageiros herda de Entidade (HERANÇA)
class Passageiros(Entidade):
    def __init__(self, id, nome, cpf, nacionalidade, data_nasc, genero, pet):
        super().__init__(id)
        self.nome = nome
        self.cpf = cpf
        self.nacionalidade = nacionalidade
        self.data_nasc = data_nasc
        self.genero = genero
        self.pet = pet

# Classe Voo herda de Entidade (HERANÇA)
class Voo(Entidade):
    def __init__(self, id, origem, destino, data_voo, num_viajantes):
        super().__init__(id)
        self.origem = origem
        self.destino = destino
        self.data_voo = data_voo
        self.num_viajantes = num_viajantes

#Classe Passagem herda de Entidade e usa associação
class Passagem(Entidade):  # HERANÇA e ASSOCIAÇÃO
    def __init__(self, id, voo, passagem_classe, bagagem):
        super().__init__(id) # Chamada ao construtor da classe base
        self.Voo = voo  # Associação com a classe Voo
        self.passagem_classe = passagem_classe
        self.bagagem = bagagem
        self.assentos = []  

    def calc_preco_total(self):
        total = sum(assento.assento_preco for assento in self.assentos)
        return total

#Classe Assentos herda de Entidade e usa associação
class Assentos(Entidade): # HERANÇA e ASSOCIAÇÃO
    def __init__(self, id, numero_assento, assento_preco, passagem):
        super().__init__(id) # Chamada ao construtor da classe base
        self.numero_assento = numero_assento
        self.assento_preco = assento_preco
        self.passagem = passagem  # Associação com a classe Passagem

# Classe Bagagem herda de Entidade e usa associação:
    def __init__(self, id, passagem, bagagem_ext, bagagem_preco):
        super().__init__(id)
        self.passagem = passagem  # Associação com a classe Passagem
        self.bagagem_ext = bagagem_ext
        self.bagagem_preco = bagagem_preco
    
    # POLIMORFISMO: Método específico de Bagagem para calcular o custo total
    def calc_preco(self):
        return self.bagagem_ext * self.bagagem_preco

# Classe Pagamento herda de Entidade e usa associação
class Pagamento(Entidade): # HERANÇA e ASSOCIAÇÃO
    def __init__(self, id, passagem, pessoa, qnt_total):
        super().__init__(id) # Chamada ao construtor da classe base
        self.passagem = passagem  # Associação com a classe Passagem
        self.pessoa = pessoa
        self.qnt_total = qnt_total
    
    # POLIMORFISMO: Método específico de Pagamento para realizar o processo
    def processo_pagamento(self):
        print(f"Processando o pagamento para {self.pessoa}: R${self.qnt_total:.2f}")

# Função para exibir o menu principal
def main_menu():
    print("\nBem-vindo ao Sistema de Reserva de Passagens Aéreas!")
    print("1. Comprar uma passagem")
    print("2. Escolher bagagens")
    print("3. Escolher assentos")
    print("4. Exibir resumo da compra e finalizar pagamento")
    print("5. Sair")

# Função para comprar passagem
def comprar_passagem(voos, passagens):
    print("\nVoos disponíveis:")
    for idx, voo in enumerate(voos):
        print(f"{idx + 1}. {voo.origem} -> {voo.destino} na data {voo.data_voo}")

    escolha_voo = int(input("Escolha um voo pelo número: ")) - 1
    voo_selecionado = voos[escolha_voo]

    print("\nClasses disponíveis:")
    classes = {"Economica": 150.0, "Executiva": 300.0, "Premium": 500.0}
    for idx, classe in enumerate(classes.keys()):
        print(f"{idx + 1}. {classe} - R${classes[classe]}")

    escolha_classe = int(input("Escolha uma classe pelo número: ")) - 1
    classe_selecionada = list(classes.keys())[escolha_classe]
    preco_classe = classes[classe_selecionada]

    nova_passagem = Passagem(f"TK{len(passagens) + 1}", voo_selecionado, classe_selecionada, 0)
    nova_passagem.assentos = []
    passagens.append(nova_passagem)

    print(f"\nPassagem adicionada! Classe: {classe_selecionada}, Preço base: R${preco_classe}")
    return nova_passagem, preco_classe

# Função para adicionar bagagem
def adicionar_bagagem(passagem, preco_total):
    bagagem_extra = int(input("Quantas bagagens extras você vai levar? (cada uma custa R$50): "))
    peso_bagagem = [float(input(f"Digite o peso (em kg) da bagagem {i + 1}: ")) for i in range(bagagem_extra)]

    preco_bagagem = bagagem_extra * 50.0
    preco_total += preco_bagagem
    print(f"\nBagagens adicionadas! Custo adicional: R${preco_bagagem}")
    return preco_total

# Função para escolher assentos
def escolher_assento(passagem, preco_total):
    print("\nEscolha seu assento:")
    for i in range(1, 21):
        print(f"{i}", end="  ")
        if i % 5 == 0:
            print()

    numero_assento = int(input("\nEscolha o número do assento: "))
    preco_assento = 50.0 if passagem.passagem_classe == "Economica" else 100.0 if passagem.passagem_classe == "Executiva" else 150.0

    novo_assento = Assentos(f"S{numero_assento}", numero_assento, preco_assento, passagem)
    passagem.assentos.append(novo_assento)
    preco_total += preco_assento
    print(f"\nAssento {numero_assento} reservado! Custo adicional: R${preco_assento}")
    return preco_total

# Função para exibir resumo e finalizar pagamento
def finalizar_pagamento(passagem, preco_total):
    print("\nResumo da compra:")
    print(f"Voo: {passagem.Voo.origem} -> {passagem.Voo.destino}")
    print(f"Classe: {passagem.passagem_classe}")

    # Validação e exibição de assentos
    try:
        assentos_escolhidos = [assento.numero_assento for assento in passagem.assentos if isinstance(assento, Assentos)]
    except AttributeError:
        print("Erro: Um ou mais assentos na lista não possuem o atributo 'numero_assento'.")
        assentos_escolhidos = []

    print(f"Assentos escolhidos: {assentos_escolhidos}")
    print(f"Preço total: R${preco_total}")

    pagamento = Pagamento(f"P{passagem.id}", passagem, "Cliente", preco_total)
    pagamento.processo_pagamento()

# Execução principal
if __name__ == "__main__":
    voos = [
        Voo("FL123", "Nova York", "São Paulo", date(2024, 12, 25), 150),
        Voo("FL456", "Rio de Janeiro", "Londres", date(2024, 12, 30), 120),
    ]
    passagens = []
    preco_total = 0.0
    passagem_atual = None

    while True:
        main_menu()
        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            passagem_atual, preco_passagem = comprar_passagem(voos, passagens)
            preco_total += preco_passagem
        elif opcao == 2:
            if passagem_atual:
                preco_total = adicionar_bagagem(passagem_atual, preco_total)
            else:
                print("Você precisa comprar uma passagem antes de adicionar bagagens.")
        elif opcao == 3:
            if passagem_atual:
                preco_total = escolher_assento(passagem_atual, preco_total)
            else:
                print("Você precisa comprar uma passagem antes de escolher assentos.")
        elif opcao == 4:
            if passagem_atual:
                finalizar_pagamento(passagem_atual, preco_total)
                break
            else:
                print("Você precisa comprar uma passagem antes de finalizar.")
        elif opcao == 5:
            print("Saindo do sistema. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")
