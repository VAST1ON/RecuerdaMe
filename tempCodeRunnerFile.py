#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MI AYUDANTE DEL HOGAR  -  Prototipo con ventanas (Tkinter)
==========================================================

App sencilla de recordatorios y tareas para NIÑOS y ADULTOS MAYORES:

  * MEDICINAS : recuerda la pastilla todos los días durante un tratamiento
                (30 días por defecto), insiste cada pocos minutos hasta que se
                confirma y, si la persona pregunta "¿ya me la tomé?", le
                asegura si ya la tomó hoy (y a qué hora) para evitar dobles dosis.
  * NIÑOS     : lista de tareas diarias con botones grandes, estrellas,
                barra de progreso y felicitación al terminar todo.
  * CASA / TRABAJO : lista de tareas con aviso opcional a cierta hora.
  * DEMOSTRACIÓN   : permite "viajar en el tiempo" para ver todo el mes de
                tratamiento sin esperar 30 días.

Cómo ejecutarlo:
    python mi_ayudante_hogar.py

Requisitos: Python 3.8+ con Tkinter (viene incluido en Windows y macOS).
Los datos se guardan en:  ~/.mi_ayudante_hogar.json

Nota: si en Linux los emojis se ven mal o la ventana se cierra sola, el programa
ya los desactiva por defecto. Para forzarlos:  AYUDANTE_EMOJIS=1 python ...
"""

import json
import os
import random
import sys
import tkinter as tk
from datetime import date, datetime, time as dtime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
#  CONFIGURACIÓN GENERAL
# ---------------------------------------------------------------------------

ARCHIVO_DATOS = Path.home() / ".OrganizaMe.json"

_env = os.environ.get("AYUDANTE_EMOJIS")
if _env is not None:
    USAR_EMOJIS = _env.strip() == "1"
else:
    # En Linux algunas versiones de Tk fallan con emojis a color.
    USAR_EMOJIS = not sys.platform.startswith("linux")

FUENTE = "Arial"

# Colores llamativos
FONDO = "#FFF8E7"
TEXTO = "#2C3E50"
BLANCO = "#FFFFFF"
VERDE = "#1FA855"
ROJO = "#E63946"
AZUL = "#2D6CDF"
NARANJA = "#E67E22"
MORADO = "#8E44AD"
ROSA = "#E0408F"
AMARILLO = "#FEE440"
TURQUESA = "#0097B2"
GRIS = "#7F8C8D"
GRIS_CLARO = "#D5D8DC"

# Símbolos (con alternativa en texto si no hay emojis)
OK = "✔" if USAR_EMOJIS else "OK"
NO = "✘" if USAR_EMOJIS else "X"
BORRAR = "✖" if USAR_EMOJIS else "X"
CAJA_VACIA = "☐" if USAR_EMOJIS else "  "
CAJA_LLENA = "✔" if USAR_EMOJIS else "OK"
ESTRELLA = "⭐" if USAR_EMOJIS else "*"
ESTRELLA_VACIA = "☆" if USAR_EMOJIS else "."

DIAS_SEMANA = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

# (dibujo, nombre corto) para las tareas de los niños
ICONOS_NINOS = [
    ("🪥", "Dientes"), ("📚", "Tarea"), ("🛏️", "Cama"), ("🧸", "Juguetes"),
    ("🍎", "Comer"), ("🛁", "Baño"), ("🐶", "Mascota"), ("🎒", "Mochila"),
    ("✏️", "Escribir"), ("🧹", "Limpiar"),
]

PALETA_NINOS = [AZUL, MORADO, ROSA, NARANJA, TURQUESA]


# ---------------------------------------------------------------------------
#  UTILIDADES
# ---------------------------------------------------------------------------

def t(texto):
    """Quita emojis/símbolos si USAR_EMOJIS es False."""
    if USAR_EMOJIS:
        return texto
    limpio = "".join(
        c for c in texto
        if not (0x2190 <= ord(c) <= 0x2BFF or ord(c) >= 0x1F000 or ord(c) == 0xFE0F)
    )
    return "\n".join(linea.strip() for linea in limpio.split("\n"))


def oscurecer(color_hex, factor=0.82):
    h = color_hex.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % (int(r * factor), int(g * factor), int(b * factor))


def hora_bonita(hhmm):
    """'08:05' -> '8:05 a. m.'"""
    try:
        h, m = (int(x) for x in hhmm.split(":"))
    except ValueError:
        return hhmm
    sufijo = "a. m." if h < 12 else "p. m."
    return f"{h % 12 or 12}:{m:02d} {sufijo}"


def fecha_bonita(d):
    return f"{DIAS_SEMANA[d.weekday()].capitalize()} {d.day} de {MESES[d.month - 1]}"


def centrar(ventana, ancho=None, alto=None):
    ventana.update_idletasks()
    sw, sh = ventana.winfo_screenwidth(), ventana.winfo_screenheight()
    w = ancho or ventana.winfo_reqwidth()
    h = alto or ventana.winfo_reqheight()
    w, h = min(w, sw - 40), min(h, sh - 100)
    ventana.geometry(f"{w}x{h}+{max(0, (sw - w) // 2)}+{max(0, (sh - h) // 2 - 20)}")


class Reloj:
    """Reloj de la app. Permite 'viajar en el tiempo' en el modo demostración."""
    desfase = timedelta(0)

    @classmethod
    def ahora(cls):
        return datetime.now() + cls.desfase

    @classmethod
    def hoy(cls):
        return cls.ahora().date()


# ---------------------------------------------------------------------------
#  DATOS (se guardan en un archivo JSON)
# ---------------------------------------------------------------------------

def datos_iniciales():
    return {
        "pastilla": {
            "persona": "Abuelito",
            "medicina": "Pastilla de la presión",
            "hora": "08:00",
            "inicio": date.today().isoformat(),
            "dias": 30,
            "repetir_min": 10,
            "tomadas": {},          # {"2026-11-18": "08:15"}
        },
        "nino": {
            "nombre": "Sofi",
            "estrellas_total": 0,
            "tareas": [
                {"id": 1, "texto": "Cepillarme los dientes", "icono": "🪥", "hora": "", "hecha": ""},
                {"id": 2, "texto": "Hacer la tarea", "icono": "📚", "hora": "", "hecha": ""},
                {"id": 3, "texto": "Guardar mis juguetes", "icono": "🧸", "hora": "", "hecha": ""},
                {"id": 4, "texto": "Tender mi cama", "icono": "🛏️", "hora": "", "hecha": ""},
                {"id": 5, "texto": "Comer mi fruta", "icono": "🍎", "hora": "", "hecha": ""},
            ],
        },
        "tareas": [
            {"id": 6, "texto": "Sacar la basura", "categoria": "Casa", "hora": "", "hecha": False},
            {"id": 7, "texto": "Lavar los platos", "categoria": "Casa", "hora": "", "hecha": False},
            {"id": 8, "texto": "Enviar el reporte", "categoria": "Trabajo", "hora": "", "hecha": False},
        ],
        "sig_id": 9,
    }


def cargar_datos():
    base = datos_iniciales()
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            d = json.load(f)
        for clave, valor in base.items():
            d.setdefault(clave, valor)
        for clave, valor in base["pastilla"].items():
            d["pastilla"].setdefault(clave, valor)
        for clave, valor in base["nino"].items():
            d["nino"].setdefault(clave, valor)
        return d
    except (OSError, ValueError, AttributeError, KeyError, TypeError):
        return base


# ---------------------------------------------------------------------------
#  COMPONENTES VISUALES REUTILIZABLES
# ---------------------------------------------------------------------------

class Etiqueta(tk.Label):
    """Label que limpia emojis si hace falta."""

    def __init__(self, master, texto="", **kw):
        kw.setdefault("font", (FUENTE, 18))
        kw.setdefault("fg", TEXTO)
        super().__init__(master, text=t(texto), **kw)

    def poner(self, texto, **kw):
        self.config(text=t(texto), **kw)


class BotonGrande(tk.Label):
    """Botón grande y colorido (funciona igual en Windows, Mac y Linux)."""

    def __init__(self, master, texto, color, comando=None, fuente=None, fg="white", **kw):
        opciones = dict(bd=5, relief="raised", padx=18, pady=12, cursor="hand2", justify="center")
        opciones.update(kw)
        super().__init__(master, text=t(texto), bg=color, fg=fg,
                         font=fuente or (FUENTE, 22, "bold"), **opciones)
        self.color = color
        self.comando = comando
        self.bind("<Enter>", lambda e: self.config(bg=oscurecer(self.color)))
        self.bind("<Leave>", lambda e: self.config(bg=self.color, relief="raised"))
        self.bind("<ButtonPress-1>", lambda e: self.config(relief="sunken"))
        self.bind("<ButtonRelease-1>", self._soltar)

    def _soltar(self, e):
        self.config(relief="raised")
        dentro = 0 <= e.x < self.winfo_width() and 0 <= e.y < self.winfo_height()
        if dentro and self.comando:
            self.comando()

    def configurar(self, texto=None, color=None, comando=None, fg=None):
        if texto is not None:
            self.config(text=t(texto))
        if color is not None:
            self.color = color
            self.config(bg=color)
        if comando is not None:
            self.comando = comando
        if fg is not None:
            self.config(fg=fg)


class MarcoDesplazable(tk.Frame):
    """Marco con barra de desplazamiento vertical (y rueda del ratón)."""

    def __init__(self, master, bg):
        super().__init__(master, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        self.barra = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview, width=26)
        self.interior = tk.Frame(self.canvas, bg=bg)
        self._ventana = self.canvas.create_window((0, 0), window=self.interior, anchor="nw")
        self.interior.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(
            self._ventana, width=e.width))
        self.canvas.configure(yscrollcommand=self.barra.set)
        self.barra.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        for secuencia in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.bind_all(secuencia, self._rueda, add="+")

    def _rueda(self, e):
        try:
            if not self.winfo_exists():
                return
            w = self.winfo_containing(e.x_root, e.y_root)
            if w is None or not (str(w) == str(self) or str(w).startswith(str(self) + ".")):
                return
            if self.canvas.yview() == (0.0, 1.0):
                return
            if getattr(e, "num", None) == 4:
                paso = -1
            elif getattr(e, "num", None) == 5:
                paso = 1
            elif sys.platform == "darwin":
                paso = -int(e.delta)
            else:
                paso = -int(e.delta / 120)
            self.canvas.yview_scroll(paso, "units")
        except (tk.TclError, KeyError):
            pass

    def reconstruir(self, construir):
        """Borra el contenido y lo vuelve a dibujar conservando la posición."""
        y = self.canvas.yview()[0]
        for w in self.interior.winfo_children():
            w.destroy()
        construir(self.interior)
        self.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(y)


class SelectorHora(tk.Frame):
    """Dos cuadritos HH : MM con flechas."""

    def __init__(self, master, bg, hora="08:00"):
        super().__init__(master, bg=bg)
        try:
            h, m = (int(x) for x in hora.split(":"))
        except ValueError:
            h, m = 8, 0
        self.vh = tk.StringVar(value=f"{h:02d}")
        self.vm = tk.StringVar(value=f"{m:02d}")
        tk.Spinbox(self, from_=0, to=23, width=3, textvariable=self.vh, wrap=True,
                   font=(FUENTE, 26, "bold"), justify="center", format="%02.0f").pack(side="left")
        Etiqueta(self, ":", bg=bg, font=(FUENTE, 28, "bold")).pack(side="left", padx=6)
        tk.Spinbox(self, from_=0, to=59, increment=5, width=3, textvariable=self.vm, wrap=True,
                   font=(FUENTE, 26, "bold"), justify="center", format="%02.0f").pack(side="left")

    def valor(self):
        try:
            h = min(23, max(0, int(self.vh.get())))
            m = min(59, max(0, int(self.vm.get())))
        except ValueError:
            h, m = 8, 0
        return f"{h:02d}:{m:02d}"


class Dialogo(tk.Toplevel):
    """
    Ventana emergente grande con mensaje y botones.
    botones: lista de (texto, color, valor).
    modal=True  -> espera la respuesta y la deja en self.resultado
    modal=False -> llama a al_elegir(valor) cuando se pulsa un botón
    (si se cierra con la X, el valor es None).
    """

    def __init__(self, app, titulo, mensaje, botones, color=BLANCO, color_titulo=AZUL,
                 al_elegir=None, modal=False, sonido=False, parent=None):
        super().__init__(parent or app.root)
        self.app = app
        self.al_elegir = al_elegir
        self.resultado = None
        self._listo = False
        self.title(t(titulo))
        self.configure(bg=color)
        self.resizable(False, False)
        try:
            self.attributes("-topmost", True)
        except tk.TclError:
            pass

        Etiqueta(self, titulo, bg=color_titulo, fg="white",
                 font=(FUENTE, 26, "bold"), padx=30, pady=14).pack(fill="x")
        Etiqueta(self, mensaje, bg=color, fg=TEXTO, font=(FUENTE, 24),
                 padx=30, pady=24, justify="center", wraplength=640).pack()
        cont = tk.Frame(self, bg=color)
        cont.pack(padx=24, pady=(0, 24), fill="x")
        for texto, col, valor in botones:
            BotonGrande(cont, texto, col, lambda v=valor: self._elegir(v),
                        fuente=(FUENTE, 22, "bold")).pack(fill="x", pady=6)

        self.protocol("WM_DELETE_WINDOW", lambda: self._elegir(None))
        app.dialogos.append(self)
        centrar(self, max(self.winfo_reqwidth(), 620))
        self.lift()
        if sonido:
            app.sonar()
        if modal:
            try:
                self.wait_visibility()
                self.grab_set()
            except tk.TclError:
                pass
            self.focus_force()
            app.root.wait_window(self)

    def _elegir(self, valor):
        if self._listo:
            return
        self._listo = True
        self.resultado = valor
        if self in self.app.dialogos:
            self.app.dialogos.remove(self)
        try:
            self.grab_release()
        except tk.TclError:
            pass
        self.destroy()
        if self.al_elegir:
            self.al_elegir(valor)


class PedirTexto(tk.Toplevel):
    """Ventanita para escribir un texto (por ejemplo, cambiar un nombre)."""

    def __init__(self, app, titulo, etiqueta, inicial, al_guardar, parent=None):
        super().__init__(parent or app.root)
        self.al_guardar = al_guardar
        bg = BLANCO
        self.title(t(titulo))
        self.configure(bg=bg)
        Etiqueta(self, titulo, bg=MORADO, fg="white", font=(FUENTE, 24, "bold"), pady=12).pack(fill="x")
        cuerpo = tk.Frame(self, bg=bg)
        cuerpo.pack(padx=30, pady=20)
        Etiqueta(cuerpo, etiqueta, bg=bg, font=(FUENTE, 20, "bold")).pack(anchor="w")
        self.entrada = tk.Entry(cuerpo, font=(FUENTE, 26), relief="solid", bd=2, width=22)
        self.entrada.pack(pady=10)
        self.entrada.insert(0, inicial)
        self.entrada.focus_set()
        self.entrada.bind("<Return>", lambda e: self.guardar())
        BotonGrande(cuerpo, "💾 GUARDAR", VERDE, self.guardar).pack(fill="x", pady=4)
        BotonGrande(cuerpo, "✖ CANCELAR", GRIS, self.destroy, fuente=(FUENTE, 18, "bold")).pack(fill="x", pady=4)
        centrar(self, 560)

    def guardar(self):
        valor = self.entrada.get().strip()
        if valor:
            self.destroy()
            self.al_guardar(valor)


class FormularioTarea(tk.Toplevel):
    """Ventana para crear una tarea o recordatorio nuevo."""

    def __init__(self, app, titulo, al_guardar, con_categoria=True, con_icono=False,
                 categoria="Casa", parent=None):
        super().__init__(parent or app.root)
        self.app = app
        self.al_guardar = al_guardar
        self.cat = categoria if categoria in ("Casa", "Trabajo") else "Casa"
        self.icono = ICONOS_NINOS[0][0]
        bg = BLANCO
        self.title(t(titulo))
        self.configure(bg=bg)

        Etiqueta(self, titulo, bg=MORADO, fg="white", font=(FUENTE, 24, "bold"), pady=12).pack(fill="x")
        cuerpo = tk.Frame(self, bg=bg)
        cuerpo.pack(padx=30, pady=14, fill="both")

        Etiqueta(cuerpo, "¿Qué hay que hacer?", bg=bg, font=(FUENTE, 20, "bold")).pack(anchor="w")
        self.entrada = tk.Entry(cuerpo, font=(FUENTE, 24), relief="solid", bd=2, width=28)
        self.entrada.pack(fill="x", pady=(4, 12))
        self.entrada.focus_set()
        self.entrada.bind("<Return>", lambda e: self.guardar())

        if con_categoria:
            Etiqueta(cuerpo, "¿Dónde?", bg=bg, font=(FUENTE, 20, "bold")).pack(anchor="w")
            fila = tk.Frame(cuerpo, bg=bg)
            fila.pack(fill="x", pady=(4, 12))
            fila.columnconfigure((0, 1), weight=1, uniform="c")
            self.btn_casa = BotonGrande(fila, "🏠 CASA", VERDE, lambda: self._cat("Casa"),
                                        fuente=(FUENTE, 20, "bold"))
            self.btn_casa.grid(row=0, column=0, sticky="ew", padx=(0, 6))
            self.btn_trab = BotonGrande(fila, "💼 TRABAJO", AZUL, lambda: self._cat("Trabajo"),
                                        fuente=(FUENTE, 20, "bold"))
            self.btn_trab.grid(row=0, column=1, sticky="ew", padx=(6, 0))
            self._cat(self.cat)

        if con_icono:
            Etiqueta(cuerpo, "Elige un dibujo:", bg=bg, font=(FUENTE, 20, "bold")).pack(anchor="w")
            rejilla = tk.Frame(cuerpo, bg=bg)
            rejilla.pack(pady=(4, 12))
            self.botones_icono = {}
            for k, (emo, nombre) in enumerate(ICONOS_NINOS):
                lbl = tk.Label(rejilla, text=t(f"{emo}\n{nombre}"), font=(FUENTE, 15, "bold"),
                               width=7, bd=3, relief="raised", cursor="hand2", bg="#F2F3F4", fg=TEXTO)
                lbl.grid(row=k // 5, column=k % 5, padx=4, pady=4)
                lbl.bind("<Button-1>", lambda e, x=emo: self._icono(x))
                self.botones_icono[emo] = lbl
            self._icono(self.icono)

        self.var_hora = tk.BooleanVar(value=False)
        fila_h = tk.Frame(cuerpo, bg=bg)
        fila_h.pack(fill="x", pady=(0, 12))
        tk.Checkbutton(fila_h, text=t("⏰ Avisarme a las:"), variable=self.var_hora, bg=bg,
                       font=(FUENTE, 20, "bold"), activebackground=bg, fg=TEXTO,
                       selectcolor=BLANCO).pack(side="left")
        self.selector = SelectorHora(fila_h, bg, "08:00")
        self.selector.pack(side="left", padx=14)

        BotonGrande(cuerpo, "💾 GUARDAR", VERDE, self.guardar).pack(fill="x", pady=4)
        BotonGrande(cuerpo, "✖ CANCELAR", GRIS, self.destroy, fuente=(FUENTE, 18, "bold")).pack(fill="x", pady=4)
        centrar(self, 680)

    def _cat(self, cat):
        self.cat = cat
        self.btn_casa.configurar(color=VERDE if cat == "Casa" else GRIS_CLARO,
                                 fg="white" if cat == "Casa" else GRIS)
        self.btn_trab.configurar(color=AZUL if cat == "Trabajo" else GRIS_CLARO,
                                 fg="white" if cat == "Trabajo" else GRIS)

    def _icono(self, emo):
        self.icono = emo
        for e, lbl in self.botones_icono.items():
            lbl.config(bg=AMARILLO if e == emo else "#F2F3F4",
                       relief="sunken" if e == emo else "raised")

    def guardar(self):
        texto = self.entrada.get().strip()
        if not texto:
            Dialogo(self.app, "Falta algo", "Escribe primero\nqué hay que hacer.",
                    [("👍 ENTENDIDO", AZUL, "ok")], color_titulo=NARANJA, modal=True, parent=self)
            return
        resultado = {
            "texto": texto,
            "categoria": self.cat,
            "icono": self.icono,
            "hora": self.selector.valor() if self.var_hora.get() else "",
        }
        self.destroy()
        self.al_guardar(resultado)


# ---------------------------------------------------------------------------
#  VENTANAS DE LA APP
# ---------------------------------------------------------------------------

class VentanaBase(tk.Toplevel):
    clave = ""

    def __init__(self, app, titulo, color_fondo, color_encabezado, ancho, alto):
        super().__init__(app.root)
        self.app = app
        self.color_fondo = color_fondo
        self.title(t(titulo))
        self.configure(bg=color_fondo)
        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        enc = tk.Frame(self, bg=color_encabezado)
        enc.pack(fill="x")
        BotonGrande(enc, "⬅ VOLVER", oscurecer(color_encabezado, 0.75), self.cerrar,
                    fuente=(FUENTE, 16, "bold"), pady=6, padx=12).pack(side="left", padx=12, pady=10)
        self.titulo_lbl = Etiqueta(enc, titulo, bg=color_encabezado, fg="white", font=(FUENTE, 26, "bold"))
        self.titulo_lbl.pack(side="left", padx=10)
        self._ancho, self._alto = ancho, alto

    def mostrar(self):
        centrar(self, self._ancho, self._alto)

    def cerrar(self):
        self.app.ventanas.pop(self.clave, None)
        self.destroy()

    def refrescar(self):
        pass

    def tick(self):
        pass


# ----------------------------- MEDICINA ------------------------------------

class VentanaPastilla(VentanaBase):
    clave = "pastilla"

    def __init__(self, app):
        super().__init__(app, "💊 Mi Medicina", "#FFF0F0", ROJO, 900, 860)
        self.cuerpo = MarcoDesplazable(self, self.color_fondo)
        self.cuerpo.pack(fill="both", expand=True)
        self.refrescar()
        self.mostrar()

    def refrescar(self):
        self.cuerpo.reconstruir(self._construir)

    def _construir(self, i):
        bg = self.color_fondo
        app = self.app
        p = app.datos["pastilla"]
        estado, n, tomada = app.pastilla_estado()
        dias = int(p["dias"])
        persona = p["persona"]
        hora = hora_bonita(p["hora"])
        inicio = date.fromisoformat(p["inicio"])

        # ---- Panel de estado (grande) ----
        if estado == "tomada":
            color = VERDE
            texto = (f"✔ ¡MUY BIEN, {persona.upper()}!\nYa te tomaste tu pastilla hoy\n"
                     f"a las {hora_bonita(tomada)}\nNo tomes otra hasta mañana 😊")
        elif estado == "pendiente":
            color = ROJO
            texto = f"⏰ Hoy toca tu pastilla\n({p['medicina']})\nTodavía NO te la has tomado"
        elif estado == "temprano":
            color = AZUL
            texto = f"Hoy te toca a las {hora}\n({p['medicina']})\nTodavía no te la has tomado"
        elif estado == "terminado":
            color = MORADO
            texto = (f"🎉 ¡TERMINASTE, {persona.upper()}!\nCompletaste los {dias} días\n"
                     f"Tomaste {app.pastilla_total_tomadas()} de {dias} pastillas")
        else:
            color = GRIS
            texto = f"Tu tratamiento empieza\nel {fecha_bonita(inicio)}"

        Etiqueta(i, texto, bg=color, fg="white", font=(FUENTE, 28, "bold"), pady=24, padx=20,
                 wraplength=780, justify="center", relief="ridge", bd=6).pack(fill="x", padx=24, pady=(20, 8))

        if estado in ("tomada", "pendiente", "temprano"):
            Etiqueta(i, f"Día {n} de {dias} del tratamiento", bg=bg, font=(FUENTE, 20, "bold")).pack(pady=(0, 6))

        # ---- Botones grandes ----
        if estado in ("pendiente", "temprano"):
            BotonGrande(i, "✅ YA ME TOMÉ LA PASTILLA", VERDE, self.tome, fuente=(FUENTE, 32, "bold"),
                        pady=28).pack(fill="x", padx=24, pady=8)
        BotonGrande(i, "🤔 ¿YA ME LA TOMÉ HOY?", AZUL, app.dialogo_consulta_pastilla,
                    fuente=(FUENTE, 26, "bold"), pady=20).pack(fill="x", padx=24, pady=8)

        # ---- Calendario del tratamiento ----
        Etiqueta(i, "MI CALENDARIO DE PASTILLAS", bg=bg, font=(FUENTE, 22, "bold")).pack(pady=(22, 0))
        Etiqueta(i, f"Llevas {app.pastilla_total_tomadas()} pastillas tomadas de {dias} días",
                 bg=bg, font=(FUENTE, 18)).pack()
        rejilla = tk.Frame(i, bg=bg)
        rejilla.pack(pady=10)
        hoy = Reloj.hoy()
        for k in range(dias):
            d = inicio + timedelta(days=k)
            iso = d.isoformat()
            if iso in p["tomadas"]:
                col, fg, marca = VERDE, "white", OK
            elif d == hoy:
                col, fg, marca = AMARILLO, TEXTO, "HOY"
            elif d < hoy:
                col, fg, marca = ROJO, "white", NO
            else:
                col, fg, marca = GRIS_CLARO, GRIS, ""
            es_hoy = d == hoy
            tk.Label(rejilla, text=f"{k + 1}\n{marca}", bg=col, fg=fg, font=(FUENTE, 15, "bold"),
                     width=5, height=2, bd=3, relief="raised",
                     highlightthickness=4 if es_hoy else 0, highlightbackground=TEXTO
                     ).grid(row=k // 7, column=k % 7, padx=3, pady=3)

        leyenda = tk.Frame(i, bg=bg)
        leyenda.pack(pady=(4, 8))
        for col, nombre in ((VERDE, "Tomada"), (ROJO, "Olvidada"), (AMARILLO, "Hoy"), (GRIS_CLARO, "Falta")):
            tk.Label(leyenda, bg=col, width=2, height=1, bd=2, relief="raised").pack(side="left", padx=(12, 4))
            Etiqueta(leyenda, nombre, bg=bg, font=(FUENTE, 15)).pack(side="left")

        # ---- Opciones pequeñas ----
        pie = tk.Frame(i, bg=bg)
        pie.pack(fill="x", padx=24, pady=(10, 24))
        if estado == "tomada":
            BotonGrande(pie, "↩ Me equivoqué: todavía NO me la tomé", GRIS, self.deshacer,
                        fuente=(FUENTE, 15, "bold"), pady=8).pack(fill="x", pady=4)
        BotonGrande(pie, "⚙ Cambiar nombre, hora o días", GRIS, lambda: app.abrir(VentanaConfigPastilla),
                    fuente=(FUENTE, 15, "bold"), pady=8).pack(fill="x", pady=4)

    def tome(self):
        self.app.marcar_pastilla(True)
        self.app.dialogo_pastilla_anotada()

    def deshacer(self):
        if self.app.confirmar("¿Seguro?", "¿Quieres borrar la pastilla\nque marcaste hoy?",
                              si="↩ SÍ, BORRAR", no="NO, DEJAR ASÍ", parent=self):
            self.app.marcar_pastilla(False)


class VentanaConfigPastilla(VentanaBase):
    clave = "config_pastilla"

    def __init__(self, app):
        super().__init__(app, "⚙ Datos de la medicina", "#F4F6F7", GRIS, 760, 800)
        p = app.datos["pastilla"]
        bg = self.color_fondo
        cuerpo = MarcoDesplazable(self, bg)
        cuerpo.pack(fill="both", expand=True)
        i = cuerpo.interior

        def campo(texto):
            marco = tk.Frame(i, bg=bg)
            marco.pack(fill="x", padx=30, pady=8)
            Etiqueta(marco, texto, bg=bg, font=(FUENTE, 18, "bold")).pack(anchor="w")
            return marco

        m = campo("¿Quién toma la pastilla?")
        self.e_persona = tk.Entry(m, font=(FUENTE, 22), relief="solid", bd=2)
        self.e_persona.pack(fill="x", pady=4)
        self.e_persona.insert(0, p["persona"])

        m = campo("¿Qué medicina es?")
        self.e_medicina = tk.Entry(m, font=(FUENTE, 22), relief="solid", bd=2)
        self.e_medicina.pack(fill="x", pady=4)
        self.e_medicina.insert(0, p["medicina"])

        m = campo("¿A qué hora se toma?")
        self.hora = SelectorHora(m, bg, p["hora"])
        self.hora.pack(anchor="w", pady=4)

        m = campo("¿Cuántos días dura el tratamiento?")
        self.v_dias = tk.StringVar(value=str(p["dias"]))
        tk.Spinbox(m, from_=1, to=365, width=5, textvariable=self.v_dias, font=(FUENTE, 24, "bold"),
                   justify="center").pack(anchor="w", pady=4)

        m = campo("Si no la toma, avisar de nuevo cada (minutos):")
        self.v_rep = tk.StringVar(value=str(p["repetir_min"]))
        tk.Spinbox(m, from_=1, to=120, width=5, textvariable=self.v_rep, font=(FUENTE, 24, "bold"),
                   justify="center").pack(anchor="w", pady=4)

        BotonGrande(i, "💾 GUARDAR CAMBIOS", VERDE, self.guardar).pack(fill="x", padx=30, pady=(18, 6))
        BotonGrande(i, "🔄 EMPEZAR EL TRATAMIENTO DE NUEVO (desde hoy)", NARANJA, self.reiniciar,
                    fuente=(FUENTE, 17, "bold"), wraplength=620).pack(fill="x", padx=30, pady=(6, 24))
        self.mostrar()

    @staticmethod
    def _entero(texto, minimo, maximo, defecto):
        try:
            return min(maximo, max(minimo, int(texto)))
        except ValueError:
            return defecto

    def guardar(self):
        p = self.app.datos["pastilla"]
        p["persona"] = self.e_persona.get().strip() or "Abuelito"
        p["medicina"] = self.e_medicina.get().strip() or "Pastilla"
        p["hora"] = self.hora.valor()
        p["dias"] = self._entero(self.v_dias.get(), 1, 365, 30)
        p["repetir_min"] = self._entero(self.v_rep.get(), 1, 120, 10)
        self.app.ultimo_aviso_pastilla = None
        self.app.guardar()
        self.app.refrescar_todo()
        self.cerrar()

    def reiniciar(self):
        if self.app.confirmar("¿Empezar de nuevo?",
                              "Se borrará el calendario actual\ny el tratamiento empezará HOY.",
                              si="🔄 SÍ, EMPEZAR", no="NO", parent=self):
            p = self.app.datos["pastilla"]
            p["inicio"] = Reloj.hoy().isoformat()
            p["tomadas"] = {}
            self.app.ultimo_aviso_pastilla = None
            self.guardar()


# ----------------------------- NIÑOS ---------------------------------------

class VentanaNino(VentanaBase):
    clave = "nino"

    def __init__(self, app):
        super().__init__(app, "⭐ Mis Tareas", "#EAF2FF", AZUL, 900, 860)
        bg = self.color_fondo
        self.info = tk.Frame(self, bg=bg)
        self.info.pack(fill="x", padx=20, pady=(10, 0))

        pie = tk.Frame(self, bg=bg)
        pie.pack(side="bottom", fill="x", padx=20, pady=12)
        pie.columnconfigure(0, weight=3)
        pie.columnconfigure(1, weight=1)
        BotonGrande(pie, "➕ AGREGAR TAREA", MORADO, self.agregar, fuente=(FUENTE, 22, "bold")
                    ).grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        BotonGrande(pie, "✏ CAMBIAR NOMBRE", GRIS, self.cambiar_nombre, fuente=(FUENTE, 14, "bold")
                    ).grid(row=0, column=1, sticky="nsew")

        self.lista = MarcoDesplazable(self, bg)
        self.lista.pack(fill="both", expand=True, padx=10, pady=6)
        self.refrescar()
        self.mostrar()

    def refrescar(self):
        app = self.app
        n = app.datos["nino"]
        hoy = Reloj.hoy().isoformat()
        tareas = n["tareas"]
        total = len(tareas)
        hechas = sum(1 for x in tareas if x["hecha"] == hoy)
        bg = self.color_fondo
        self.titulo_lbl.poner(f"⭐ Tareas de {n['nombre']}")

        for w in self.info.winfo_children():
            w.destroy()
        if total == 0:
            mensaje = "No hay tareas todavía.\n¡Agrega una!"
        elif hechas == total:
            mensaje = f"🎉 ¡LO LOGRASTE, {n['nombre'].upper()}! 🎉\n¡Hiciste todas tus tareas de hoy!"
        else:
            mensaje = f"¡Hola, {n['nombre']}! Hoy llevas {hechas} de {total}"
        Etiqueta(self.info, mensaje, bg=bg, font=(FUENTE, 24, "bold"), justify="center").pack()
        if total:
            Etiqueta(self.info, ESTRELLA * hechas + ESTRELLA_VACIA * (total - hechas), bg=bg,
                     font=(FUENTE, 28)).pack()
            barra = tk.Canvas(self.info, width=640, height=30, bg=bg, highlightthickness=0)
            barra.pack(pady=4)
            barra.create_rectangle(2, 2, 638, 28, fill=GRIS_CLARO, outline=GRIS)
            if hechas:
                barra.create_rectangle(2, 2, 2 + int(636 * hechas / total), 28, fill=VERDE, outline=GRIS)
        Etiqueta(self.info, f"{ESTRELLA} Estrellas ganadas en total: {n['estrellas_total']}",
                 bg=bg, font=(FUENTE, 16)).pack(pady=(0, 4))

        self.lista.reconstruir(lambda i: self._filas(i, hoy))

    def _filas(self, i, hoy):
        app = self.app
        for k, x in enumerate(app.datos["nino"]["tareas"]):
            hecha = x["hecha"] == hoy
            texto = f"{OK if hecha else x['icono']}  {x['texto']}"
            if x["hora"]:
                texto += f"   ⏰ {hora_bonita(x['hora'])}"
            fila = tk.Frame(i, bg=self.color_fondo)
            fila.pack(fill="x", padx=14, pady=6)
            fila.columnconfigure(0, weight=1)
            BotonGrande(fila, texto, VERDE if hecha else PALETA_NINOS[k % len(PALETA_NINOS)],
                        lambda tid=x["id"]: app.alternar_tarea_nino(tid),
                        fuente=(FUENTE, 24, "bold"), pady=16, anchor="w", justify="left",
                        wraplength=640).grid(row=0, column=0, sticky="ew")
            BotonGrande(fila, BORRAR, GRIS, lambda tid=x["id"]: self.borrar(tid),
                        fuente=(FUENTE, 16, "bold"), padx=10, pady=8).grid(row=0, column=1, padx=(8, 0))

    def agregar(self):
        def guardar(r):
            self.app.agregar_tarea_nino(r["texto"], r["icono"], r["hora"])
        FormularioTarea(self.app, f"➕ Nueva tarea para {self.app.datos['nino']['nombre']}", guardar,
                        con_categoria=False, con_icono=True, parent=self)

    def borrar(self, tid):
        tarea = next((x for x in self.app.datos["nino"]["tareas"] if x["id"] == tid), None)
        if tarea and self.app.confirmar("¿Borrar tarea?", f"¿Quieres borrar esta tarea?\n\n{tarea['texto']}",
                                        parent=self):
            self.app.borrar_tarea_nino(tid)

    def cambiar_nombre(self):
        def guardar(nombre):
            self.app.datos["nino"]["nombre"] = nombre
            self.app.guardar()
            self.app.refrescar_todo()
        PedirTexto(self.app, "✏ Cambiar nombre", "¿Cómo se llama el niño o la niña?",
                   self.app.datos["nino"]["nombre"], guardar, parent=self)


# ----------------------------- CASA / TRABAJO ------------------------------

class VentanaTareas(VentanaBase):
    clave = "tareas"

    def __init__(self, app, filtro="Todas"):
        super().__init__(app, "📋 Mis Tareas", "#F0FFF4", VERDE, 900, 860)
        self.filtro = filtro
        bg = self.color_fondo

        barra = tk.Frame(self, bg=bg)
        barra.pack(fill="x", padx=16, pady=(12, 4))
        barra.columnconfigure((0, 1, 2), weight=1, uniform="f")
        self.botones_filtro = {}
        for col, (clave, texto, color) in enumerate((("Todas", "📋 TODAS", MORADO),
                                                     ("Casa", "🏠 CASA", VERDE),
                                                     ("Trabajo", "💼 TRABAJO", AZUL))):
            b = BotonGrande(barra, texto, color, lambda c=clave: self.poner_filtro(c),
                            fuente=(FUENTE, 20, "bold"), pady=10)
            b.grid(row=0, column=col, sticky="ew", padx=5)
            self.botones_filtro[clave] = (b, color)

        pie = tk.Frame(self, bg=bg)
        pie.pack(side="bottom", fill="x", padx=20, pady=12)
        pie.columnconfigure(0, weight=3)
        pie.columnconfigure(1, weight=1)
        BotonGrande(pie, "➕ NUEVA TAREA", MORADO, self.nueva, fuente=(FUENTE, 22, "bold")
                    ).grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        BotonGrande(pie, "🧹 QUITAR\nTERMINADAS", GRIS, self.quitar_terminadas,
                    fuente=(FUENTE, 13, "bold")).grid(row=0, column=1, sticky="nsew")

        self.lista = MarcoDesplazable(self, bg)
        self.lista.pack(fill="both", expand=True, padx=10, pady=6)
        self.refrescar()
        self.mostrar()

    def poner_filtro(self, filtro):
        self.filtro = filtro
        self.refrescar()

    def refrescar(self):
        nombres = {"Todas": "📋 Todas mis tareas", "Casa": "🏠 Tareas de la casa",
                   "Trabajo": "💼 Tareas del trabajo"}
        self.titulo_lbl.poner(nombres[self.filtro])
        for clave, (b, color) in self.botones_filtro.items():
            activo = clave == self.filtro
            b.configurar(color=color if activo else GRIS_CLARO, fg="white" if activo else GRIS)
        self.lista.reconstruir(self._filas)

    def _filas(self, i):
        app = self.app
        bg = self.color_fondo
        info = {"Casa": ("🏠", VERDE), "Trabajo": ("💼", AZUL)}
        tareas = [x for x in app.datos["tareas"] if self.filtro == "Todas" or x["categoria"] == self.filtro]
        tareas.sort(key=lambda x: (x["hecha"], x["hora"] or "99:99", x["id"]))
        if not tareas:
            Etiqueta(i, "🎉 ¡No hay nada pendiente!\nPresiona ➕ para agregar una tarea.",
                     bg=bg, font=(FUENTE, 24), pady=60).pack(fill="x")
            return
        for x in tareas:
            icono, color = info.get(x["categoria"], ("📌", GRIS))
            hecha = x["hecha"]
            fila = tk.Frame(i, bg=BLANCO, bd=3, relief="ridge")
            fila.pack(fill="x", padx=14, pady=6)
            BotonGrande(fila, CAJA_LLENA if hecha else CAJA_VACIA, VERDE if hecha else color,
                        lambda tid=x["id"]: app.alternar_tarea(tid), fuente=(FUENTE, 30, "bold"),
                        width=3, pady=6).pack(side="left", padx=10, pady=10)
            BotonGrande(fila, BORRAR, GRIS, lambda tid=x["id"]: self.borrar(tid),
                        fuente=(FUENTE, 16, "bold"), padx=10, pady=6).pack(side="right", padx=10)
            centro = tk.Frame(fila, bg=BLANCO)
            centro.pack(side="left", fill="x", expand=True, padx=6)
            Etiqueta(centro, x["texto"], bg=BLANCO, fg=GRIS if hecha else TEXTO,
                     font=(FUENTE, 22, "bold overstrike" if hecha else "bold"),
                     anchor="w", justify="left", wraplength=470).pack(fill="x")
            detalle = f"{icono} {x['categoria']}"
            if x["hora"]:
                detalle += f"     ⏰ {hora_bonita(x['hora'])}"
            Etiqueta(centro, detalle, bg=BLANCO, fg=GRIS, font=(FUENTE, 15), anchor="w").pack(fill="x")

    def nueva(self):
        def guardar(r):
            self.app.agregar_tarea(r["texto"], r["categoria"], r["hora"])
        FormularioTarea(self.app, "➕ Nueva tarea", guardar, con_categoria=True,
                        categoria="Trabajo" if self.filtro == "Trabajo" else "Casa", parent=self)

    def borrar(self, tid):
        tarea = next((x for x in self.app.datos["tareas"] if x["id"] == tid), None)
        if tarea and self.app.confirmar("¿Borrar tarea?", f"¿Quieres borrar esta tarea?\n\n{tarea['texto']}",
                                        parent=self):
            self.app.borrar_tarea(tid)

    def quitar_terminadas(self):
        if any(x["hecha"] for x in self.app.datos["tareas"]):
            if self.app.confirmar("¿Limpiar lista?", "¿Quitar todas las tareas\nque ya están terminadas?",
                                  si="🧹 SÍ, QUITAR", parent=self):
                self.app.quitar_terminadas()


# ----------------------------- DEMOSTRACIÓN --------------------------------

class VentanaDemo(VentanaBase):
    clave = "demo"

    def __init__(self, app):
        super().__init__(app, "🧪 Modo demostración", "#E8F8FF", TURQUESA, 800, 860)
        bg = self.color_fondo
        cuerpo = MarcoDesplazable(self, bg)
        cuerpo.pack(fill="both", expand=True)
        i = cuerpo.interior
        Etiqueta(i, "Aquí puedes «viajar en el tiempo» para ver cómo se comporta la app durante "
                    "todo el mes, sin esperar 30 días.", bg=bg, font=(FUENTE, 17), wraplength=700,
                 justify="center").pack(padx=24, pady=(18, 8))
        self.lbl = Etiqueta(i, "", bg=BLANCO, font=(FUENTE, 24, "bold"), relief="ridge", bd=4, pady=14,
                            wraplength=700)
        self.lbl.pack(fill="x", padx=24, pady=8)

        def boton(texto, color, comando, **kw):
            BotonGrande(i, texto, color, comando, fuente=(FUENTE, 19, "bold"), wraplength=680,
                        pady=12, **kw).pack(fill="x", padx=24, pady=6)

        boton("⏩ ADELANTAR 1 HORA", AZUL, lambda: app.avanzar(hours=1))
        boton("⏩ ADELANTAR 1 DÍA", AZUL, lambda: app.avanzar(days=1))
        boton("⏰ IR A LA HORA DE LA PASTILLA", ROJO, app.ir_a_hora_pastilla)
        boton("📅 LLENAR EL CALENDARIO CON UN EJEMPLO (15 días)", MORADO, self.ejemplo)
        boton("↩ VOLVER A LA FECHA Y HORA REAL", GRIS, app.volver_a_hora_real)
        boton("🗑 BORRAR TODOS MIS DATOS", oscurecer(ROJO, 0.7), self.borrar_todo)
        Etiqueta(i, "Tip: adelanta un día sin marcar la pastilla y verás ese día en ROJO "
                    "en el calendario.", bg=bg, font=(FUENTE, 15), wraplength=700, fg=GRIS
                 ).pack(padx=24, pady=(10, 24))
        self.tick()
        self.mostrar()

    def tick(self):
        extra = "" if Reloj.desfase == timedelta(0) else "\n(hora simulada)"
        self.lbl.poner(f"{fecha_bonita(Reloj.hoy())}\n{hora_bonita(Reloj.ahora().strftime('%H:%M'))}{extra}")

    def ejemplo(self):
        self.app.llenar_ejemplo()
        self.app.dialogo_simple("📅 Listo", "Se llenaron 15 días de ejemplo.\nRevisa la ventana de medicinas.",
                                parent=self)

    def borrar_todo(self):
        if self.app.confirmar("¿Borrar todo?", "Se borrarán TODOS tus datos\ny la app volverá a empezar.",
                              si="🗑 SÍ, BORRAR TODO", parent=self):
            self.app.borrar_todo()


# ---------------------------------------------------------------------------
#  APLICACIÓN PRINCIPAL
# ---------------------------------------------------------------------------

class App:
    def __init__(self):
        self.datos = cargar_datos()
        self.root = tk.Tk()
        self.root.title(t("Mi Ayudante del Hogar"))
        self.root.configure(bg=FONDO)
        self.ventanas = {}
        self.dialogos = []
        self.avisados = set()
        self.ultimo_aviso_pastilla = None
        self._firma = None

        self.construir_principal()
        centrar(self.root, 880, 800)
        self.root.minsize(640, 560)
        self.root.protocol("WM_DELETE_WINDOW", self.salir)
        self.refrescar_todo()
        self.reloj_tick()
        self.root.after(2500, self.revisar_recordatorios)

    def run(self):
        self.root.mainloop()

    def salir(self):
        self.guardar()
        self.root.destroy()

    # ------------------------------------------------------------------ datos
    def guardar(self):
        try:
            with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
                json.dump(self.datos, f, ensure_ascii=False, indent=2)
        except OSError:
            pass

    def nuevo_id(self):
        i = self.datos["sig_id"]
        self.datos["sig_id"] = i + 1
        return i

    # ------------------------------------------------------------ pantalla principal
    def construir_principal(self):
        r = self.root
        Etiqueta(r, "🏠 Mi Ayudante del Hogar", bg=FONDO, font=(FUENTE, 34, "bold")).pack(pady=(14, 0))
        self.lbl_fecha = Etiqueta(r, "", bg=FONDO, font=(FUENTE, 18))
        self.lbl_fecha.pack(pady=(0, 6))

        self.banner = BotonGrande(r, "", VERDE, self.abrir_pastilla, fuente=(FUENTE, 20, "bold"),
                                  pady=14, wraplength=760)
        self.banner.pack(fill="x", padx=28, pady=6)

        cuadricula = tk.Frame(r, bg=FONDO)
        cuadricula.pack(fill="both", expand=True, padx=20, pady=4)
        cuadricula.columnconfigure((0, 1), weight=1, uniform="c")
        cuadricula.rowconfigure((0, 1), weight=1, uniform="r")
        grande = (FUENTE, 26, "bold")
        self.btn_med = BotonGrande(cuadricula, "", ROJO, self.abrir_pastilla, fuente=grande)
        self.btn_nino = BotonGrande(cuadricula, "", AZUL, self.abrir_nino, fuente=grande)
        self.btn_casa = BotonGrande(cuadricula, "", VERDE, lambda: self.abrir_tareas("Casa"), fuente=grande)
        self.btn_trab = BotonGrande(cuadricula, "", NARANJA, lambda: self.abrir_tareas("Trabajo"), fuente=grande)
        self.btn_med.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self.btn_nino.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
        self.btn_casa.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
        self.btn_trab.grid(row=1, column=1, sticky="nsew", padx=8, pady=8)

        fila = tk.Frame(r, bg=FONDO)
        fila.pack(fill="x", padx=20, pady=(4, 16))
        fila.columnconfigure(0, weight=3)
        fila.columnconfigure(1, weight=1)
        BotonGrande(fila, "➕ NUEVO RECORDATORIO", MORADO, self.nueva_tarea_rapida,
                    fuente=(FUENTE, 22, "bold")).grid(row=0, column=0, sticky="nsew", padx=8)
        BotonGrande(fila, "🧪 DEMOSTRACIÓN", TURQUESA, lambda: self.abrir(VentanaDemo),
                    fuente=(FUENTE, 14, "bold")).grid(row=0, column=1, sticky="nsew", padx=8)

    def refrescar_principal(self):
        estado, n, tomada = self.pastilla_estado()
        p = self.datos["pastilla"]
        dias = int(p["dias"])
        hora = hora_bonita(p["hora"])
        if estado == "tomada":
            banner = (f"💊 Pastilla de hoy:  ✔ ¡YA LA TOMASTE!  ({hora_bonita(tomada)})", VERDE)
            sub = f"Día {n} de {dias}\n✔ Ya tomada hoy"
        elif estado == "pendiente":
            banner = (f"💊 Pastilla de hoy:  ⏰ TODAVÍA NO  (tocaba a las {hora})", ROJO)
            sub = f"Día {n} de {dias}\n⏰ ¡Falta la de hoy!"
        elif estado == "temprano":
            banner = (f"💊 Pastilla de hoy:  toca a las {hora}", AZUL)
            sub = f"Día {n} de {dias}\nHoy a las {hora}"
        elif estado == "terminado":
            banner = (f"🎉 ¡Terminaste los {dias} días de tratamiento!", MORADO)
            sub = "🎉 ¡Terminado!"
        else:
            inicio = date.fromisoformat(p["inicio"])
            banner = (f"💊 El tratamiento empieza el {inicio:%d/%m/%Y}", GRIS)
            sub = "Aún no empieza"
        self.banner.configurar(texto=banner[0], color=banner[1])
        self.btn_med.configurar(texto=f"💊 MEDICINAS\n{sub}")

        nino = self.datos["nino"]
        hoy = Reloj.hoy().isoformat()
        total = len(nino["tareas"])
        hechas = sum(1 for x in nino["tareas"] if x["hecha"] == hoy)
        self.btn_nino.configurar(texto=f"⭐ {nino['nombre'].upper()}\n{hechas} de {total} tareas hechas")

        def pendientes(cat):
            n_pend = sum(1 for x in self.datos["tareas"] if x["categoria"] == cat and not x["hecha"])
            return "¡Todo listo! ✔" if n_pend == 0 else f"{n_pend} pendiente{'s' if n_pend != 1 else ''}"

        self.btn_casa.configurar(texto=f"🏠 CASA\n{pendientes('Casa')}")
        self.btn_trab.configurar(texto=f"💼 TRABAJO\n{pendientes('Trabajo')}")

    def refrescar_todo(self):
        self.refrescar_principal()
        for clave, v in list(self.ventanas.items()):
            try:
                if v.winfo_exists():
                    v.refrescar()
                else:
                    self.ventanas.pop(clave, None)
            except tk.TclError:
                self.ventanas.pop(clave, None)

    def reloj_tick(self):
        ahora = Reloj.ahora()
        self.lbl_fecha.poner(f"{fecha_bonita(ahora.date())}  —  "
                             f"{hora_bonita(ahora.strftime('%H:%M'))}")
        firma = (self.pastilla_estado()[0], ahora.date())
        if firma != self._firma:
            self._firma = firma
            self.refrescar_todo()
        for v in list(self.ventanas.values()):
            try:
                v.tick()
            except tk.TclError:
                pass
        self.root.after(1000, self.reloj_tick)

    # ------------------------------------------------------------- ventanas
    def abrir(self, clase, *args):
        v = self.ventanas.get(clase.clave)
        if v is not None and v.winfo_exists():
            v.deiconify()
            v.lift()
            v.focus_force()
            return v
        v = clase(self, *args)
        self.ventanas[clase.clave] = v
        return v

    def abrir_pastilla(self):
        self.abrir(VentanaPastilla)

    def abrir_nino(self):
        self.abrir(VentanaNino)

    def abrir_tareas(self, filtro="Todas"):
        v = self.abrir(VentanaTareas, filtro)
        v.poner_filtro(filtro)

    def nueva_tarea_rapida(self):
        def guardar(r):
            self.agregar_tarea(r["texto"], r["categoria"], r["hora"])
            self.abrir_tareas(r["categoria"])
        FormularioTarea(self, "➕ Nuevo recordatorio", guardar, con_categoria=True)

    # ----------------------------------------------------------- diálogos
    def sonar(self, veces=3):
        def pitido():
            try:
                import winsound
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            except Exception:
                self.root.bell()
        for k in range(veces):
            self.root.after(k * 700, pitido)

    def confirmar(self, titulo, mensaje, si="🗑 SÍ, BORRAR", no="✖ NO", parent=None):
        d = Dialogo(self, titulo, mensaje, [(si, ROJO, True), (no, GRIS, False)],
                    color_titulo=NARANJA, modal=True, parent=parent)
        return d.resultado is True

    def dialogo_simple(self, titulo, mensaje, parent=None):
        Dialogo(self, titulo, mensaje, [("👍 ENTENDIDO", AZUL, "ok")], modal=True, parent=parent)

    # --------------------------------------------------------------- pastilla
    def pastilla_estado(self):
        """Devuelve (estado, número_de_día, hora_tomada)."""
        p = self.datos["pastilla"]
        hoy = Reloj.hoy()
        inicio = date.fromisoformat(p["inicio"])
        dias = int(p["dias"])
        n = (hoy - inicio).days + 1
        tomada = p["tomadas"].get(hoy.isoformat())
        if n < 1:
            return "sin_empezar", n, None
        if n > dias:
            return "terminado", n, None
        if tomada:
            return "tomada", n, tomada
        try:
            hh, mm = (int(x) for x in p["hora"].split(":"))
        except ValueError:
            hh, mm = 8, 0
        if Reloj.ahora().time() >= dtime(hh, mm):
            return "pendiente", n, None
        return "temprano", n, None

    def pastilla_total_tomadas(self):
        p = self.datos["pastilla"]
        inicio = date.fromisoformat(p["inicio"])
        fin = inicio + timedelta(days=int(p["dias"]))
        total = 0
        for k in p["tomadas"]:
            try:
                if inicio <= date.fromisoformat(k) < fin:
                    total += 1
            except ValueError:
                pass
        return total

    def marcar_pastilla(self, tomada):
        p = self.datos["pastilla"]
        hoy = Reloj.hoy().isoformat()
        if tomada:
            p["tomadas"].setdefault(hoy, Reloj.ahora().strftime("%H:%M"))
        else:
            p["tomadas"].pop(hoy, None)
            self.ultimo_aviso_pastilla = None
        self.guardar()
        self.refrescar_todo()

    def dialogo_pastilla_anotada(self, modal=True):
        p = self.datos["pastilla"]
        hora = hora_bonita(self.datos["pastilla"]["tomadas"].get(Reloj.hoy().isoformat(), "00:00"))
        Dialogo(self, "¡Muy bien!",
                f"✔ Anotado, {p['persona']}.\nTe tomaste tu pastilla hoy\na las {hora}.\n\n"
                "¡Nos vemos mañana! 😊",
                [("👍 GRACIAS", VERDE, "ok")], color="#E8FFF0", color_titulo=VERDE, modal=modal)

    def dialogo_consulta_pastilla(self):
        estado, n, tomada = self.pastilla_estado()
        p = self.datos["pastilla"]
        if estado == "tomada":
            Dialogo(self, "¿Ya me la tomé hoy?",
                    f"✔ ¡SÍ!\nYa te tomaste tu pastilla hoy\na las {hora_bonita(tomada)}.\n\n"
                    "No tomes otra hasta mañana.",
                    [("👍 ENTENDIDO", VERDE, "ok")], color="#E8FFF0", color_titulo=VERDE, modal=True)
        elif estado in ("pendiente", "temprano"):
            Dialogo(self, "¿Ya me la tomé hoy?",
                    f"✘ TODAVÍA NO.\nHoy aún no te has tomado\n{p['medicina'].lower()}.\n\n"
                    "Cuando la tomes,\npresiona el botón verde.",
                    [("👍 ENTENDIDO", ROJO, "ok")], color="#FFF0F0", color_titulo=ROJO, modal=True)
        elif estado == "terminado":
            self.dialogo_simple("¿Ya me la tomé hoy?", "🎉 Ya terminaste tu tratamiento.\nYa no necesitas tomarla.")
        else:
            self.dialogo_simple("¿Ya me la tomé hoy?", "Tu tratamiento todavía no empieza.")

    def aviso_pastilla(self):
        p = self.datos["pastilla"]

        def elegido(valor):
            if valor == "tomada":
                self.marcar_pastilla(True)
                self.dialogo_pastilla_anotada(modal=False)

        Dialogo(self, "⏰ ¡Hora de tu medicina!",
                f"{p['persona']}, es hora de tomar:\n{p['medicina']}\n(a las {hora_bonita(p['hora'])})",
                [("✅ YA ME LA TOMÉ", VERDE, "tomada"),
                 (f"⏳ Recuérdame en {p['repetir_min']} min", NARANJA, "luego")],
                color="#FFF0F0", color_titulo=ROJO, al_elegir=elegido, sonido=True)

    # ------------------------------------------------------------ niños
    def poner_tarea_nino(self, tid, hecha):
        hoy = Reloj.hoy().isoformat()
        n = self.datos["nino"]
        tarea = next((x for x in n["tareas"] if x["id"] == tid), None)
        if tarea is None:
            return
        ya = tarea["hecha"] == hoy
        if hecha and not ya:
            tarea["hecha"] = hoy
            n["estrellas_total"] += 1
        elif not hecha and ya:
            tarea["hecha"] = ""
            n["estrellas_total"] = max(0, n["estrellas_total"] - 1)
        else:
            return
        self.guardar()
        self.refrescar_todo()
        if hecha and all(x["hecha"] == hoy for x in n["tareas"]):
            Dialogo(self, "🎉 ¡FELICIDADES! 🎉",
                    f"¡Lo lograste, {n['nombre']}!\nHiciste todas tus tareas de hoy.\n\n¡Eres un campeón! 🏆",
                    [("🎈 ¡HURRA!", VERDE, "ok")], color="#FFF9DB", color_titulo=ROSA, sonido=True)

    def alternar_tarea_nino(self, tid):
        hoy = Reloj.hoy().isoformat()
        tarea = next((x for x in self.datos["nino"]["tareas"] if x["id"] == tid), None)
        if tarea:
            self.poner_tarea_nino(tid, tarea["hecha"] != hoy)

    def agregar_tarea_nino(self, texto, icono, hora):
        tarea = {"id": self.nuevo_id(), "texto": texto, "icono": icono, "hora": hora, "hecha": ""}
        self.datos["nino"]["tareas"].append(tarea)
        self._silenciar_si_paso(("nino", tarea["id"]), hora)
        self.guardar()
        self.refrescar_todo()

    def borrar_tarea_nino(self, tid):
        self.datos["nino"]["tareas"] = [x for x in self.datos["nino"]["tareas"] if x["id"] != tid]
        self.guardar()
        self.refrescar_todo()

    def aviso_tarea_nino(self, tarea):
        nombre = self.datos["nino"]["nombre"]

        def elegido(valor):
            if valor == "hecha":
                self.poner_tarea_nino(tarea["id"], True)

        Dialogo(self, "⭐ ¡Es hora de tu tarea!", f"¡{nombre}, es hora de:\n\n{tarea['icono']}  {tarea['texto']}",
                [("✅ ¡YA LA HICE!", VERDE, "hecha"), ("⏳ Ahorita voy", NARANJA, "luego")],
                color="#EAF2FF", color_titulo=AZUL, al_elegir=elegido, sonido=True)

    # ------------------------------------------------------- casa / trabajo
    def agregar_tarea(self, texto, categoria, hora):
        tarea = {"id": self.nuevo_id(), "texto": texto, "categoria": categoria, "hora": hora, "hecha": False}
        self.datos["tareas"].append(tarea)
        self._silenciar_si_paso(("tarea", tarea["id"]), hora)
        self.guardar()
        self.refrescar_todo()

    def poner_tarea(self, tid, hecha):
        for x in self.datos["tareas"]:
            if x["id"] == tid:
                x["hecha"] = hecha
        self.guardar()
        self.refrescar_todo()

    def alternar_tarea(self, tid):
        tarea = next((x for x in self.datos["tareas"] if x["id"] == tid), None)
        if tarea:
            self.poner_tarea(tid, not tarea["hecha"])

    def borrar_tarea(self, tid):
        self.datos["tareas"] = [x for x in self.datos["tareas"] if x["id"] != tid]
        self.guardar()
        self.refrescar_todo()

    def quitar_terminadas(self):
        self.datos["tareas"] = [x for x in self.datos["tareas"] if not x["hecha"]]
        self.guardar()
        self.refrescar_todo()

    def aviso_tarea(self, tarea):
        def elegido(valor):
            if valor == "hecha":
                self.poner_tarea(tarea["id"], True)

        icono = "🏠" if tarea["categoria"] == "Casa" else "💼"
        Dialogo(self, f"{icono} ¡Recordatorio!", f"{tarea['texto']}\n\n({tarea['categoria']})",
                [("✅ YA LO HICE", VERDE, "hecha"), ("⏳ Después", NARANJA, "luego")],
                color="#F0FFF4", color_titulo=VERDE if tarea["categoria"] == "Casa" else AZUL,
                al_elegir=elegido, sonido=True)

    # ------------------------------------------------------- recordatorios
    def _silenciar_si_paso(self, base, hora):
        """Si se crea una tarea con una hora que ya pasó hoy, no avisar de inmediato."""
        if hora and Reloj.ahora().strftime("%H:%M") >= hora:
            self.avisados.add(base + (Reloj.hoy().isoformat(),))

    def revisar_recordatorios(self):
        try:
            self._revisar()
        except tk.TclError:
            pass
        finally:
            self.root.after(5000, self.revisar_recordatorios)

    def _revisar(self):
        self.dialogos = [d for d in self.dialogos if d.winfo_exists()]
        if self.dialogos:
            return  # ya hay un aviso abierto: se muestra de uno en uno
        ahora = Reloj.ahora()
        hoy = ahora.date().isoformat()
        hhmm = ahora.strftime("%H:%M")

        # 1) Pastilla: insiste cada N minutos hasta que se confirme
        estado, _, _ = self.pastilla_estado()
        if estado == "pendiente":
            u = self.ultimo_aviso_pastilla
            if u is not None and (u > ahora or u.date() != ahora.date()):
                u = self.ultimo_aviso_pastilla = None
            repetir = timedelta(minutes=max(1, int(self.datos["pastilla"]["repetir_min"])))
            if u is None or ahora - u >= repetir:
                self.ultimo_aviso_pastilla = ahora
                self.aviso_pastilla()
                return

        # 2) Tareas del niño con hora
        for x in self.datos["nino"]["tareas"]:
            if x["hora"] and x["hecha"] != hoy and hhmm >= x["hora"]:
                clave = ("nino", x["id"], hoy)
                if clave not in self.avisados:
                    self.avisados.add(clave)
                    self.aviso_tarea_nino(x)
                    return

        # 3) Tareas de casa / trabajo con hora
        for x in self.datos["tareas"]:
            if x["hora"] and not x["hecha"] and hhmm >= x["hora"]:
                clave = ("tarea", x["id"], hoy)
                if clave not in self.avisados:
                    self.avisados.add(clave)
                    self.aviso_tarea(x)
                    return

    # --------------------------------------------------------- demostración
    def _tras_cambio_reloj(self):
        self.refrescar_todo()
        try:
            self._revisar()
        except tk.TclError:
            pass

    def avanzar(self, **kw):
        Reloj.desfase += timedelta(**kw)
        self._tras_cambio_reloj()

    def ir_a_hora_pastilla(self):
        try:
            hh, mm = (int(x) for x in self.datos["pastilla"]["hora"].split(":"))
        except ValueError:
            hh, mm = 8, 0
        destino = datetime.combine(Reloj.hoy(), dtime(hh, mm))
        Reloj.desfase = destino - datetime.now()
        self.ultimo_aviso_pastilla = None
        self._tras_cambio_reloj()

    def volver_a_hora_real(self):
        Reloj.desfase = timedelta(0)
        self.ultimo_aviso_pastilla = None
        self._tras_cambio_reloj()

    def llenar_ejemplo(self):
        p = self.datos["pastilla"]
        hoy = Reloj.hoy()
        p["inicio"] = (hoy - timedelta(days=14)).isoformat()
        p["tomadas"] = {}
        hh, mm = (int(x) for x in p["hora"].split(":"))
        for k in range(14):
            if random.random() < 0.85:
                minuto = min(59 * 60, (hh * 60 + mm + random.randint(0, 40)))
                p["tomadas"][(hoy - timedelta(days=14 - k)).isoformat()] = f"{minuto // 60:02d}:{minuto % 60:02d}"
        self.ultimo_aviso_pastilla = None
        self.guardar()
        self.refrescar_todo()

    def borrar_todo(self):
        self.datos = datos_iniciales()
        Reloj.desfase = timedelta(0)
        self.avisados.clear()
        self.ultimo_aviso_pastilla = None
        self.guardar()
        self.refrescar_todo()


if __name__ == "__main__":
    App().run()