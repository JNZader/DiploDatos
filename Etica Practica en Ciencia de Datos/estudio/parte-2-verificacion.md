# Segunda parte: "Ética Práctica para Ciencia de Datos", con material externo

**Esta es la continuación de** `etica-practica-ciencia-de-datos-apunte-de-estudio.md`, `etica-practica-ciencia-de-datos-guia-de-implementacion.md` y `etica-practica-ciencia-de-datos-complemento-videos-2020.md` (las clases de la materia Ética Práctica para Ciencia de Datos de la diplomatura de FAMAF UNC, dictadas por Laura Alonso Alemany y Luciana Benotti el 21 y 22 de agosto de 2026, más los videos de 2020 que la materia sigue recomendando). Esos archivos resumen lo que dice la materia. Esta segunda parte suma material externo para verificar las cifras y los casos que las docentes cuentan de memoria, resolver los nombres que la transcripción automática deformó, proponer mejoras concretas para el práctico y para el trabajo real, y marcar dónde el enfoque tiene límites. Revisé todo el 02/10/2026. Solo cito páginas que abrí; cuando una página no cargó y la leí por otra vía (por ejemplo, con `curl` desde el box), lo digo, y cuando solo tengo un resultado de búsqueda, también.

> Cómo leer esto: cuando digo "la materia" o "las docentes" me refiero a lo que dicen Laura y Luciana en las clases. Las marcas de tiempo usan la etiqueta de cada grabación del apunte (C1P1 es la clase 1, parte 1, y así hasta C2P2; los videos de 2020 son "2020-EPCD.1", "2020-EPCD.3", "2020-Grave", "2020-Caja" y "2020-Barreras") y llevan al minuto exacto en la grabación. Cuando digo "sugerencia" es una idea mía que combina fuentes, no algo que diga una fuente puntual. Los ejemplos de código y los cálculos sin fuente son míos; el ejemplo de Fairlearn lo corrí en el box sobre los datos públicos de ProPublica. Varias fuentes tienen conflictos de interés y lo marco donde importa: empresas que hablan de sus propios productos (Anthropic, Holistic AI), organizaciones que son parte en los casos que describen (CELS, Civio) o que hacen incidencia (ACLU, Amnesty, Access Now), un diputado que promueve su propio proyecto de ley, estudios jurídicos que venden asesoramiento, y herramientas hechas por las propias docentes (EDIA).

---

## Checklist actualizado (curso + mejoras)

1. Antes de usar un dataset en el práctico, escribí su data statement o su datasheet completo, incluidas las secciones de motivación, composición, recolección, usos previstos y mantenimiento que proponen Gebru y otras.
2. Usá las definiciones de la ley 25.326 (sancionada el 04/10/2000), pero sabé que es una ley de casi 26 años con multas de $1.000 a $100.000 por infracción, actualizadas por última vez en esa escala por la Resolución AAIP 126/2024.
3. Si tu sistema apoya decisiones judiciales o administrativas sobre personas, recordá que el artículo 20 de la ley 25.326 ya dice que, si implican valorar conductas humanas, no pueden tener como único fundamento un perfil armado por tratamiento informatizado de datos.
4. No digas que Argentina "ratificó en 2022" el Convenio 108+: el Congreso lo aprobó con la ley 27.699 en 2022 y el depósito de la ratificación fue el 17/04/2023, y el protocolo todavía no entró en vigor.
5. Seguí los proyectos de reforma de la ley de datos, pero leelos con cuidado: hay al menos cuatro entre 2025 y 2026 (Carro, Doñate, Yeza y Rossi), y las fuentes que los difunden suelen ser sus autores o estudios jurídicos.
6. Separá siempre la casilla de consentimiento de los términos y condiciones, y ofrecé un camino alternativo cuando el trámite garantiza un derecho, como pide el artículo 36 de la ley 10.618 de Córdoba para personas en situación de vulnerabilidad.
7. Medí las métricas de error desagregadas por grupo (falsos positivos, falsos negativos, valor predictivo) con Fairlearn o Aequitas, en vez de mirar solo la exactitud global.
8. Antes de elegir una métrica de equidad, aceptá que no podés tenerlas todas: Chouldechova y Kleinberg y otros demostraron que, si la prevalencia difiere entre grupos, calibración y tasas de error iguales no pueden darse a la vez (salvo un predictor perfecto).
9. Elegí la métrica a partir del escenario de daño, como enseña la clase 2, y escribí por qué ese error es el que más importa para las personas afectadas.
10. Medí la amplificación del sesgo comparando la distribución de la etiqueta en los datos con la de las predicciones, como hicieron Zhao y otros en "Men also like shopping" (del 33% al 68% en *cooking*).
11. Acompañá cada modelo con una model card (Mitchell y otras, 2019) que diga el uso previsto, los usos fuera de alcance y los resultados por grupo y por intersección de grupos.
12. Usá EDIA, de Fundación Vía Libre, para explorar sesgos en embeddings y modelos de lenguaje en español sin programar, sabiendo que la desarrollaron con la participación de las propias docentes.
13. Registrá los riesgos en un archivo versionado con severidad, métrica, umbral y mitigación, y poné una compuerta que impida desplegar si un riesgo alto no tiene mitigación.
14. Incluí "no desplegar" como resultado posible del análisis y decidilo antes de entrenar, no después.
15. Si trabajás con clientes europeos o con IA generativa, tené en cuenta que el artículo 50 de la AI Act se aplica desde el 02/08/2026 y que el Digital Omnibus no lo postergó (solo dio hasta el 02/12/2026 para el marcado de sistemas generativos ya existentes).
16. Para ordenar la gestión de riesgos, mirá NIST AI RMF (gratuito) e ISO/IEC 42001 (pago), que según el AI Index 2026 entraron en 2025 como influencias citadas por el 33% y el 36% de las organizaciones encuestadas (el RGPD sigue primero, con 60%).
17. Cuando cites casos, citá bien: Amazon abandonó su filtro de CV sin sanciones, la foto de "gorilas" es de Google Photos (2015) y lo del Congreso es Amazon Rekognition (ACLU, 2018), y el despixelizador (PULSE) es de Duke, no de Meta.
18. Cuando cites el caso neerlandés, separá los hechos: el sistema de riesgo se introdujo en 2013, el escándalo estalló en 2018 y 2019, el gobierno cayó en enero de 2021 y los 30.000 € son la compensación fija a las familias afectadas.
19. Revisá si en tu país hay derecho a explicación: en la Unión Europea, el tribunal de apelaciones de Ámsterdam obligó en 2023 a Uber a explicar la lógica de desactivaciones automatizadas de cuentas de choferes.
20. Mirá la base AIID (AI Incident Database) antes de diseñar: registró 362 incidentes en 2025, contra 233 en 2024, y casi siempre hay un caso parecido al tuyo.
21. Para el contexto latinoamericano, leé el informe de Access Now de 2024 sobre regulación de IA en la región y seguí el caso de reconocimiento facial de la Ciudad de Buenos Aires, declarado inconstitucional.
22. Confirmá la fecha de entrega del práctico en el aula virtual: la clase dice "1 de octubre", pero no está publicada en ninguna página abierta.

---

## Versión completa

### 1. Los datos del curso, verificados

Las docentes cuentan muchos casos y cifras de memoria y avisan que hay que revisarlos. Los revisé y los ordené de la corrección más importante a la menos importante. "Sí" quiere decir que la fuente lo confirma, "En parte" que es correcto con matices importantes, "No" que la fuente lo contradice, "Desactualizado" que fue cierto pero ya no lo es, y "No verificable" que no encontré una fuente primaria que lo confirme o lo niegue.

| Afirmación | Resultado | Matiz | Fuente |
|---|---|---|---|
| Amazon tuvo "sanciones firmes" porque su filtro de currículums descartaba a las mujeres para puestos técnicos C2P1 1:24:25, C2P1 1:24:57 | No | No hubo sanciones. Según Reuters, Amazon armó el sistema desde 2014, en 2015 vio que penalizaba la palabra "women's" y a egresadas de dos universidades solo de mujeres, y disolvió el equipo a comienzos de 2017. Amazon dice que sus reclutadores "nunca" lo usaron para evaluar candidatos. El caso sirve igual como ejemplo de daño de asignación, pero es un caso de prensa, no judicial. | [Reuters, Dastin, octubre de 2018](https://www.reuters.com/article/us-amazon-com-jobs-automation-insight-idUSKCN1MK08G) |
| Un sistema de Google etiquetaba personas negras como gorilas, y pasó con personas del Congreso de Estados Unidos C2P1 1:25:58, C2P1 1:26:31 | En parte (mezcla dos casos) | Lo de gorilas es Google Photos: Jacky Alciné lo denunció el 28/06/2015 y Google pidió disculpas y sacó la etiqueta. Lo del Congreso es otro caso: en julio de 2018, la ACLU mostró que Amazon Rekognition confundió a 28 miembros del Congreso con fotos policiales, y que el 40% de esas falsas coincidencias eran personas de color. La ACLU hace incidencia; tomalo como su prueba, no como una auditoría neutral. | [The Verge, 01/07/2015](https://www.theverge.com/2015/7/1/8880363/google-apologizes-photos-app-tags-two-black-people-gorillas); [ACLU, julio de 2018](https://www.aclu.org/news/privacy-technology/amazons-face-recognition-falsely-matched-28) |
| El reconstructor de alta resolución que convertía a Obama en un hombre blanco era "un producto de Meta" C2P2 1:06:36 | No | Es PULSE, un trabajo académico de la Universidad de Duke construido sobre StyleGAN, de NVIDIA. El video de 2020 lo atribuye bien a Duke 2020-Grave 2:25. La confusión probablemente viene de que quien respondió "los sistemas de ML están sesgados cuando los datos están sesgados" fue Yann LeCun, jefe de IA de Facebook (hoy Meta) y premio Turing, y lo criticaron Timnit Gebru y Deborah Raji. El paper de PULSE incluye una model card. | [arXiv 2003.03808](https://arxiv.org/abs/2003.03808); [The Verge, 23/06/2020](https://www.theverge.com/21298762/face-depixelizer-ai-machine-learning-tool-pulse-stylegan-obama-bias) |
| En Países Bajos, el sistema mandaba mails exigiendo devolver "unos 30.000 €", "2012, algo así" C1P1 9:04, C1P1 10:14 | En parte (corrección del monto y la fecha) | Los 30.000 € son la **compensación** fija (Catshuisregeling) que el Estado paga a cada familia afectada por suspensiones o reclamos injustos entre 2005 y el 23/10/2019, con más dinero por evaluación individual; no es lo que se exigía devolver. Según Amnesty, el algoritmo se introdujo en **2013**, usaba la nacionalidad como factor de riesgo, aprendía solo y afectó a decenas de miles de familias; el gobierno cayó en enero de 2021. El 07/12/2021 la autoridad de datos neerlandesa multó a la administración tributaria con 2,75 millones de euros por procesar la doble nacionalidad de forma ilícita y discriminatoria. Amnesty hace incidencia. | [Amnesty, 25/10/2021](https://www.amnesty.org/en/latest/news/2021/10/xenophobic-machines-dutch-child-benefit-scandal/); [Herstel Toeslagen (oficial)](https://herstel.toeslagen.nl/herstelregelingen/catshuisregeling/); [Autoriteit Persoonsgegevens, 07/12/2021](https://www.autoriteitpersoonsgegevens.nl/actueel/boete-belastingdienst-voor-discriminerende-en-onrechtmatige-werkwijze) (la página devolvió 403 al lector web; la leí con `curl`) |
| La documentación de datos de los modelos de lenguaje cambió cuando se publicó GPT-3 "en el 2019" C1P2 48:09, C1P2 48:45 | No | GPT-3 ("Language Models are Few-Shot Learners") se publicó en mayo de **2020**. GPT-2 es de 2019. | [arXiv 2005.14165](https://arxiv.org/abs/2005.14165) |
| Argentina suscribió en 2022 el Convenio 108 Plus, que suma los datos biométricos como sensibles C1P1 40:20 | En parte | El Congreso aprobó el protocolo con la ley 27.699 en noviembre de 2022, pero la ratificación se depositó el 17/04/2023 (Argentina fue el Estado número 23 y el segundo de América Latina). Argentina es parte del Convenio 108 original desde el 01/06/2019. El 108+ necesita 38 Partes para entrar en vigor, así que todavía no rige. Lo de los datos biométricos y genéticos como categorías especiales es correcto. Marval es un estudio jurídico. | [AAIP](https://www.argentina.gob.ar/aaip/comite-consultivo-del-convenio-108-coe); [Marval](https://www.marval.com/publicacion/argentina-ratifica-el-convenio-108-15441) |
| Caso de Córdoba: un alumno creó con IA imágenes pornográficas de compañeras, pasó en 2024 y "llegó a juicio en 2025" C1P1 56:23, C1P1 57:03 | En parte | Los hechos son de 2024, en la Escuela Manuel Belgrano (UNC). El acusado tiene 19 años y hay al menos 16 víctimas de 15 y 16 años; la imputación es lesiones graves calificadas por violencia de género. La causa se **elevó a juicio** el 23/09/2025 y la Cámara de Acusación lo confirmó el 16/03/2026; el juicio todavía no se hizo. No verifiqué el "caso parecido con chicos de 13 o 14 años". | [La Nación, 23/09/2025](https://www.lanacion.com.ar/seguridad/confirman-la-elevacion-a-juicio-de-joven-que-uso-ia-para-crear-imagenes-pornograficas-de-sus-nid23092025/); [Poder Judicial de Córdoba, 16/03/2026](https://www.justiciacordoba.gob.ar/cargawebweb/_News/NovedadesDetalle.aspx?idNovedad=44170) |
| En la Ciudad de Buenos Aires se había aprobado "recientemente" el reconocimiento facial con fines policiales (video de 2020) 2020-Grave 8:05 | Desactualizado | Según CELS, el juez Liberatori declaró inconstitucional el Sistema de Reconocimiento Facial de Prófugos en septiembre de 2022, y la Cámara lo confirmó el 28/04/2023. No puede reactivarse sin órganos de control, un estudio de impacto diferencial y publicidad. Se usó para buscar a más de 15.000 personas que no estaban en el registro de prófugos. CELS es parte en la causa. | [CELS, 29/04/2023](https://www.cels.org.ar/web/2023/04/confirman-la-inconstitucionalidad-del-uso-del-sistema-de-reconocimiento-facial/) |
| En la conferencia AAAI se recibieron 40.000 artículos y los revisores marcaron tres cuartos como generados con IA C1P1 1:08:49, C1P1 1:09:23 | En parte | El volumen es plausible: según AAAI, la edición 2026 recibió casi 29.000 envíos (unos 23.000 llegaron a revisión), casi 20.000 de China. Los 40.000 de AAAI-27 y los "tres de cada cuatro" generados con IA solo los encontré en una publicación de LinkedIn de Lionel Briand que cita a revisores que conoce. Es una anécdota, no una cifra oficial. | [AAAI-26, actualización del proceso de revisión](https://aaai.org/conference/aaai/aaai-26/review-process-update/); [Lionel Briand en LinkedIn](https://www.linkedin.com/posts/lionel-briand-5082b1_40000-submissions-at-aaai-2027-based-on-activity-7495951022545121280-RKyn) |
| Huella de carbono de entrenar un transformer comparada con un vuelo Nueva York San Francisco, una vida en Estados Unidos y un auto (video de 2020) 2020-Grave 19:37 | En parte | Es la tabla 1 de Strubell y otros (2019), en libras de CO2e: vuelo 1.984; un estadounidense por año 36.156; un auto en su vida útil 126.000; Transformer grande 192; Transformer con búsqueda de arquitectura neuronal (NAS) 626.155. La cifra enorme corresponde a la búsqueda de arquitectura, no a un entrenamiento normal. No verifiqué la nota del posteo del futbolista. | [arXiv 1906.02243](https://arxiv.org/abs/1906.02243) |
| La ley 25.326 tiene "casi 26 años" C1P1 22:29 | Sí | Se sancionó el 04/10/2000 y se promulgó el 30/10/2000. | [Texto actualizado en InfoLEG](https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/texact.htm) |
| Las multas de la ley van de 1.000 a 100.000 pesos C1P1 51:59, C1P1 53:36 | Sí, con un matiz | El artículo 31 fija esa escala, y la Resolución AAIP 126/2024 (vigente desde el 01/06/2024) la mantiene: leves de $1.000 a $80.000, graves hasta $90.000 y muy graves hasta $100.000. El matiz es que la acumulación de conductas idénticas permite multiplicar hasta 500 veces (unos $50 millones), y hay un 50% de descuento por pago voluntario en 20 días hábiles. | [InfoLEG, ley 25.326](https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/texact.htm); [Res. AAIP 126/2024](https://servicios.infoleg.gob.ar/infolegInternet/anexos/395000-399999/399750/norma.htm) |
| En Brasil el tope es el 2% de la facturación C1P1 53:36 | Sí | El artículo 52 de la LGPD fija una multa simple de hasta el 2% de la facturación en Brasil del último ejercicio, con un tope de 50 millones de reales por infracción. | [Ley 13.709 (LGPD), Planalto](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm) (leída con `curl`) |
| La ley de modernización 10.618 de Córdoba prevé canales para personas vulnerables digitalmente C1P1 45:14 | Sí | La ley 10.618 (27/03/2019) dice en su artículo 36 que la autoridad debe dar a las personas en situación de vulnerabilidad un trato adecuado, asistencia en el uso de las TIC o mecanismos que garanticen el ejercicio pleno de sus derechos. Lo leí en un sitio que consolida leyes, no en el boletín oficial. | [Ley 10.618, art. 36 (leyes-ar.com)](https://leyes-ar.com/simplificacion_y_modernizacion_de_la_administracion_cordoba/36.htm) |
| Entre las cinco empresas más caras del mundo está primero Nvidia, y las demás tienen como insumo básico el dato C1P2 5:42 | Sí, con un matiz | El 02/10/2026 el ranking era Nvidia (unos USD 5,6 billones), Apple, Alphabet, Microsoft y Amazon. Apple vende sobre todo hardware, así que "insumo básico el dato" le cabe menos. | [companiesmarketcap.com](https://companiesmarketcap.com/) |
| El artículo 50 de la AI Act pide marcar las salidas de la IA generativa en un formato legible por máquina y que la marca no se pueda manipular fácilmente C1P1 59:13, C1P1 59:45 | Sí (lo de "no manipular" es una paráfrasis) | El 50(2) pide que las salidas sintéticas estén marcadas en un formato legible por máquina y detectables, con soluciones "effective, interoperable, robust and reliable"; "robustas" es lo más cercano a "que no se pueda manipular". También obliga a avisar de los deepfakes y del texto sobre asuntos de interés público. Se aplica desde el 02/08/2026. El Digital Omnibus (Reglamento 2026/1744) postergó las obligaciones de alto riesgo, pero no el artículo 50; solo dio hasta el 02/12/2026 para el marcado de sistemas generativos ya existentes (esto último lo leí en una fuente secundaria). Hay un código de prácticas final desde el 10/06/2026. | [Artículo 50](https://artificialintelligenceact.eu/article/50/); [Comisión Europea, código de prácticas](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content); [CPD, sobre el Omnibus](https://www.cpduk.co.uk/news/deadline-moved-and-duty-did-not-ai-act-transparency-obligations-after-digital-omnibus) |
| Anthropic anunció que Claude marca el texto que genera, lo desplegó globalmente aunque la norma es europea, y no liberó el detector C1P1 58:43, C1P1 1:00:17 | Sí | La nota del 14/08/2026 (actualizada el 01/09) dice que usa una técnica basada en SynthID-Text, que lo aplica globalmente porque todavía no tiene una forma durable de limitarlo por región, que la API de detección está en vista previa privada y que las imágenes llevan credenciales C2PA. Es la página del propio proveedor. | [Anthropic](https://www.anthropic.com/news/claude-text-watermark) |
| El reporte de Stanford muestra que los incidentes reportados con IA suben cada año C1P1 5:06, C1P1 5:41 | Sí | El capítulo de IA responsable del AI Index 2026 dice que la AIID registró 362 incidentes en 2025 contra 233 en 2024, y menos de 100 por año hasta 2022. El monitor de la OCDE llegó a 435 por mes en enero de 2026. | [AI Index 2026, IA responsable](https://hai.stanford.edu/ai-index/2026-ai-index-report/responsible-ai) |
| En una base de incidentes, el 20% afecta por raza, el 10% por sexo, el 6% por religión u origen y el 5% por discapacidad C1P1 7:23 | No verificable | Esas proporciones no están en el capítulo del AI Index que leí, y la clase no dice de qué base salen. | [AI Index 2026, IA responsable](https://hai.stanford.edu/ai-index/2026-ai-index-report/responsible-ai) |
| COMPAS: entre quienes no reincidieron, 23% de las personas blancas y 45% de las negras tenían riesgo alto; entre las de riesgo bajo, casi 50% de las blancas y 30% de las negras reincidieron C2P1 24:49, C2P1 25:25 | Sí | ProPublica da 23,5% contra 44,9% y 47,7% contra 28,0%, sobre más de 7.000 personas del condado de Broward. La exactitud global era 61%, y para delitos violentos solo acertaba el 20%. Northpointe disputa el análisis. ProPublica aclara que la financia la Fundación Arnold, que hace una herramienta competidora. En el box, con los filtros de la notebook de ProPublica y el umbral "medio o alto", me dio 42,3% contra 22,0% (sección 3). | [ProPublica, 23/05/2016](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing) |
| "Men also like shopping" es de alrededor de 2017, ganó el premio al mejor paper, y en *cooking* el dataset tenía 33% más mujeres y el modelo subía la disparidad al 68% C2P1 51:07, C2P1 53:55 | Sí | Zhao, Wang, Yatskar, Ordonez y Chang, EMNLP 2017. Las cifras coinciden, y el método redujo la amplificación 47,5% y 40,5%. El premio a mejor paper largo lo vi en resultados de búsqueda (página de UCLA), no en una página que abrí. | [ACL Anthology D17-1323](https://aclanthology.org/D17-1323/) |
| Cada vez más artículos de PLN tienen sección de consideraciones éticas, pero pocos discuten quién se daña y casi ninguno las poblaciones vulnerables C1P2 21:37, C1P2 22:41 | Sí para la cualidad; las cifras son de otro año | El trabajo publicado de Benotti y Blackburn (EMNLP 2022) clasificó a mano las secciones de ACL 2021: el 15,7% de los artículos tenía una; de esas, el 74% describe beneficios, el 52% daños, el 23% daños a grupos vulnerables, y el 20% eran solo descargos ("disclaimers"). La serie hasta 2024 que muestra la clase no la encontré publicada. Es un trabajo de la propia docente. | [ACL Anthology 2022.emnlp-main.299](https://aclanthology.org/2022.emnlp-main.299/) |
| Un consejo de expertos en IA de las Naciones Unidas sigue trabajando en consensos globales C1P2 9:04 | Sí, con nombre | Es probablemente el Panel Científico Internacional Independiente sobre IA, creado por la resolución A/RES/79/325 del 26/08/2025, con 40 miembros nombrados en febrero de 2026. Eligió como copresidentes a Yoshua Bengio y Maria Ressa y publicó su primer informe preliminar el 01/07/2026. Antes existió el Órgano Asesor de Alto Nivel del Secretario General. | [Preguntas frecuentes del Panel](https://www.un.org/independent-international-scientific-panel-ai/en/faq) (leída con `curl`) |
| Wang y Kosinski entrenaron un clasificador de orientación sexual con fotos de una app de citas, con más precisión para hombres que para mujeres C1P2 15:54, C1P2 16:27 | Sí | Journal of Personality and Social Psychology, 2018: 35.326 imágenes de un sitio de citas; con una imagen, 81% para hombres y 74% para mujeres, contra 61% y 54% de jueces humanos. Hay críticas metodológicas a la replicación que no abrí. | [Stanford GSB](https://www.gsb.stanford.edu/faculty-research/publications/deep-neural-networks-are-more-accurate-humans-detecting-sexual) |
| El laboratorio de California estaba financiado "casi en un 90%" por una agencia de defensa ("dar") 2020-EPCD.1 10:47, C1P2 40:34 | En parte | El USC Institute for Creative Technologies se presenta como un University Affiliated Research Center patrocinado por el Ejército de Estados Unidos (US Army). "dar" es probablemente "the Army", no DARPA. El 90% no lo pude verificar. | [ICT, USC](https://ict.usc.edu/) |
| Se dice que DeepSeek destiló modelos comerciales C1P2 50:25 | Sí (según una de las partes) | Anthropic dice que DeepSeek hizo más de 150.000 intercambios para destilar Claude, Moonshot 3,4 millones y MiniMax 13 millones, con unas 24.000 cuentas fraudulentas. Es la acusación de la empresa afectada. | [Anthropic, 23/02/2026](https://www.anthropic.com/research/detecting-and-preventing-distillation-attacks) |
| En educación, finanzas y trabajo es obligatorio por ley que un algoritmo explique su decisión; si Uber no puede explicar por qué te asigna un viaje, podés denunciar C2P2 1:34:19, C2P2 1:34:56 | En parte | El caso real más cercano es europeo y de protección de datos, no laboral: el 04/04/2023 el tribunal de apelaciones de Ámsterdam ordenó a Uber dar a tres choferes "información útil sobre la lógica" de la desactivación automatizada de sus cuentas por fraude (artículos 15 y 22 del RGPD), con una multa de 4.000 € por día de incumplimiento, porque la revisión humana no había sido significativa. No trata de asignación de viajes ni rige en Argentina, donde el artículo 20 de la ley 25.326 es lo más parecido. | [Gerechtshof Amsterdam, ECLI:NL:GHAMS:2023:793 (texto en lexboost)](https://www.lexboost.com/rechtspraak/ECLI:NL:GHAMS:2023:793) |
| La dipirona en Europa está prohibida y se usa como rescate en hospitales C2P2 21:55 | No | No está prohibida en la Unión Europea. La EMA revisó el riesgo de agranulocitosis en 2024 y concluyó que los beneficios siguen superando los riesgos, con advertencias reforzadas (decisión de la Comisión del 22/11/2024). Está autorizada en 18 países de la UE, entre ellos España, Alemania, Italia y Países Bajos; en Finlandia se retiró. Que no se comercialice en Reino Unido, Suecia o Estados Unidos lo vi solo en resultados de búsqueda. | [EMA, metamizol](https://www.ema.europa.eu/en/medicines/human/referrals/metamizole-containing-medicinal-products-0) |
| Informe de 2024 de "Access" sobre regulación de IA en Latinoamérica C2P2 1:37:13, C2P2 1:37:50 | Sí, con nombre | Es "Radiografía normativa: ¿Dónde, qué y cómo se está regulando la inteligencia artificial en América Latina?", de Access Now con TrustLaw (Thomson Reuters Foundation), del 26/02/2024. Cubre Argentina, Brasil, Chile, Colombia, Costa Rica, Perú, México y Uruguay. Access Now hace incidencia. | [Access Now](https://www.accessnow.org/press-release/reporte-inteligencia-artificial-en-america-latina/) |
| Civio ("esbio") tuvo hace poco una gran victoria judicial que todavía no se efectivizó C2P2 1:33:47 | Sí en lo primero | El Tribunal Supremo español (STS 1119/2025) ordenó dar acceso al código fuente de BOSCO, la aplicación que decide el bono social eléctrico, después de una pelea que Civio empezó en 2018. No verifiqué si ya se entregó el código, ni el análisis de errores de IA en sanidad que menciona la clase. Civio es parte. | [Civio, 17/09/2025](https://civio.es/novedades/2025/09/17/civio-abre-camino-en-la-transparencia-algoritmica-el-supremo-condena-al-gobierno-a-entregar-el-codigo-fuente-de-bosco/) |
| Definición de sesgo de Friedman y Nissenbaum (1996) 2020-EPCD.3 1:43 | Sí | "Systematically and unfairly discriminate against certain individuals or groups of individuals in favor of others", en ACM TOIS 14(3), julio de 1996, páginas 330 a 347, con tres categorías: preexistente, técnico y emergente. | [PDF de Nissenbaum](https://nissenbaum.tech.cornell.edu/papers/biasincomputers.pdf) |
| Fecha de entrega del práctico: "la fecha es el 1 de octubre" C1P2 1:01:36 | No verificable | La página pública de materias optativas de la diplomatura no publica fechas, y no encontré la fecha en ningún otro lado. Confirmala en el aula virtual; si era el 01/10/2026, ya pasó. | [Diplodatos, materias optativas](https://diplodatos.famaf.unc.edu.ar/metodologia-y-modalidad-de-cursado/materias-optativas/) |
| En salud se implementan sistemas con tasas de error del orden del 30% C2P2 1:32:40 | No verificable | La clase no dice qué sistema ni de dónde sale la cifra. | No encontré fuente |
| Hispanos en COMPAS con una tasa de reincidencia más baja C2P2 1:22:28 | No verificable | El artículo de ProPublica que leí se concentra en personas blancas y negras. | [ProPublica](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing) |
| Un detector de somnolencia entrenado con personas occidentales daba falsas alarmas en Asia C1P2 42:54 | No verificable | No encontré el caso original. | No encontré fuente |
| Un estudio en Nature sobre la copa de vino y el corazón que olvidaba la clase social C2P1 35:13 | No verificable | La clase no da autor ni año, y no lo busqué a fondo. | No encontré fuente |

**Lo más importante para corregir en el apunte.** Las correcciones que cambian lo que dirías en un examen o en el práctico son cinco: Amazon no tuvo sanciones (abandonó el sistema), el caso del Congreso es Amazon Rekognition y no Google Photos, el despixelizador PULSE es de Duke y no de Meta, los 30.000 € del caso neerlandés son la compensación y el sistema es de 2013, y GPT-3 es de 2020. También conviene ajustar tres fechas jurídicas: el Convenio 108+ se ratificó en 2023 y todavía no rige, el caso de Córdoba está elevado a juicio pero sin juicio, y el reconocimiento facial porteño fue declarado inconstitucional. Las cifras de AAAI ("tres cuartos generados con IA") y de Strubell (la búsqueda de arquitectura, no un entrenamiento) hay que contarlas con su matiz. Lo legal argentino salió muy bien parado: la edad de la ley, las multas, el artículo 36 de la ley cordobesa y la cifra de Brasil son correctos.

### 2. Nombres y dudas de la transcripción, resueltos

| En la transcripción | Resultado | Cómo lo resolví |
|---|---|---|
| AETAS, ACTAS, Equira, "un framework de un proyecto europeo" C2P2 3:59, C2P2 1:24:08 | **Aequitas**, confirmado | El README de Aequitas lo presenta como un toolkit abierto de auditoría de sesgo, alojado en la organización dssg de GitHub y con sitio en dsapp.uchicago.edu (Universidad de Chicago), y trae una notebook de demostración con COMPAS; la entrada usa las columnas `score`, `label_value` y los atributos sensibles. Lo de "proyecto europeo" no lo pude confirmar, porque el README no lo menciona ([README](https://raw.githubusercontent.com/dssg/aequitas/master/README.md)) |
| Holistic, "un framework de fairness" con datasets C2P2 2:54 | **holisticai**, probable | Es la biblioteca abierta de la organización holistic-ai en GitHub, "an open-source tool to assess and improve the trustworthiness of AI systems" ([GitHub](https://github.com/holistic-ai/holisticai)). Detrás está la empresa Holistic AI, que vende auditorías; no abrí su sitio |
| "De KIDA en Machine Learning" C2P2 2:54 | "De **equidad** en Machine Learning", probable | Por el contexto ("un framework de fairness, de equidad en machine learning"); el glosario del apunte lo tomaba como nombre de la notebook |
| Edia, Edy, Edas C2P2 1:21:16 | **EDIA**, confirmado | Es la herramienta de Fundación Vía Libre para explorar sesgos en embeddings y modelos de lenguaje, con código abierto en GitHub (fvialibre/edia) y una versión 2.0 de 2026 que suma imágenes ([ia.vialibre.org.ar](https://ia.vialibre.org.ar/)). Según una página de FAMAF que vi en resultados de búsqueda, la desarrollaron con Laura Alonso Alemany y Luciana Benotti: conflicto de interés a favor |
| esbio, "una ONG española de transparencia" C2P2 1:33:47 | **Civio**, confirmado | Civio es la fundación española que litigó por el código de BOSCO ([Civio](https://civio.es/novedades/2025/09/17/civio-abre-camino-en-la-transparencia-algoritmica-el-supremo-condena-al-gobierno-a-entregar-el-codigo-fuente-de-bosco/)) |
| Access, "informe de 2024" C2P2 1:37:50 | **Access Now**, confirmado | Informe "Radiografía normativa", del 26/02/2024 ([Access Now](https://www.accessnow.org/press-release/reporte-inteligencia-artificial-en-america-latina/)) |
| índice latinoamericano de IA C2P2 1:37:13 | Probablemente el **ILIA** (Índice Latinoamericano de Inteligencia Artificial, de CENIA, Chile); dudoso | Lo vi en resultados de búsqueda; no abrí su página |
| AI GDAR, AI Gator C1P2 16:27, C1P2 18:11 | El clasificador de **Wang y Kosinski** (2018), confirmado; el nombre deformado es dudoso | La descripción coincide con el paper (fotos de un sitio de citas, más precisión para hombres). Popularmente se lo conoce como "AI gaydar" (lo vi en resultados de búsqueda), lo que explica la deformación ([Stanford GSB](https://www.gsb.stanford.edu/faculty-research/publications/deep-neural-networks-are-more-accurate-humans-detecting-sexual)) |
| chapapote de Microsoft 2020-EPCD.1 9:04 | **Tay**, muy probable | El chatbot de Microsoft que aprendió a decir barbaridades racistas en Twitter y apagaron en menos de 24 horas en marzo de 2016 ([The Verge, 24/03/2016](https://www.theverge.com/2016/3/24/11297050/tay-microsoft-chatbot-racist)) |
| universidad de sauce, universidad de salsa en California 2020-EPCD.1 3:27, 2020-EPCD.1 10:47 | **USC** (University of Southern California), Institute for Creative Technologies, muy probable | "Instituto de tecnologías creativas" y humanos virtuales coinciden con el ICT ([ict.usc.edu](https://ict.usc.edu/)) |
| financiado por "dar" 2020-EPCD.1 10:47 | **the Army** (Ejército de Estados Unidos), probable; no DARPA | El ICT se presenta como University Affiliated Research Center patrocinado por el US Army ([ict.usc.edu](https://ict.usc.edu/)) |
| humanas virtuales "y grace" 2020-EPCD.1 3:27 | **Ada y Grace**, probable | Las guías virtuales del Museum of Science de Boston (2009), hechas con el ICT; lo vi solo en resultados de búsqueda |
| friedmann y nissan brawn 2020-EPCD.3 1:43 | **Friedman y Nissenbaum**, confirmado | "Bias in Computer Systems", ACM TOIS, 1996 ([PDF](https://nissenbaum.tech.cornell.edu/papers/biasincomputers.pdf)) |
| despixelizador C2P2 1:06:36, 2020-Grave 2:25 | **PULSE**, de Duke, confirmado | [arXiv 2003.03808](https://arxiv.org/abs/2003.03808) |
| Jan Lecun; "un ganador del premio Turing" sin nombre 2020-Grave 4:46 | **Yann LeCun**, confirmado | The Verge cita su tuit sobre PULSE ([The Verge](https://www.theverge.com/21298762/face-depixelizer-ai-machine-learning-tool-pulse-stylegan-obama-bias)) |
| la FIP o rentas de Países Bajos | La **Belastingdienst** (administración tributaria), que administraba los subsidios por medio de su dirección de Toeslagen, confirmado | La multa de la autoridad de datos está dirigida a la Belastingdienst ([Autoriteit Persoonsgegevens](https://www.autoriteitpersoonsgegevens.nl/actueel/boete-belastingdienst-voor-discriminerende-en-onrechtmatige-werkwijze)) |
| consejo de expertos de las Naciones Unidas C1P2 9:04 | **Panel Científico Internacional Independiente sobre IA**, probable | Es el órgano científico vigente de la ONU sobre IA ([preguntas frecuentes](https://www.un.org/independent-international-scientific-panel-ai/en/faq)) |
| tomás balmaseda 2020-Grave 18:30 | **Tomás Balmaceda**, confirmado | Integrante de GIFT, el grupo que hizo la Caja de Herramientas ([grupo.gift](https://grupo.gift/)) |
| Grupo Gift | **GIFT**, Grupo de Investigación de Inteligencia Artificial, Filosofía y Tecnología (SADAF), confirmado | [grupo.gift](https://grupo.gift/) |
| diana, universidad del litoral 2020-Grave 0:05 | Sin resolver | Podría ser Diana Pérez, de GIFT, pero la transcripción la asocia a otra universidad; no lo pude confirmar |
| emirates code 2020-EPCD.1 15:53 | Sin resolver | No encontré la charla o autora original en la que se basa el video |
| Mariela, de la licenciatura en ciencia de datos de la UNSAM | Sin resolver (apellido) | No busqué el apellido para no adivinar |
| "la sección 5.4 de un libro" C2P2 52:11 | Sin resolver | La clase no nombra el libro |

### 3. Medir la equidad desagregada: de la notebook a Fairlearn y Aequitas

**Qué dice el curso.** La clase 2 arma las métricas a mano: partís de la matriz de confusión de cada grupo y comparás tasas de falsos positivos y falsos negativos, con COMPAS como ejemplo C2P1 1:34:21, C2P1 1:35:27. La notebook de la segunda parte usa el dataset de COMPAS publicado en el repositorio de Aequitas y menciona Holistic como fuente de otros datasets C2P2 2:54, C2P2 3:59. Laura insiste en que lo que importa son "buenas preguntas" C2P1 1:42:47.

**Qué suma el material externo.**
- **Fairlearn** es un proyecto abierto y comunitario con métricas y algoritmos de mitigación, y su portada dice "fairness is sociotechnical": la equidad depende de más que de correr código ([fairlearn.org](https://fairlearn.org/)).
- **AIF360**, del grupo Trusted-AI, reúne métricas para datasets y modelos, explicaciones de esas métricas y algoritmos de mitigación ([GitHub](https://github.com/Trusted-AI/AIF360)).
- **Aequitas** produce un informe de sesgo a partir de un archivo con `score`, `label_value` y los atributos sensibles, y su README trae la demo de COMPAS ([README](https://raw.githubusercontent.com/dssg/aequitas/master/README.md)).
- Las model cards proponen reportar la evaluación "disaggregated" por grupo y también por intersecciones, con intervalos de confianza ([Mitchell y otras, 2019](https://arxiv.org/abs/1810.03993)).

**Cómo implementarlo.** Este script reproduce el análisis de ProPublica con Fairlearn. Lo corrí en el box el 02/10/2026 con Fairlearn 0.14.0, pandas 3.0.6 y scikit-learn 1.9.1, sobre `compas-scores-two-years.csv` del repositorio público de ProPublica:

```python
import pandas as pd
from fairlearn.metrics import MetricFrame, false_positive_rate, false_negative_rate, selection_rate
from sklearn.metrics import precision_score

url = "https://raw.githubusercontent.com/propublica/compas-analysis/master/compas-scores-two-years.csv"
df = pd.read_csv(url)
# Mismos filtros que la notebook de ProPublica
df = df[(df.days_b_screening_arrest.between(-30, 30)) & (df.is_recid != -1)
        & (df.c_charge_degree != "O") & (df.score_text != "N/A")]
df = df[df.race.isin(["African-American", "Caucasian"])]
y_true = df.two_year_recid
y_pred = (df.decile_score >= 5).astype(int)   # riesgo "medio o alto"

mf = MetricFrame(
    metrics={"FPR": false_positive_rate, "FNR": false_negative_rate,
             "PPV": precision_score, "tasa_seleccion": selection_rate},
    y_true=y_true, y_pred=y_pred, sensitive_features=df.race)
print(mf.by_group.round(3))
print("prevalencia:", df.groupby("race").two_year_recid.mean().round(3).to_dict())
print("diferencia máxima:", mf.difference().round(3).to_dict())
```

Resultado sobre 5.278 personas:

| Grupo | FPR | FNR | PPV | Tasa de selección | — |
|---|---|---|---|---|---|
| Personas negras (African-American) | 0,423 | 0,285 | 0,650 | 0,576 | 0,523 |
| Personas blancas (Caucasian) | 0,220 | 0,496 | 0,595 | 0,331 | 0,391 |

La diferencia de FPR es 0,203 y la de FNR 0,212: es la misma historia que cuenta la clase (más falsos positivos para personas negras, más falsos negativos para blancas), con números un poco distintos a los de ProPublica porque el umbral y los filtros no son idénticos. Fijate que el PPV es parecido entre grupos; eso es lo que defendía Northpointe, y la sección 4 explica por qué las dos partes tienen razón a la vez.

**Sugerencia para el práctico.** Si tu dataset no tiene un modelo, entrená uno simple (una regresión logística) solo para medir; si tiene más de un atributo sensible, pasá un `DataFrame` con las dos columnas a `sensitive_features` y Fairlearn calcula las intersecciones.

### 4. Los teoremas de imposibilidad: por qué "maximizar todas" no se puede

**Qué dice el curso.** Laura avisa que algunas métricas de equidad son complementarias, que si una es alta otra es baja por definición, y que querer el modelo "que maximiza todas" no puede ser C2P2 52:11.

**Qué suma el material externo.** La afirmación tiene demostración formal, y conviene citarla así:
- **Chouldechova (2017)** muestra que COMPAS está aproximadamente calibrado y tiene paridad predictiva, pero que, cuando la prevalencia de reincidencia difiere entre grupos (en su análisis, 51% contra 39%), un instrumento con paridad predictiva no puede tener a la vez tasas de falsos positivos y de falsos negativos iguales ([arXiv 1703.00056](https://arxiv.org/abs/1703.00056)).
- **Kleinberg, Mullainathan y Raghavan (2016)** prueban que calibración y balance para las dos clases solo se pueden cumplir juntos con un predictor perfecto o con tasas base iguales ([arXiv 1609.05807](https://arxiv.org/abs/1609.05807)).

La relación de Chouldechova se puede verificar con los números de la sección 3. Para cada grupo, con prevalencia `p`:

```python
# FPR = p/(1-p) * (1-PPV)/PPV * (1-FNR)
for g, r in mf.by_group.iterrows():
    p = y_true[df.race == g].mean()
    fpr = p/(1-p) * (1-r.PPV)/r.PPV * (1-r.FNR)
    print(g, "FPR por identidad:", round(fpr, 3), "FPR medido:", round(r.FPR, 3))
# African-American FPR por identidad: 0.423 FPR medido: 0.423
# Caucasian FPR por identidad: 0.22 FPR medido: 0.22
```

**Cómo implementarlo.** La consecuencia práctica es que elegir una métrica de equidad es una decisión de valores, no técnica. En el práctico, escribí cuál de los dos errores daña más a las personas afectadas en tu escenario (por ejemplo, un falso positivo que lleva a una sanción) y fijá esa métrica como la que tiene que ser igual entre grupos, aceptando por escrito que otra va a quedar desigual. Es lo que la clase llama formalizar el escenario de daño, con el respaldo de un teorema.

### 5. Documentar datos y modelos: datasheets, data statements y model cards

**Qué dice el curso.** El práctico es un data statement 2020-EPCD.3 1:43, y Luciana cuenta que las autoras de la metodología intentaron que OpenAI documentara así sus datos cuando salió ChatGPT, sin éxito C1P2 48:45, C1P2 49:19. En el video de barreras, Laura presenta los data statements como una de las dos herramientas para instrumentalizar los consensos sociales 2020-Barreras 17:35.

**Qué suma el material externo.**
- **Data Statements** (Bender y Friedman, TACL 2018) es la propuesta específica para PLN que usa el práctico ([ACL Anthology Q18-1041](https://aclanthology.org/Q18-1041/)).
- **Datasheets for Datasets** (Gebru y otras) organiza las preguntas en motivación, composición, proceso de recolección, preprocesamiento, usos, distribución y mantenimiento, y aclara que no está pensado para automatizarse ([arXiv 1803.09010](https://arxiv.org/abs/1803.09010)).
- **Model Cards** (Mitchell y otras, FAT* 2019) es el complemento para modelos: detalles del modelo, uso previsto y fuera de alcance, factores, métricas, datos de evaluación y entrenamiento, análisis cuantitativo por grupo e intersección, consideraciones éticas, advertencias y recomendaciones. Las autoras advierten que su utilidad "relies on the integrity of the creator(s)" y que no alcanzan solas, sin auditorías externas ([arXiv 1810.03993](https://arxiv.org/abs/1810.03993)).

**Cómo implementarlo.** Una plantilla corta que combina las tres, para pegar al lado del data statement del práctico (sugerencia):

```markdown
# Ficha de datos y modelo: <nombre>

## Motivación (datasheet)
- ¿Para qué se creó el dataset? ¿Quién lo financió?
## Composición (datasheet + data statement)
- ¿Qué representa cada fila? ¿Hay datos sensibles según la ley 25.326 (origen, salud, opiniones, religión, vida sexual)?
- Variedad de lengua, perfil de hablantes y de anotadores (data statement)
## Recolección y consentimiento
- ¿Cómo se obtuvo? ¿Hubo consentimiento informado, libre y expreso? ¿Para qué finalidad?
## Usos previstos y fuera de alcance (model card)
- Para qué sí. Para qué no, y por qué.
## Evaluación desagregada (model card)
- Métrica elegida y escenario de daño que la justifica.
- Resultados por grupo y por intersección, con intervalos (pegá el MetricFrame).
## Riesgos y decisión
- Riesgos abiertos (ver registro). ¿Se despliega? Sí / No / Con condiciones.
## Mantenimiento
- Quién actualiza, cada cuánto, y a quién se reportan errores.
```

### 6. Un registro de riesgos con compuerta de "no desplegar"

**Qué dice el curso.** La materia trabaja la reflexión del equipo: las preguntas fundamentales (quién se beneficia, quién se daña), la autoetnografía y los escenarios de daño. Laura, en 2020, lista los trucos para que nada cambie, entre ellos "cuando pase, lo arreglamos" y eludir la responsabilidad 2020-Barreras 8:39, 2020-Barreras 10:07. El curso no propone un artefacto que obligue a frenar.

**Qué suma el material externo.**
- La Declaración de Montreal pide que los sistemas, antes de salir al mercado, pasen pruebas de confiabilidad que no pongan en peligro a las personas, y que los errores se compartan públicamente en los sectores de riesgo (principio de prudencia) ([Montreal](https://montrealdeclaration-responsibleai.com/the-declaration/)).
- NIST publicó el AI Risk Management Framework 1.0 el 26/01/2023 y un perfil para IA generativa en julio de 2024; es gratuito y lo están revisando ([NIST](https://www.nist.gov/itl/ai-risk-management-framework)).
- ISO/IEC 42001:2023 es la norma de sistemas de gestión de IA (primera edición, diciembre de 2023), certificable y paga: el PDF cuesta 225 francos suizos ([ISO](https://www.iso.org/standard/42001), leída con `curl` porque el lector web la bloqueó).
- El AI Index 2026 dice que el RGPD sigue siendo la influencia regulatoria más citada por las organizaciones (60%), y que en 2025 aparecen ISO 42001 (36%) y NIST AI RMF (33%) ([AI Index 2026](https://hai.stanford.edu/ai-index/2026-ai-index-report/responsible-ai)).

**Cómo implementarlo.** Un registro en YAML, versionado junto al código, y una compuerta que corre en la integración continua (lo probé en el box con PyYAML 6.0.3):

```yaml
# riesgos.yaml
sistema: scoring de créditos blandos (caso de la Caja de Herramientas)
responsable: "nombre y rol de quien firma"
riesgos:
  - id: R1
    dano: "Mujeres jefas de hogar con trabajo no registrado quedan excluidas"
    tipo: asignacion
    severidad: alta
    metrica: "diferencia de FNR entre grupos"
    umbral: 0.05
    mitigacion: "revisión humana de todo rechazo; quitar código postal"
  - id: R2
    dano: "Datos de salud enviados a un proveedor en el exterior"
    tipo: privacidad
    severidad: alta
    metrica: null
    umbral: null
    mitigacion: ""
```

```python
# gate.py: devuelve código 1 (y frena el despliegue) si hay motivos para no desplegar
import sys, yaml

def revisar(registro, mediciones):
    motivos = []
    for r in registro["riesgos"]:
        if r["severidad"] == "alta" and not r.get("mitigacion"):
            motivos.append(f'{r["id"]}: riesgo alto sin mitigación ({r["dano"]})')
        if r.get("metrica") and r["id"] in mediciones:
            if mediciones[r["id"]] > r["umbral"]:
                motivos.append(f'{r["id"]}: {r["metrica"]} = {mediciones[r["id"]]:.3f} supera {r["umbral"]}')
        elif r.get("metrica"):
            motivos.append(f'{r["id"]}: falta medir {r["metrica"]}')
    return motivos

registro = yaml.safe_load(open("riesgos.yaml"))
motivos = revisar(registro, {"R1": 0.212})   # por ejemplo, mf.difference()["FNR"]
for m in motivos:
    print("NO DESPLEGAR:", m)
sys.exit(1 if motivos else 0)
```

Con esos datos, la compuerta frena por los dos riesgos. La idea no es que un script decida la ética, sino que "no desplegar" quede escrito como resultado posible y que saltearlo exija cambiar un archivo firmado.

### 7. Herramientas y casos en español y desde la región

**Qué dice el curso.** La materia recomienda material local: la Caja de Herramientas de GIFT, EDIA, el informe de Access Now y el caso de Córdoba. Laura cuenta en 2020 que no encontraba la Declaración de Montreal en castellano 2020-Barreras 15:45.

**Qué suma el material externo.**
- **EDIA** permite explorar sesgos en embeddings y modelos de lenguaje en español sin programar; los datos se guardan en servidores del CCAD, y la versión 2.0 suma imágenes ([ia.vialibre.org.ar](https://ia.vialibre.org.ar/)).
- **La Caja de Herramientas Humanísticas** de GIFT, hecha en colaboración con fAIr LAC, tiene casos ambientados en Argentina (créditos en el conurbano, Chagas, un exoesqueleto en un puerto). El link del video ya no funciona; está en [proyectoguia.lat](https://proyectoguia.lat/wp-content/uploads/2020/05/Caja-de-herramientas-Humanistas.pdf).
- **La Declaración de Montreal** hoy está en 10 idiomas, incluido el español ([Montreal](https://montrealdeclaration-responsibleai.com/the-declaration/)).
- **Casos argentinos para el práctico:** el reconocimiento facial porteño ([CELS](https://www.cels.org.ar/web/2023/04/confirman-la-inconstitucionalidad-del-uso-del-sistema-de-reconocimiento-facial/)) y el caso de deepfakes de la Escuela Manuel Belgrano ([Poder Judicial de Córdoba](https://www.justiciacordoba.gob.ar/cargawebweb/_News/NovedadesDetalle.aspx?idNovedad=44170)).
- **Un caso en español fuera de la región:** BOSCO y el fallo del Supremo que obliga a abrir su código ([Civio](https://civio.es/novedades/2025/09/17/civio-abre-camino-en-la-transparencia-algoritmica-el-supremo-condena-al-gobierno-a-entregar-el-codigo-fuente-de-bosco/)).

**Cómo implementarlo.** **Sugerencia:** para la parte de embeddings del práctico, compará lo que muestra la notebook de las docentes con lo que muestra EDIA sobre las mismas palabras (por ejemplo, profesiones), y anotá dónde difieren. Como EDIA es de las propias docentes, sumá una segunda herramienta (por ejemplo, las métricas de AIF360) para no evaluar solo con la vara de quien te corrige.

### 8. La parte legal, actualizada

**Qué dice el curso.** Luciana explica la ley 25.326 (definiciones, principios, consentimiento) y aclara que no es abogada C1P1 41:57; una estudiante abogada suma el Convenio 108+ C1P1 40:20, y la clase cierra con la AI Act y las marcas de agua C1P1 59:13.

**Qué suma el material externo.**
- **Decisiones automatizadas:** el artículo 20 de la ley 25.326 ya prohíbe que una decisión judicial o administrativa que implique apreciar el comportamiento humano se base solo en un perfil automatizado ([InfoLEG](https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/texact.htm)).
- **Multas:** la Resolución AAIP 126/2024 mantiene la escala de $1.000 a $100.000, permite multiplicarla por acumulación y derogó las resoluciones 240/22 y 244/22 ([Res. 126/2024](https://servicios.infoleg.gob.ar/infolegInternet/anexos/395000-399999/399750/norma.htm)).
- **Reforma:** según el sitio del diputado Yeza, los proyectos del Poder Ejecutivo de 2017 y 2023 perdieron estado parlamentario. En 2025 y 2026 hay proyectos de Carro (1948-D-2025), Doñate (644-S-2025), Yeza (1751-D-2026) y Rossi (3397-D-2026). El de Rossi, presentado el 16/07/2026, reproduce el de 2023, con multas del 2% al 4% de la facturación global, aviso de brechas en 72 horas y revisión humana de decisiones automatizadas ([abogados.com.ar, 05/08/2026](https://abogados.com.ar/index.php/nuevo-proyecto-de-ley-de-proteccion-de-datos-personales/39762)). El sitio de Yeza lo promueve el propio diputado y todavía cita la resolución de multas derogada ([leydedatospersonales.tech](https://leydedatospersonales.tech/)). La Unión Europea renovó la adecuación de Argentina el 15/01/2024, según ese mismo sitio.
- **Fuera de Argentina:** la AI Act es la referencia si tu sistema llega a la Unión Europea (sección 1), y Brasil tiene multas de hasta el 2% de la facturación con tope de 50 millones de reales.

**Cómo implementarlo.** En el práctico, cuando analices el consentimiento, citá el artículo y no "la ley dice": consentimiento (artículo 5), datos sensibles (artículo 7), decisiones automatizadas (artículo 20) y sanciones (artículo 31). Y si mencionás la reforma, decí que es un proyecto, con número y fecha.

---

## Críticas y límites

1. **Casos contados de memoria, con errores que se repiten.** Es normal en una clase oral, pero cinco casos clásicos salieron con un dato cambiado (Amazon, Google y el Congreso, PULSE, los 30.000 €, GPT-3). Para una materia que enseña a desconfiar de los datos, conviene que las diapositivas lleven la fuente de cada caso; la tabla de la sección 1 puede ir al lado del apunte.
2. **La equidad se queda en COMPAS y en Estados Unidos.** El ejemplo central de métricas es COMPAS, y los casos de daño son casi todos de Estados Unidos o Europa. Hay casos argentinos documentados (el reconocimiento facial porteño, el caso de Córdoba) que permitirían hacer el mismo ejercicio con datos o con fallos locales.
3. **Falta el teorema detrás del "no se puede maximizar todas".** La clase lo dice bien pero sin nombrar a Chouldechova ni a Kleinberg y otros, y remite a un libro que no se nombra. Sin la demostración, el estudiante puede creer que es un problema de su modelo y no una propiedad matemática.
4. **No hay herramientas de producción.** La notebook calcula todo a mano, lo que es bueno para entender, pero no muestra Fairlearn, AIF360 ni el informe de Aequitas, que son lo que se usa en un equipo real. La sección 3 cubre ese hueco.
5. **La reflexión no tiene un "freno".** La autoetnografía y los escenarios de daño ayudan a ver problemas, pero el curso no propone un artefacto (un registro de riesgos, una compuerta, una persona responsable) que obligue a actuar. El propio estudio de Benotti y Blackburn muestra que, sin revisión, solo el 23% de las secciones de ética habla de grupos vulnerables y el 20% son descargos.
6. **Regulación poco actualizada en lo internacional.** La clase menciona la AI Act y "poca regulación en Latinoamérica", pero no el Digital Omnibus, el Convenio 108+ como tratado pendiente de vigencia, ni el derecho a explicación que ya aplicaron tribunales europeos.
7. **Conflictos de interés que conviene decir en voz alta.** EDIA y el estudio sobre secciones de ética son de las propias docentes, y las dos cosas son buenas, pero el estudiante debería saberlo. Del lado de las fuentes externas: Anthropic habla de su producto, CELS y Civio son parte en sus casos, ACLU, Amnesty y Access Now hacen incidencia, ProPublica la financia una fundación con una herramienta competidora de COMPAS, Holistic AI vende servicios, y los sitios sobre la reforma de la ley son de su autor o de estudios jurídicos.
8. **El enfoque depende de la buena voluntad.** "Aportar nuestro granito de arena" C2P2 1:37:50 es honesto, pero si el equipo o quien decide no quiere frenar, la reflexión individual no alcanza. Es justo el punto que ataca el análisis adversario.
9. **Límites de esta revisión.**
    - La página de ISO 42001, la de la autoridad de datos neerlandesa, la LGPD y las preguntas frecuentes del panel de la ONU no cargaron en el lector web; las leí con `curl`. La declaración del Secretario General de la ONU sobre los nombramientos no cargó (pide JavaScript).
    - No abrí el boletín oficial de Córdoba; leí el artículo 36 de la ley 10.618 en un sitio que consolida leyes.
    - El premio a mejor paper de "Men also like shopping", las guías Ada y Grace, la participación de las docentes en EDIA y el ILIA los vi solo en resultados de búsqueda.
    - Lo del Digital Omnibus y el plazo del 02/12/2026 lo leí en una fuente secundaria (CPD), no en el reglamento.
    - No verifiqué el 90% de financiamiento militar del ICT, el caso del detector de somnolencia, el estudio de la copa de vino, la cifra del 30% de error en salud, el dato de los hispanos en COMPAS, la nota del futbolista ni la serie hasta 2024 de secciones de ética.
    - De varios papers (Chouldechova, Kleinberg y otros, PULSE, Jobin y otros) leí el resumen y no el paper completo.
    - Corrí el ejemplo de Fairlearn y la compuerta en el box; la plantilla de documentación no tiene nada que correr.

---

## Análisis adversario

> Cómo leer esta sección: pongo el enfoque de la materia contra la alternativa más fuerte que encontré, presentada en su mejor versión. La idea no es desarmar la materia, sino ver en qué contextos conviene y en cuáles no. Solo cito fuentes que abrí el 02/10/2026.

**La tesis, en dos oraciones.** La materia sostiene que la ética de un sistema de ciencia de datos se construye en el equipo que lo hace: cada persona arma su propia definición de ética, se pregunta quién se beneficia y quién se daña, formaliza escenarios de daño, documenta los datos y mide los errores por grupo. Las herramientas técnicas (data statements, métricas desagregadas, mitigación de sesgos) sirven a esa reflexión, y el aporte de cada profesional es "nuestro granito de arena" C2P2 1:37:50.

### La alternativa más fuerte: cumplimiento y gestión de riesgos primero

**Qué propone.** En vez de partir de la reflexión del equipo, partir de un proceso institucional obligatorio: clasificar el sistema según su riesgo (como hace la AI Act), adoptar un sistema de gestión de IA (ISO/IEC 42001) o un marco de gestión de riesgos (NIST AI RMF), hacer evaluaciones de impacto, asignar responsables con nombre y cargo, y dejar que auditorías, autoridades de datos y tribunales controlen. La versión seria no dice "la ética no importa", sino "la ética que depende de la buena voluntad de cada equipo no escala; hay que convertirla en obligaciones verificables".

**Qué dice el curso sobre esta alternativa.** La materia no la descarta: dedica un bloque a la ley 25.326 porque los estudiantes lo pidieron C1P1 21:55, discute que una cosa es que la ley exista y otra que se cumpla C1P1 51:59 y cierra con la AI Act y la "poca" regulación latinoamericana C2P2 1:37:13. Pero distingue ética de regulación y pone el centro en la ética personal y de equipo. En 2020, Laura lista entre los trucos para que nada cambie el de los "vacíos legales": agarrarse de la letra de la ley y no de su espíritu 2020-Barreras 9:45, 2020-Barreras 10:01. Es una crítica justa al cumplimiento mínimo, pero no a la versión fuerte de la alternativa.

**Por qué elegí esta.** Es la que discute la premisa de la materia (que la ética vive en el equipo), es la que efectivamente adoptan las organizaciones (según el AI Index 2026, el 60% cita el RGPD, el 36% ISO 42001 y el 33% NIST AI RMF como influencias en sus prácticas) y tiene casos donde la ley, y no la reflexión, fue lo que frenó un sistema. Otras alternativas que consideré:
- **Las herramientas técnicas de equidad como solución.** Medir y mitigar con Fairlearn o AIF360 en vez de reflexionar. No es la contraria más fuerte porque sus propios autores la rechazan: la portada de Fairlearn dice que la equidad "is sociotechnical" y que no se reduce a correr código ([fairlearn.org](https://fairlearn.org/)), y la materia ya enseña las métricas.
- **El rechazo o la abolición.** La crítica de que las métricas de equidad legitiman sistemas dañinos y que a veces la respuesta correcta es no construirlos. El Feminist Data Manifest-No rechaza "any code of phony 'ethics' and false proclamations of transparency that are wielded as cover" y quiere que "no" sea una opción real ([Manifest-No](https://www.manifestno.com/)). Es la crítica moral más fuerte, y el caso de Ámsterdam la respalda, pero no es un proceso alternativo para quien tiene que entregar un sistema; la incorporo al híbrido como compuerta.

### La alternativa en su mejor versión

**Quién la defiende y qué dice.**
- **La Unión Europea**, con la AI Act: obligaciones por nivel de riesgo, transparencia obligatoria para la IA generativa desde el 02/08/2026 (artículo 50) y multas de hasta 15 millones de euros o el 3% de la facturación por esa parte ([artículo 50](https://artificialintelligenceact.eu/article/50/)).
- **NIST**, con el AI RMF 1.0, gratuito y con un perfil para IA generativa ([NIST](https://www.nist.gov/itl/ai-risk-management-framework)).
- **ISO e IEC**, con la norma 42001:2023, certificable ([ISO](https://www.iso.org/standard/42001)).
- **Las autoridades de datos y los tribunales**, que ya aplican el derecho de datos a sistemas automatizados.

**Qué evidencia la respalda.**
- **La ley frenó lo que la reflexión no frenó.** En la Ciudad de Buenos Aires, un juez declaró inconstitucional el reconocimiento facial y la Cámara lo confirmó, con condiciones concretas para reactivarlo (órganos de control, estudio de impacto diferencial, publicidad) ([CELS](https://www.cels.org.ar/web/2023/04/confirman-la-inconstitucionalidad-del-uso-del-sistema-de-reconocimiento-facial/)). En Ámsterdam, un tribunal obligó a Uber a explicar la lógica de sus desactivaciones automatizadas, con multa diaria ([ECLI:NL:GHAMS:2023:793](https://www.lexboost.com/rechtspraak/ECLI:NL:GHAMS:2023:793)). En España, el Supremo ordenó abrir el código de BOSCO ([Civio](https://civio.es/novedades/2025/09/17/civio-abre-camino-en-la-transparencia-algoritmica-el-supremo-condena-al-gobierno-a-entregar-el-codigo-fuente-de-bosco/)).
- **Hay consecuencias.** La autoridad neerlandesa multó con 2,75 millones de euros a la administración tributaria por usar la doble nacionalidad, y el Estado paga 30.000 € de compensación a cada familia afectada ([Autoriteit Persoonsgegevens](https://www.autoriteitpersoonsgegevens.nl/actueel/boete-belastingdienst-voor-discriminerende-en-onrechtmatige-werkwijze); [Herstel Toeslagen](https://herstel.toeslagen.nl/herstelregelingen/catshuisregeling/)).
- **La reflexión voluntaria es despareja.** En ACL 2021, solo el 15,7% de los artículos tenía sección de ética, y de esas, solo el 23% hablaba de grupos vulnerables; los artículos que pasaron por revisión ética discutían más los daños ([Benotti y Blackburn, 2022](https://aclanthology.org/2022.emnlp-main.299/)). Es decir, una instancia externa obligatoria mejoró lo que la buena voluntad no garantizaba.
- **Asigna responsabilidad.** Responde a los trucos que lista Laura ("los datos son así", "lo arreglamos cuando pase"): un proceso con responsables firmantes hace más difícil lavarse las manos.

**Qué evidencia la contradice.**
- **El caso neerlandés pasó con reglas.** El RGPD rige desde 2018 y la ley neerlandesa de datos ya existía; según la propia autoridad, los datos de doble nacionalidad debían borrarse en enero de 2014 y en mayo de 2018 seguían registrados para 1,4 millones de personas. La multa llegó en diciembre de 2021, años después del daño.
- **Ámsterdam siguió el manual y falló igual.** Según MIT Technology Review y Lighthouse Reports, el sistema Smart Check de Ámsterdam se diseñó desde 2019 con un modelo explicable (una explainable boosting machine sobre 15 variables), se probó por sesgos y se reponderó cuando discriminaba a solicitantes no neerlandeses y a hombres. En el piloto real (de la primavera a noviembre de 2023, unas 1.600 solicitudes) marcó a más personas, no fue mejor que el personal y el sesgo se invirtió (contra neerlandeses y mujeres, y contra quienes tenían hijos). El consejo de participación se oponía desde 2022, porque el fraude es cerca del 3% de las solicitudes. La ciudad lo frenó a fines de noviembre de 2023, después de gastar unos 500.000 € más 35.000 € en Deloitte. El proceso manual también tenía sesgos ([MIT Technology Review, 11/06/2025](https://www.technologyreview.com/2025/06/11/1118233/amsterdam-fair-welfare-ai-discriminatory-algorithms-failure/); [Lighthouse Reports](https://www.lighthousereports.com/investigation/the-limits-of-ethical-ai/)).
- **El cumplimiento llega tarde y cambia de fecha.** El Digital Omnibus postergó las obligaciones de alto riesgo de la AI Act al 02/12/2027 y al 02/08/2028 ([CPD](https://www.cpduk.co.uk/news/deadline-moved-and-duty-did-not-ai-act-transparency-obligations-after-digital-omnibus)), y en Argentina las multas siguen en una escala de $1.000 a $100.000.
- **Adopción no es efectividad.** Que el 36% de las organizaciones cite ISO 42001 dice cuánto se usa, no cuánto daño evita ([AI Index 2026](https://hai.stanford.edu/ai-index/2026-ai-index-report/responsible-ai)).

### Comparación directa

| Criterio | A: reflexión ética en el equipo (la materia) | B: cumplimiento y gestión de riesgos primero |
|---|---|---|
| Costo | Bajo: tiempo del equipo y herramientas gratuitas (Fairlearn, Aequitas, EDIA, plantillas). | Alto: asesoramiento legal, auditorías, personal dedicado y certificación; solo la norma ISO 42001 cuesta 225 francos suizos, aunque NIST AI RMF es gratuito. |
| — | Baja a media: un data statement, métricas desagregadas y una discusión guiada. | Alta: sistema de gestión, roles, registros, evaluaciones de impacto, auditorías y seguimiento normativo en cada jurisdicción. |
| Tiempo hasta obtener valor | Días: en una semana tenés la ficha de datos y el MetricFrame del práctico. | Meses: implementar un sistema de gestión y certificarlo; el control judicial llega años después del daño. |
| Riesgo | Depende de la buena voluntad y de la composición del equipo; quien decide puede ignorarla; no deja un responsable formal. | Cumplimiento de fachada (marcar casillas), falsa sensación de seguridad, y casos como el neerlandés y el de Ámsterdam, donde las reglas o el manual no evitaron el daño. |
| Madurez | Métodos publicados desde 2018 y 2019 (datasheets, data statements, model cards) y muy citados, pero sin estándar ni obligación. | Marcos jóvenes pero con respaldo institucional: NIST AI RMF de 2023, ISO 42001 de diciembre de 2023, AI Act en vigor por etapas hasta 2028. |
| Evidencia disponible | Casos y estudios de documentación; el estudio de Benotti y Blackburn muestra que la reflexión voluntaria es despareja. | Cifras de adopción (AI Index) y casos donde la ley frenó un sistema (CABA, Uber, BOSCO), pero sin estudios que midan si los marcos reducen daños. |
| Tipo de equipo/contexto | Equipos chicos, academia, startups, el práctico, y países como Argentina donde la regulación es débil; etapas tempranas de diseño. | Organizaciones grandes, sectores regulados (finanzas, salud, sector público), productos para la Unión Europea y sistemas de alto riesgo. |

### Dónde gana la alternativa

- **Cuando el equipo no quiere o no puede frenar.** Un proceso con responsables firmantes y auditoría externa no depende de la conciencia de nadie.
- **Cuando hay mucho en juego.** En beneficios sociales, justicia o crédito, las personas afectadas necesitan derechos exigibles (explicación, revisión humana, impugnación), no buenas intenciones.
- **Cuando vendés a la Unión Europea.** El artículo 50 ya se aplica, con multas reales.
- **Para dejar rastro.** Un registro de riesgos y una evaluación de impacto sirven de prueba cuando algo sale mal, cosa que una discusión de equipo no deja.

### Dónde pierde

- **Velocidad y costo.** Para un equipo chico o un práctico, un sistema de gestión certificable es desproporcionado.
- **Lo que todavía no está en la ley.** Laura lo dice en 2020: hay sesgos emergentes que hoy no conocemos 2020-Barreras 13:37, 2020-Barreras 14:01. Un proceso de cumplimiento mira lo que la norma ya nombra; la reflexión es lo que encuentra lo nuevo.
- **Argentina hoy.** Con multas de hasta $100.000 y la reforma sin aprobar, el "cumplimiento primero" tiene pocos dientes locales.
- **El caso de Ámsterdam.** Hacer todo "bien" según el manual no evitó el sesgo; lo que faltó fue escuchar a quienes decían que no hacía falta el sistema.

### Cómo decidir

**Elegí A (reflexión ética en el equipo, la materia) si** sos un equipo chico, estás en la academia o en una startup, estás en la etapa de diseño o de exploración de datos, el sistema no toma decisiones de alto impacto sobre personas, o trabajás en Argentina sin clientes europeos y necesitás resultados en días.

**Elegí B (cumplimiento y gestión de riesgos primero) si** tu organización es grande o está regulada (finanzas, salud, sector público), el sistema decide sobre derechos (beneficios, crédito, empleo, justicia, vigilancia), vendés o desplegás en la Unión Europea, o necesitás que la responsabilidad quede asignada y auditable aunque cambie el equipo.

**Un híbrido posible (sugerencia).**
1. Empezá como la materia: escribí el data statement o la ficha de la sección 5 y formalizá los escenarios de daño con el equipo, sumando una persona que no conozca el dataset.
2. Convertí cada escenario de daño en una fila del registro de riesgos de la sección 6, con severidad, métrica, umbral y responsable.
3. Medí con Fairlearn o Aequitas (sección 3) y elegí la métrica de equidad por escrito, aceptando lo que dicen los teoremas de la sección 4.
4. Poné la compuerta de "no desplegar" en la integración continua, y escribí antes de entrenar qué resultado te haría abandonar el sistema: esa es la parte del rechazo que el Manifest-No y el caso de Ámsterdam piden.
5. Si el sistema es de alto impacto o va a la Unión Europea, mapeá ese registro a NIST AI RMF o ISO 42001 y a las obligaciones de la AI Act; no empieces de cero, porque la reflexión ya te dio el inventario.
6. Escuchá a las personas afectadas antes del piloto, no después: en Ámsterdam el consejo de participación tenía razón desde 2022.

**Veredicto.** Para el práctico y para la mayoría de los equipos argentinos, el enfoque de la materia es el punto de partida correcto: es barato, rápido y es lo que encuentra los daños que ninguna norma nombró todavía. Pero la evidencia (el estudio de secciones de ética, los fallos de CABA, Uber y BOSCO) dice que la reflexión voluntaria es despareja y que lo que frenó sistemas dañinos fueron obligaciones exigibles. Y los casos neerlandés y de Ámsterdam dicen que ni la reflexión ni el cumplimiento alcanzan si "no construirlo" no está sobre la mesa. Lo más sensato es el híbrido: reflexión para encontrar los daños, un registro con responsables para que no se pierdan, y una compuerta con la opción de no desplegar.

---

## Material para seguir

**En español y desde la región**
- [EDIA, de Fundación Vía Libre](https://ia.vialibre.org.ar/): la herramienta para explorar sesgos en embeddings y modelos de lenguaje en español sin programar (la hicieron con participación de las docentes).
- [Caja de Herramientas Humanísticas, de GIFT](https://proyectoguia.lat/wp-content/uploads/2020/05/Caja-de-herramientas-Humanistas.pdf): los casos que resume el video 2020-Caja, con el desarrollo filosófico completo.
- [Radiografía normativa, de Access Now (2024)](https://www.accessnow.org/press-release/reporte-inteligencia-artificial-en-america-latina/): el mapa de qué se regula y qué no en ocho países de la región.
- [Fallo sobre el reconocimiento facial porteño, según CELS](https://www.cels.org.ar/web/2023/04/confirman-la-inconstitucionalidad-del-uso-del-sistema-de-reconocimiento-facial/): el mejor caso argentino para discutir sesgo, vigilancia y control judicial.
- [Civio y el código de BOSCO](https://civio.es/novedades/2025/09/17/civio-abre-camino-en-la-transparencia-algoritmica-el-supremo-condena-al-gobierno-a-entregar-el-codigo-fuente-de-bosco/): cómo una ONG consiguió que un tribunal obligue a abrir un algoritmo público.
- [Declaración de Montreal](https://montrealdeclaration-responsibleai.com/the-declaration/): los 10 principios que recomienda el video de barreras, hoy también en español.

**Papers fundamentales**
- [Friedman y Nissenbaum (1996), "Bias in Computer Systems"](https://nissenbaum.tech.cornell.edu/papers/biasincomputers.pdf): la definición de sesgo que usa el práctico y las tres categorías (preexistente, técnico, emergente).
- [Chouldechova (2017)](https://arxiv.org/abs/1703.00056) y [Kleinberg, Mullainathan y Raghavan (2016)](https://arxiv.org/abs/1609.05807): por qué no se pueden igualar todas las métricas a la vez.
- [Zhao y otros (2017), "Men also like shopping"](https://aclanthology.org/D17-1323/): el paper de amplificación que lee Laura en clase.
- [Benotti y Blackburn (2022)](https://aclanthology.org/2022.emnlp-main.299/): qué dicen (y qué no) las secciones de ética de los artículos de PLN; útil para escribir la tuya.
- [Jobin, Ienca y Vayena (2019)](https://arxiv.org/abs/1906.11668): el mapa de guías de ética de IA del que salen las cinco áreas del video de barreras.

**Documentación**
- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010): las preguntas para documentar un dataset, ordenadas por etapa.
- [Data Statements (Bender y Friedman, 2018)](https://aclanthology.org/Q18-1041/): la metodología del práctico, pensada para datos de lenguaje.
- [Model Cards (Mitchell y otras, 2019)](https://arxiv.org/abs/1810.03993): cómo reportar un modelo con evaluación por grupo e intersección.

**Herramientas**
- [Fairlearn](https://fairlearn.org/): métricas desagregadas y mitigación, con guías que insisten en el lado social del problema.
- [AIF360](https://github.com/Trusted-AI/AIF360): una alternativa con muchas métricas y algoritmos de mitigación.
- [Aequitas](https://raw.githubusercontent.com/dssg/aequitas/master/README.md): el informe de sesgo y la demo de COMPAS que usa la notebook de la materia.
- [holisticai](https://github.com/holistic-ai/holisticai): la biblioteca de donde la clase saca otros datasets (de una empresa de auditoría).

**Casos**
- [Machine Bias, de ProPublica](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing): el análisis de COMPAS con las cifras originales.
- [Amsterdam y Smart Check, en MIT Technology Review](https://www.technologyreview.com/2025/06/11/1118233/amsterdam-fair-welfare-ai-discriminatory-algorithms-failure/) y [Lighthouse Reports](https://www.lighthousereports.com/investigation/the-limits-of-ethical-ai/): el caso que muestra los límites de la "IA ética" bien hecha.
- [Amnesty sobre el caso neerlandés](https://www.amnesty.org/en/latest/news/2021/10/xenophobic-machines-dutch-child-benefit-scandal/): cómo la nacionalidad terminó siendo un factor de riesgo.
- [Reuters sobre el filtro de Amazon](https://www.reuters.com/article/us-amazon-com-jobs-automation-insight-idUSKCN1MK08G): el caso real, sin sanciones.
- [AI Index 2026, capítulo de IA responsable](https://hai.stanford.edu/ai-index/2026-ai-index-report/responsible-ai): las cifras de incidentes y de adopción de marcos.

**Regulación y gestión de riesgos**
- [Ley 25.326 (texto actualizado)](https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/texact.htm) y [Resolución AAIP 126/2024](https://servicios.infoleg.gob.ar/infolegInternet/anexos/395000-399999/399750/norma.htm): la base legal argentina y las multas vigentes.
- [Artículo 50 de la AI Act](https://artificialintelligenceact.eu/article/50/) y [el código de prácticas de la Comisión](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content): lo que se exige hoy sobre contenido generado.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework): el marco gratuito para ordenar la gestión de riesgos.
- [Feminist Data Manifest-No](https://www.manifestno.com/): la crítica de fondo a la "ética de fachada" y la defensa de poder decir que no.
