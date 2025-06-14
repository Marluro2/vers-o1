import flet as ft
import random
import threading
import time

nomes = ["Joana", "Lucas", "Maria", "Pedro", "Ana", "Carlos", "Beatriz", "Rafael", "Lívia", "Gustavo"]
itens = ["celular", "bicicleta", "livro", "notebook", "tênis", "mochila"]

modelos_problemas = [
    "{nome} comprou um(a) {item} por R$ {total:,.2f}. Após um tempo, o preço sofreu um aumento de {perc}%. Qual o valor do(a) {item} após o aumento?",
    "{nome} fez uma compra de R$ {total:,.2f} e recebeu um desconto de {perc}%. Qual o valor final da compra?",
    "O salário de {nome} é R$ {total:,.2f}. Ele recebeu um aumento de {perc}%. Qual o novo salário de {nome}?",
    "{nome} tinha R$ {total:,.2f} guardados e gastou {perc}% desse valor. Quanto sobrou com {nome}?",
    "Uma loja vendeu um produto por R$ {total:,.2f} com {perc}% de desconto. Qual foi o preço final pago por {nome}?",
]

frases_motivacionais = [
    "🎉 PARABÉNS! VOCÊ É SENSACIONAL!",
    "👏 UAU! QUE RACIOCÍNIO INCRÍVEL!",
    "🚀 CONTINUE ASSIM, VOCÊ VAI LONGE!",
    "🌟 SUA DEDICAÇÃO ESTÁ INCRÍVEL!",
    "🦸‍♂️ VOCÊ ESTÁ SUPERANDO OS DESAFIOS!",
    "🔥 QUE SHOW! VAMOS PARA O PRÓXIMO!"
]

def criar_problema(nivel):
    perc = random.choice([10, 15, 20, 25, 30, 40, 50])
    resultado = random.randint(2 + nivel, 10 + nivel * 2)
    total = resultado * 100 // perc
    if nivel >= 6:
        nome = random.choice(nomes)
        item = random.choice(itens)
        modelo = random.choice(modelos_problemas)
        # Para problemas de aumento
        if "aumento" in modelo and "celular" in modelo or "salário" in modelo:
            enunciado = modelo.format(nome=nome, item=item, total=total, perc=perc)
            valor_final = total * (1 + perc/100)
            resultado = round(valor_final, 2)
            passos = [
                f"1️⃣ Valor inicial: R$ {total:,.2f}",
                f"2️⃣ Cálculo do aumento: {perc}% de {total} = {perc/100} × {total} = R$ {total*perc/100:,.2f}",
                f"3️⃣ Valor final: {total} + {total*perc/100:,.2f} = R$ {resultado:,.2f}"
            ]
        # Para problemas de desconto
        elif "desconto" in modelo:
            enunciado = modelo.format(nome=nome, item=item, total=total, perc=perc)
            valor_final = total * (1 - perc/100)
            resultado = round(valor_final, 2)
            passos = [
                f"1️⃣ Valor inicial: R$ {total:,.2f}",
                f"2️⃣ Cálculo do desconto: {perc}% de {total} = {perc/100} × {total} = R$ {total*perc/100:,.2f}",
                f"3️⃣ Valor final: {total} - {total*perc/100:,.2f} = R$ {resultado:,.2f}"
            ]
        # Para problemas de salário
        elif "salário" in modelo:
            enunciado = modelo.format(nome=nome, total=total, perc=perc)
            novo_salario = total * (1 + perc/100)
            resultado = round(novo_salario, 2)
            passos = [
                f"1️⃣ Salário inicial: R$ {total:,.2f}",
                f"2️⃣ Cálculo do aumento: {perc}% de {total} = {perc/100} × {total} = R$ {total*perc/100:,.2f}",
                f"3️⃣ Novo salário: {total} + {total*perc/100:,.2f} = R$ {resultado:,.2f}"
            ]
        elif "guardados" in modelo:
            enunciado = modelo.format(nome=nome, total=total, perc=perc)
            gasto = total * perc/100
            resultado = round(total - gasto, 2)
            passos = [
                f"1️⃣ Valor inicial: R$ {total:,.2f}",
                f"2️⃣ Valor gasto: {perc}% de {total} = {perc/100} × {total} = R$ {gasto:,.2f}",
                f"3️⃣ Valor restante: {total} - {gasto:,.2f} = R$ {resultado:,.2f}"
            ]
        else:
            enunciado = modelo.format(nome=nome, item=item, total=total, perc=perc)
            valor_final = total * (1 - perc/100)
            resultado = round(valor_final, 2)
            passos = [
                f"1️⃣ Valor do produto: R$ {total:,.2f}",
                f"2️⃣ Cálculo do desconto: {perc}% de {total} = R$ {total*perc/100:,.2f}",
                f"3️⃣ Preço final: {total} - {total*perc/100:,.2f} = R$ {resultado:,.2f}"
            ]
        return enunciado, resultado, passos
    else:
        questao = f"Quanto é {perc}% de {total}?"
        resultado = round(perc/100 * total, 2)
        passos = [
            f"1️⃣ Transforme {perc}% em fração: {perc}/100",
            f"2️⃣ Multiplique: {total} × {perc}/100 = {resultado}"
        ]
        return questao, resultado, passos

def gerar_alternativas(resposta_certa):
    alternativas = [resposta_certa]
    while len(alternativas) < 4:
        erro = random.randint(-5, 5)
        alternativa = round(resposta_certa + erro, 2)
        if alternativa != resposta_certa and alternativa not in alternativas and alternativa > 0:
            alternativas.append(alternativa)
    random.shuffle(alternativas)
    return alternativas

def main(page: ft.Page):
    page.title = "Jogo da Porcentagem"
    page.bgcolor = ft.Colors.LIGHT_BLUE_50
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.window_width = 880
    page.window_height = 650

    nivel = 1
    score = 0
    resposta_certa = 0
    passos_resolucao = []
    alternativas = []
    tempo_restante = 30
    timer_running = False
    timer_thread = None

    problema_texto = ft.Text("", size=30, weight="bold", color=ft.Colors.BLUE_900, text_align="center")
    nivel_text = ft.Text("Nível: 1", size=24, weight="bold", color=ft.Colors.INDIGO_800)
    score_text = ft.Text("Pontos: 0", size=24, weight="bold", color=ft.Colors.INDIGO_800)
    status = ft.Text("", size=22, weight="bold")
    tempo_text = ft.Text("Tempo: 30 s", size=28, weight="bold", color=ft.Colors.RED_400, text_align="center")

    resolucao_col = ft.Column([], spacing=6, horizontal_alignment="start")
    avancar_btn = ft.ElevatedButton(
        "Avançar",
        visible=False,
        width=180,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=13),
            elevation=7,
            text_style=ft.TextStyle(size=22, weight="bold")
        )
    )

    resolucao_container = ft.Container(
        content=ft.Column([resolucao_col, avancar_btn]),
        bgcolor=ft.Colors.GREEN_50,
        border=ft.border.all(2, ft.Colors.GREEN_400),
        border_radius=18,
        padding=18,
        expand=True,
        visible=False
    )

    motivacional_text = ft.Text("", size=28, weight="bold", color=ft.Colors.PINK_700, text_align="center", visible=False)
    motivacional_btn = ft.ElevatedButton(
        "Continuar", visible=False, width=180,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.PINK_400,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=13),
            elevation=7,
            text_style=ft.TextStyle(size=22, weight="bold")
        )
    )
    motivacional_container = ft.Column(
        [motivacional_text, motivacional_btn],
        alignment="center", horizontal_alignment="center", visible=False
    )

    botoes_alternativas = [
        ft.ElevatedButton(
            "...",
            width=220,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.CYAN_200,
                color=ft.Colors.BLUE_900,
                shape=ft.RoundedRectangleBorder(radius=18),
                elevation=8,
                text_style=ft.TextStyle(size=22, weight="bold")
            ),
            on_click=None
        )
        for _ in range(4)
    ]

    def parar_timer():
        nonlocal timer_running
        timer_running = False

    def iniciar_timer():
        nonlocal tempo_restante, timer_running, timer_thread
        tempo_restante = 30
        tempo_text.value = f"Tempo: {tempo_restante} s"
        timer_running = True

        def run():
            nonlocal tempo_restante, timer_running
            while timer_running and tempo_restante > 0:
                time.sleep(1)
                if not timer_running:
                    break
                tempo_restante -= 1
                tempo_text.value = f"Tempo: {tempo_restante} s"
                page.update()
            if tempo_restante == 0 and timer_running:
                mostrar_resolucao_erro()
                page.update()

        timer_thread = threading.Thread(target=run, daemon=True)
        timer_thread.start()

    def novo_problema():
        nonlocal resposta_certa, alternativas, passos_resolucao
        questao, resposta_certa, passos_resolucao = criar_problema(nivel)
        alternativas = gerar_alternativas(resposta_certa)
        problema_texto.value = questao
        for i, btn in enumerate(botoes_alternativas):
            btn.text = str(alternativas[i])
            btn.on_click = conferir
            btn.bgcolor = ft.Colors.CYAN_200
            btn.disabled = False
        status.value = ""
        resolucao_col.controls = []
        resolucao_container.visible = False
        avancar_btn.visible = False
        motivacional_container.visible = False
        motivacional_text.visible = False
        motivacional_btn.visible = False
        page.update()
        iniciar_timer()

    def mostrar_resolucao_erro():
        nonlocal nivel, score
        parar_timer()
        for btn in botoes_alternativas:
            btn.disabled = True
            if float(btn.text) == resposta_certa:
                btn.bgcolor = ft.Colors.GREEN_400
            else:
                btn.bgcolor = ft.Colors.CYAN_200
        status.value = "❌ Não desista, você consegue!"
        resolucao_col.controls = [
            ft.Text("Veja a resolução passo a passo:", size=20, weight="bold", color=ft.Colors.GREEN_700)
        ]
        for p in passos_resolucao:
            cor = ft.Colors.GREEN_900 if "✅" not in p else ft.Colors.GREEN_600
            resolucao_col.controls.append(
                ft.Container(
                    content=ft.Text(p, size=20, color=cor, weight="bold"),
                    padding=ft.padding.only(left=8, top=2, bottom=2)
                )
            )
        nivel = 1
        score = 0
        nivel_text.value = "Nível: 1"
        score_text.value = "Pontos: 0"
        resolucao_container.visible = True
        avancar_btn.visible = True
        motivacional_container.visible = False
        motivacional_text.visible = False
        motivacional_btn.visible = False
        page.update()

    def mostrar_motivacional():
        frase = random.choice(frases_motivacionais)
        motivacional_text.value = frase
        motivacional_text.visible = True
        motivacional_btn.visible = True
        motivacional_container.visible = True
        resolucao_container.visible = False
        status.value = ""
        page.update()

    def conferir(e):
        nonlocal nivel, score
        parar_timer()
        escolha = float(e.control.text.replace(",", "."))
        for btn in botoes_alternativas:
            btn.disabled = True
            if float(btn.text) == resposta_certa:
                btn.bgcolor = ft.Colors.GREEN_400
            elif btn == e.control:
                btn.bgcolor = ft.Colors.RED_400
        if escolha == resposta_certa:
            status.value = "🎉 Correto! +1 ponto"
            resolucao_col.controls = []
            resolucao_container.visible = False
            score += 1
            nivel += 1
            nivel_text.value = f"Nível: {nivel}"
            score_text.value = f"Pontos: {score}"
            if nivel > 1 and (nivel-1) % 3 == 0:
                mostrar_motivacional()
            else:
                page.update()
                time.sleep(1.2)
                novo_problema()
        else:
            mostrar_resolucao_erro()

    def avancar(e):
        resolucao_col.controls = []
        resolucao_container.visible = False
        status.value = ""
        avancar_btn.visible = False
        page.update()
        novo_problema()

    def avancar_motivacional(e):
        motivacional_container.visible = False
        motivacional_text.visible = False
        motivacional_btn.visible = False
        page.update()
        novo_problema()

    avancar_btn.on_click = avancar
    motivacional_btn.on_click = avancar_motivacional

    def reiniciar_jogo():
        nonlocal nivel, score
        parar_timer()
        nivel = 1
        score = 0
        nivel_text.value = "Nível: 1"
        score_text.value = "Pontos: 0"
        novo_problema()

    def iniciar_jogo(e):
        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Text("Jogo da Porcentagem", size=36, weight="bold", color=ft.Colors.PINK_700, text_align="center"),
                padding=10,
                alignment=ft.alignment.center,
            ),
            ft.Row([nivel_text, score_text], alignment="center"),
            tempo_text,
            problema_texto,
            ft.Row([
                ft.Column(botoes_alternativas, alignment="center", horizontal_alignment="center", spacing=15),
                resolucao_container,
            ], alignment="center", vertical_alignment="start", spacing=25),
            status,
            motivacional_container
        )
        reiniciar_jogo()

    page.add(
        ft.Container(
            content=ft.Text("Bem-vindo ao Jogo da Porcentagem!", size=34, weight="bold", color=ft.Colors.PINK_600, text_align="center"),
            padding=20,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.CYAN_100,
            border_radius=12,
        ),
        ft.Container(
            content=ft.Text("Teste seus conhecimentos de porcentagem e avance de nível!", size=22, color=ft.Colors.INDIGO_700, text_align="center"),
            padding=10,
            alignment=ft.alignment.center,
        ),
        ft.ElevatedButton(
            "Começar Jogo",
            on_click=iniciar_jogo,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.PINK_400,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=16),
                elevation=10,
                text_style=ft.TextStyle(size=26, weight="bold")
            ),
            width=280,
            height=60
        )
    )

ft.app(target=main)