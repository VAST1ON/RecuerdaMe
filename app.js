/* app.js - Lógica completa para RecuerdaMe */

const STORAGE_KEY = "recuerdame_datos_v4";

const ICONS = {
  check: `<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>`,
  clock: `<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
  pill: `<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/></svg>`,
  phone: `<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>`,
  pin: `<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>`,
  flame: `<svg aria-hidden="true" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg>`,
  star: `<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`,
  alert: `<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`,
  barrer: `<svg aria-hidden="true" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 3 9 13"/><path d="m5 15 4 4"/><path d="M3 21c2-2 4-5 4-5l4 4s-3 2-5 4"/><path d="m14 4 6 6"/></svg>`,
  trapear: `<svg aria-hidden="true" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v13"/><path d="M7 15h10l2 6H5l2-6Z"/><path d="M9 18v3"/><path d="M15 18v3"/></svg>`,
  trastes: `<svg aria-hidden="true" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="13" r="7"/><circle cx="12" cy="13" r="3"/><path d="M5 4v2"/><path d="M4 5h2"/><path d="M19 3v3"/><path d="M17.5 4.5h3"/></svg>`,
  dientes: `<svg aria-hidden="true" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 15h18"/><path d="M14 15v-3h6v3"/><path d="M16 12v-2"/><path d="M18 12v-2"/><path d="M6 6l1 2 2 1-2 1-1 2-1-2-2-1 2-1 1-2z"/></svg>`,
  tarea: `<svg aria-hidden="true" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/><path d="m9 10 2 2 4-4"/></svg>`
};

// Personajes con consejos personalizados y pregunta para el diario
const EMOCIONES_PERSONAJES = [
  {
    id: "sol",
    nombre: "¡Muy Feliz!",
    consejoTitulo: "Consejo de Solecito:",
    consejoTexto: "¡Qué alegría verte así! Comparte una sonrisa con tu familia, juega un rato y aprovecha esta energía bonita para terminar tus tareas.",
    preguntaDiario: "¿Qué fue lo más bonito que te pasó hoy para sentirte así de feliz?",
    svg: `<svg aria-hidden="true" width="54" height="54" viewBox="0 0 64 64" fill="none">
      <circle cx="32" cy="32" r="18" fill="#FB923C" stroke="#123973" stroke-width="3"/>
      <path d="M32 5V10M32 54V59M5 32H10M54 32H59M13 13L17 17M47 47L51 51M51 13L47 17M17 47L13 51" stroke="#FB923C" stroke-width="4" stroke-linecap="round"/>
      <circle cx="27" cy="30" r="2.2" fill="#123973"/><circle cx="37" cy="30" r="2.2" fill="#123973"/>
      <ellipse cx="23" cy="34" rx="2.8" ry="1.6" fill="#F472B6"/><ellipse cx="41" cy="34" rx="2.8" ry="1.6" fill="#F472B6"/>
      <path d="M27 36 Q32 42 37 36" stroke="#123973" stroke-width="2.5" stroke-linecap="round" fill="none"/>
    </svg>`
  },
  {
    id: "estrella",
    nombre: "¡Emocionado!",
    consejoTitulo: "Consejo de Estrellita:",
    consejoTexto: "¡Cuando estamos muy emocionados dan ganas de saltar! Respira hondo, cuéntale a mamá o papá qué te emociona y úsalo para ganar stickers.",
    preguntaDiario: "¿Qué es eso tan genial que te tiene tan emocionado hoy?",
    svg: `<svg aria-hidden="true" width="54" height="54" viewBox="0 0 64 64" fill="none">
      <polygon points="32,5 39,21 56,23 44,35 47,52 32,43 17,52 20,35 8,23 25,21" fill="#FACC15" stroke="#123973" stroke-width="3" stroke-linejoin="round"/>
      <circle cx="27" cy="29" r="2.2" fill="#123973"/><circle cx="37" cy="29" r="2.2" fill="#123973"/>
      <ellipse cx="23" cy="33" rx="2.8" ry="1.6" fill="#F472B6"/><ellipse cx="41" cy="33" rx="2.8" ry="1.6" fill="#F472B6"/>
      <ellipse cx="32" cy="37" rx="3.5" ry="4" fill="#123973"/>
    </svg>`
  },
  {
    id: "corazon",
    nombre: "¡Tranquilo!",
    consejoTitulo: "Consejo de Corazón:",
    consejoTexto: "Sentirse tranquilo es como estar en una nube suave. Es un gran momento para leer un cuento, dibujar o hacer tus deberes con calma.",
    preguntaDiario: "¿Qué actividad hiciste hoy que te ayudó a sentirte tranquilo?",
    svg: `<svg aria-hidden="true" width="54" height="54" viewBox="0 0 64 64" fill="none">
      <path d="M32 52 C14 40 10 26 18 18 C24 12 32 18 32 23 C32 18 40 12 46 18 C54 26 50 40 32 52 Z" fill="#E11D48" stroke="#123973" stroke-width="3" stroke-linejoin="round"/>
      <path d="M24 27 Q26 30 28 27" stroke="#123973" stroke-width="2.2" stroke-linecap="round" fill="none"/>
      <path d="M36 27 Q38 30 40 27" stroke="#123973" stroke-width="2.2" stroke-linecap="round" fill="none"/>
      <ellipse cx="22" cy="31" rx="2.6" ry="1.5" fill="#FDA4AF"/><ellipse cx="42" cy="31" rx="2.6" ry="1.5" fill="#FDA4AF"/>
      <path d="M28 34 Q32 38 36 34" stroke="#123973" stroke-width="2.5" stroke-linecap="round" fill="none"/>
    </svg>`
  },
  {
    id: "nube",
    nombre: "Un poco triste",
    consejoTitulo: "Consejo de Nubecita:",
    consejoTexto: "Está bien sentirse triste a veces, todos los días tienen nubes y sol. Pídele un abrazo fuerte a mamá o papá y escribe aquí abajo qué pasó.",
    preguntaDiario: "¿Quieres contar por qué te sientes triste? Mamá o papá lo leerán para ayudarte:",
    svg: `<svg aria-hidden="true" width="54" height="54" viewBox="0 0 64 64" fill="none">
      <path d="M18 44 H46 A10 10 0 0 0 46 24 A14 14 0 0 0 20 22 A10 10 0 0 0 18 44 Z" fill="#7DD3FC" stroke="#123973" stroke-width="3" stroke-linejoin="round"/>
      <circle cx="27" cy="31" r="2.2" fill="#123973"/><circle cx="37" cy="31" r="2.2" fill="#123973"/>
      <path d="M28 38 Q32 34 36 38" stroke="#123973" stroke-width="2.5" stroke-linecap="round" fill="none"/>
    </svg>`
  },
  {
    id: "fuego",
    nombre: "Enojado",
    consejoTitulo: "Consejo de Fueguito:",
    consejoTexto: "Cuando sientas calor de enojo: 1) Infla tu pancita respirando como un globo, 2) Suelta el aire despacio 3 veces, 3) Toma un vasito de agua y escríbelo aquí.",
    preguntaDiario: "¿Qué pasó que te hizo enojar hoy? Escríbelo con calma:",
    svg: `<svg aria-hidden="true" width="54" height="54" viewBox="0 0 64 64" fill="none">
      <path d="M32 10 C42 22 50 28 48 42 C46 50 38 54 32 54 C24 54 16 48 16 38 C16 28 24 22 26 16 C28 20 30 22 32 10 Z" fill="#EA580C" stroke="#123973" stroke-width="3" stroke-linejoin="round"/>
      <path d="M23 32 L28 34M41 32 L36 34" stroke="#123973" stroke-width="2.5" stroke-linecap="round"/>
      <circle cx="26" cy="36" r="2" fill="#123973"/><circle cx="38" cy="36" r="2" fill="#123973"/>
      <path d="M28 44 Q32 40 36 44" stroke="#123973" stroke-width="2.5" stroke-linecap="round" fill="none"/>
    </svg>`
  }
];

// Guías visuales paso a paso para "¿Cómo lo hago?"
const GUIAS_COMO_LO_HAGO = [
  {
    id: "guia-agujetas",
    titulo: "Abrocharse las agujetas",
    subtitulo: "En 3 pasos fáciles",
    iconoPrincipal: `<svg aria-hidden="true" width="44" height="44" viewBox="0 0 64 64" fill="none">
      <path d="M10 42 C10 34 18 28 28 28 L38 18 L48 26 L54 38 C56 42 54 46 48 46 H14 C10 46 10 44 10 42 Z" fill="#38BDF8" stroke="#123973" stroke-width="3" stroke-linejoin="round"/>
      <path d="M12 42 H53" stroke="#FFFFFF" stroke-width="4"/>
      <path d="M32 24 C24 16 20 24 30 26 C40 24 36 16 32 24 Z" fill="#FACC15" stroke="#123973" stroke-width="2.5"/>
    </svg>`,
    pasos: [
      {
        numero: "Paso 1",
        texto: "Cruza las dos puntas formando una X y pasa una por debajo.",
        svg: `<svg aria-hidden="true" width="46" height="46" viewBox="0 0 48 48" fill="none">
          <path d="M10 38 L38 10" stroke="#E11D48" stroke-width="5" stroke-linecap="round"/>
          <path d="M38 38 L10 10" stroke="#2563EB" stroke-width="5" stroke-linecap="round"/>
          <circle cx="24" cy="24" r="4" fill="#FACC15" stroke="#123973" stroke-width="2"/>
        </svg>`
      },
      {
        numero: "Paso 2",
        texto: "Dobla cada punta para hacer dos orejitas de conejo.",
        svg: `<svg aria-hidden="true" width="46" height="46" viewBox="0 0 48 48" fill="none">
          <path d="M24 34 C12 34 10 14 20 14 C25 14 24 26 24 34 Z" fill="#FDE047" stroke="#123973" stroke-width="3"/>
          <path d="M24 34 C36 34 38 14 28 14 C23 14 24 26 24 34 Z" fill="#FDE047" stroke="#123973" stroke-width="3"/>
        </svg>`
      },
      {
        numero: "Paso 3",
        texto: "Cruza las orejitas, mete una por el huequito y jala suave.",
        svg: `<svg aria-hidden="true" width="46" height="46" viewBox="0 0 48 48" fill="none">
          <ellipse cx="15" cy="22" rx="8" ry="5" transform="rotate(-20 15 22)" fill="#4ADE80" stroke="#123973" stroke-width="2.8"/>
          <ellipse cx="33" cy="22" rx="8" ry="5" transform="rotate(20 33 22)" fill="#4ADE80" stroke="#123973" stroke-width="2.8"/>
          <circle cx="24" cy="24" r="4.5" fill="#FB923C" stroke="#123973" stroke-width="2.5"/>
          <path d="M22 28 L16 38 M26 28 L32 38" stroke="#123973" stroke-width="3" stroke-linecap="round"/>
        </svg>`
      }
    ]
  },
  {
    id: "guia-cama",
    titulo: "Tender la cama",
    subtitulo: "Para que quede súper ordenada",
    iconoPrincipal: `<svg aria-hidden="true" width="44" height="44" viewBox="0 0 64 64" fill="none">
      <rect x="10" y="24" width="44" height="24" rx="6" fill="#A78BFA" stroke="#123973" stroke-width="3"/>
      <rect x="14" y="16" width="16" height="10" rx="4" fill="#FFFFFF" stroke="#123973" stroke-width="2.8"/>
      <rect x="34" y="16" width="16" height="10" rx="4" fill="#FFFFFF" stroke="#123973" stroke-width="2.8"/>
      <path d="M10 34 H54" stroke="#123973" stroke-width="3"/>
      <path d="M14 48 V54 M50 48 V54" stroke="#123973" stroke-width="3.5" stroke-linecap="round"/>
    </svg>`,
    pasos: [
      {
        numero: "Paso 1",
        texto: "Estira la sábana de abajo jalando las esquinas sin arrugas.",
        svg: `<svg aria-hidden="true" width="46" height="46" viewBox="0 0 48 48" fill="none">
          <rect x="8" y="16" width="32" height="18" rx="4" fill="#BAE6FD" stroke="#123973" stroke-width="2.8"/>
          <path d="M14 25 H34 M29 21 L34 25 L29 29" stroke="#123973" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>`
      },
      {
        numero: "Paso 2",
        texto: "Sube la cobija hasta arriba y dobla el borde con tus manos.",
        svg: `<svg aria-hidden="true" width="46" height="46" viewBox="0 0 48 48" fill="none">
          <rect x="8" y="14" width="32" height="22" rx="4" fill="#C084FC" stroke="#123973" stroke-width="2.8"/>
          <rect x="8" y="14" width="32" height="7" rx="3" fill="#FACC15" stroke="#123973" stroke-width="2.5"/>
          <path d="M24 31 V23 M20 26 L24 22 L28 26" stroke="#FFFFFF" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>`
      },
      {
        numero: "Paso 3",
        texto: "Sacude tu almohada y colócala derechita en la parte de arriba.",
        svg: `<svg aria-hidden="true" width="46" height="46" viewBox="0 0 48 48" fill="none">
          <rect x="10" y="16" width="28" height="16" rx="7" fill="#FFFFFF" stroke="#123973" stroke-width="3"/>
          <polygon points="38,8 40,12 44,13 41,16 42,20 38,18 34,20 35,16 32,13 36,12" fill="#FACC15" stroke="#123973" stroke-width="1.8"/>
        </svg>`
      }
    ]
  },
  {
    id: "guia-manos",
    titulo: "Lavarse bien las manos",
    subtitulo: "Limpias y sin microbios",
    iconoPrincipal: `<svg aria-hidden="true" width="44" height="44" viewBox="0 0 64 64" fill="none">
      <circle cx="24" cy="22" r="7" fill="#7DD3FC" stroke="#123973" stroke-width="2.5"/>
      <circle cx="38" cy="18" r="9" fill="#BAE6FD" stroke="#123973" stroke-width="2.5"/>
      <circle cx="44" cy="30" r="5" fill="#E0F2FE" stroke="#123973" stroke-width="2.5"/>
      <rect x="16" y="34" width="32" height="18" rx="9" fill="#FDBA74" stroke="#123973" stroke-width="3"/>
    </svg>`,
    pasos: [
      {
        numero: "Paso 1",
        texto: "Moja tus manos con agua limpia y ponte un poco de jabón.",
        svg: `<svg aria-hidden="true" width="46" height="46" viewBox="0 0 48 48" fill="none">
          <path d="M24 10 C24 10 34 22 34 29 A10 10 0 0 1 14 29 C14 22 24 10 24 10 Z" fill="#38BDF8" stroke="#123973" stroke-width="2.8"/>
          <circle cx="21" cy="30" r="2.5" fill="#FFFFFF"/>
        </svg>`
      },
      {
        numero: "Paso 2",
        texto: "Frota palmas, dedos y uñas haciendo espuma por 20 segundos.",
        svg: `<svg aria-hidden="true" width="46" height="46" viewBox="0 0 48 48" fill="none">
          <circle cx="18" cy="22" r="8" fill="#E0F2FE" stroke="#123973" stroke-width="2.5"/>
          <circle cx="30" cy="20" r="9" fill="#BAE6FD" stroke="#123973" stroke-width="2.5"/>
          <circle cx="25" cy="31" r="7" fill="#FFFFFF" stroke="#123973" stroke-width="2.5"/>
        </svg>`
      },
      {
        numero: "Paso 3",
        texto: "Enjuaga toda la espuma con agua y sécate con una toalla.",
        svg: `<svg aria-hidden="true" width="46" height="46" viewBox="0 0 48 48" fill="none">
          <rect x="12" y="10" width="24" height="28" rx="4" fill="#FDE047" stroke="#123973" stroke-width="2.8"/>
          <path d="M12 31 H36" stroke="#123973" stroke-width="2.5" stroke-dasharray="3 3"/>
          <polyline points="19,20 23,24 30,17" stroke="#166534" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>`
      }
    ]
  }
];

const FORMA_LABELS = {
  redonda: "Redonda",
  pildora: "Píldora",
  capsula: "Cápsula"
};

const DEFAULT_DATA = {
  rachaAdulto: 6,
  medicamentos: [
    {
      id: "med-1",
      nombre: "Losartán 50 mg (Presión arterial)",
      horario: "08:00",
      forma: "pildora",
      colorNombre: "Blanca",
      colorHex: "#FFFFFF",
      diasTotales: 10,
      diasLlevados: 6,
      tomadaHoy: false
    },
    {
      id: "med-2",
      nombre: "Metformina 850 mg (Con el desayuno)",
      horario: "09:00",
      forma: "redonda",
      colorNombre: "Azul cielo",
      colorHex: "#BAE6FD",
      diasTotales: 14,
      diasLlevados: 11,
      tomadaHoy: true
    }
  ],
  importantes: [
    {
      id: "imp-1",
      titulo: "Hijo: Josep Pelayo (Emergencias)",
      detalle: "33 1425 8890",
      tipo: "telefono",
      nota: "Llamar en caso de emergencias o necesitar ayuda"
    },
    {
      id: "imp-2",
      titulo: "Cita en el IMSS clinica 96",
      detalle: "Viernes 28 de noviembre, 10:30 AM - Consultorio 4",
      tipo: "lugar",
      nota: "Llevar INE y receta anterior"
    }
  ],
  emocionNino: "sol",
  diarioEmociones: [
    {
      id: "dia-1",
      emocionId: "sol",
      emocionNombre: "¡Muy Feliz!",
      fecha: "Hoy · 14:20 hrs",
      texto: "Me sentí muy feliz porque ayudé a lavar los trastes y me gané una estrella.",
      revisadoPorPadres: false
    }
  ],
  guiasAprendidas: [],
  tareasNino: [
    {
      id: "kid-1",
      titulo: "Barrer el patio y mi cuarto",
      icono: "barrer",
      horario: "16:30",
      completada: false
    },
    {
      id: "kid-2",
      titulo: "Trapear el piso de la sala",
      icono: "trapear",
      horario: "17:00",
      completada: false
    },
    {
      id: "kid-3",
      titulo: "Lavar los trastes después de comer",
      icono: "trastes",
      horario: "15:15",
      completada: true
    }
  ],
  recordatoriosNino: [
    {
      id: "rec-1",
      titulo: "Lavarse los dientes después de desayunar",
      icono: "dientes",
      horario: "07:45",
      completada: true
    },
    {
      id: "rec-2",
      titulo: "Lavarse los dientes antes de dormir",
      icono: "dientes",
      horario: "20:30",
      completada: false
    },
    {
      id: "rec-3",
      titulo: "Revisar mochila y tarea escolar",
      icono: "tarea",
      horario: "18:30",
      completada: false
    }
  ],
  rachaNino: 5,
  rachaIncrementadaHoy: false
};

function getData() {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (!saved) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(DEFAULT_DATA));
    return structuredClone(DEFAULT_DATA);
  }
  try {
    return JSON.parse(saved);
  } catch {
    return structuredClone(DEFAULT_DATA);
  }
}

function saveData(data) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

function announce(message) {
  const region = document.getElementById("live-status");
  if (region) {
    region.textContent = "";
    setTimeout(() => {
      region.textContent = message;
    }, 50);
  }
}

function setupModal(openBtnId, dialogId, closeBtnId) {
  const openBtn = document.getElementById(openBtnId);
  const dialog = document.getElementById(dialogId);
  const closeBtn = document.getElementById(closeBtnId);
  if (!openBtn || !dialog) return null;

  openBtn.addEventListener("click", () => {
    dialog.showModal();
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      dialog.close();
      openBtn.focus();
    });
  }

  dialog.addEventListener("close", () => {
    openBtn.focus();
  });

  return dialog;
}

/* 1. Menú de Inicio (index.html) */
function renderHomeMenu() {
  const adultSummary = document.getElementById("resumen-adulto");
  const kidSummary = document.getElementById("resumen-nino");
  if (!adultSummary || !kidSummary) return;

  const data = getData();
  const pendingMeds = data.medicamentos.filter(m => !m.tomadaHoy).length;
  const totalKidItems = data.tareasNino.length + data.recordatoriosNino.length;
  const doneKidItems =
    data.tareasNino.filter(t => t.completada).length +
    data.recordatoriosNino.filter(r => r.completada).length;

  adultSummary.textContent =
    pendingMeds === 0
      ? `¡Al día! Racha de ${data.rachaAdulto} días seguidos.`
      : `${pendingMeds} medicina(s) pendiente(s) hoy · Racha de ${data.rachaAdulto} días.`;

  kidSummary.textContent = `Racha de ${data.rachaNino} días · ${doneKidItems} de ${totalKidItems} completados hoy.`;
}

/* 2. Panel Adulto Mayor (adulto.html) */
function buildTreatmentDaysHtml(med) {
  const total = Math.max(1, Number(med.diasTotales) || 1);
  const done = Math.min(total, Math.max(0, Number(med.diasLlevados) || 0));
  const remaining = Math.max(0, total - done);
  const percent = Math.round((done / total) * 100);

  const maxDots = Math.min(total, 14);
  let dotsHtml = "";
  for (let i = 1; i <= maxDots; i++) {
    if (i <= done) {
      dotsHtml += `<span class="day-dot day-dot-done" title="Día ${i} completado">✓</span>`;
    } else if (i === done + 1 && !med.tomadaHoy) {
      dotsHtml += `<span class="day-dot day-dot-today" title="Día ${i} (Hoy)">${i}</span>`;
    } else {
      dotsHtml += `<span class="day-dot" title="Día ${i} pendiente">${i}</span>`;
    }
  }
  if (total > 14) {
    dotsHtml += `<span class="day-dot" title="Total ${total} días">+${total - 14}</span>`;
  }

  return `
    <div class="treatment-widget" aria-label="Progreso del tratamiento: llevas ${done} días, te faltan ${remaining} días de ${total}">
      <div class="treatment-stats">
        <span>Llevas: ${done} ${done === 1 ? "día" : "días"}</span>
        <span>Te faltan: ${remaining} ${remaining === 1 ? "día" : "días"} (de ${total})</span>
      </div>
      <div class="progress-bar-wrap" style="height:14px;">
        <div class="progress-bar-fill" style="width:${percent}%;"></div>
      </div>
      <div class="days-dots" aria-hidden="true">${dotsHtml}</div>
    </div>
  `;
}

function renderAdulto() {
  const medsContainer = document.getElementById("lista-medicamentos");
  const infoContainer = document.getElementById("lista-importantes");
  const streakLabel = document.getElementById("racha-adulto-texto");
  if (!medsContainer || !infoContainer) return;

  const data = getData();
  if (streakLabel) {
    streakLabel.innerHTML = `${ICONS.flame} Racha de cuidado: ${data.rachaAdulto} días seguidos`;
  }

  medsContainer.innerHTML = data.medicamentos
    .map(med => {
      const formaLabel = FORMA_LABELS[med.forma] || "Redonda";
      const statusBadge = med.tomadaHoy
        ? `<span class="badge badge-done">${ICONS.check} Dosis de hoy tomada</span>`
        : `<span class="badge badge-pending">${ICONS.clock} Pendiente hoy (${med.horario} hrs)</span>`;

      const btnText = med.tomadaHoy
        ? `${ICONS.check} Tomada hoy (Deshacer)`
        : `${ICONS.pill} Ya me tomé esta medicina`;

      const btnClass = med.tomadaHoy ? "btn btn-outline btn-full" : "btn btn-primary btn-full";

      return `
        <article class="card card-adult ${med.tomadaHoy ? "card-done" : ""}">
          <div>
            ${statusBadge}
            <h3 style="margin-top:0.65rem;">${med.nombre}</h3>

            <div class="pill-visual-box" aria-label="Forma ${formaLabel}, color ${med.colorNombre}">
              <span class="pill-graphic shape-${med.forma}" style="background-color:${med.colorHex};"></span>
              <div>
                <div><strong>Cómo se ve:</strong> ${formaLabel} · Color ${med.colorNombre}</div>
                <div style="font-size:0.95rem; color:var(--text-muted);">Hora: ${med.horario} hrs</div>
              </div>
            </div>

            <div style="margin-top:0.85rem;">
              ${buildTreatmentDaysHtml(med)}
            </div>
          </div>

          <button type="button" class="${btnClass}" data-toggle-med="${med.id}">
            ${btnText}
          </button>
        </article>
      `;
    })
    .join("");

  infoContainer.innerHTML = data.importantes
    .map(item => {
      const isPhone = item.tipo === "telefono";
      const icon = isPhone ? ICONS.phone : ICONS.pin;
      const action = isPhone
        ? `<a class="btn btn-primary btn-full" href="tel:${item.detalle.replace(/\s+/g, "")}">${ICONS.phone} Llamar al ${item.detalle}</a>`
        : `<p style="margin:0;"><strong>Lugar / Fecha:</strong> ${item.detalle}</p>`;

      return `
        <article class="card card-adult">
          <div>
            <h3>${icon} ${item.titulo}</h3>
            <p style="margin-bottom:0;">${item.nota}</p>
          </div>
          ${action}
        </article>
      `;
    })
    .join("");

  medsContainer.querySelectorAll("[data-toggle-med]").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-toggle-med");
      const current = getData();
      const target = current.medicamentos.find(m => m.id === id);
      if (target) {
        target.tomadaHoy = !target.tomadaHoy;
        if (target.tomadaHoy) {
          target.diasLlevados = Math.min(target.diasTotales, target.diasLlevados + 1);
        } else {
          target.diasLlevados = Math.max(0, target.diasLlevados - 1);
        }
        saveData(current);
        renderAdulto();
        announce(
          target.tomadaHoy
            ? `¡Excelente! Registraste ${target.nombre}. Llevas ${target.diasLlevados} de ${target.diasTotales} días.`
            : `Se regresó ${target.nombre} a pendiente.`
        );
      }
    });
  });
}

function initAdultoModals() {
  const medDialog = setupModal("btn-abrir-modal-med", "modal-medicina", "btn-cerrar-modal-med");
  const infoDialog = setupModal("btn-abrir-modal-info", "modal-info", "btn-cerrar-modal-info");

  const medForm = document.getElementById("form-modal-medicina");
  if (medForm && medDialog) {
    const previewShape = document.getElementById("preview-pill-shape");
    const previewText = document.getElementById("preview-pill-text");
    const diasInput = document.getElementById("modal-med-dias");

    function updateLivePreview() {
      const forma = medForm.querySelector('input[name="modal-forma"]:checked')?.value || "redonda";
      const colorRadio = medForm.querySelector('input[name="modal-color"]:checked');
      const colorHex = colorRadio?.value || "#FFFFFF";
      const colorNombre = colorRadio?.getAttribute("data-color-name") || "Blanca";
      const dias = Math.max(1, Number(diasInput?.value) || 7);

      if (previewShape) {
        previewShape.className = `pill-graphic shape-${forma}`;
        previewShape.style.backgroundColor = colorHex;
      }
      if (previewText) {
        previewText.textContent = `${FORMA_LABELS[forma]} · Color ${colorNombre} · ${dias} días`;
      }
    }

    medForm.querySelectorAll('input[name="modal-forma"], input[name="modal-color"]').forEach(inp => {
      inp.addEventListener("change", updateLivePreview);
    });
    if (diasInput) diasInput.addEventListener("input", updateLivePreview);
    updateLivePreview();

    medForm.addEventListener("submit", e => {
      e.preventDefault();
      const nombreInput = document.getElementById("modal-med-nombre");
      const errorNombre = document.getElementById("error-modal-med-nombre");
      const horarioInput = document.getElementById("modal-med-hora");
      const diasVal = Math.max(1, Number(diasInput.value) || 7);

      nombreInput.setAttribute("aria-invalid", "false");
      errorNombre.innerHTML = "";

      if (!nombreInput.value.trim() || nombreInput.value.trim().length < 2) {
        nombreInput.setAttribute("aria-invalid", "true");
        errorNombre.innerHTML = `${ICONS.alert} Escribe el nombre de la medicina (ejemplo: Omeprazol 20 mg).`;
        nombreInput.focus();
        return;
      }

      const forma = medForm.querySelector('input[name="modal-forma"]:checked').value;
      const colorRadio = medForm.querySelector('input[name="modal-color"]:checked');
      const colorHex = colorRadio.value;
      const colorNombre = colorRadio.getAttribute("data-color-name");

      const data = getData();
      data.medicamentos.unshift({
        id: "med-" + Date.now(),
        nombre: nombreInput.value.trim(),
        horario: horarioInput.value || "08:00",
        forma,
        colorNombre,
        colorHex,
        diasTotales: diasVal,
        diasLlevados: 0,
        tomadaHoy: false
      });

      saveData(data);
      medForm.reset();
      updateLivePreview();
      medDialog.close();
      renderAdulto();
      announce(`Medicina ${nombreInput.value.trim()} agregada por ${diasVal} días.`);
    });
  }

  const infoForm = document.getElementById("form-modal-info");
  if (infoForm && infoDialog) {
    infoForm.addEventListener("submit", e => {
      e.preventDefault();
      const tituloInput = document.getElementById("modal-info-titulo");
      const detalleInput = document.getElementById("modal-info-detalle");
      const tipoSelect = document.getElementById("modal-info-tipo");
      const notaInput = document.getElementById("modal-info-nota");

      if (!tituloInput.value.trim() || !detalleInput.value.trim()) {
        tituloInput.focus();
        return;
      }

      const data = getData();
      data.importantes.unshift({
        id: "imp-" + Date.now(),
        titulo: tituloInput.value.trim(),
        detalle: detalleInput.value.trim(),
        tipo: tipoSelect.value,
        nota: notaInput.value.trim() || "Recordatorio importante"
      });

      saveData(data);
      infoForm.reset();
      infoDialog.close();
      renderAdulto();
      announce("Recordatorio importante guardado correctamente.");
    });
  }
}

/* 3. Panel Niños (nino.html) */
function renderDiarioPadres() {
  const diaryList = document.getElementById("lista-diario-padres");
  if (!diaryList) return;

  const data = getData();
  const entries = Array.isArray(data.diarioEmociones) ? data.diarioEmociones : [];

  if (entries.length === 0) {
    diaryList.innerHTML = `<p style="margin:0; font-weight:700;">Aún no hay notas escritas hoy en el diario.</p>`;
    return;
  }

  diaryList.innerHTML = entries
    .map(entry => {
      const emoObj = EMOCIONES_PERSONAJES.find(e => e.id === entry.emocionId) || EMOCIONES_PERSONAJES[0];
      const miniSvg = emoObj.svg.replace('width="54" height="54"', 'width="38" height="38"');

      const reviewBtn = entry.revisadoPorPadres
        ? `<button type="button" class="btn btn-outline" style="min-height:40px; padding:0.35rem 0.85rem; font-size:0.9rem;" data-review-diary="${entry.id}">
             ${ICONS.check} Revisado por mamá/papá
           </button>`
        : `<button type="button" class="btn btn-secondary" style="min-height:40px; padding:0.35rem 0.85rem; font-size:0.9rem;" data-review-diary="${entry.id}">
             Marcar como revisado
           </button>`;

      return `
        <article class="diary-entry-card ${entry.revisadoPorPadres ? "diary-entry-reviewed" : ""}">
          <div class="diary-entry-header">
            <div style="display:flex; align-items:center; gap:0.6rem;">
              ${miniSvg}
              <div>
                <strong style="font-size:1.05rem;">Se sintió: ${entry.emocionNombre}</strong>
                <div style="font-size:0.88rem; color:var(--text-muted); font-weight:700;">${entry.fecha}</div>
              </div>
            </div>
            ${reviewBtn}
          </div>
          <p class="diary-entry-text">"${entry.texto}"</p>
        </article>
      `;
    })
    .join("");

  diaryList.querySelectorAll("[data-review-diary]").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-review-diary");
      const current = getData();
      const target = current.diarioEmociones?.find(d => d.id === id);
      if (target) {
        target.revisadoPorPadres = !target.revisadoPorPadres;
        saveData(current);
        renderDiarioPadres();
        announce(
          target.revisadoPorPadres
            ? "Nota marcada como revisada por mamá o papá."
            : "Se quitó la marca de revisión."
        );
      }
    });
  });
}

function initDiarioForm() {
  const form = document.getElementById("form-diario-emocion");
  if (!form) return;

  form.addEventListener("submit", e => {
    e.preventDefault();
    const textarea = document.getElementById("input-diario-texto");
    const errorEl = document.getElementById("error-diario-texto");

    textarea.setAttribute("aria-invalid", "false");
    errorEl.innerHTML = "";

    if (!textarea.value.trim() || textarea.value.trim().length < 3) {
      textarea.setAttribute("aria-invalid", "true");
      errorEl.innerHTML = `${ICONS.alert} Escribe unas palabritas sobre cómo te sientes antes de guardar.`;
      textarea.focus();
      return;
    }

    const data = getData();
    const activeEmo = EMOCIONES_PERSONAJES.find(em => em.id === data.emocionNino) || EMOCIONES_PERSONAJES[0];
    const ahora = new Date();
    const horaStr = ahora.toLocaleTimeString("es-MX", { hour: "2-digit", minute: "2-digit" });
    const fechaStr = ahora.toLocaleDateString("es-MX", { day: "numeric", month: "short" });

    if (!Array.isArray(data.diarioEmociones)) data.diarioEmociones = [];
    data.diarioEmociones.unshift({
      id: "dia-" + Date.now(),
      emocionId: activeEmo.id,
      emocionNombre: activeEmo.nombre,
      fecha: `${fechaStr} · ${horaStr} hrs`,
      texto: textarea.value.trim(),
      revisadoPorPadres: false
    });

    saveData(data);
    textarea.value = "";
    renderDiarioPadres();
    announce("Tu nota se guardó en el diario para que mamá o papá la puedan leer.");
  });
}

function renderNino() {
  const choresContainer = document.getElementById("lista-tareas-hogar");
  const remindersContainer = document.getElementById("lista-recordatorios-nino");
  const emotionsContainer = document.getElementById("selector-emociones");
  const emotionBadge = document.getElementById("emocion-actual-badge");
  const adviceBox = document.getElementById("consejo-emocion-box");
  const diaryLabel = document.getElementById("label-diario-texto");
  const stickersAlbum = document.getElementById("album-stickers");
  const streakText = document.getElementById("texto-racha");
  const progressText = document.getElementById("texto-progreso");
  const progressBar = document.getElementById("barra-progreso");
  if (!choresContainer || !remindersContainer) return;

  const data = getData();

  // Selector "Mis Emociones" + Consejo dinámico + Pregunta del diario
  if (emotionsContainer) {
    const activeEmo = EMOCIONES_PERSONAJES.find(e => e.id === data.emocionNino) || EMOCIONES_PERSONAJES[0];
    if (emotionBadge) {
      emotionBadge.textContent = `Hoy me siento: ${activeEmo.nombre}`;
    }
    if (adviceBox) {
      adviceBox.innerHTML = `
        <div class="advice-content">
          <div class="advice-avatar">${activeEmo.svg}</div>
          <div>
            <strong class="advice-title">${activeEmo.consejoTitulo}</strong>
            <p class="advice-text">${activeEmo.consejoTexto}</p>
          </div>
        </div>
      `;
    }
    if (diaryLabel) {
      diaryLabel.textContent = `Mi Diario: ${activeEmo.preguntaDiario}`;
    }

    emotionsContainer.innerHTML = EMOCIONES_PERSONAJES.map(emo => {
      const isSelected = emo.id === activeEmo.id;
      return `
        <button type="button" class="emotion-btn" data-emo-id="${emo.id}" aria-pressed="${isSelected}">
          ${emo.svg}
          <span>${emo.nombre}</span>
        </button>
      `;
    }).join("");

    emotionsContainer.querySelectorAll("[data-emo-id]").forEach(btn => {
      btn.addEventListener("click", () => {
        const chosenId = btn.getAttribute("data-emo-id");
        const current = getData();
        current.emocionNino = chosenId;
        saveData(current);
        renderNino();
        const chosenObj = EMOCIONES_PERSONAJES.find(e => e.id === chosenId);
        if (chosenObj) announce(`Elegiste: ${chosenObj.nombre}. Revisa tu consejo y tu diario.`);
      });
    });
  }

  renderDiarioPadres();

  const total = data.tareasNino.length + data.recordatoriosNino.length;
  const doneCount =
    data.tareasNino.filter(t => t.completada).length +
    data.recordatoriosNino.filter(r => r.completada).length;
  const percent = total > 0 ? Math.round((doneCount / total) * 100) : 0;

  if (streakText) {
    streakText.innerHTML = `${ICONS.flame} Racha activa: ${data.rachaNino} días seguidos`;
  }
  if (progressText) {
    progressText.textContent = `¡Llevas ${doneCount} de ${total} actividades completadas hoy (${percent} %)!`;
  }
  if (progressBar) {
    progressBar.style.width = `${percent}%`;
    progressBar.setAttribute("aria-valuenow", String(percent));
  }

  // Álbum de Stickers desbloqueados
  if (stickersAlbum) {
    const stickerChars = EMOCIONES_PERSONAJES.slice(0, 4);
    stickersAlbum.innerHTML = stickerChars
      .map((st, idx) => {
        const unlocked = doneCount > idx;
        return `
          <span class="sticker-token ${unlocked ? "" : "sticker-locked"}" title="${
          unlocked ? "Sticker ganado: " + st.nombre : "Completa una tarea para ganar este sticker"
        }">
            ${st.svg.replace('width="54" height="54"', 'width="34" height="34"')}
          </span>
        `;
      })
      .join("");
  }

  function buildKidCard(item, listType) {
    const isHygiene = listType === "recordatoriosNino";
    const iconSvg = ICONS[item.icono] || (isHygiene ? ICONS.dientes : ICONS.tarea);
    const statusBadge = item.completada
      ? `<span class="badge badge-done">${ICONS.star} ¡Completado! (+1 Sticker)</span>`
      : `<span class="badge badge-pending">${ICONS.clock} Hora: ${item.horario} hrs</span>`;

    const btnClass = item.completada
      ? "btn btn-outline btn-full"
      : "btn btn-kid-action btn-full";

    const btnLabel = item.completada
      ? `${ICONS.check} ¡Listo! (Desmarcar)`
      : `${ICONS.star} ¡Ya lo hice!`;

    return `
      <article class="card ${isHygiene ? "card-hygiene" : "card-kid"} ${item.completada ? "card-done" : ""}">
        <div>
          ${statusBadge}
          <div class="chore-header" style="margin-top:0.75rem;">
            <div class="chore-illustration ${isHygiene ? "hygiene-illustration" : ""}">
              ${iconSvg}
            </div>
            <div>
              <h3 style="margin:0;">${item.titulo}</h3>
              <p style="margin:0.2rem 0 0; font-size:0.95rem; font-weight:700;">
                ${isHygiene ? "Recordatorio diario" : "Tarea del hogar"}
              </p>
            </div>
          </div>
        </div>
        <button type="button" class="${btnClass}" data-kid-list="${listType}" data-kid-id="${item.id}">
          ${btnLabel}
        </button>
      </article>
    `;
  }

  choresContainer.innerHTML = data.tareasNino.map(t => buildKidCard(t, "tareasNino")).join("");
  remindersContainer.innerHTML = data.recordatoriosNino
    .map(r => buildKidCard(r, "recordatoriosNino"))
    .join("");

  document.querySelectorAll("[data-kid-id]").forEach(btn => {
    btn.addEventListener("click", () => {
      const listType = btn.getAttribute("data-kid-list");
      const id = btn.getAttribute("data-kid-id");
      const current = getData();
      const target = current[listType]?.find(x => x.id === id);
      if (target) {
        target.completada = !target.completada;
        const allDone =
          current.tareasNino.every(t => t.completada) &&
          current.recordatoriosNino.every(r => r.completada);
        if (allDone && !current.rachaIncrementadaHoy) {
          current.rachaNino += 1;
          current.rachaIncrementadaHoy = true;
        }
        saveData(current);
        renderNino();
        announce(
          target.completada
            ? `¡Súper bien! Completaste: ${target.titulo}. Ganaste un sticker.`
            : `Se marcó como pendiente: ${target.titulo}.`
        );
      }
    });
  });

  // Sección "¿Cómo lo hago?"
  const howtoContainer = document.getElementById("lista-como-lo-hago");
  if (howtoContainer) {
    const learnedList = Array.isArray(data.guiasAprendidas) ? data.guiasAprendidas : [];

    howtoContainer.innerHTML = GUIAS_COMO_LO_HAGO.map(guia => {
      const isLearned = learnedList.includes(guia.id);
      const stepsHtml = guia.pasos
        .map(
          paso => `
          <li class="howto-step-item">
            <div class="howto-step-visual">${paso.svg}</div>
            <div>
              <span class="howto-step-badge">${paso.numero}</span>
              <p class="howto-step-text">${paso.texto}</p>
            </div>
          </li>
        `
        )
        .join("");

      return `
        <article class="howto-card ${isLearned ? "howto-card-learned" : ""}">
          <div>
            <div class="howto-header">
              <div class="howto-main-icon">${guia.iconoPrincipal}</div>
              <div>
                <h3 style="margin:0; font-family:'Fredoka','Nunito',sans-serif; font-size:1.3rem;">${guia.titulo}</h3>
                <p style="margin:0.15rem 0 0; font-size:0.95rem; font-weight:700;">${guia.subtitulo}</p>
              </div>
            </div>
            <ol class="howto-steps-list" style="margin-top:0.9rem;">
              ${stepsHtml}
            </ol>
          </div>
          <button type="button" class="btn ${isLearned ? "btn-outline" : "btn-kid-action"} btn-full" data-learn-guide="${guia.id}">
            ${isLearned ? `${ICONS.check} ¡Ya sé hacerlo! (Practicar otra vez)` : `${ICONS.star} ¡Ya aprendí a hacerlo!`}
          </button>
        </article>
      `;
    }).join("");

    howtoContainer.querySelectorAll("[data-learn-guide]").forEach(btn => {
      btn.addEventListener("click", () => {
        const guideId = btn.getAttribute("data-learn-guide");
        const current = getData();
        if (!Array.isArray(current.guiasAprendidas)) current.guiasAprendidas = [];
        const guideObj = GUIAS_COMO_LO_HAGO.find(g => g.id === guideId);

        if (!current.guiasAprendidas.includes(guideId)) {
          current.guiasAprendidas.push(guideId);
        }
        saveData(current);
        renderNino();
        if (guideObj) {
          announce(`¡Felicidades! Aprendiste a: ${guideObj.titulo}.`);
        }
      });
    });
  }
}

function initNinoModal() {
  const kidDialog = setupModal("btn-abrir-modal-nino", "modal-nino", "btn-cerrar-modal-nino");
  const kidForm = document.getElementById("form-modal-nino");
  if (!kidDialog || !kidForm) return;

  kidForm.querySelectorAll("[data-preset-titulo]").forEach(btn => {
    btn.addEventListener("click", () => {
      document.getElementById("modal-nino-titulo").value = btn.getAttribute("data-preset-titulo");
      document.getElementById("modal-nino-tipo").value = btn.getAttribute("data-preset-tipo");
      document.getElementById("modal-nino-icono").value = btn.getAttribute("data-preset-icono");
    });
  });

  kidForm.addEventListener("submit", e => {
    e.preventDefault();
    const tituloInput = document.getElementById("modal-nino-titulo");
    const errorEl = document.getElementById("error-modal-nino-titulo");
    const tipo = document.getElementById("modal-nino-tipo").value;
    const icono = document.getElementById("modal-nino-icono").value;
    const horario = document.getElementById("modal-nino-hora").value || "16:00";

    tituloInput.setAttribute("aria-invalid", "false");
    errorEl.innerHTML = "";

    if (!tituloInput.value.trim() || tituloInput.value.trim().length < 3) {
      tituloInput.setAttribute("aria-invalid", "true");
      errorEl.innerHTML = `${ICONS.alert} Escribe qué actividad hay que hacer (ejemplo: "Barrer la entrada").`;
      tituloInput.focus();
      return;
    }

    const data = getData();
    const newItem = {
      id: "kid-" + Date.now(),
      titulo: tituloInput.value.trim(),
      icono,
      horario,
      completada: false
    };

    if (tipo === "recordatorio") {
      data.recordatoriosNino.unshift(newItem);
    } else {
      data.tareasNino.unshift(newItem);
    }

    saveData(data);
    kidForm.reset();
    kidDialog.close();
    renderNino();
    announce(`Actividad "${newItem.titulo}" agregada a la lista.`);
  });
}

function initResetButton() {
  const resetBtn = document.getElementById("btn-reset-demo");
  if (!resetBtn) return;

  resetBtn.addEventListener("click", () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(DEFAULT_DATA));
    renderHomeMenu();
    renderAdulto();
    renderNino();
    announce("Datos de demostración restaurados.");
  });
}

document.addEventListener("DOMContentLoaded", () => {
  renderHomeMenu();
  renderAdulto();
  initAdultoModals();
  renderNino();
  initDiarioForm();
  initNinoModal();
  initResetButton();
});

/* ===== Retroalimentación visual: confeti y "pop" al completar (respeta movimiento reducido) ===== */
function lanzarConfeti(origen, cantidad = 26, colores = ["#58CC02", "#FACC15", "#FB923C", "#F472B6", "#38BDF8", "#A78BFA"]) {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const r = origen.getBoundingClientRect();
  const x0 = r.left + r.width / 2, y0 = r.top + r.height / 2;
  for (let i = 0; i < cantidad; i++) {
    const p = document.createElement("span");
    p.setAttribute("aria-hidden", "true");
    p.className = "confetti-piece";
    p.style.cssText = `left:${x0}px;top:${y0}px;background:${colores[i % colores.length]};border-radius:${i % 3 ? "2px" : "50%"}`;
    document.body.appendChild(p);
    const ang = Math.random() * Math.PI * 2, dist = 70 + Math.random() * 130;
    p.animate(
      [
        { transform: "translate(0,0) rotate(0deg) scale(1)", opacity: 1 },
        { transform: `translate(${Math.cos(ang) * dist}px,${Math.sin(ang) * dist - 60}px) rotate(${Math.random() * 540}deg) scale(1)`, opacity: 1, offset: 0.55 },
        { transform: `translate(${Math.cos(ang) * dist * 1.1}px,${Math.sin(ang) * dist + 120}px) rotate(720deg) scale(.6)`, opacity: 0 }
      ],
      { duration: 900 + Math.random() * 500, easing: "cubic-bezier(.2,.7,.3,1)" }
    ).onfinish = () => p.remove();
  }
}

// Fase de captura: corre antes de que el render reemplace el botón
document.addEventListener("click", e => {
  const kid = e.target.closest(".btn-kid-action[data-kid-id], .btn-kid-action[data-learn-guide]");
  if (kid) lanzarConfeti(kid, 30);
  const med = e.target.closest(".btn-primary[data-toggle-med]");
  if (med) lanzarConfeti(med, 16, ["#0B6E4F", "#58CC02", "#FACC15", "#38BDF8"]);
}, true);