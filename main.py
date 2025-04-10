import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from pynput import mouse, keyboard
import json
import os


class EnhancedAutoClicker:
    def __init__(self):
        # Configurações padrão
        self.clicking = False
        self.click_thread = None
        self.interval = 0.1  # Intervalo entre cliques (segundos)
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()
        self.hotkey = keyboard.Key.f6
        self.hotkey_string = "F6"
        self.click_type = "single"  # single, double, triple
        self.button_type = "left"  # left, right, middle
        self.click_position = "cursor"  # cursor, fixed
        self.fixed_x = 0
        self.fixed_y = 0
        self.send_key = False
        self.key_to_send = ""

        # Carregar configurações se existirem
        self.config_path = "autoclicker_config.json"
        self.load_config()

        # Configuração da UI
        self.create_ui()

        # Iniciar listener do teclado para tecla de atalho
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

    def create_ui(self):
        # Configuração da janela principal
        self.root = tk.Tk()
        self.root.title("Auto Clicker Pro")
        self.root.geometry("450x500")
        self.root.resizable(False, False)

        # Definir tema e estilo
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Cores e estilos personalizados
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10, "bold"))
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"), foreground="#444444")
        self.style.configure("Status.TLabel", font=("Arial", 10, "bold"))
        self.style.configure("GreenButton.TButton", background="green")
        self.style.configure("RedButton.TButton", background="red")

        # Container principal
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = ttk.Label(main_frame, text="Auto Clicker Pro", style="Header.TLabel")
        title_label.pack(pady=(0, 15))

        # Criar notebook para abas
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Aba de configurações principais
        main_tab = ttk.Frame(notebook, padding=10)
        notebook.add(main_tab, text="Configurações Principais")

        # Aba de configurações avançadas
        advanced_tab = ttk.Frame(notebook, padding=10)
        notebook.add(advanced_tab, text="Configurações Avançadas")

        # Aba sobre
        about_tab = ttk.Frame(notebook, padding=10)
        notebook.add(about_tab, text="Sobre")

        # --- Configurações Principais ---
        # Intervalo entre cliques
        interval_frame = ttk.Frame(main_tab)
        interval_frame.pack(fill=tk.X, pady=5)

        ttk.Label(interval_frame, text="Intervalo entre cliques (segundos):").pack(side=tk.LEFT)

        self.interval_var = tk.StringVar(value=str(self.interval))
        interval_entry = ttk.Entry(interval_frame, textvariable=self.interval_var, width=8)
        interval_entry.pack(side=tk.LEFT, padx=5)

        # Tipo de clique
        click_frame = ttk.Frame(main_tab)
        click_frame.pack(fill=tk.X, pady=10)

        ttk.Label(click_frame, text="Tipo de clique:").pack(side=tk.LEFT)

        self.click_type_var = tk.StringVar(value=self.click_type)
        ttk.Radiobutton(click_frame, text="Único", variable=self.click_type_var, value="single").pack(side=tk.LEFT,
                                                                                                      padx=(5, 2))
        ttk.Radiobutton(click_frame, text="Duplo", variable=self.click_type_var, value="double").pack(side=tk.LEFT,
                                                                                                      padx=2)
        ttk.Radiobutton(click_frame, text="Triplo", variable=self.click_type_var, value="triple").pack(side=tk.LEFT,
                                                                                                       padx=2)

        # Botão do mouse
        button_frame = ttk.Frame(main_tab)
        button_frame.pack(fill=tk.X, pady=5)

        ttk.Label(button_frame, text="Botão do mouse:").pack(side=tk.LEFT)

        self.button_type_var = tk.StringVar(value=self.button_type)
        ttk.Radiobutton(button_frame, text="Esquerdo", variable=self.button_type_var, value="left").pack(side=tk.LEFT,
                                                                                                         padx=(5, 2))
        ttk.Radiobutton(button_frame, text="Direito", variable=self.button_type_var, value="right").pack(side=tk.LEFT,
                                                                                                         padx=2)
        ttk.Radiobutton(button_frame, text="Meio", variable=self.button_type_var, value="middle").pack(side=tk.LEFT,
                                                                                                       padx=2)

        # Posição do clique
        position_frame = ttk.Frame(main_tab)
        position_frame.pack(fill=tk.X, pady=10)

        ttk.Label(position_frame, text="Posição do clique:").pack(side=tk.LEFT)

        self.position_var = tk.StringVar(value=self.click_position)
        ttk.Radiobutton(position_frame, text="Cursor", variable=self.position_var,
                        value="cursor", command=self.toggle_position_fields).pack(side=tk.LEFT, padx=(5, 2))
        ttk.Radiobutton(position_frame, text="Posição fixa", variable=self.position_var,
                        value="fixed", command=self.toggle_position_fields).pack(side=tk.LEFT, padx=2)

        # Coordenadas da posição fixa
        self.coord_frame = ttk.Frame(main_tab)
        self.coord_frame.pack(fill=tk.X, pady=5)

        ttk.Label(self.coord_frame, text="X:").pack(side=tk.LEFT)
        self.x_var = tk.StringVar(value=str(self.fixed_x))
        ttk.Entry(self.coord_frame, textvariable=self.x_var, width=6).pack(side=tk.LEFT, padx=(2, 10))

        ttk.Label(self.coord_frame, text="Y:").pack(side=tk.LEFT)
        self.y_var = tk.StringVar(value=str(self.fixed_y))
        ttk.Entry(self.coord_frame, textvariable=self.y_var, width=6).pack(side=tk.LEFT, padx=2)

        ttk.Button(self.coord_frame, text="Capturar posição atual", command=self.capture_position).pack(side=tk.LEFT,
                                                                                                        padx=(10, 0))

        # Mostrar/esconder campos de coordenadas conforme seleção
        self.toggle_position_fields()

        # --- Configurações Avançadas ---
        # Tecla de atalho
        hotkey_frame = ttk.Frame(advanced_tab)
        hotkey_frame.pack(fill=tk.X, pady=10)

        ttk.Label(hotkey_frame, text="Tecla de atalho:").pack(side=tk.LEFT)

        self.hotkey_var = tk.StringVar(value=self.hotkey_string)
        self.hotkey_entry = ttk.Entry(hotkey_frame, textvariable=self.hotkey_var, width=10, state="readonly")
        self.hotkey_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(hotkey_frame, text="Definir nova tecla", command=self.set_new_hotkey).pack(side=tk.LEFT, padx=5)

        # Opção para enviar tecla em vez de clicar
        key_press_frame = ttk.Frame(advanced_tab)
        key_press_frame.pack(fill=tk.X, pady=10)

        self.send_key_var = tk.BooleanVar(value=self.send_key)
        send_key_check = ttk.Checkbutton(key_press_frame, text="Enviar tecla em vez de clicar",
                                         variable=self.send_key_var, command=self.toggle_key_field)
        send_key_check.pack(side=tk.LEFT)

        # Campo para a tecla a ser enviada
        self.key_frame = ttk.Frame(advanced_tab)
        self.key_frame.pack(fill=tk.X, pady=5)

        ttk.Label(self.key_frame, text="Tecla a enviar:").pack(side=tk.LEFT)
        self.key_to_send_var = tk.StringVar(value=self.key_to_send)
        self.key_entry = ttk.Entry(self.key_frame, textvariable=self.key_to_send_var, width=10)
        self.key_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(self.key_frame, text="(Ex: a, b, enter, space)").pack(side=tk.LEFT, padx=5)

        # Salvar configurações
        save_frame = ttk.Frame(advanced_tab)
        save_frame.pack(fill=tk.X, pady=15)

        ttk.Button(save_frame, text="Salvar configurações", command=self.save_config).pack(side=tk.LEFT)
        ttk.Button(save_frame, text="Restaurar padrões", command=self.restore_defaults).pack(side=tk.LEFT, padx=10)

        # --- Sobre ---
        about_text = """Auto Clicker Pro

Versão: 1.0

Este é um programa de autoclicker avançado que permite:
• Clicar em intervalos personalizados
• Escolher entre clique simples, duplo ou triplo
• Selecionar o botão do mouse (esquerdo, direito, meio)
• Definir posição fixa ou seguir o cursor
• Personalizar tecla de atalho
• Opção para enviar teclas em vez de cliques

Desenvolvido com Python e Tkinter.
"""
        about_label = ttk.Label(about_tab, text=about_text, justify=tk.LEFT, wraplength=380)
        about_label.pack(pady=10)

        # --- Painel de Status e Controle (comum a todas as abas) ---
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=10)

        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
        self.status_label = ttk.Label(status_frame, text="Desativado", foreground="red", style="Status.TLabel")
        self.status_label.pack(side=tk.LEFT, padx=5)

        # Botões de controle
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=10)

        self.start_button = ttk.Button(control_frame, text="Iniciar", command=self.start_clicking)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(control_frame, text="Parar", command=self.stop_clicking, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, text="Sair", command=self.root.destroy).pack(side=tk.LEFT, padx=5)

        # Mostrar/esconder campo de tecla conforme seleção
        self.toggle_key_field()

        # Configurar fechamento correto
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def toggle_position_fields(self):
        if self.position_var.get() == "fixed":
            for child in self.coord_frame.winfo_children():
                child.configure(state=tk.NORMAL)
        else:
            for child in self.coord_frame.winfo_children():
                child.configure(state=tk.DISABLED)

    def toggle_key_field(self):
        if self.send_key_var.get():
            for child in self.key_frame.winfo_children():
                child.configure(state=tk.NORMAL)
        else:
            for child in self.key_frame.winfo_children():
                child.configure(state=tk.DISABLED)

    def capture_position(self):
        # Minimizar a janela para não interferir
        self.root.iconify()
        time.sleep(1)  # Dar tempo para o usuário posicionar o mouse

        # Capturar posição atual do mouse
        current_position = self.mouse_controller.position
        self.x_var.set(str(int(current_position[0])))
        self.y_var.set(str(int(current_position[1])))

        # Restaurar a janela
        self.root.deiconify()

    def set_new_hotkey(self):
        # Desativar o listener atual para evitar conflitos
        if hasattr(self, 'keyboard_listener') and self.keyboard_listener.is_alive():
            self.keyboard_listener.stop()

        # Atualizar UI
        self.hotkey_entry.configure(state=tk.NORMAL)
        self.hotkey_var.set("Pressione uma tecla...")

        # Criar listener temporário para capturar a nova tecla
        self.temp_listener = keyboard.Listener(on_press=self.capture_hotkey)
        self.temp_listener.start()

    def capture_hotkey(self, key):
        try:
            # Tentar obter o caractere da tecla
            key_char = key.char
            key_name = key_char.upper()
        except AttributeError:
            # Para teclas especiais como F1, F2, etc.
            key_name = str(key).replace("Key.", "").upper()

        # Atualizar a interface e variáveis
        self.hotkey = key
        self.hotkey_string = key_name
        self.hotkey_var.set(key_name)

        # Restaurar o estado do entry
        self.hotkey_entry.configure(state="readonly")

        # Parar o listener temporário
        self.temp_listener.stop()

        # Reiniciar o listener principal
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

        return False  # Parar após a primeira tecla

    def on_key_press(self, key):
        if key == self.hotkey:
            if not self.clicking:
                self.start_clicking()
            else:
                self.stop_clicking()

    def update_settings(self):
        # Atualizar todas as configurações a partir da UI
        try:
            self.interval = float(self.interval_var.get())
            if self.interval < 0.01:
                self.interval = 0.01
                self.interval_var.set("0.01")
        except ValueError:
            self.interval = 0.1
            self.interval_var.set("0.1")
            messagebox.showwarning("Aviso", "Valor de intervalo inválido. Usando 0.1 segundos.")

        self.click_type = self.click_type_var.get()
        self.button_type = self.button_type_var.get()
        self.click_position = self.position_var.get()

        try:
            self.fixed_x = int(self.x_var.get())
            self.fixed_y = int(self.y_var.get())
        except ValueError:
            self.fixed_x = 0
            self.fixed_y = 0
            self.x_var.set("0")
            self.y_var.set("0")
            messagebox.showwarning("Aviso", "Coordenadas inválidas. Usando (0,0).")

        self.send_key = self.send_key_var.get()
        self.key_to_send = self.key_to_send_var.get()

    def start_clicking(self):
        self.update_settings()

        self.clicking = True
        self.status_label.config(text="Ativado", foreground="green")
        self.start_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)

        self.click_thread = threading.Thread(target=self.perform_action)
        self.click_thread.daemon = True
        self.click_thread.start()

    def stop_clicking(self):
        self.clicking = False
        self.status_label.config(text="Desativado", foreground="red")
        self.start_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)

    def perform_action(self):
        button_map = {
            "left": mouse.Button.left,
            "right": mouse.Button.right,
            "middle": mouse.Button.middle
        }

        while self.clicking:
            if self.send_key and self.key_to_send:
                # Enviar tecla em vez de clicar
                try:
                    # Lidar com teclas especiais
                    if self.key_to_send.lower() in ["enter", "return"]:
                        self.keyboard_controller.press(keyboard.Key.enter)
                        self.keyboard_controller.release(keyboard.Key.enter)
                    elif self.key_to_send.lower() == "space":
                        self.keyboard_controller.press(keyboard.Key.space)
                        self.keyboard_controller.release(keyboard.Key.space)
                    elif self.key_to_send.lower() == "tab":
                        self.keyboard_controller.press(keyboard.Key.tab)
                        self.keyboard_controller.release(keyboard.Key.tab)
                    elif self.key_to_send.lower() == "esc":
                        self.keyboard_controller.press(keyboard.Key.esc)
                        self.keyboard_controller.release(keyboard.Key.esc)
                    else:
                        # Tecla regular
                        self.keyboard_controller.press(self.key_to_send)
                        self.keyboard_controller.release(self.key_to_send)
                except Exception as e:
                    print(f"Erro ao enviar tecla: {e}")
            else:
                # Realizar clique
                button = button_map.get(self.button_type, mouse.Button.left)

                # Mover para posição fixa se configurado
                if self.click_position == "fixed":
                    current_pos = self.mouse_controller.position
                    self.mouse_controller.position = (self.fixed_x, self.fixed_y)

                # Executar clique conforme o tipo selecionado
                if self.click_type == "single":
                    self.mouse_controller.click(button)
                elif self.click_type == "double":
                    self.mouse_controller.click(button, 2)
                elif self.click_type == "triple":
                    self.mouse_controller.click(button, 3)

                # Restaurar posição original se mudou para posição fixa
                if self.click_position == "fixed":
                    self.mouse_controller.position = current_pos

            # Aguardar o intervalo configurado
            time.sleep(self.interval)

    def save_config(self):
        self.update_settings()

        config = {
            "interval": self.interval,
            "hotkey_string": self.hotkey_string,
            "click_type": self.click_type,
            "button_type": self.button_type,
            "click_position": self.click_position,
            "fixed_x": self.fixed_x,
            "fixed_y": self.fixed_y,
            "send_key": self.send_key,
            "key_to_send": self.key_to_send
        }

        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f)
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar configurações: {e}")

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)

                self.interval = config.get("interval", 0.1)
                self.hotkey_string = config.get("hotkey_string", "F6")
                self.click_type = config.get("click_type", "single")
                self.button_type = config.get("button_type", "left")
                self.click_position = config.get("click_position", "cursor")
                self.fixed_x = config.get("fixed_x", 0)
                self.fixed_y = config.get("fixed_y", 0)
                self.send_key = config.get("send_key", False)
                self.key_to_send = config.get("key_to_send", "")

                # Converter a string da tecla de atalho para objeto Key
                key_name = self.hotkey_string.lower()
                if key_name.startswith("f") and key_name[1:].isdigit():
                    # Teclas de função (F1-F12)
                    self.hotkey = getattr(keyboard.Key, key_name.lower())
                elif hasattr(keyboard.Key, key_name):
                    # Outras teclas especiais
                    self.hotkey = getattr(keyboard.Key, key_name)
                else:
                    # Teclas regulares
                    self.hotkey = keyboard.KeyCode.from_char(key_name)

            except Exception as e:
                print(f"Erro ao carregar configurações: {e}")

    def restore_defaults(self):
        # Restaurar valores padrão
        self.interval = 0.1
        self.hotkey = keyboard.Key.f6
        self.hotkey_string = "F6"
        self.click_type = "single"
        self.button_type = "left"
        self.click_position = "cursor"
        self.fixed_x = 0
        self.fixed_y = 0
        self.send_key = False
        self.key_to_send = ""

        # Atualizar UI
        self.interval_var.set(str(self.interval))
        self.hotkey_var.set(self.hotkey_string)
        self.click_type_var.set(self.click_type)
        self.button_type_var.set(self.button_type)
        self.position_var.set(self.click_position)
        self.x_var.set(str(self.fixed_x))
        self.y_var.set(str(self.fixed_y))
        self.send_key_var.set(self.send_key)
        self.key_to_send_var.set(self.key_to_send)

        # Atualizar estados dos widgets
        self.toggle_position_fields()
        self.toggle_key_field()

        messagebox.showinfo("Padrões restaurados", "As configurações foram restauradas para os valores padrão.")

    def on_closing(self):
        # Parar clique e listener antes de fechar
        self.clicking = False
        if hasattr(self, 'keyboard_listener') and self.keyboard_listener.is_alive():
            self.keyboard_listener.stop()

        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    try:
        app = EnhancedAutoClicker()
        app.run()
    except Exception as e:
        messagebox.showerror("Erro fatal", f"Ocorreu um erro: {e}")