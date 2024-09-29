import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import multiprocessing
import time
import random
import sqlite3
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import PyPDF2
import os

# Simulación de una base de datos de empleados
empleados = {
    1: {"nombre": "Juan Pérez", "salario": 50000, "departamento": "IT"},
    2: {"nombre": "María García", "salario": 55000, "departamento": "RRHH"},
    3: {"nombre": "Carlos Rodríguez", "salario": 48000, "departamento": "Ventas"},
    4: {"nombre": "Ana Martínez", "salario": 52000, "departamento": "Marketing"},
}

# Función para calcular la nómina
def calcular_nomina(empleado_id, queue):
    print(f"Calculando nómina para empleado ID: {empleado_id}")
    empleado = empleados[empleado_id]
    salario_base = empleado['salario']
    impuestos = salario_base * 0.15
    seguro_social = salario_base * 0.07
    salario_neto = salario_base - impuestos - seguro_social
    time.sleep(2)  # Simular tiempo de cálculo
    queue.put(("Nómina calculada", {
        "empleado_id": empleado_id,
        "nombre": empleado['nombre'],
        "salario_base": salario_base,
        "impuestos": impuestos,
        "seguro_social": seguro_social,
        "salario_neto": salario_neto
    }))

# Función para actualizar la base de datos
def actualizar_bd(datos_nomina, queue):
    print("Actualizando base de datos...")
    # Aquí iría el código para actualizar una base de datos real
    time.sleep(1.5)  # Simular tiempo de actualización
    queue.put(("Base de datos actualizada", None))

# Función para generar reporte
def generar_reporte(datos_nomina, queue):
    print("Generando reporte...")
    reporte = f"Reporte de Nómina - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    reporte += f"Empleado: {datos_nomina['nombre']}\n"
    reporte += f"Salario Base: ${datos_nomina['salario_base']:.2f}\n"
    reporte += f"Impuestos: ${datos_nomina['impuestos']:.2f}\n"
    reporte += f"Seguro Social: ${datos_nomina['seguro_social']:.2f}\n"
    reporte += f"Salario Neto: ${datos_nomina['salario_neto']:.2f}\n"
    time.sleep(1)  # Simular tiempo de generación de reporte
    queue.put(("Reporte generado", reporte))

# Función para enviar notificación
def enviar_notificacion(empleado_id, queue):
    print("Enviando notificación...")
    time.sleep(0.5)  # Simular tiempo de envío
    queue.put(("Notificación enviada", f"Notificación enviada al empleado {empleado_id}"))

class CoopcibaoApp:
    def __init__(self, master):
        self.master = master
        master.title("Coopcibao - Sistema de Nómina")
        master.geometry("800x600")
        master.configure(bg='#f0f0f0')

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', background='#4CAF50', foreground='white', font=('Arial', 10, 'bold'))
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 11))
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'))

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.procesar_frame = ttk.Frame(self.notebook, padding="20")
        self.consultar_frame = ttk.Frame(self.notebook, padding="20")

        self.notebook.add(self.procesar_frame, text="Procesar Nómina")
        self.notebook.add(self.consultar_frame, text="Consultar Reportes")

        self.setup_procesar_frame()
        self.setup_consultar_frame()

        self.pdf_path = None
        self.datos_nomina = None

    def setup_procesar_frame(self):
        ttk.Label(self.procesar_frame, text="Coopcibao - Sistema de Nómina", style='Header.TLabel').grid(column=0, row=0, columnspan=2, pady=20)

        ttk.Label(self.procesar_frame, text="Seleccione el empleado:").grid(column=0, row=1, sticky=tk.W, pady=10)
        self.empleado_var = tk.StringVar()
        self.empleado_combo = ttk.Combobox(self.procesar_frame, textvariable=self.empleado_var, state="readonly", width=30)
        self.empleado_combo['values'] = [f"{id}: {emp['nombre']}" for id, emp in empleados.items()]
        self.empleado_combo.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=10)
        self.empleado_combo.current(0)

        ttk.Button(self.procesar_frame, text="Procesar Nómina", command=self.procesar_nomina).grid(column=0, row=2, columnspan=2, pady=20)

        self.progress = ttk.Progressbar(self.procesar_frame, orient=tk.HORIZONTAL, length=300, mode='indeterminate')
        self.progress.grid(column=0, row=3, columnspan=2, pady=10)

        self.status_label = ttk.Label(self.procesar_frame, text="")
        self.status_label.grid(column=0, row=4, columnspan=2, pady=10)

        self.result_text = tk.Text(self.procesar_frame, height=15, width=70, wrap=tk.WORD, font=('Arial', 10))
        self.result_text.grid(column=0, row=5, columnspan=2, pady=10)
        self.result_text.config(state=tk.DISABLED)

        ttk.Button(self.procesar_frame, text="Descargar PDF", command=self.descargar_pdf).grid(column=0, row=6, columnspan=2, pady=20)

    def setup_consultar_frame(self):
        ttk.Label(self.consultar_frame, text="Consulta de Reportes", style='Header.TLabel').grid(column=0, row=0, columnspan=2, pady=20)

        ttk.Button(self.consultar_frame, text="Cargar Reporte", command=self.cargar_reporte).grid(column=0, row=1, columnspan=2, pady=20)

        self.consulta_text = tk.Text(self.consultar_frame, height=20, width=70, wrap=tk.WORD, font=('Arial', 10))
        self.consulta_text.grid(column=0, row=2, columnspan=2, pady=10)
        self.consulta_text.config(state=tk.DISABLED)

    def procesar_nomina(self):
        empleado_id = int(self.empleado_var.get().split(':')[0])
        self.progress.start()
        self.status_label.config(text="Procesando nómina...")
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.config(state=tk.DISABLED)

        queue = multiprocessing.Queue()
        
        proceso_nomina = multiprocessing.Process(target=calcular_nomina, args=(empleado_id, queue))
        proceso_nomina.start()
        proceso_nomina.join()

        mensaje, self.datos_nomina = queue.get()
        
        procesos = [
            multiprocessing.Process(target=actualizar_bd, args=(self.datos_nomina, queue)),
            multiprocessing.Process(target=generar_reporte, args=(self.datos_nomina, queue)),
            multiprocessing.Process(target=enviar_notificacion, args=(empleado_id, queue))
        ]

        for proceso in procesos:
            proceso.start()

        self.master.after(100, self.check_queue, queue, len(procesos))

    def check_queue(self, queue, total_procesos):
        try:
            mensaje, datos = queue.get_nowait()
            self.status_label.config(text=mensaje)
            if mensaje == "Reporte generado":
                self.result_text.config(state=tk.NORMAL)
                self.result_text.insert(tk.END, datos)
                self.result_text.config(state=tk.DISABLED)
                self.generar_pdf(datos)
            total_procesos -= 1
        except:
            pass

        if total_procesos > 0:
            self.master.after(100, self.check_queue, queue, total_procesos)
        else:
            self.progress.stop()
            self.status_label.config(text="Proceso de nómina completado")
            messagebox.showinfo("Éxito", "Nómina procesada con éxito")

    def generar_pdf(self, reporte):
        pdf_filename = f"reporte_nomina_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        elements.append(Paragraph("Reporte de Nómina", styles['Title']))
        elements.append(Paragraph(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Paragraph(" ", styles['Normal']))

        data = [line.split(": ") for line in reporte.split("\n") if line.strip()]
        table = Table(data)
        table.setStyle(TableStyle)[
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]
        elements.append(table)

        doc.build(elements)
        self.pdf_path = pdf_filename

    def descargar_pdf(self):
        if self.pdf_path:
            save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if save_path:
                import shutil
                shutil.copy(self.pdf_path, save_path)
                messagebox.showinfo("Éxito", f"PDF guardado como: {save_path}")
        else:
            messagebox.showerror("Error", "No hay un reporte PDF generado para descargar.")

    def cargar_reporte(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                
                self.consulta_text.config(state=tk.NORMAL)
                self.consulta_text.delete('1.0', tk.END)
                self.consulta_text.insert(tk.END, f"Reporte cargado: {os.path.basename(file_path)}\n\n")
                self.consulta_text.insert(tk.END, text)
                self.consulta_text.config(state=tk.DISABLED)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo PDF: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CoopcibaoApp(root)
    root.mainloop()

