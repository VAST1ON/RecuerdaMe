# RecuerdaMe 

Aplicación web accesible diseñada para apoyar la organización diaria mediante dos perfiles adaptados visual y funcionalmente: **Adulto Mayor** y **Niños**.

🔗 **Ver página en vivo: https://vast1on.github.io/RecuerdaMe/ 



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
├── app.js         # Lógica de datos, eventos y almacenamiento en localStorage
└── README.md      # Documentación del proyecto
