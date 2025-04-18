# === EXTENSÕES ===
import csv
from datetime import datetime
import ast

# === FERRAMENTAS ===
# Colocando informação temporais
def parse_data(data_str):
    for fmt in ('%Y-%m-%d', '%Y/%m/%d'):
        try:
            return datetime.strptime(data_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Formato de data inválido: {data_str}")

#Função de carregar estoque
def carregar_estoque():
    estoque = []
    try:
        with open('estoque.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile) # criação e leitura do CSV
            for row in reader:
                row['quantidade'] = int(row['quantidade'])
                row['preco_unitario'] = float(row['preco_unitario'])
                estoque.append(row)
    except FileNotFoundError:
        print("Arquivo de estoque não encontrado. Criando novo estoque...")
    return estoque

#Função para salvar itens no estoque
def salvar_estoque(estoque):
    with open('estoque.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['codigo', 'nome', 'quantidade', 'unidade_medida', 'preco_unitario', 'data_validade']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for produto in estoque:
            writer.writerow(produto)

# ------------------------- FUNÇÕES DE ESTOQUE -------------------------
# Cadastro do produto
def cadastrar_produto(estoque):
    print("\n🔹 Cadastro de Produto:")
    codigo = input("Código: ")
    nome = input("Nome: ")
    quantidade = int(input("Quantidade: "))
    unidade_medida = input("Unidade de medida: ")
    preco_unitario = float(input("Preço unitário: "))
    data_validade = input("Data de validade (AAAA-MM-DD ou AAAA/MM/DD): ")
    
    novo_produto = {
        'codigo': codigo,
        'nome': nome,
        'quantidade': quantidade,
        'unidade_medida': unidade_medida,
        'preco_unitario': preco_unitario,
        'data_validade': data_validade
    }
    estoque.append(novo_produto)
    salvar_estoque(estoque)
    print(f"✅ Produto '{nome}' cadastrado com sucesso!")

# Consultar o estoque
def consultar_estoque(estoque):
    print("\n📦 Estoque Atual:")
    if not estoque:
        print("Estoque vazio.")
        return
    for produto in estoque:
        print(f"{produto['codigo']} | {produto['nome']} | {produto['quantidade']} {produto['unidade_medida']} | R${produto['preco_unitario']} | Vence: {produto['data_validade']}")

# Atualizar o estoque
def atualizar_estoque(estoque):
    codigo = input("\nDigite o código do produto a ser atualizado: ")
    for produto in estoque:
        if produto['codigo'] == codigo:
            produto['nome'] = input("Novo nome: ")
            produto['quantidade'] = int(input("Nova quantidade: "))
            produto['unidade_medida'] = input("Nova unidade de medida: ")
            produto['preco_unitario'] = float(input("Novo preço unitário: "))
            produto['data_validade'] = input("Nova data de validade (AAAA-MM-DD ou AAAA/MM/DD): ")
            salvar_estoque(estoque)
            print("✅ Produto atualizado com sucesso.")
            return
    print("❌ Produto não encontrado.")

# Verificação de vencimento e quantidade mínima de produtos
def verificar_produtos_baixos_ou_vencendo(estoque):
    print("\n🚨 Produtos com estoque baixo ou vencendo:")
    hoje = datetime.now().date()
    for produto in estoque:
        nome = produto['nome']
        quantidade = produto['quantidade']
        validade_str = produto['data_validade']

        if quantidade < 10:
            print(f"⚠ Produto {nome} com estoque baixo ({quantidade} unidades).")

        try:
            data_validade = parse_data(validade_str).date()
            dias_restantes = (data_validade - hoje).days

            if dias_restantes < 0:
                print(f"❌ Produto {nome} está vencido desde {validade_str}.")
            elif dias_restantes == 0:
                print(f"⚠ Produto {nome} vence HOJE ({validade_str}).")
            elif dias_restantes <= 30:
                print(f"⚠ Produto {nome} vence em {dias_restantes} dias ({validade_str}).")
        except ValueError as e:
            print(f"❌ Erro ao ler data de validade do produto {nome}: {e}")

# ------------------------- MENU DE ESTOQUE -------------------------
# Acesso ao menu do estoque
def menu_estoque(estoque):
    while True:
        print("\n--- Menu de Estoque ---")
        print("1. Cadastrar produto")
        print("2. Consultar estoque")
        print("3. Atualizar produto")
        print("4. Verificar produtos com estoque baixo ou vencendo")
        print("0. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            cadastrar_produto(estoque)
        elif opcao == '2':
            consultar_estoque(estoque)
        elif opcao == '3':
            atualizar_estoque(estoque)
        elif opcao == '4':
            verificar_produtos_baixos_ou_vencendo(estoque)
        elif opcao == '0':
            break
        else:
            print("❌ Opção inválida.")

# === GESTÃO DA COZINHA ===
# Criação do cardápio em CSV
def carregar_cardapio():
    cardapio = []
    try:
        with open('cardapio.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['preco'] = float(row['preco'])
                row['ingredientes'] = ast.literal_eval(row['ingredientes'])
                cardapio.append(row)
    except FileNotFoundError:
        pass
    return cardapio

#Salvamento do cardápio em CSV
def salvar_cardapio(cardapio):
    with open('cardapio.csv', 'w', newline='', encoding='utf-8') as f:
        cols = ['nome','descricao','preco','ingredientes']
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for item in cardapio:
            tmp = item.copy()
            tmp['ingredientes'] = str(tmp['ingredientes'])
            writer.writerow(tmp)

#Cadastrando um item no cardápio
def cadastrar_item_cardapio(cardapio):
    nome = input("Nome do prato: ")
    desc = input("Descrição: ")
    preco = float(input("Preço: "))
    ings = []
    while True:
        ing = input("Ingrediente (ENTER para sair): ")
        if not ing: break
        qtd = int(input(f"Qtd de '{ing}': "))
        ings.append((ing, qtd))
    cardapio.append({'nome': nome, 'descricao': desc, 'preco': preco, 'ingredientes': ings})
    salvar_cardapio(cardapio)
    print("✅ Prato cadastrado.")
#Consultar o cardápio 
def consultar_cardapio(cardapio):
    print("\n📋 Cardápio:")
    for i in cardapio:
        print(f"• {i['nome']} – R${i['preco']:.2f}")
        print(f"  {i['descricao']}")
        print(f"  Ingredientes: {i['ingredientes']}")
        print("-"*30)
#Atualizar itens do cardápio
def atualizar_item_cardapio(cardapio):
    alvo = input("Nome do prato p/ atualizar: ")
    for i in cardapio:
        if i['nome'].lower() == alvo.lower():
            i['descricao'] = input("Nova descrição: ")
            i['preco'] = float(input("Novo preço: "))
            ings = []
            while True:
                ing = input("Ingrediente (ENTER p/ sair): ")
                if not ing: break
                qtd = int(input(f"Qtd de '{ing}': "))
                ings.append((ing, qtd))
            i['ingredientes'] = ings
            salvar_cardapio(cardapio)
            print("✅ Cardápio atualizado.")
            return
    print("❌ Prato não encontrado.")

# Acesso ao menu do cardápio
def menu_cozinha(cardapio):
    while True:
        print("\n--- Gestão da Cozinha ---")
        print("1. Cadastrar item")
        print("2. Consultar cardápio")
        print("3. Atualizar item")
        print("0. Voltar")
        o = input("Escolha: ")
        if o == '1':
            cadastrar_item_cardapio(cardapio)
        elif o == '2':
            consultar_cardapio(cardapio)
        elif o == '3':
            atualizar_item_cardapio(cardapio)
        elif o == '0':
            break
        else:
            print("Opção inválida.")

# === GESTÃO DE MESAS ===
# Criando o código para as mesas
class Mesa:
    def __init__(self, numero, capacidade):
        self.numero = numero
        self.capacidade = capacidade
        self.status = 'livre'
        self.cliente = None
    def atribuir(self, cliente):
        if self.status=='livre':
            self.cliente = cliente; self.status = "ocupada"
        else:
            print("Não está livre.")
    def reservar(self):
        if self.status=='livre':
            self.status='reservada'
        else:
            print("Não pôde reservar.")
    def liberar(self):
        self.status='livre'; self.cliente=None
    def __str__(self):
        cli = self.cliente or '—'
        return f"Mesa {self.numero} ({self.capacidade}): {self.status} | Cliente: {cli}"

# Criação das mesas com CSV
def carregar_mesas():
    mesas = []
    try:
        with open('mesas.csv', newline='', encoding='utf-8') as f:
            r = csv.DictReader(f)
            for row in r:
                m = Mesa(int(row['numero']), int(row['capacidade']))
                m.status = row['status']
                mesas.append(m)
    except FileNotFoundError:
        pass
    return mesas

# Salvamento das mesas
def salvar_mesas(mesas):
    with open('mesas.csv','w', newline='', encoding='utf-8') as f:
        cols = ['numero','capacidade','status']
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for m in mesas:
            w.writerow({'numero':m.numero,'capacidade':m.capacidade,'status':m.status})

# Acesso ao menu das mesas
def menu_mesas(mesas):
    while True:
        print("\n--- Gestão de Mesas ---")
        print("1. Cadastrar mesa")
        print("2. Atribuir cliente")
        print("3. Reservar mesa")
        print("4. Liberar mesa")
        print("5. Visualizar mesas")
        print("0. Voltar")
        o = input("Escolha: ")
        if o=='1':
            n = int(input("Número: "))
            c = int(input("Capacidade: "))
            mesas.append(Mesa(n,c)); salvar_mesas(mesas)
        elif o=='2':
            n = int(input("Mesa: ")); cli = input("Cliente: ")
            m = next((x for x in mesas if x.numero==n), None)
            if m: m.atribuir(cli); salvar_mesas(mesas)
        elif o=='3':
            n = int(input("Mesa: ")); m=next((x for x in mesas if x.numero==n),None)
            if m: m.reservar(); salvar_mesas(mesas)
        elif o=='4':
            n = int(input("Mesa: ")); m=next((x for x in mesas if x.numero==n),None)
            if m: m.liberar(); salvar_mesas(mesas)
        elif o=='5':
            print(); [print(m) for m in mesas]
        elif o=='0':
            break
        else:
            print("Inválido.")

# === GESTÃO DE PEDIDOS ===
# Criação do código para os pedidos
def carregar_fila_pedidos():
    try:
        with open('fila_pedidos.csv', newline='', encoding='utf-8') as f: 
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []

# Salvando os pedidos no CSV    
def salvar_fila_pedidos(fila):
    with open('fila_pedidos.csv','w',newline='',encoding='utf-8') as f:
        cols=['mesa','item','status']
        w=csv.DictWriter(f,fieldnames=cols)
        w.writeheader()
        for p in fila:
            w.writerow(p)

# Verificando os ingredientes disponíveis
def verificar_ingredientes_disponiveis(item, estoque):
    for ing,q in item['ingredientes']:
        prod = next((x for x in estoque if x['nome'].lower()==ing.lower()),None)
        if not prod or prod['quantidade']<q:
            return False
    return True

# Diminuição dos ingredientes pelo uso
def baixar_ingredientes(item, estoque):
    for ing,q in item['ingredientes']:
        for prod in estoque:
            if prod['nome'].lower()==ing.lower():
                prod['quantidade']-=q
    salvar_estoque(estoque) 

# Registramento dos pedidos
def registrar_pedido(mesas, fila, cardapio, estoque):
    n = int(input("Mesa: "))
    m = next((x for x in mesas if x.numero==n), None)
    if not m or m.status!='ocupada':
        print("Mesa não ocupada.")
        return
    itens=[]
    while True:
        nome = input("Prato (ENTER p/ sair): ")
        if not nome: break
        it = next((x for x in cardapio if x['nome'].lower()==nome.lower()), None)
        if not it:
            print("Não existe.")
        elif not verificar_ingredientes_disponiveis(it, estoque):
            print("Sem ingredientes.")
        else:
            baixar_ingredientes(it, estoque)
            itens.append(it)
    for it in itens:
        fila.append({'mesa':str(n),'item':it['nome'],'status':'recebido'})
    salvar_fila_pedidos(fila)
    print("✅ Pedido registrado.")

# Visualizando os pedidos feitos
def visualizar_pedidos(fila):
    print("\n🍽️ Fila de Pedidos:")
    for p in fila:
        print(f"Mesa {p['mesa']} – {p['item']} – {p['status']}")

# Atualização dos pedidos
def atualizar_status_pedido(fila):
    n = input("Mesa: "); prato = input("Prato: ")
    for p in fila:
        if p['mesa']==n and p['item'].lower()==prato.lower():
            p['status']=input("Novo status: ")
            salvar_fila_pedidos(fila)
            print("✅ Status atualizado.")
            return
    print("❌ Não encontrado.")

# Cancelamento dos pedidos
def cancelar_pedido(fila):
    mesa = input("Número da mesa: ")
    prato = input("Nome do prato a cancelar: ")
    for i, p in enumerate(fila):
        if p['mesa'] == mesa and p['item'].lower() == prato.lower():
            confirmacao = input(f"Cancelar o pedido de '{prato}' da mesa {mesa}? (sim/não): ").lower()
            if confirmacao == "sim":
                pedido_cancelado = fila.pop(i)
                salvar_fila_pedidos(fila)
                print(f"✅ Pedido '{pedido_cancelado['item']}' da mesa {pedido_cancelado['mesa']} cancelado com sucesso.")
            else:
                print("❌ Cancelamento abortado.")
            return
    print("❌ Pedido não encontrado.")

# Acesso ao menu dos pedidos
def menu_pedidos(mesas, fila, cardapio, estoque):
    while True:
        print("\n--- Gestão de Pedidos ---")
        print("1. Registrar pedido")
        print("2. Ver fila")
        print("3. Atualizar status")
        print("4. Cancelar pedido")
        print("0. Voltar")
        o = input("Escolha: ")
        if o=='1':
            registrar_pedido(mesas, fila, cardapio, estoque)
        elif o=='2':
            visualizar_pedidos(fila)
        elif o=='3':
            atualizar_status_pedido(fila)
        elif o=='4':
            cancelar_pedido(fila)
        elif o=='0':
            break
        else:
            print("Inválido.")

# === GESTÃO DE PAGAMENTOS ===
# Carregamento de pagamentos em CSV
def carregar_pagamentos():
    try:
        with open('pagamentos.csv', newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []

# Salvando em CSV o pagamento
def salvar_pagamentos(pagamentos):
    with open('pagamentos.csv', 'w', newline='', encoding='utf-8') as f:
        campos = ['mesa', 'itens', 'total', 'forma', 'troco', 'data']
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for pag in pagamentos:
            pag_copia = pag.copy()
            pag_copia['itens'] = str(pag['itens']) 
            w.writerow(pag_copia)

# Calculando os totais de pedidos
def calcular_total_pedidos(mesa_num, fila, cardapio):
    total = 0.0
    itens = []
    for p in fila:
        if p['mesa'] == str(mesa_num):
            item = next((x for x in cardapio if x['nome'].lower() == p['item'].lower()), None)
            if item:
                total += item['preco']
                itens.append(item['nome'])
    return total, itens

# Registrando o pagamento
def registrar_pagamento(mesas, fila, cardapio, pagamentos):
    try:
        mesa_num = int(input("Número da mesa: "))
        mesa = next((m for m in mesas if m.numero == mesa_num), None)
        if not mesa or mesa.status != 'ocupada':
            print("❌ Mesa não está ocupada.")
            return

        total, itens = calcular_total_pedidos(mesa_num, fila, cardapio)
        if not itens:
            print("❌ Nenhum pedido registrado para essa mesa.")
            return

        print(f"Subtotal: R${total:.2f}")

        # Aplicar taxa de serviço ou desconto
        taxa = float(input("Taxa de serviço (%) ou desconto (-%): "))
        total += total * (taxa / 100)
        print(f"Total com ajustes: R${total:.2f}")

        # Divisão entre clientes
        dividir = input("Dividir entre quantas pessoas? (ENTER para não dividir): ")
        if dividir:
            partes = int(dividir)
            valor_individual = total / partes
            print(f"Cada pessoa paga: R${valor_individual:.2f}")

        # Forma de pagamento
        forma = input("Forma de pagamento (dinheiro/cartão): ").lower()
        troco = 0.0
        if forma == 'dinheiro':
            pago = float(input("Valor pago: R$"))
            troco = pago - total
            if troco < 0:
                print("❌ Valor insuficiente.")
                return
            print(f"Troco: R${troco:.2f}")
        else:
            print("Pagamento em cartão confirmado.")

        pagamento = { 
            'mesa': str(mesa_num),
            'itens': itens,
            'total': f"{total:.2f}",
            'forma': forma,
            'troco': f"{troco:.2f}",
            'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        pagamentos.append(pagamento)
        salvar_pagamentos(pagamentos)

        # Limpar pedidos e liberar mesa
        fila[:] = [p for p in fila if p['mesa'] != str(mesa_num)]
        salvar_fila_pedidos(fila)
        mesas[:] = [m for m in mesas if m.numero != mesa_num]
        salvar_mesas(mesas)
        print(f"🧾 Mesa {mesa_num} fechada e removida do sistema.")

        print(f"✅ Pagamento registrado com sucesso.")

    except ValueError:
        print("❌ Entrada inválida.")

# Relatório dos pagamentos
def relatorio_pagamentos(pagamentos):
    print("\n📄 Relatório de Pagamentos:")
    if not pagamentos:
        print("Nenhum pagamento registrado.")
        return
    total_dia = 0
    mesas = set()
    itens_vendidos = {}

    # Pagamento por mesa
    for pag in pagamentos:
        print(f"Mesa {pag['mesa']} | Total: R${pag['total']} | Forma: {pag['forma']} | Itens: {pag['itens']} | Data: {pag['data']}")
        total_dia += float(pag['total'])
        mesas.add(pag['mesa'])

        for item in eval(pag['itens']):
            itens_vendidos[item] = itens_vendidos.get(item, 0) + 1

    print(f"\n📊 Total de vendas do dia: R${total_dia:.2f}") # vendar do dia
    if mesas:
        print(f"💺 Valor médio por mesa: R${(total_dia / len(mesas)):.2f}") # valor médio por mesa

    # quantidade dos itens mais vendidos por mesa
    if itens_vendidos:
        print("\n🍽️ Itens mais vendidos:")
        for item, qtd in sorted(itens_vendidos.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {item}: {qtd}x")

# Acesso ao menu de pagamentos
def menu_pagamentos(mesas, fila, cardapio):
    pagamentos = carregar_pagamentos()
    while True:
        print("\n--- Gestão de Pagamentos ---")
        print("1. Registrar pagamento")
        print("2. Ver relatórios financeiros")
        print("0. Voltar")
        o = input("Escolha: ")
        if o == '1':
            registrar_pagamento(mesas, fila, cardapio, pagamentos)
        elif o == '2':
            relatorio_pagamentos(pagamentos)
        elif o == '0':
            break
        else:
            print("Opção inválida.")

# === MENU GERAL ===
# Acesso ao menu geral de serviços
def menu_gestao_pedidos(mesas, fila, cardapio, estoque):
    while True:
        print("\n--- Gestão de Pedidos e Mesas ---")
        print("1. Gestão de Mesas")
        print("2. Gestão de Pedidos")
        print("0. Voltar")
        o = input("Escolha: ")
        if o=='1':
            menu_mesas(mesas)
        elif o=='2':
            menu_pedidos(mesas, fila, cardapio, estoque)
        elif o=='0':
            break
        else:
            print("Inválido.")

# Acesso ao menu de estoques
def menu_principal():
    estoque  = carregar_estoque()
    cardapio = carregar_cardapio()
    fila     = carregar_fila_pedidos()
    mesas    = carregar_mesas()

    while True:
        print("\n===== Sistema de Restaurante =====")
        print("1. Gestão de Estoque")
        print("2. Gestão da Cozinha")
        print("3. Gestão de Pedidos")
        print("4. Gestão de Pagamentos")
        print("0. Sair")
        o = input("Escolha: ")
        if o=='1':
            menu_estoque(estoque)
        elif o=='2':
            menu_cozinha(cardapio)
        elif o=='3':
            menu_gestao_pedidos(mesas, fila, cardapio, estoque)
        elif o == '4':
            menu_pagamentos(mesas, fila, cardapio)
        elif o=='0':
            salvar_estoque(estoque)
            salvar_cardapio(cardapio)
            salvar_fila_pedidos(fila)
            salvar_mesas(mesas)
            print("Até logo!")
            break
        else:
            print("Inválido.")

# inicializando o código
if __name__ == "__main__":
    menu_principal()
