# RecuerdaMe 

Aplicación web accesible diseñada para apoyar la organización diaria mediante dos perfiles adaptados visual y funcionalmente: **Adulto Mayor** y **Niños**.

🔗 **Ver página en vivo:** https://vast1on.github.io/RecuerdaMe/



Funcionalidades Principales

Perfil Adulto Mayor 
* **Control visual de medicamentos:** Identificación de pastillas por forma (redonda, píldora, cápsula), color y horario.
* **Seguimiento de tratamiento:** Contador visual de días completados y días restantes por medicina.
* **Contactos y citas importantes:** Acceso directo a llamadas de emergencia y recordatorios médicos.
* **Racha de cuidado:** Registro de días consecutivos cumpliendo las tomas.

Perfil Niños
* **¿Cómo me siento hoy?:** Selector interactivo de emociones con consejos personalizados según el estado de ánimo.
* **Diario de emociones para padres:** Espacio para que el niño escriba por qué se siente así y los padres puedan marcar las notas como revisadas.
* **Tareas y hábitos con stickers:** Lista de tareas del hogar y rutinas diarias con barra de progreso, racha semanal y álbum de stickers desbloqueables.
* **¿Cómo lo hago?:** Guías ilustradas paso a paso para aprender actividades cotidianas (abrocharse las agujetas, tender la cama y lavarse las manos).

-

Tecnologías Utilizadas
HTML semántico (estructura accesible con soporte para lectores de pantalla y navegación por teclado).
CSS3(variables personalizadas, diseño responsivo y alto contraste).
JavaScript  (renderizado dinámico, ventanas modales `<dialog>` y persistencia local mediante `localStorage`).

---

 Estructura del Proyecto

├── index.html     # Menú principal de selección de perfil
├── adulto.html    # Vista y controles para Adulto Mayor
├── nino.html      # Vista interactiva, diario y guías para Niños
├── styles.css     # Estilos globales, temas por perfil y diseño responsivo
├── app.js         # Lógica de datos, eventos, teclado, modo oscuro y almacenamiento en localStorage
├── pruebas/
│   └── prueba_teclado.py   # Pruebas automáticas de uso solo con teclado
└── README.md      # Documentación del proyecto

---

## Uso con teclado

Toda la aplicación se puede usar sin mouse. El orden de Tab sigue el orden visual de la página
(encabezado → contenido → ventanas emergentes) y el foco siempre se ve con un contorno de color.

| Tecla | Qué hace |
|---|---|
| `Tab` / `Shift + Tab` | Avanzar / retroceder entre botones, enlaces y campos |
| `Enter` o `Espacio` | Activar el botón (marcar medicina, completar tarea, elegir emoción…) |
| `Tab` y luego `Enter` (al entrar a la página) | "Saltar al contenido principal" |
| `←` `→` `↑` `↓` | Moverse entre los personajes de emociones; cambiar forma y color de la medicina |
| `Inicio` / `Fin` | Ir a la primera / última emoción |
| `Esc` | Cerrar una ventana emergente (el foco vuelve al botón que la abrió) |

Detalles que ayudan:
* Al abrir una ventana emergente, el foco entra directo al primer campo y `Tab` no se escapa a la página.
* Al marcar algo con el teclado, el foco se queda en el mismo botón (no hay que volver a tabular desde el inicio).
* El selector de emociones es una sola parada de `Tab`; dentro se usan las flechas.

### Cómo probarlo

**Automático** (necesita Python):

    pip install playwright
    playwright install chromium
    python pruebas/prueba_teclado.py

**Manual** (30 segundos, sin instalar nada): desconecta el mouse y comprueba que puedes
1. Entrar a cada perfil desde el menú, y volver con "Cambiar perfil".
2. Marcar una medicina / tarea y que el contorno de foco siga sobre ese botón.
3. Abrir "Agregar Medicina", escribir, cambiar forma y color con las flechas, guardar con `Enter`.
4. Cerrar esa ventana con `Esc` y ver que el foco regresa a "Agregar Medicina".
5. Elegir una emoción con flechas + `Enter` y guardar una nota en el diario.
6. Cambiar el modo claro/oscuro desde el encabezado.

## Modo oscuro y paletas

* **Modo oscuro opcional:** botón "Modo oscuro / Modo claro" en el encabezado de cada página.
  Si la persona nunca eligió, se usa el modo de su dispositivo; si elige, se recuerda en `localStorage`
  (clave `recuerdame_tema`).
* **Paleta Adulto Mayor** (menú, pastillero): fondo crema en lugar de blanco puro, texto azul-grisáceo de contraste alto
  y verde azulado sereno como color principal. En oscuro: gris cálido (no negro puro) y texto marfil.
* **Paleta Niños:** cielo celeste suave, tarjetas crema y contornos azul marino (la estética de siempre) con verde y
  amarillo un poco más suaves. En oscuro: cielo nocturno con contornos azul claro; los dibujos se mantienen sobre fichas claras.
* Todas las combinaciones cumplen contraste WCAG AA (texto ≥ 4.5:1). Los colores viven como variables CSS al inicio de
  `styles.css` (`:root`, `.theme-nino`, `html[data-theme="dark"]`), así que ajustar un color es cambiar una línea.
