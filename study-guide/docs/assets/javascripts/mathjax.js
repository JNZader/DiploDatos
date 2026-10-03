window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  },
  // startup.typeset: false disables MathJax's own auto-typeset pass on load.
  // tex-mml-chtml.js (deferred) schedules its built-in typeset for
  // DOMContentLoaded, which races the document$.subscribe() pass below (both
  // fire on the same event) and produces 2x uncaught TypeError (replaceChild
  // on null) inside tex-mml-chtml.js. The document$ subscription fires on
  // initial load too, so math still renders without the built-in pass.
  startup: {
    typeset: false
  }
};

document$.subscribe(() => {
  MathJax.typesetPromise();
});
