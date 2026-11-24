"""
Pruebas de teclado de RecuerdaMe (solo teclado, sin mouse).

Cómo correrlas (una sola vez la instalación):
    pip install playwright
    playwright install chromium
    python pruebas/prueba_teclado.py

Comprueban: orden de Tab, "Saltar al contenido", Enter/Espacio, que el foco no se
pierda al redibujar listas, ventanas emergentes (foco, Tab, Esc), flechas en
emociones/forma/color, y el modo oscuro (también solo con teclado).
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent.parent.as_uri() + "/"
resultados = []
def ok(nombre, cond, detalle=""):
    resultados.append((nombre, bool(cond), detalle))
    print(("PASS " if cond else "FAIL ") + nombre + (f"  → {detalle}" if detalle else ""))

DESC = """() => { const e=document.activeElement; if(!e) return 'null';
  const t=(e.innerText||e.value||'').trim().replace(/\\s+/g,' ').slice(0,40);
  return e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(t?' «'+t+'»':''); }"""

with sync_playwright() as p:
    b = p.chromium.launch()
    errores = []

    # ---------------- ADULTO ----------------
    ctx = b.new_context(color_scheme="light", viewport={"width":1100,"height":900})
    pg = ctx.new_page(); pg.on("pageerror", lambda e: errores.append(str(e))); pg.on("console", lambda m: errores.append(m.text) if m.type=="error" and "fonts" not in m.text.lower() and "ERR_" not in m.text else None)
    pg.goto(BASE+"adulto.html"); pg.wait_for_selector("[data-toggle-med]")
    orden = []
    for _ in range(8):
        pg.keyboard.press("Tab"); orden.append(pg.evaluate(DESC))
    print("Orden de Tab (adulto):"); [print("   ",i+1,o) for i,o in enumerate(orden)]
    ok("A1 primer Tab = enlace 'Saltar al contenido'", "Saltar al contenido" in orden[0], orden[0])
    ok("A2 orden: marca → Cambiar perfil → Modo oscuro → Agregar Medicina",
       "RecuerdaMe" in orden[1] and "Cambiar perfil" in orden[2] and "Modo oscuro" in orden[3] and "Agregar Medicina" in orden[4], " | ".join(orden[1:5]))

    # Saltar al contenido mueve el foco a <main>
    pg.reload(); pg.wait_for_selector("[data-toggle-med]")
    pg.keyboard.press("Tab"); pg.keyboard.press("Enter")
    pg.keyboard.press("Tab")
    sig = pg.evaluate(DESC)
    ok("A3 'Saltar al contenido' lleva el foco al contenido (siguiente Tab = primer control del main)", "Agregar Medicina" in sig, sig)

    # Activar una medicina con Enter y conservar el foco
    pg.focus("[data-toggle-med]")
    med_id = pg.evaluate("document.activeElement.getAttribute('data-toggle-med')")
    antes = pg.evaluate("document.activeElement.innerText.trim()")
    pg.keyboard.press("Enter"); pg.wait_for_timeout(150)
    mismo = pg.evaluate("(id)=>document.activeElement.getAttribute('data-toggle-med')===id", med_id)
    despues = pg.evaluate("document.activeElement.innerText.trim()")
    ok("A4 tras marcar medicina con Enter, el foco sigue en el mismo botón", mismo, f"«{antes}» → «{despues}»")
    pg.keyboard.press("Space"); pg.wait_for_timeout(150)
    ok("A5 Space también funciona y conserva el foco", pg.evaluate("(id)=>document.activeElement.getAttribute('data-toggle-med')===id", med_id))

    # Modal medicina
    pg.focus("#btn-abrir-modal-med"); pg.keyboard.press("Enter"); pg.wait_for_timeout(150)
    ok("A6 al abrir la ventana, el foco va al campo 'Nombre'", pg.evaluate(DESC).startswith("input#modal-med-nombre"), pg.evaluate(DESC))
    pg.keyboard.type("Prueba 10 mg")
    # Tab dentro del modal (no se escapa)
    fuera=[]
    for _ in range(30):
        pg.keyboard.press("Tab")
        r=pg.evaluate("""()=>{const e=document.activeElement; return e!==document.body && !e.closest('#modal-medicina') ? e.tagName+(e.id?'#'+e.id:'') : ''}""")
        if r: fuera.append(r)
    ok("A7 Tab nunca sale de la ventana emergente hacia la página", not fuera, str(fuera))
    # Radios con flechas
    pg.focus("input[name=modal-forma]:checked")
    pg.keyboard.press("ArrowRight")
    forma = pg.evaluate("document.querySelector('input[name=modal-forma]:checked').value")
    prev = pg.inner_text("#preview-pill-text")
    ok("A8 flechas cambian la forma y la vista previa se actualiza", forma=="pildora" and "Píldora" in prev, prev)
    pg.focus("input[name=modal-color]:checked"); pg.keyboard.press("ArrowRight"); pg.keyboard.press("ArrowRight")
    prev = pg.inner_text("#preview-pill-text")
    ok("A9 flechas cambian el color", "Amarilla" in prev, prev)
    # Esc
    pg.keyboard.press("Escape"); pg.wait_for_timeout(150)
    ok("A10 Esc cierra y el foco vuelve a 'Agregar Medicina'", pg.evaluate("!document.getElementById('modal-medicina').open") and pg.evaluate(DESC).startswith("button#btn-abrir-modal-med"), pg.evaluate(DESC))
    # Guardar con Enter
    pg.keyboard.press("Enter"); pg.wait_for_timeout(150)
    pg.fill("#modal-med-nombre", "Prueba 10 mg"); pg.focus("#modal-med-nombre"); pg.keyboard.press("Enter"); pg.wait_for_timeout(250)
    ok("A11 Enter en el formulario guarda, cierra y devuelve el foco", pg.evaluate("!document.getElementById('modal-medicina').open") and "Prueba 10 mg" in pg.inner_text("#lista-medicamentos") and pg.evaluate(DESC).startswith("button#btn-abrir-modal-med"), pg.evaluate(DESC))
    # Error de validación: foco en campo con error
    pg.keyboard.press("Enter"); pg.wait_for_timeout(100)
    pg.focus("#modal-med-nombre"); pg.fill("#modal-med-nombre", ""); pg.keyboard.press("Enter"); pg.wait_for_timeout(100)
    ok("A12 con el nombre vacío aparece el aviso y el foco queda en el campo", pg.evaluate(DESC).startswith("input#modal-med-nombre") and "Escribe el nombre" in pg.inner_text("#error-modal-med-nombre"))
    pg.keyboard.press("Escape")
    ctx.close()

    # ---------------- NIÑOS ----------------
    ctx = b.new_context(color_scheme="light", viewport={"width":1100,"height":900})
    pg = ctx.new_page(); pg.on("pageerror", lambda e: errores.append(str(e)))
    pg.goto(BASE+"nino.html"); pg.wait_for_selector("[data-emo-id]")
    tabs = pg.evaluate("[...document.querySelectorAll('[data-emo-id]')].map(e=>e.tabIndex)")
    ok("B1 el selector de emociones es UNA sola parada de Tab", sorted(tabs)==[-1,-1,-1,-1,0], str(tabs))
    pg.focus("[data-emo-id][tabindex='0']")
    ini = pg.evaluate("document.activeElement.dataset.emoId")
    pg.keyboard.press("ArrowRight"); sig = pg.evaluate("document.activeElement.dataset.emoId")
    pg.keyboard.press("End"); fin = pg.evaluate("document.activeElement.dataset.emoId")
    pg.keyboard.press("Home"); home = pg.evaluate("document.activeElement.dataset.emoId")
    pg.keyboard.press("ArrowLeft"); envuelve = pg.evaluate("document.activeElement.dataset.emoId")
    ok("B2 flechas, Inicio y Fin recorren los 5 personajes (y dan la vuelta)", len({ini,sig,fin})==3 and home==ini and envuelve==fin, f"{ini}→{sig}, fin={fin}, home={home}, ←={envuelve}")
    pg.keyboard.press("ArrowLeft")  # un personaje distinto
    elegido = pg.evaluate("document.activeElement.dataset.emoId")
    pg.keyboard.press("Enter"); pg.wait_for_timeout(200)
    st = pg.evaluate("(id)=>{const a=document.activeElement;return [a.dataset.emoId===id, a.getAttribute('aria-pressed')]}", elegido)
    ok("B3 Enter elige la emoción y el foco no se pierde", st==[True,"true"], str(st))
    pg.keyboard.press("ArrowRight")
    ok("B4 se puede seguir usando las flechas después de elegir", pg.evaluate("!!document.activeElement.dataset.emoId") and pg.evaluate("document.activeElement.dataset.emoId")!=elegido)
    # Tarea con teclado
    pg.focus("[data-kid-id]"); kid_id = pg.evaluate("document.activeElement.dataset.kidId")
    pg.keyboard.press("Space"); pg.wait_for_timeout(200)
    ok("B5 completar una tarea con teclado conserva el foco", pg.evaluate("(id)=>document.activeElement.dataset.kidId===id", kid_id))
    # Guía
    pg.focus("[data-learn-guide]"); gid = pg.evaluate("document.activeElement.dataset.learnGuide")
    pg.keyboard.press("Enter"); pg.wait_for_timeout(200)
    ok("B6 '¡Ya aprendí a hacerlo!' conserva el foco", pg.evaluate("(id)=>document.activeElement.dataset.learnGuide===id", gid))
    # Diario: guardar y revisar
    pg.fill("#input-diario-texto", "Hoy jugué"); pg.focus("#form-diario-emocion button[type=submit]"); pg.keyboard.press("Enter"); pg.wait_for_timeout(200)
    pg.focus("[data-review-diary]"); rid = pg.evaluate("document.activeElement.dataset.reviewDiary"); pg.keyboard.press("Enter"); pg.wait_for_timeout(200)
    ok("B7 'Marcar como revisado' conserva el foco", pg.evaluate("(id)=>document.activeElement.dataset.reviewDiary===id", rid))
    # Modal niño
    pg.focus("#btn-abrir-modal-nino"); pg.keyboard.press("Enter"); pg.wait_for_timeout(150)
    ok("B8 ventana de niños: el foco entra al primer control del formulario", pg.evaluate("!!document.activeElement.closest('.modal-body')"), pg.evaluate(DESC))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
    ok("B9 Esc devuelve el foco a 'Agregar Tarea'", pg.evaluate(DESC).startswith("button#btn-abrir-modal-nino"))
    ctx.close()

    # ---------------- MODO OSCURO ----------------
    ctx = b.new_context(color_scheme="light", viewport={"width":1100,"height":900})
    pg = ctx.new_page(); pg.goto(BASE+"index.html"); pg.wait_for_selector("#btn-tema")
    ok("C1 sistema claro → arranca claro", pg.evaluate("document.documentElement.dataset.theme")=="light")
    pg.focus("#btn-tema"); pg.keyboard.press("Enter"); pg.wait_for_timeout(100)
    ok("C2 el botón activa modo oscuro con teclado y cambia su texto", pg.evaluate("document.documentElement.dataset.theme")=="dark" and "Modo claro" in pg.inner_text("#btn-tema"), pg.inner_text("#btn-tema"))
    ok("C3 el foco sigue en el botón de tema", pg.evaluate(DESC).startswith("button#btn-tema"))
    pg.goto(BASE+"nino.html")
    ok("C4 la elección se recuerda en otra página", pg.evaluate("document.documentElement.dataset.theme")=="dark" and pg.evaluate("localStorage.getItem('recuerdame_tema')")=="oscuro")
    ctx.close()
    ctx = b.new_context(color_scheme="dark", viewport={"width":1100,"height":900})
    pg = ctx.new_page(); pg.goto(BASE+"adulto.html"); pg.wait_for_selector("#btn-tema")
    ok("C5 sistema oscuro y sin elección previa → arranca oscuro", pg.evaluate("document.documentElement.dataset.theme")=="dark")
    pg.focus("#btn-tema"); pg.keyboard.press("Enter"); pg.reload(); pg.wait_for_selector("#btn-tema")
    ok("C6 si elige claro con el sistema oscuro, se respeta al recargar", pg.evaluate("document.documentElement.dataset.theme")=="light")
    ctx.close()

    ok("D0 sin errores de JavaScript", not errores, "; ".join(errores)[:200])
    b.close()

fallos = [r for r in resultados if not r[1]]
print(f"\n{len(resultados)-len(fallos)}/{len(resultados)} pruebas correctas")
sys.exit(1 if fallos else 0)
