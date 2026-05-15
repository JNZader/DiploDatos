# 10 — Preguntas guía para estudiar

Estas preguntas no son un examen: son un espejo. Si podés responderlas en voz alta con ejemplos concretos de los TPs, entendés. Si balbuceás o decís "sí, más o menos", hay un hueco.

---

## Sobre Python y pandas

1. ¿Qué diferencia hay entre `df['col'].mean()` y `df.groupby('grupo')['col'].mean()`? ¿En qué ejercicio de TP1 usaste ambas?
2. ¿Por qué en TP1 tuviste que hacer `.str.split(",").explode()` con la columna de lenguajes? ¿Qué problema de formato resolviste?
3. Si una columna numérica está como `object` en pandas, ¿qué puede estar pasando y cómo lo arreglás?

## Sobre EDA y tipos de datos

4. ¿Cuál es la unidad de análisis de la encuesta Sysarmy? ¿Qué representa cada fila?
5. ¿Por qué `profile_studies_level` es ordinal y `work_province` es nominal? ¿Qué operaciones podés hacer con una que no podés con la otra?
6. Si tu pregunta es "¿qué lenguaje paga más?" y no filtrás por dedicación, ¿qué confusor estás ignorando?
7. ¿Qué tres problemas de calidad detectaste en TP1 antes de analizar los lenguajes?

## Sobre probabilidad

8. ¿Cuál es la diferencia entre P(salario alto | sabe Python) y P(sabe Python | salario alto)? ¿Por qué no son lo mismo?
9. En TP1 calculaste "lift" para varios lenguajes. ¿Qué significa un lift de +40% para Go en el umbral de $3M?
10. Si P(A|B) = P(A), ¿qué podés decir sobre la relación entre A y B? ¿Cómo lo verificaste en TP1 Ejercicio 2c?

## Sobre descriptiva y visualización

11. ¿Por qué en TP1 ordenaste los lenguajes por mediana y no por media en el boxplot?
12. Dos lenguajes tienen la misma mediana pero distinto IQR. ¿Qué podés inferir sobre sus distribuciones?
13. ¿Qué ventaja tiene un violinplot sobre un boxplot? ¿Y qué desventaja?
14. En TP1 Ejercicio 2b, la correlación entre bruto y neto fue r ≈ 0.95. ¿Eso significa que uno causa al otro? ¿Por qué?
15. ¿Qué es la paradoja de Simpson y cómo se relaciona con el concepto de "relación marginal vs condicional"?

## Sobre estimación e inferencia

16. ¿Cuál es la diferencia entre desvío estándar y error estándar? Usá números de TP2 para explicarlo.
17. ¿Por qué el error estándar de la diferencia de medias es la raíz de una suma de varianzas y no la resta?
18. En TP2, el IC 95% para la diferencia de medias fue aproximadamente [$276.000, $481.000]. ¿Qué significa eso en términos del procedimiento? ¿Por qué no decimos "hay 95% de probabilidad de que la diferencia real esté ahí"?
19. Si duplicás el tamaño muestral de ambos grupos, ¿qué le pasa al ancho del IC (aproximadamente)?
20. ¿Por qué usaste Welch en TP2 en lugar de un t-test clásico con varianzas iguales?

## Sobre test de hipótesis

21. Plantea H0 y H1 de TP2 Ejercicio 2 con palabras propias. ¿Por qué es bilateral?
22. ¿Qué decisión tomás si p-valor = 0.03 y α = 0.05? ¿Y si p-valor = 0.03 pero Cohen's d = 0.05?
23. ¿Cuál es la diferencia entre error tipo I y error tipo II? ¿Cuál controla α?
24. ¿Por qué el rechazo de H0 en TP2 no demuestra que el género "cause" la diferencia salarial?
25. ¿Qué son los chequeos de robustez y por qué los hiciste en TP2? ¿Qué resultados obtuviste?
26. Explicá qué es la potencia de un test y por qué en TP2 hiciste una simulación Monte Carlo (método que usa números aleatorios repetidos para estimar probabilidades) para estimarla.
27. ¿Qué es el tamaño de efecto y por qué no alcanza con mirar solo el p-valor?

## Sobre visualización y comunicación

28. ¿Qué diferencia hay entre el boxplot de TP1 Ejercicio 1 y el errorbar de TP2 Ejercicio 3? ¿Por qué cada uno era adecuado para su objetivo?
29. Si tuvieras que presentar el resultado de TP2 a un CEO sin formación estadística, ¿qué elementos del gráfico cambiarías o agregarías?
30. ¿Qué principio de Knaflic o Cairo usaste en TP2 Ejercicio 3 al diseñar el gráfico de comunicación?
31. ¿Por qué un gráfico 3D es generalmente una mala idea para comparar magnitudes?

## Sobre limpieza y calidad

32. Describí el pipeline de limpieza de TP2 paso a paso. ¿Por qué ese orden y no otro?
33. ¿Eliminarías automáticamente un salario de $8.000.000? ¿Qué preguntarías antes de decidir?
34. ¿Qué sesgos de la encuesta Sysarmy persisten incluso después de una limpieza impecable?
35. ¿Por qué filtraste por `work_dedication == "Full-Time"` en ambos TPs?

## Sobre el curso en general

36. ¿Cómo se conecta el EDA de TP1 con la inferencia de TP2? ¿Por qué no podés saltear el EDA?
37. Si un alumno te dice "mi p-valor es 0.001, entonces mi conclusión es definitiva", ¿qué le respondés?
38. ¿Qué limitaciones metodológicas reconocerías antes de presentar los resultados de TP2 como "la brecha salarial en la industria IT argentina"?
39. ¿Cómo relacionás el concepto de "modelo" (Bonamente) con la construcción de un intervalo de confianza?
40. ¿Qué cambiarías en el pipeline de TP2 si la encuesta fuera obligatoria en lugar de voluntaria?

---

**Cómo usar estas preguntas**

- Respondelas en voz alta o por escrito.
- Si una pregunta te deja en blanco, volvé al archivo correspondiente y releé la sección de "Intuición".
- Si podés responderlas todas con ejemplos numéricos concretos de los TPs, estás listo.

**Próximo paso**: `11-bibliografia.md`
