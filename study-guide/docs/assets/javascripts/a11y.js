/**
 * a11y.js — correcciones de accesibilidad aplicadas tras cada render.
 *
 * Material 9.x re-renderiza el DOM en cada navegación instantánea
 * (document$.subscribe, el mismo hook que usa mathjax.js), así que todos los
 * arreglos se vuelven a aplicar en cada evento. Cada querySelector está
 * guardado: los elementos pueden no existir según la página.
 */
(function () {
  "use strict";

  // Breakpoint del drawer off-canvas de Material (76.25em = 1220px).
  // Debajo de este ancho el sidebar primario vive fuera de pantalla
  // cuando el drawer está cerrado.
  var MOBILE = window.matchMedia("(max-width: 1219px)");

  /**
   * Sincroniza el estado accesible del drawer con su estado visual:
   * - drawer cerrado en móvil: sidebar oculto para AT y enlaces fuera de
   *   tab order (están off-canvas; el foco no debe caer en ellos).
   * - drawer abierto o desktop: se restaura el tab order original.
   */
  function applyDrawerAccessibility() {
    var drawer = document.querySelector("#__drawer");
    var sidebar = document.querySelector(".md-sidebar--primary");
    if (!drawer || !sidebar) return;

    var closed = MOBILE.matches && !drawer.checked;
    sidebar.setAttribute("aria-hidden", closed ? "true" : "false");

    // Enlaces/toggles del sidebar: tabindex -1 mientras esté off-canvas.
    var focusables = sidebar.querySelectorAll(
      "a[href], summary, button, label[tabindex], [tabindex]"
    );
    for (var i = 0; i < focusables.length; i++) {
      var el = focusables[i];
      if (closed) {
        if (el.getAttribute("tabindex") !== "-1") {
          el.dataset.a11yTab = el.getAttribute("tabindex") || "";
          el.setAttribute("tabindex", "-1");
        }
      } else if (el.dataset.a11yTab !== undefined) {
        if (el.dataset.a11yTab === "") {
          el.removeAttribute("tabindex");
        } else {
          el.setAttribute("tabindex", el.dataset.a11yTab);
        }
        delete el.dataset.a11yTab;
      }
    }

    // Botón de cierre del drawer (vive dentro del sidebar): solo tabulable
    // con el drawer abierto en móvil. En desktop no es un control útil.
    var navTitleToggle = sidebar.querySelector('.md-nav__title[for="__drawer"]');
    if (navTitleToggle) {
      if (!MOBILE.matches) {
        navTitleToggle.removeAttribute("tabindex");
      } else {
        navTitleToggle.setAttribute("tabindex", closed ? "-1" : "0");
      }
    }
  }

  /**
   * Hace que un label del drawer sea operable por teclado (los labels no son
   * focuseables de forma nativa). Enter/Space disparan la activación nativa
   * del label, que togglea el checkbox #__drawer.
   */
  function setupDrawerToggle(label) {
    if (label.getAttribute("tabindex") === "0") return;
    label.setAttribute("tabindex", "0");
    label.addEventListener("keydown", function (event) {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        // Material escucha keydown en window y hace click en labels con Enter;
        // al detener la propagación evitamos un doble toggle.
        event.stopPropagation();
        label.click();
      }
    });
  }

  document$.subscribe(function () {
    // (a) Tablas con scroll horizontal: foco por teclado.
    // El wrapper .md-typeset__table lo crea Material antes que este hook.
    var tables = document.querySelectorAll(".md-typeset__table");
    for (var i = 0; i < tables.length; i++) {
      var table = tables[i];
      if (
        table.scrollWidth > table.clientWidth &&
        table.getAttribute("tabindex") !== "0"
      ) {
        table.setAttribute("tabindex", "0");
      }
    }

    // (b) Diálogo de búsqueda sin nombre accesible.
    var search = document.querySelector(".md-search");
    if (
      search &&
      search.getAttribute("role") === "dialog" &&
      !search.getAttribute("aria-label")
    ) {
      search.setAttribute("aria-label", "Búsqueda");
    }

    // (c) Barra de progreso de navegación instantánea: fuera de landmarks,
    // se oculta para tecnologías de asistencia.
    var progress = document.querySelector('[data-md-component="progress"]');
    if (progress && progress.getAttribute("aria-hidden") !== "true") {
      progress.setAttribute("aria-hidden", "true");
    }

    // (d) Drawer: toggle por teclado + manejo de enlaces off-canvas.
    var drawer = document.querySelector("#__drawer");
    if (drawer) {
      // El overlay es un backdrop de click (no un control): se excluye.
      var toggles = document.querySelectorAll(
        'label[for="__drawer"]:not(.md-overlay)'
      );
      for (var t = 0; t < toggles.length; t++) {
        setupDrawerToggle(toggles[t]);
      }
      drawer.addEventListener("change", applyDrawerAccessibility);
    }
    applyDrawerAccessibility();

    // (e) Landmarks duplicados de "copiar código": se quita el rol de navegación.
    var codeNavs = document.querySelectorAll(".md-code__nav");
    for (var c = 0; c < codeNavs.length; c++) {
      codeNavs[c].setAttribute("role", "none");
    }
  });

  // Cambios de viewport (rotación/resize) re-evalúan el estado del drawer.
  // Se registra una sola vez: el handler re-consulta el DOM vigente.
  if (!window.__a11yDrawerBound) {
    window.__a11yDrawerBound = true;
    MOBILE.addEventListener("change", applyDrawerAccessibility);
  }
})();