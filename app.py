import flet as ft
import speech_recognition as sr
import pyttsx3
import winsound

# 1. FUNÇÃO DE FALA
def falar(texto):
    try:
        engine_local = pyttsx3.init()
        engine_local.setProperty('rate', 160) 
        engine_local.say(texto)
        engine_local.runAndWait()
        engine_local.stop()
    except:
        pass

def main(page: ft.Page):
    page.title = "App de Crochê da Rita"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # CONFIGURAÇÃO DE PÁGINA PARA CENTRALIZAR TUDO
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 50 # Dá um respiro nas bordas

    numero_voltas = ft.Ref[ft.Text]()

    # --- LÓGICA DO CONTADOR ---
    def somar_volta(e):
        valor = int(numero_voltas.current.value) + 1
        numero_voltas.current.value = str(valor)
        page.update()
        if valor == 5:
            winsound.Beep(1500, 500)
            falar(f"Parabéns! Você completou 5 carreiras!")
        else:
            falar(f"Carreira {valor}")

    def zerar_contador(e):
        numero_voltas.current.value = "0"
        page.update()
        falar("Zerei")

    def ouvir_vovo(e):
        rec = sr.Recognizer()
        try:
            with sr.Microphone() as mic:
                page.snack_bar = ft.SnackBar(ft.Text("Ouvindo..."))
                page.snack_bar.open = True
                page.update()
                audio = rec.listen(mic, timeout=5)
                texto = rec.recognize_google(audio, language="pt-BR")
                if "próximo" in texto.lower() or "mais um" in texto.lower():
                    winsound.Beep(1000, 150)
                    somar_volta(None)
                elif "zerar" in texto.lower():
                    zerar_contador(None)
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Não entendi"))
            page.snack_bar.open = True
            page.update()

    # --- TELA 3: CONTADOR ---
    def abrir_contador(nome_projeto):
        page.clean() # Limpa a tela de forma mais bruta
        
        page.floating_action_button = ft.FloatingActionButton(
            content=ft.Text("OUVIR", weight="bold"),
            on_click=ouvir_vovo, bgcolor="green"
        )

        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(nome_projeto.upper(), size=25, weight="bold", color="pink"),
                        ft.Text(value="0", size=100, weight="bold", color="blue", ref=numero_voltas),
                        ft.ElevatedButton("SOMAR CARREIRA", on_click=somar_volta, height=80, width=300, bgcolor="pink", color="white"),
                        ft.TextButton("Voltar ao Menu", on_click=mostrar_menu)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                expand=True # Faz o container ocupar a tela toda para centralizar
            )
        )
        falar(f"Iniciando {nome_projeto}")

    # --- TELA 2: ESCOLA DE PONTOS  ---
    def abrir_aprendizado(e):
        page.clean()
        
        # textos:
        pontos = {
            "Correntinha": "Inicie com um nó corrediço na agulha. Lace o fio e puxe-o por dentro da argola na agulha. Repita esse movimento — laçar e puxar — para criar cada nova corrente.",
            "Ponto Baixo": "Pule o primeiro furo a partir da agulha, insira a agulha no segundo, lace o fio, puxe duas alças na agulha, lace novamente e passe pelas duas alças.",
            "Ponto Alto": "Lace o fio, insira a agulha na base, puxe o fio, terá três argolas na agulha, lace e passe por duas argolas, lace novamente e passe pelas duas últimas."
        }
        
        coluna_pontos = ft.Column(
            [
                ft.Text("ESCOLA DE PONTOS", size=25, weight="bold", color="pink"), 
                ft.Divider(height=20, color="transparent")
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        # Criando os botões com as novas descrições
        for nome, desc in pontos.items():
            coluna_pontos.controls.append(
                ft.ElevatedButton(
                    content=ft.Text(f"OUVIR: {nome}", size=16),
                    on_click=lambda _, n=nome, d=desc: falar(f"{n}: {d}"),
                    width=350, # Aumentei um pouco o botão para o texto caber bem
                    height=60
                )
            )
        
        coluna_pontos.controls.append(
            ft.TextButton("Voltar ao Menu", on_click=mostrar_menu)
        )
        
        page.add(
            ft.Row(
                [coluna_pontos],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        page.update()

    # --- TELA 1: MENU PRINCIPAL ---
    def mostrar_menu(e=None):
        page.clean()
        page.floating_action_button = None
        
        menu = ft.Column(
            [
                ft.Text("O QUE VAMOS FAZER?", size=25, weight="bold"),
                ft.Divider(height=40, color="transparent"),
                ft.ElevatedButton("📚 APRENDER PONTOS", on_click=abrir_aprendizado, width=300, bgcolor="blue", color="white", height=60),
                ft.ElevatedButton("🧶 TAPETE", on_click=lambda _: abrir_contador("Tapete"), width=300, height=60),
                ft.ElevatedButton("🧶 SOUSPLAT", on_click=lambda _: abrir_contador("Sousplat"), width=300, height=60),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        page.add(ft.Container(content=menu, expand=True))

    # --- TELA ZERO: BOAS-VINDAS ---
    def tela_inicial():
        page.clean()
        boas_vindas = ft.Column(
            [
                ft.Text("PROJETO CROCHÊ ACESSÍVEL", size=30, weight="bold", color="pink", text_align="center"),
                ft.Divider(height=50, color="transparent"),
                ft.ElevatedButton("ENTRAR NO APP", on_click=mostrar_menu, height=100, width=300)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        page.add(ft.Container(content=boas_vindas, expand=True))

    tela_inicial()

ft.app(target=main)