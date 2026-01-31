import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pyautogui
import sys
import os
from datetime import datetime

class AutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automación de Clicks")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Variables para controlar la ejecución
        self.running = False
        self.paused = False
        self.thread = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal con mejor organización
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título centrado
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        title_label = ttk.Label(title_frame, text="Automación de Clicks", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, pady=5)
        
        # Frame de configuración
        config_frame = ttk.LabelFrame(main_frame, text="Configuración", padding="10")
        config_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Entrada para número de repeticiones
        ttk.Label(config_frame, text="Número de repeticiones:", 
                 font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.repetitions_var = tk.StringVar(value="1")
        repetitions_entry = ttk.Entry(config_frame, textvariable=self.repetitions_var, 
                                     width=10, font=("Arial", 10))
        repetitions_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Frame de controles
        control_frame = ttk.LabelFrame(main_frame, text="Controles", padding="10")
        control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Botones en un frame interno
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=0, column=0, columnspan=2)
        
        # Botón de inicio
        self.start_button = ttk.Button(button_frame, text="Iniciar Automatización", 
                                      command=self.start_automation, width=18)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Botón de pausa/continua
        self.pause_button = ttk.Button(button_frame, text="Pausar", 
                                      command=self.toggle_pause, state=tk.DISABLED, width=15)
        self.pause_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Botón de cancelar
        self.cancel_button = ttk.Button(button_frame, text="Cancelar", 
                                       command=self.cancel_automation, state=tk.DISABLED, width=15)
        self.cancel_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Frame de estado
        status_frame = ttk.LabelFrame(main_frame, text="Estado de Ejecución", padding="10")
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Estado principal
        self.status_var = tk.StringVar(value="Listo para ejecutar")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                foreground="blue", font=("Arial", 10, "bold"))
        status_label.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        
        # Estado de pausa
        self.pause_status_var = tk.StringVar(value="")
        pause_status_label = ttk.Label(status_frame, textvariable=self.pause_status_var, 
                                      foreground="orange", font=("Arial", 10, "bold"))
        pause_status_label.grid(row=1, column=0, columnspan=2, pady=2)
        
        # Contador de espera
        self.countdown_var = tk.StringVar(value="")
        countdown_label = ttk.Label(status_frame, textvariable=self.countdown_var, 
                                   font=("Arial", 11), foreground="red")
        countdown_label.grid(row=2, column=0, columnspan=2, pady=2)
        
        # Información de repetición actual
        self.repetition_info_var = tk.StringVar(value="")
        repetition_info_label = ttk.Label(status_frame, textvariable=self.repetition_info_var,
                                         font=("Arial", 9))
        repetition_info_label.grid(row=3, column=0, columnspan=2, pady=2)
        
        # Frame de información
        info_frame = ttk.LabelFrame(main_frame, text="Secuencia por Repetición", padding="10")
        info_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Información de la secuencia
        info_text = """• Espera inicial: 3 segundos
• Captura de pantalla
• Espera 3 segundos
• Click izquierdo
• Espera 2 segundos
• Espera 3 segundos

Puedes pausar/cancelar en cualquier momento"""
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT, font=("Arial", 9))
        info_label.grid(row=0, column=0, sticky=tk.W)
        
        # Configurar el peso de las columnas para centrado
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        config_frame.columnconfigure(1, weight=1)
        status_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(0, weight=1)
    
    def start_automation(self):
        try:
            repetitions = int(self.repetitions_var.get())
            if repetitions <= 0:
                messagebox.showerror("Error", "El número de repeticiones debe ser mayor a 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un número válido")
            return
        
        # Cambiar estado de los botones
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.NORMAL)
        self.status_var.set("Preparando ejecución...")
        self.paused = False
        self.pause_button.config(text="Pausar")
        self.pause_status_var.set("")
        
        # Iniciar el hilo de automatización
        self.running = True
        self.thread = threading.Thread(target=self.automation_loop, args=(repetitions,))
        self.thread.daemon = True
        self.thread.start()
    
    def toggle_pause(self):
        if self.paused:
            # Reanudar ejecución
            self.paused = False
            self.pause_button.config(text="Pausar")
            self.pause_status_var.set("")
            self.status_var.set("Reanudando ejecución...")
        else:
            # Pausar ejecución
            self.paused = True
            self.pause_button.config(text="Continuar")
            self.pause_status_var.set("⏸️ EJECUCIÓN EN PAUSA")
            self.status_var.set("Ejecución pausada")
    
    def wait_if_paused(self):
        """Espera mientras esté en pausa"""
        while self.paused and self.running:
            time.sleep(0.1)
    
    def automation_loop(self, repetitions):
        try:
            # Espera inicial de 3 segundos (cancelable)
            self.root.after(0, lambda: self.status_var.set("Espera inicial de 3 segundos..."))
            
            for second in range(3, 0, -1):
                if not self.running:
                    break
                self.wait_if_paused()
                if not self.running:
                    break
                # Actualizar contador en la interfaz
                self.root.after(0, lambda s=second: self.countdown_var.set(f"Iniciando en: {s}"))
                time.sleep(1)
            
            self.root.after(0, lambda: self.countdown_var.set(""))
            
            if not self.running:
                self.root.after(0, self.finish_automation)
                return
            
            for i in range(repetitions):
                if not self.running:
                    break
                
                # Actualizar información de repetición
                self.root.after(0, lambda: self.repetition_info_var.set(f"Repetición: {i+1}/{repetitions}"))
                self.root.after(0, lambda: self.status_var.set(f"Iniciando repetición {i+1}"))
                
                # 1. Captura de pantalla
                if self.running:
                    self.wait_if_paused()
                    if not self.running:
                        break
                    
                    self.root.after(0, lambda: self.status_var.set(f"Rep {i+1}: Capturando pantalla..."))
                    try:
                        # Crear carpeta si no existe
                        if not os.path.exists("screenshots"):
                            os.makedirs("screenshots")
                        
                        # Tomar y guardar screenshot directamente con pyautogui
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"screenshots/screenshot_{timestamp}_rep{i+1}.png"
                        pyautogui.screenshot(filename)
                        print(f"Captura guardada: {filename}")
                    except Exception as e:
                        print(f"Error al tomar screenshot: {e}")
                        self.root.after(0, lambda: messagebox.showwarning("Advertencia", 
                                                                         "No se pudo tomar la captura de pantalla"))
                
                # 2. Espera 3 segundos
                if self.running:
                    self.wait_if_paused()
                    if not self.running:
                        break
                    
                    self.root.after(0, lambda: self.status_var.set(f"Rep {i+1}: Esperando 3 segundos..."))
                    for sec in range(3, 0, -1):
                        if not self.running:
                            break
                        self.wait_if_paused()
                        if not self.running:
                            break
                        self.root.after(0, lambda s=sec: self.countdown_var.set(f"Espera: {s}s"))
                        time.sleep(1)
                    self.root.after(0, lambda: self.countdown_var.set(""))
                
                # 3. Click izquierdo (ÚNICO CLICK)
                if self.running:
                    self.wait_if_paused()
                    if not self.running:
                        break
                    
                    self.root.after(0, lambda: self.status_var.set(f"Rep {i+1}: Click izquierdo..."))
                    pyautogui.click()
                
                # 4. Espera 2 segundos
                if self.running:
                    self.wait_if_paused()
                    if not self.running:
                        break
                    
                    self.root.after(0, lambda: self.status_var.set(f"Rep {i+1}: Esperando 2 segundos..."))
                    for sec in range(2, 0, -1):
                        if not self.running:
                            break
                        self.wait_if_paused()
                        if not self.running:
                            break
                        self.root.after(0, lambda s=sec: self.countdown_var.set(f"Espera: {s}s"))
                        time.sleep(1)
                    self.root.after(0, lambda: self.countdown_var.set(""))
                
                # 5. Espera 3 segundos (sin click)
                if self.running:
                    self.wait_if_paused()
                    if not self.running:
                        break
                    
                    self.root.after(0, lambda: self.status_var.set(f"Rep {i+1}: Esperando 3 segundos..."))
                    for sec in range(3, 0, -1):
                        if not self.running:
                            break
                        self.wait_if_paused()
                        if not self.running:
                            break
                        self.root.after(0, lambda s=sec: self.countdown_var.set(f"Espera: {s}s"))
                        time.sleep(1)
                    self.root.after(0, lambda: self.countdown_var.set(""))
            
            # Finalizar ejecución
            self.root.after(0, self.finish_automation)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Ocurrió un error: {str(e)}"))
            self.root.after(0, self.finish_automation)
    
    def cancel_automation(self):
        self.running = False
        self.paused = False
        self.status_var.set("Cancelando...")
        self.pause_status_var.set("")
        self.countdown_var.set("")
        self.pause_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.DISABLED)
    
    def finish_automation(self):
        self.running = False
        self.paused = False
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.DISABLED)
        self.pause_status_var.set("")
        self.countdown_var.set("")
        self.repetition_info_var.set("")
        
        if self.thread and self.thread.is_alive():
            self.status_var.set("Finalizando...")
        else:
            if not self.running:
                self.status_var.set("Ejecución cancelada")
            else:
                self.status_var.set("Ejecución completada")
                
        # Mostrar mensaje de finalización
        self.root.after(1000, lambda: self.status_var.set("Listo para ejecutar"))

def main():
    # Verificar que pyautogui esté disponible
    try:
        import pyautogui
    except ImportError:
        print("Error: Necesitas instalar pyautogui. Ejecuta: pip install pyautogui")
        sys.exit(1)
    
    root = tk.Tk()
    app = AutomationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
