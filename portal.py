import customtkinter as ctk
import threading
import json
import os
from PIL import Image
from scraper import obter_dados_portal

DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__))

COR_FUNDO = "#10141D"
COR_QUADRO = "#1C2333"
COR_DESTAQUE = "#F4B41A"
COR_TEXTO = "#E0E5F0"
ARQUIVO_CACHE = "dados_salvos.json"

app = ctk.CTk()
app.title("PortalPy")
app.geometry("900x800") 
app.attributes('-alpha', 0.95) 

FONTE_TITULO = ("Segoe UI", 26, "bold")
FONTE_SUBTITULO = ("Segoe UI", 16, "bold")
FONTE_TEXTO = ("Segoe UI", 13)

try:
    caminho_fundo = os.path.join(DIRETORIO_BASE, "fundo_gradiente.jpg")
    img_fundo_pil = Image.open(caminho_fundo)
    img_fundo = ctk.CTkImage(light_image=img_fundo_pil, dark_image=img_fundo_pil, size=(900, 800))
    bg_label = ctk.CTkLabel(app, image=img_fundo, text="PortalPy")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    
    def adaptar_fundo(event):
        
        if event.widget == app:
            
            img_fundo.configure(size=(event.width, event.height))

    
    app.bind("<Configure>", adaptar_fundo)

except Exception as e:
    print(f"Fundo não encontrado: {e}")

container_principal = ctk.CTkFrame(app, fg_color=COR_FUNDO, corner_radius=25, border_width=1, border_color="#2A344C")
container_principal.pack(pady=40, padx=40, fill="both", expand=True)


titulo = ctk.CTkLabel(container_principal, text="PortalPy - UVV", font=FONTE_TITULO, text_color=COR_DESTAQUE)
titulo.pack(pady=(20, 10))


frame_conteudo = ctk.CTkScrollableFrame(container_principal, fg_color="transparent")
frame_conteudo.pack(fill="both", expand=True, padx=10, pady=5)


try:
    caminho_portal = os.path.join(DIRETORIO_BASE, "Logo Portalpy_ Tecnologia e Educação.png")
    imagem_pil = Image.open(caminho_portal)
    logo_img = ctk.CTkImage(light_image=imagem_pil, dark_image=imagem_pil, size=(300, 300))
    logo_label = ctk.CTkLabel(frame_conteudo, image=logo_img, text="")
except Exception as e:
    print(f"Aviso: Não foi possível carregar a imagem da logo. Erro: {e}")
    logo_label = None

frame_blog = ctk.CTkFrame(frame_conteudo, fg_color=COR_QUADRO, corner_radius=15, border_width=1, border_color="#2A344C")
frame_atividades = ctk.CTkFrame(frame_conteudo, fg_color=COR_QUADRO, corner_radius=15, border_width=1, border_color="#2A344C")
frame_boletim = ctk.CTkFrame(frame_conteudo, fg_color=COR_QUADRO, corner_radius=15, border_width=1, border_color="#2A344C")

frame_botoes = ctk.CTkFrame(app, fg_color="transparent")
frame_botoes.pack(side="bottom", pady=20)

def exibir_tela_inicial():
    frame_blog.pack_forget()
    frame_atividades.pack_forget()
    frame_boletim.pack_forget()
    
    if logo_label:
        logo_label.pack(pady=80) 
    
    botao_voltar.pack_forget()
    botao_acessar.pack(side="left", padx=10)
    botao_atualizar.pack(side="left", padx=10)
    titulo.configure(text="PortalPy - UVV")
    
def animar_transicao(alfa_atual=0.0):
    if alfa_atual < 0.95: 
        alfa_atual += 0.08
        app.attributes('-alpha', min(alfa_atual, 0.95))
        app.after(15, animar_transicao, alfa_atual) 
    else:
        app.attributes('-alpha', 0.95)

def exibir_tela_dados():
    if logo_label:
        logo_label.pack_forget()

    frame_blog.pack(pady=10, padx=20, fill="x")
    frame_atividades.pack(pady=10, padx=20, fill="x")
    frame_boletim.pack(pady=10, padx=20, fill="x")

    botao_acessar.pack_forget()
    botao_voltar.pack(side="left", padx=10)
    botao_atualizar.pack(side="left", padx=10)

def preencher_interface(dados):
    for frame in (frame_blog, frame_atividades, frame_boletim):
        for widget in frame.winfo_children(): widget.destroy()
        
    ctk.CTkLabel(frame_blog, text="📰 Novidades do Blog", font=FONTE_SUBTITULO, text_color=COR_DESTAQUE).pack(pady=(15, 5), padx=20, anchor="w")
    ctk.CTkLabel(frame_atividades, text="📅 Atividades Pendentes", font=FONTE_SUBTITULO, text_color=COR_DESTAQUE).pack(pady=(15, 5), padx=20, anchor="w")
    ctk.CTkLabel(frame_boletim, text="📊 Boletim", font=FONTE_SUBTITULO, text_color=COR_DESTAQUE).pack(pady=(15, 5), padx=20, anchor="w")

    exibir_tela_dados()

    for aviso in dados.get("notificacoes", [])[:5]: 
        linha = ctk.CTkFrame(frame_blog, fg_color="transparent")
        linha.pack(fill="x", padx=20, pady=2)
        ctk.CTkLabel(linha, text=f"• {aviso['titulo']}", font=FONTE_TEXTO, text_color=COR_TEXTO, anchor="w", justify="left").pack(side="left", fill="x", expand=True, pady=2)
        if aviso['data']:
            ctk.CTkLabel(linha, text=aviso['data'], font=("Segoe UI", 11, "bold"), text_color="#7A8CA8").pack(side="right", padx=(10, 0))
    ctk.CTkLabel(frame_blog, text="", font=("Segoe UI", 5)).pack()

    if not dados.get("atividades"):
        ctk.CTkLabel(frame_atividades, text="Tudo em dia! Nenhuma atividade pendente.", font=FONTE_TEXTO, text_color="#A3D9A5").pack(anchor="w", padx=20, pady=(5, 15))
    else:
        for ativ in dados["atividades"]:
            ctk.CTkLabel(frame_atividades, text=f"• {ativ}", font=FONTE_TEXTO, text_color=COR_TEXTO).pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(frame_atividades, text="", font=("Segoe UI", 5)).pack()
        
    for nota in dados.get("boletim", []):
        linha = ctk.CTkFrame(frame_boletim, fg_color="transparent")
        linha.pack(fill="x", padx=20, pady=4)
        
        if isinstance(nota, dict):
            ctk.CTkLabel(linha, text=f"• {nota['disciplina']}", font=FONTE_TEXTO, text_color=COR_TEXTO, anchor="w", justify="left").pack(side="left", fill="x", expand=True)
            
            frame_notas = ctk.CTkFrame(linha, fg_color="transparent")
            frame_notas.pack(side="right")
            
            ctk.CTkLabel(frame_notas, text=f"Faltas: {nota['tf1']}", font=("Segoe UI", 12, "bold"), text_color="#E07A5F").pack(side="left", padx=10) 
            ctk.CTkLabel(frame_notas, text=f"AV1: {nota['av1']}", font=("Segoe UI", 12, "bold"), text_color="#81B29A").pack(side="left", padx=10) 
            ctk.CTkLabel(frame_notas, text=nota['status'], font=("Segoe UI", 11), text_color="#7A8CA8").pack(side="left", padx=5) 
        else:
            ctk.CTkLabel(linha, text=f"• {nota}", font=FONTE_TEXTO, text_color=COR_TEXTO).pack(anchor="w")
            
    ctk.CTkLabel(frame_boletim, text="", font=("Segoe UI", 5)).pack()

def carregar_dados_rapido():
    if os.path.exists(ARQUIVO_CACHE):
        with open(ARQUIVO_CACHE, "r", encoding="utf-8") as f:
            dados_salvos = json.load(f)
        preencher_interface(dados_salvos)
        titulo.configure(text="Painel do Aluno - UVV")
    else:
        titulo.configure(text="Nenhum dado salvo. Clique em Atualizar.")

def buscar_dados():
    botao_atualizar.configure(text="A extrair...", state="disabled", fg_color="#7A5A0D")
    botao_acessar.configure(state="disabled")
    botao_voltar.configure(state="disabled")
    thread = threading.Thread(target=executar_scraper)
    thread.start()

def executar_scraper():
    dados = obter_dados_portal()
    with open(ARQUIVO_CACHE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
        
    preencher_interface(dados)
    botao_atualizar.configure(text="Atualizar Dados", state="normal", fg_color=COR_DESTAQUE)
    botao_acessar.configure(state="normal")
    botao_voltar.configure(state="normal")
    titulo.configure(text="Painel do Aluno - UVV")

botao_voltar = ctk.CTkButton(frame_botoes, text="Voltar", font=FONTE_SUBTITULO, text_color=COR_TEXTO, fg_color="#4A5568", hover_color="#2D3748", corner_radius=8, height=45, command=exibir_tela_inicial)
botao_acessar = ctk.CTkButton(frame_botoes, text="Acessar Arquivo", font=FONTE_SUBTITULO, text_color=COR_TEXTO, fg_color="#2A344C", hover_color="#3D4A66", corner_radius=8, height=45, command=carregar_dados_rapido)
botao_atualizar = ctk.CTkButton(frame_botoes, text="Atualizar Dados", font=FONTE_SUBTITULO, text_color=COR_FUNDO, fg_color=COR_DESTAQUE, hover_color="#D19A14", corner_radius=8, height=45, command=buscar_dados)

exibir_tela_inicial()
app.mainloop()