#!/usr/bin/env python3
"""
Rewrite auto-challenges to new multi-language format.
- 58 challenges → new template with 4-language CodeTabs
- 85 challenges → draft: true
"""
import os
import sys
import re
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.solutions_db import lookup as db_lookup, generate_generic

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DIR = os.path.join(BASE, "src/content/auto-challenges")

LANGUAGES = ["python", "javascript", "java", "typescript"]

# ── 58 keepers ──────────────────────────────────────────────
KEEP = {
    # INICIACIÓN (19)
    "guia-plus-reto-inicial-01-suma-de-digitos",
    "guia-plus-reto-inicial-06-par-o-impar",
    "guia-plus-reto-inicial-07-invertir-palabra",
    "guia-detector-de-palindromos",
    "guia-contador-de-vocales",
    "guia-maximo-de-tres-numeros",
    "guia-verificador-de-edad",
    "guia-el-contador-de-pasos",
    "guia-lista-de-compras",
    "guia-tabla-de-multiplicar",
    "guia-el-reclutador-de-la-banda",
    "guia-generador-de-nicknames",
    "guia-plus-reto-inicial-10-celsius-a-kelvin",
    "guia-plus-reto-inicial-11-area-de-triangulo",
    "guia-plus-reto-inicial-15-ano-bisiesto",
    "guia-plus-reto-inicial-18-precio-con-iva",
    "guia-plus-reto-inicial-19-descuento-simple",
    "guia-plus-reto-inicial-24-raiz-cuadrada-redondeada",
    "guia-plus-reto-inicial-30-limpieza-de-texto",

    # INTERMEDIO (18)
    "guia-fibonacci-recursivo",
    "guia-ordenamiento-por-burbuja",
    "guia-consumo-de-api-mock",
    "guia-gestion-de-inventario-oop",
    "guia-juego-de-adivinar-numero",
    "guia-filtro-de-spam-por-keywords",
    "guia-cifrado-cesar-basico",
    "guia-manejador-de-contexto-files",
    "guia-conversion-de-monedas",
    "guia-eliminar-duplicados",
    "guia-buscador-de-minas-logica",
    "guia-plus-reto-intermedio-03-simulador-de-pila-stack",
    "guia-plus-reto-intermedio-04-colas-queue-basicas",
    "guia-plus-reto-intermedio-10-transposicion-de-matrices",
    "guia-plus-reto-intermedio-12-procesador-de-json",
    "guia-plus-reto-intermedio-15-juego-de-palabras-anagramas",
    "guia-plus-reto-intermedio-30-manejador-de-historial-undo",
    "guia-plus-reto-intermedio-38-validador-de-isbn",

    # AVANZADO (21)
    "guia-plus-reto-avanzado-02-grafos-bfs-dfs",
    "guia-plus-reto-avanzado-03-optimizacion-de-rutas-greedy",
    "guia-plus-reto-avanzado-04-manejador-de-hilos-threading",
    "guia-plus-reto-avanzado-05-asyncio-para-scrapers",
    "guia-plus-reto-avanzado-06-middleware-de-seguridad",
    "guia-plus-reto-avanzado-07-inyector-de-dependencias",
    "guia-plus-reto-avanzado-08-patron-strategy-en-apis",
    "guia-plus-reto-avanzado-09-cache-decorator-memoization",
    "guia-plus-reto-avanzado-10-validador-de-esquema-json",
    "guia-compresor-de-cadenas-rle",
    "guia-decorador-de-medicion-de-tiempo",
    "guia-motor-de-busqueda-binaria",
    "guia-jwt-generator-manual",
    "guia-optimizacion-de-consultas",
    "guia-patron-singleton-logger",
    "guia-consistencia-de-base-de-datos",
    "guia-plus-reto-avanzado-01-arboles-binarios-de-busqueda",
    "guia-plus-reto-avanzado-11-simulador-de-blockchain",
    "guia-plus-reto-avanzado-19-compresion-huffman",
    "guia-plus-reto-avanzado-20-diff-de-archivos-levenshtein",
    "guia-plus-reto-avanzado-14-worker-queue-con-prioridad",
}

# ── GEN expanded content ────────────────────────────────────
# For the 19 GEN challenges that need content expansion
GEN = {
    "guia-plus-reto-inicial-10-celsius-a-kelvin": {
        "desc": "Convierte grados Celsius a Kelvin usando la fórmula K = C + 273.15. Es la conversión más básica entre escalas de temperatura y un excelente punto de partida para entender funciones de transformación directa.",
        "p1": "**Análisis del problema:** La conversión de Celsius a Kelvin es directa: suma 273.15 al valor en Celsius. Matemáticamente: K = C + 273.15. Es una función pura y determinista. **Ejemplo concreto:** 0°C → 273.15 K, 100°C → 373.15 K. **Edge cases:** cero absoluto (-273.15°C da 0 K), valores negativos, entrada no numérica.",
        "p2": "**Implementación:** La solución es una línea. En todos los lenguajes, se define una función que recibe un número y devuelve el resultado de sumarle 273.15. Se debe validar que la entrada sea numérica y, en lenguajes tipados, definir el tipo correcto.",
        "p3": "**Complejidad:** O(1) tiempo y O(1) espacio. Es una operación aritmética simple sin iteraciones ni estructuras auxiliares. **Aplicaciones:** sistemas de monitoreo de temperatura, APIs meteorológicas, conversión de unidades en datos científicos.",
        "big_o_time": "O(1)", "big_o_space": "O(1)",
        "tests": "0 | 273.15\n100 | 373.15\n-273.15 | 0\n25 | 298.15",
    },
    "guia-plus-reto-inicial-11-area-de-triangulo": {
        "desc": "Calcula el área de un triángulo dados su base y altura usando la fórmula (base × altura) / 2. Un ejercicio clásico de geometría computacional.",
        "p1": "**Análisis del problema:** El área de un triángulo se calcula como base × altura / 2. Es una fórmula directa sin dependencias. **Ejemplo concreto:** base=3, altura=4 → 3×4/2 = 6. **Edge cases:** base o altura negativa (no válido geométricamente), valores cero (área 0), valores muy grandes (desbordamiento).",
        "p2": "**Implementación:** Se define una función que toma base y altura, valida que sean positivas, aplica la fórmula y devuelve el resultado. En lenguajes con tipado estático, se usan tipos float/double.",
        "p3": "**Complejidad:** O(1) tiempo y espacio. **Aplicaciones:** cálculo de materiales en construcción, gráficos por computadora, problemas de optimización geométrica.",
        "big_o_time": "O(1)", "big_o_space": "O(1)",
        "tests": "3, 4 | 6\n5, 5 | 12.5\n0, 5 | 0\n10, 2 | 10",
    },
    "guia-plus-reto-inicial-15-ano-bisiesto": {
        "desc": "Determina si un año es bisiesto según las reglas del calendario gregoriano: divisible entre 4, excepto si es divisible entre 100, a menos que sea divisible entre 400.",
        "p1": "**Análisis del problema:** Un año es bisiesto si cumple: (divisible entre 4 Y no entre 100) O (divisible entre 400). Es una lógica booleana con tres condiciones. **Ejemplo concreto:** 2024 → sí (divisible entre 4, no entre 100), 1900 → no (divisible entre 100, no entre 400), 2000 → sí (divisible entre 400). **Edge cases:** años negativos (según convención), año 0, años muy grandes.",
        "p2": "**Implementación:** Se evalúa la condición compuesta: `(año % 4 == 0 and año % 100 != 0) or (año % 400 == 0)`. Es un clásico para practicar operadores lógicos y precedencia.",
        "p3": "**Complejidad:** O(1) tiempo y espacio. **Aplicaciones:** sistemas de calendario, cálculo de días entre fechas, planificación de eventos recurrentes.",
        "big_o_time": "O(1)", "big_o_space": "O(1)",
        "tests": "2024 | true\n2023 | false\n1900 | false\n2000 | true\n2400 | true",
    },
    "guia-plus-reto-inicial-18-precio-con-iva": {
        "desc": "Calcula el precio final de un producto aplicando un porcentaje de IVA. Dado el precio base y el porcentaje de IVA, devuelve el total.",
        "p1": "**Análisis del problema:** El IVA se calcula como precio_base × (porcentaje / 100) y se suma al base. **Ejemplo concreto:** precio=100, IVA=21% → total = 100 + 100×0.21 = 121. **Edge cases:** IVA 0%, IVA 100%, precio negativo, porcentaje negativo.",
        "p2": "**Implementación:** Función pura que recibe precio y porcentaje, calcula y devuelve el total. Se debe manejar precisión decimal para evitar errores de redondeo.",
        "p3": "**Complejidad:** O(1). **Aplicaciones:** sistemas POS, carritos de compra, facturación electrónica, cálculos contables.",
        "big_o_time": "O(1)", "big_o_space": "O(1)",
        "tests": "100, 21 | 121\n50, 10 | 55\n200, 0 | 200\n15.99, 7 | 17.1093",
    },
    "guia-plus-reto-inicial-19-descuento-simple": {
        "desc": "Aplica un descuento porcentual a un precio y devuelve el precio final. Similar al cálculo de IVA pero restando en vez de sumar.",
        "p1": "**Análisis del problema:** Descuento = precio × (porcentaje / 100). Precio final = precio - descuento. **Ejemplo concreto:** precio=100, descuento=15% → final = 100 - 15 = 85. **Edge cases:** descuento 0%, descuento 100%, precio negativo.",
        "p2": "**Implementación:** Una línea: `precio * (1 - descuento / 100)`. Importante: validar que el descuento esté entre 0 y 100.",
        "p3": "**Complejidad:** O(1). **Aplicaciones:** e-commerce, sistemas de promociones, liquidación de inventario.",
        "big_o_time": "O(1)", "big_o_space": "O(1)",
        "tests": "100, 15 | 85\n200, 50 | 100\n80, 0 | 80\n50, 100 | 0",
    },
    "guia-plus-reto-inicial-24-raiz-cuadrada-redondeada": {
        "desc": "Calcula la raíz cuadrada de un número y la redondea al entero más cercano. Introduce el uso de funciones matemáticas de la librería estándar.",
        "p1": "**Análisis del problema:** Se usa la función sqrt() de la librería matemática y luego round() para redondear. **Ejemplo concreto:** 10 → sqrt(10) ≈ 3.162 → redondeado → 3. **Edge cases:** número negativo (dominio inválido en reales), cero (0), números negativos muy grandes.",
        "p2": "**Implementación:** `round(sqrt(n))`. En lenguajes sin round integrado, se suma 0.5 y se trunca. Manejar excepción para números negativos.",
        "p3": "**Complejidad:** La función sqrt tiene complejidad O(log n) en implementaciones típicas (aproximación de Newton). **Aplicaciones:** procesamiento de señales, gráficos 3D, estadística.",
        "big_o_time": "O(log n)", "big_o_space": "O(1)",
        "tests": "10 | 3\n16 | 4\n25 | 5\n2 | 1\n0 | 0",
    },
    "guia-plus-reto-inicial-30-limpieza-de-texto": {
        "desc": "Limpia una cadena de texto eliminando caracteres no deseados: espacios extra, signos de puntuación, o caracteres especiales según configuración.",
        "p1": "**Análisis del problema:** La limpieza de texto consiste en aplicar transformaciones como eliminar espacios múltiples, signos de puntuación, o normalizar a minúsculas. **Ejemplo concreto:** '  HOLA   MUNDO!  ' → 'hola mundo'. **Edge cases:** cadena vacía, solo símbolos, caracteres Unicode/acentos.",
        "p2": "**Implementación:** Usar expresiones regulares para reemplazar patrones. En Python: `re.sub(r'[^a-z0-9\\s]', '', s.lower()).strip()` seguido de `re.sub(r'\\s+', ' ', s)`.",
        "p3": "**Complejidad:** O(n) tiempo, O(n) espacio donde n es la longitud del texto. **Aplicaciones:** sanitización de input de usuarios, preparación de datos para NLP, limpieza de logs.",
        "big_o_time": "O(n)", "big_o_space": "O(n)",
        "tests": "'  HOLA   MUNDO!  ' | 'hola mundo'\n'Python!!!' | 'python'\n'' | ''\n'  a  b  c  ' | 'a b c'",
    },
    "guia-plus-reto-intermedio-03-simulador-de-pila-stack": {
        "desc": "Implementa una pila (stack) con operaciones push, pop, peek y isEmpty. Estructura LIFO fundamental en informática.",
        "p1": "**Análisis del problema:** Una pila sigue el principio LIFO (Last In, First Out). Las operaciones básicas son: push (insertar), pop (eliminar y devolver el tope), peek (ver el tope sin eliminar), isEmpty. **Ejemplo concreto:** push(1), push(2), push(3), pop() → 3, peek() → 2. **Edge cases:** pop en pila vacía, push de null/None, capacidad máxima.",
        "p2": "**Implementación:** Usar una lista/array como almacenamiento subyacente. push → append, pop → pop, peek → [-1], isEmpty → len==0. Versión orientada a objetos con una clase Stack.",
        "p3": "**Complejidad:** Todas las operaciones: O(1) tiempo amortizado (con lista dinámica). O(n) espacio. **Aplicaciones:** historial de navegador, llamado de funciones (call stack), parseo de expresiones, algoritmo de retroceso (backtracking).",
        "big_o_time": "O(1)", "big_o_space": "O(n)",
        "tests": "push(1),push(2),pop() | 2\npush(5),peek() | 5\nisEmpty() | true\npush(3),pop(),pop() | error",
    },
    "guia-plus-reto-intermedio-04-colas-queue-basicas": {
        "desc": "Implementa una cola (queue) con operaciones enqueue, dequeue, front e isEmpty. Estructura FIFO fundamental.",
        "p1": "**Análisis del problema:** Una cola sigue el principio FIFO (First In, First Out). Operaciones: enqueue (insertar al final), dequeue (eliminar del frente), front (ver el frente), isEmpty. **Ejemplo concreto:** enqueue(1), enqueue(2), enqueue(3), dequeue() → 1, front() → 2. **Edge cases:** dequeue en cola vacía.",
        "p2": "**Implementación:** Usar collections.deque en Python, ArrayDeque en Java, o una lista con dos punteros. En JavaScript, un array con push/shift funciona pero es O(n) en shift. La versión con lista enlazada es eficiente.",
        "p3": "**Complejidad:** O(1) amortizado con deque/ArrayDeque. O(1) con lista enlazada. O(n) espacio. **Aplicaciones:** buffers de datos, impresión por lotes, BFS en grafos, sistemas de tickets.",
        "big_o_time": "O(1)", "big_o_space": "O(n)",
        "tests": "enqueue(1),enqueue(2),dequeue() | 1\nenqueue(5),front() | 5\nisEmpty() | true\nenqueue(3),dequeue(),dequeue() | error",
    },
    "guia-plus-reto-intermedio-10-transposicion-de-matrices": {
        "desc": "Transpone una matriz: intercambia filas por columnas. Si la entrada es una matriz M de tamaño m×n, la salida es M^T de tamaño n×m.",
        "p1": "**Análisis del problema:** La transposición convierte cada fila en columna. Dada M[i][j], la matriz transpuesta tiene M^T[j][i] = M[i][j]. **Ejemplo concreto:** [[1,2],[3,4]] → [[1,3],[2,4]]. **Edge cases:** matriz vacía, matriz 1×1, matriz no rectangular (irregular), matriz muy grande.",
        "p2": "**Implementación:** En Python: `zip(*matriz)` o list comprehension `[list(f) for f in zip(*m)]`. En otros lenguajes, dos bucles anidados intercambiando índices.",
        "p3": "**Complejidad:** O(n×m) tiempo y O(n×m) espacio. **Aplicaciones:** álgebra lineal, procesamiento de imágenes (rotación), bases de datos (pivot), gráficos 3D.",
        "big_o_time": "O(n×m)", "big_o_space": "O(n×m)",
        "tests": "[[1,2],[3,4]] | [[1,3],[2,4]]\n[[1]] | [[1]]\n[[1,2,3]] | [[1],[2],[3]]\n[] | []",
    },
    "guia-plus-reto-intermedio-12-procesador-de-json": {
        "desc": "Procesa datos en formato JSON: parsea, filtra por una condición y devuelve los resultados transformados. Simula una API de datos.",
        "p1": "**Análisis del problema:** Dado un string JSON que contiene una lista de objetos, se debe filtrar según una propiedad y devolver solo los campos solicitados. **Ejemplo concreto:** entrada='[{\"nombre\":\"A\",\"edad\":25},{\"nombre\":\"B\",\"edad\":17}]', min=18 → '[{\"nombre\":\"A\",\"edad\":25}]'. **Edge cases:** JSON vacío, campo faltante, tipo de dato incorrecto.",
        "p2": "**Implementación:** Parsear con json.loads (Python) o JSON.parse (JS). Filtrar con filter/condición y transformar con map. Devolver json.dumps/JSON.stringify.",
        "p3": "**Complejidad:** O(n) tiempo, O(n) espacio. **Aplicaciones:** ETL, APIs REST, procesamiento de configuraciones, almacenamiento NoSQL.",
        "big_o_time": "O(n)", "big_o_space": "O(n)",
        "tests": "'[{\"a\":1},{\"a\":2}]', 'a>1' | '[{\"a\":2}]'\n'[]', 'x' | '[]'\n'[{\"n\":\"x\"}]', 'n==\"x\"' | '[{\"n\":\"x\"}]'",
    },
    "guia-plus-reto-intermedio-15-juego-de-palabras-anagramas": {
        "desc": "Determina si dos palabras son anagramas (contienen las mismas letras en diferente orden). Ejemplo: 'listen' y 'silent' son anagramas.",
        "p1": "**Análisis del problema:** Dos palabras son anagramas si tienen exactamente los mismos caracteres con las mismas frecuencias. **Ejemplo concreto:** 'listen' → {l:1,i:1,s:1,t:1,e:1,n:1}, 'silent' → misma frecuencia → true. **Edge cases:** cadenas vacías (son anagramas), diferente longitud (false), mayúsculas (normalizar), caracteres acentuados.",
        "p2": "**Implementación:** Dos enfoques: 1) Ordenar las cadenas y comparar: `sorted(s1) == sorted(s2)`. 2) Contar frecuencias con un diccionario/hashmap: incrementar para s1, decrementar para s2, verificar que todos sean 0.",
        "p3": "**Complejidad:** Ordenar: O(n log n) tiempo, O(n) espacio. Con mapa de frecuencias: O(n) tiempo, O(1) espacio (solo 26 letras si son alfabéticas). **Aplicaciones:** juegos de palabras, correctores ortográficos, criptografía.",
        "big_o_time": "O(n)", "big_o_space": "O(1)",
        "tests": "listen, silent | true\nhola, adios | false\n'', '' | true\nabc, cab | true",
    },
    "guia-plus-reto-intermedio-30-manejador-de-historial-undo": {
        "desc": "Implementa un sistema de historial con capacidad de deshacer (undo) y rehacer (redo) usando dos pilas.",
        "p1": "**Análisis del problema:** Se mantienen dos pilas: una de acciones realizadas y otra de acciones deshechas. Al hacer undo, la acción actual pasa a la pila de redo. Al hacer una acción nueva, se vacía la pila de redo. **Ejemplo concreto:** escribir('a'), escribir('b'), undo() → 'a', redo() → 'ab'. **Edge cases:** undo sin acciones, redo sin acciones, capacidad máxima de historial.",
        "p2": "**Implementación:** Clase Historial con métodos: add(accion), undo(), redo(). Usar dos listas como pilas (append/pop). El estado actual se reconstruye aplicando todas las acciones de la pila de undo.",
        "p3": "**Complejidad:** Todas las operaciones O(1). O(n) espacio para el historial. **Aplicaciones:** editores de texto, IDEs, sistemas de diseño, editores de imágenes, terminales.",
        "big_o_time": "O(1)", "big_o_space": "O(n)",
        "tests": "add('a'),add('b'),undo() | 'a'\nadd('x'),undo(),redo() | 'x'\nundo() | error\nadd('a'),add('b'),undo(),add('c'),redo() | 'ac'",
    },
    "guia-plus-reto-intermedio-38-validador-de-isbn": {
        "desc": "Valida un número ISBN-10 o ISBN-13 según su algoritmo de checksum.",
        "p1": "**Análisis del problema:** ISBN-10: la suma de (dígito × posición), módulo 11, debe dar 0. El último dígito puede ser 'X' (valor 10). ISBN-13: la suma ponderada (1,3,1,3...) debe ser múltiplo de 10. **Ejemplo concreto:** ISBN-10 0-306-40615-2 → check = (0×10+3×9+0×8+6×7+4×6+0×5+6×4+1×3+5×2+2×1) mod 11 = 0 → válido. **Edge cases:** ISBN con guiones/espacios, carácter X, longitud incorrecta.",
        "p2": "**Implementación:** 1) Limpiar el string (eliminar guiones, espacios). 2) Verificar longitud (10 o 13). 3) Aplicar algoritmo según tipo. 4) Para ISBN-10, manejar X como 10.",
        "p3": "**Complejidad:** O(n) tiempo, O(1) espacio. **Aplicaciones:** sistemas bibliotecarios, commerce de libros, validación de datos en formularios.",
        "big_o_time": "O(n)", "big_o_space": "O(1)",
        "tests": "'0-306-40615-2' | true\n'978-0-306-40615-7' | true\n'1234567890' | false\n'' | false",
    },
    "guia-plus-reto-avanzado-01-arboles-binarios-de-busqueda": {
        "desc": "Implementa un Árbol Binario de Búsqueda (BST) con inserción y búsqueda. Cada nodo tiene un valor, hijo izquierdo (menor) y derecho (mayor).",
        "p1": "**Análisis del problema:** Un BST es una estructura donde para cada nodo, todos los valores del subárbol izquierdo son menores y los del derecho son mayores. Esto permite búsqueda binaria O(log n). **Ejemplo concreto:** insertar 5, 3, 7, 1, 9. Buscar 7 → encontrado. Buscar 4 → no encontrado. **Edge cases:** árbol vacío (root=null), valores duplicados (según implementación), inserción secuencial (degenera a lista), árbol muy profundo.",
        "p2": "**Implementación:** Clase Nodo con val, left, right. Insertar: si root es None, crear nodo. Si valor < root.val, insertar en left; si >, en right. Buscar: similar, comparando en cada nivel.",
        "p3": "**Complejidad:** O(log n) promedio, O(n) peor caso (árbol desbalanceado). O(n) espacio para almacenar n nodos. Mejorable con árboles AVL o Red-Black. **Aplicaciones:** búsquedas dinámicas, diccionarios en memoria, implementación de sets, sistemas de archivos.",
        "big_o_time": "O(log n) promedio, O(n) peor caso", "big_o_space": "O(n)",
        "tests": "insertar(5,3,7,1,9), buscar(7) | true\ninsertar(5,3,7), buscar(4) | false\ninsertar(), buscar(1) | false\ninsertar(1,2,3), buscar(3) | true",
    },
    "guia-plus-reto-avanzado-11-simulador-de-blockchain": {
        "desc": "Implementa una cadena de bloques simple con validación de integridad mediante hashes SHA-256 y prueba de trabajo (proof of work).",
        "p1": "**Análisis del problema:** Cada bloque contiene datos, su propio hash, el hash del bloque anterior, y un nonce (para proof of work). La cadena es válida si cada bloque apunta al hash correcto del anterior. **Ejemplo concreto:** Bloque 1: 'genesis', hash=abc... → Bloque 2: 'tx1', prev=abc..., hash=def... Si alguien modifica el bloque 1, su hash cambia y el bloque 2 queda inválido. **Edge cases:** cadena vacía (solo bloque genesis), bloque con datos vacíos, nonce que nunca encuentra solución, hash collisions.",
        "p2": "**Implementación:** Clase Bloque con índice, timestamp, datos, prev_hash, nonce, hash. Método mine_block(dificultad) que incrementa nonce hasta que el hash empiece por 'difficulty' ceros. Clase Blockchain con lista de bloques y método is_chain_valid.",
        "p3": "**Complejidad:** Inserción/propagación de bloques: O(1). Verificación de cadena: O(n). Minería (proof of work): exponencial en la dificultad — O(16^difficulty). **Aplicaciones:** criptomonedas, certificación de documentos, registros inmutables, trazabilidad en supply chain.",
        "big_o_time": "O(1) inserción, O(n) verificación", "big_o_space": "O(n)",
        "tests": "crearCadena(), addBloque('tx1') | valida\ncrearCadena(), modificarBloque(0) | invalida\naddBloque(''), addBloque('abc') | 2 bloques",
    },
    "guia-plus-reto-avanzado-19-compresion-huffman": {
        "desc": "Implementa el algoritmo de compresión de Huffman: construye un árbol de frecuencias, asigna códigos binarios y comprime/descomprime texto.",
        "p1": "**Análisis del problema:** Huffman asigna códigos más cortos a caracteres más frecuentes. Se construye un árbol binario donde las hojas son caracteres con su frecuencia, y los caminos izquierda=0, derecha=1 forman el código. **Ejemplo concreto:** 'aaabbc' → frecuencias: a:3, b:2, c:1 → árbol con a='0', b='11', c='10' → comprimido: '000111110'. **Edge cases:** texto con un solo carácter repetido, caracteres con misma frecuencia, texto vacío, Unicode.",
        "p2": "**Implementación:** 1) Contar frecuencias. 2) Construir cola de prioridad con nodos. 3) Fusionar los dos de menor frecuencia hasta que quede uno (el árbol). 4) Recorrer el árbol generando códigos. 5) Codificar el texto original con los códigos. 6) Decodificar recorriendo el árbol.",
        "p3": "**Complejidad:** O(n log n) para construir el árbol (usando heap). O(n) para codificar/decodificar. **Aplicaciones:** compresión de archivos (ZIP, gzip), códecs de imagen (JPEG), transmisión de datos.",
        "big_o_time": "O(n log n)", "big_o_space": "O(n)",
        "tests": "'aaabbc' | comprimido\n'aaaa' | comprimido\n'' | ''\n'a' | codigo='0'",
    },
    "guia-plus-reto-avanzado-20-diff-de-archivos-levenshtein": {
        "desc": "Calcula la distancia de Levenshtein (edit distance) entre dos cadenas: mínimo número de inserciones, eliminaciones y sustituciones para transformar una en otra.",
        "p1": "**Análisis del problema:** Se usa programación dinámica con una matriz de (m+1)×(n+1). Cada celda dp[i][j] representa el costo mínimo para transformar los primeros i caracteres de s1 en los primeros j de s2. **Ejemplo concreto:** 'casa' → 'calle' = 3 (c→c:0, a→a:0, s→l:1, a→l:1, e:1). **Edge cases:** cadenas vacías, una cadena vacía (distancia = longitud de la otra), cadenas iguales (distancia 0), cadenas de longitudes muy diferentes.",
        "p2": "**Implementación:** Matriz dp con dimensiones len(s1)+1 × len(s2)+1. Inicializar primera fila y columna con índices. Para cada celda: si s1[i]==s2[j], dp[i][j]=dp[i-1][j-1]; si no, 1+min(insertar, eliminar, sustituir). Devolver dp[m][n]. Optimización: solo dos filas en vez de la matriz completa para O(min(m,n)) espacio.",
        "p3": "**Complejidad:** O(m×n) tiempo, O(min(m,n)) espacio con optimización. **Aplicaciones:** correctores ortográficos, detección de plagio, alineamiento de secuencias de ADN, sistemas de control de versiones, deduplicación de registros.",
        "big_o_time": "O(m×n)", "big_o_space": "O(min(m,n))",
        "tests": "'casa', 'calle' | 3\n'', 'abc' | 3\n'hola', 'hola' | 0\n'abc', '' | 3\n'gato', 'pato' | 1",
    },
    "guia-plus-reto-avanzado-14-worker-queue-con-prioridad": {
        "desc": "Implementa un sistema de cola de trabajos con prioridad donde los trabajos con mayor prioridad se ejecutan primero (max-heap).",
        "p1": "**Análisis del problema:** Una cola de prioridad es un heap máximo: el elemento con mayor prioridad está siempre en la raíz. Operaciones: add(tarea, prioridad), execute() → ejecuta la de mayor prioridad y la elimina. **Ejemplo concreto:** add('A',3), add('B',1), add('C',2) → execute() → 'A' (prio 3), execute() → 'C' (prio 2). **Edge cases:** cola vacía, prioridades iguales (orden FIFO), tareas sin prioridad, muchas tareas con la misma prioridad.",
        "p2": "**Implementación:** Usar un heap (max-heap) implementado con lista. Las operaciones principales: insert (push al final y subir/burbujear hacia arriba), extract_max (intercambiar raíz con último, bajar/burbujear hacia abajo). En Python, heapq es min-heap: se usa prioridad negativa para simular max-heap.",
        "p3": "**Complejidad:** Inserción y extracción: O(log n) cada una. **Aplicaciones:** schedulers de SO, planificación de procesos, sistemas de colas de mensajes (RabbitMQ), procesamiento por lotes prioritario, algoritmos de Dijkstra/Prim.",
        "big_o_time": "O(log n)", "big_o_space": "O(n)",
        "tests": "add('A',3),add('B',1),execute() | 'A'\nadd('X',5),execute() | 'X'\nexecute() | error (empty)\nadd('A',1),add('B',1),execute() | 'A' (FIFO en empate)",
    },
}

# ── Helpers ─────────────────────────────────────────────────

def esc(s):
    """Escape for YAML double-quoted strings."""
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('{', '&#123;').replace('}', '&#125;').replace('<', '&lt;').replace('>', '&gt;')


def esc_attr(s):
    """Escape for JSX attribute values (inside double-quoted attrs)."""
    return s.replace('"', '&quot;').replace('{', '&#123;').replace('}', '&#125;').replace('<', '&lt;').replace('>', '&gt;')


def extract_between(text, start_marker, end_markers):
    """Extract text between start_marker and the earliest end_marker."""
    start = text.find(start_marker)
    if start == -1:
        return ""
    start += len(start_marker)
    ends = []
    for em in end_markers:
        e = text.find(em, start)
        if e != -1:
            ends.append(e)
    if not ends:
        return text[start:].strip()
    return text[start:min(ends)].strip()


def extract_table_rows(text):
    """Extract test case rows from an MDX table."""
    lines = text.split('\n')
    in_table = False
    rows = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|') and 'Entrada' not in stripped and '---' not in stripped:
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            if len(cells) >= 2:
                rows.append(f"{cells[0]} | {cells[1]}")
    return rows


def get_code(title, lang):
    """Get solution code for a challenge in a specific language."""
    from scripts.solutions_db import _normalize_key
    slug = _normalize_key(title)

    # 5 curated entries have proper multi-language code in DB
    curated = {"suma-de-digitos", "par-o-impar", "invertir-palabra",
               "fibonacci-recursivo", "detector-de-palindromos"}
    is_curated = any(c in slug or slug in c for c in curated)

    if is_curated:
        sol = db_lookup(title, lang)
        if sol and sol.get("codigo"):
            return sol["codigo"]

    if lang == "python":
        sol = db_lookup(title, lang)
        if sol:
            return sol.get("codigo", "")

    # Generate language-specific code (avoids Python fallback for Java/TS)
    gen = generate_generic(title, lang)
    return gen.get("codigo", "")


def truncate_words(text, max_chars):
    """Truncate text at word boundary within max_chars."""
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    last_space = truncated.rfind(' ')
    if last_space > max_chars * 0.7:
        truncated = truncated[:last_space]
    return truncated.rstrip('.,;:!?-, ') + '...'


def build_mdx(slug, title, desc, p1, p2, p3, big_o_time, big_o_space, tests, codes, difficulty):
    """Build a complete MDX file with the new multi-language template."""
    tags = json.dumps(["retos", difficulty.lower(), "multilenguaje"])
    now = datetime.now().strftime("%Y-%m-%d")

    # Escape body content for MDX safety (no stray {, }, <, >)
    desc_body = esc_attr(desc)
    p1_body = esc_attr(p1)
    p2_body = esc_attr(p2)
    p3_body = esc_attr(p3)

    test_rows = []
    for t in tests:
        parts = t.split('|', 1)
        if len(parts) == 2:
            test_rows.append(f"| `{esc(parts[0].strip())}` | `{esc(parts[1].strip())}` |")

    tabla = '\n'.join(test_rows) if test_rows else "| `ejemplo` | `resultado` |"

    new_slug = slug.replace("guia-plus-reto-", "reto-").replace("guia-", "reto-")
    img_path = f"img/{new_slug}_cover-1200.webp"

    return f"""---
draft: false
title: "🏆 RETO: {title}"
description: "{esc(truncate_words(desc, 160))}"
pubDate: "{now}"
tags: {tags}
slug: "{new_slug}"
image: "{img_path}"
author: "Jorge Beneyto Castelló"
difficulty: "{difficulty}"
languages: ["python", "javascript", "java", "typescript"]
---

import Challenge from '@components/Challenge.astro';
import CodeTabs from '@components/CodeTabs.svelte';

# 🎯 Desafío: {title}

### 📝 Descripción del Reto
{desc_body}

<Challenge 
  nivel="{difficulty}" 
  mision="{esc_attr(truncate_words(desc, 120))}" 
/>

---

### 🧪 Casos de Prueba

| Entrada | Salida esperada |
|---------|-----------------|
{tabla}

---

## 💡 Guía de Solución Paso a Paso

<details>
<summary><b>Ver explicación y código 🛠️ (¡No hagas spoiler!)</b></summary>
<div class="details-content">

### 🏗️ Paso 1: Análisis de la lógica
{p1_body}

### ⚙️ Paso 2: Implementación
{p2_body}

### 🚀 Paso 3: Complejidad y Optimización

**Complejidad temporal:** {big_o_time}  
**Complejidad espacial:** {big_o_space}  

{p3_body}

### 💻 Código de la Solución

<CodeTabs client:load>

```python
{codes.get('python', '')}
```

```javascript
{codes.get('javascript', '')}
```

```java
{codes.get('java', '')}
```

```typescript
{codes.get('typescript', '')}
```

</CodeTabs>

</div>
</details>
"""


# ── Process all files ───────────────────────────────────────

def main():
    if not os.path.isdir(DIR):
        print(f"❌ Directory not found: {DIR}")
        sys.exit(1)

    files = sorted([f for f in os.listdir(DIR) if f.endswith('.mdx')])
    print(f"📁 Found {len(files)} files in {DIR}")

    kept = 0
    drafted = 0
    errors = []

    for filename in files:
        filepath = os.path.join(DIR, filename)
        slug = filename.replace('.mdx', '')
        print(f"\n{'='*60}")
        print(f"📄 {filename}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if slug not in KEEP:
                # Mark as draft — remove any existing draft: lines, add clean one
                new_content = re.sub(r'^draft: .*\n?', '', content, flags=re.MULTILINE)
                new_content = new_content.replace('---\n', '---\ndraft: true\n', 1)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                drafted += 1
                print(f"   → Drafted")
                continue

            # Extract metadata
            title_m = re.search(r'^title: "(.+?)"', content, re.MULTILINE)
            title = title_m.group(1) if title_m else slug
            # Strip existing "RETO:" prefix(es) if present (build_mdx adds it)
            title = re.sub(r'^(?:[🏆🎯⭐]\s*RETO:\s*)+', '', title).strip()

            diff_m = re.search(r'^difficulty: "?(Iniciación|Intermedio|Avanzado)"?', content, re.MULTILINE)
            difficulty = diff_m.group(1) if diff_m else "Intermedio"

            # If this is a GEN challenge, use hardcoded content
            if slug in GEN:
                gen = GEN[slug]
                desc = gen["desc"]
                p1 = gen["p1"]
                p2 = gen["p2"]
                p3 = gen["p3"]
                big_o_time = gen["big_o_time"]
                big_o_space = gen["big_o_space"]
                tests = gen["tests"].split('\n')
            else:
                # CUR challenge — extract existing content
                desc = extract_between(content, "### 📝 Descripción del Reto\n",
                                       ["\n<Challenge", "\n---", "\n\n---"])
                # Clean up any italic preamble that might remain
                desc = re.sub(r'\*?\*?Este problema requiere.*?\*?\*?', '', desc).strip()
                # Clean boilerplate descriptions that mention Rust
                if 'Rust' in desc or 'en Rust' in desc or desc.startswith('Este reto'):
                    desc = f"Resuelve el desafío '{title}'. Implementa una solución completa siguiendo las mejores prácticas de programación."

                p1 = extract_between(content, "### 🏗️ Paso 1: Análisis de la lógica\n",
                                     ["### ⚙️ Paso 2:"])
                # Remove any "Para profundizar..." boilerplate
                p1 = re.sub(r'\*\*Para profundizar.*?\*\*[\s\S]*?$', '', p1).strip()
                # Clean boilerplate p1
                if 'Rust' in p1 or 'Entrada vacía o nula' in p1:
                    p1 = f"**Análisis del problema:** {title}. Identifica la entrada, la salida esperada, y los casos límite. Diseña una estrategia de solución eficiente."

                p2 = extract_between(content, "### ⚙️ Paso 2:",
                                     ["### 🚀 Paso 3:"])
                # Remove heading text that leaks into the content
                p2 = re.sub(r'^.*?Implementación(?:\s+en\s+\w+)?\s*\n+', '', p2).strip()
                p2 = re.sub(r'\*\*Para enriquecer.*?\*\*[\s\S]*?$', '', p2).strip()
                if 'Rust' in p2:
                    p2 = f"**Implementación:** Traduce el análisis a código. Sigue la estructura definida en el análisis y maneja correctamente los casos límite."

                # For paso 3, extract complexity values and analysis separately
                p3_section = extract_between(content, "### 🚀 Paso 3:",
                                             ["### 💻 Código"])
                # Extract big_o_time
                bt_m = re.search(r'\*\*Complejidad temporal:\*\* (.+)', p3_section)
                big_o_time = bt_m.group(1).strip() if bt_m else "O(n)"
                # Extract big_o_space
                bs_m = re.search(r'\*\*Complejidad espacial:\*\* (.+)', p3_section)
                big_o_space = bs_m.group(1).strip() if bs_m else "O(n)"
                # Remove complexity header lines + any "Para un análisis..." boilerplate
                p3 = re.sub(r'\*\*Complejidad temporal:\*\* .+', '', p3_section)
                p3 = re.sub(r'\*\*Complejidad espacial:\*\* .+', '', p3)
                p3 = re.sub(r'\*\*Para un análisis.*?\*\*[\s\S]*?$', '', p3).strip()

                # Extract test cases
                tests_raw = extract_between(content, "### 🧪 Casos de Prueba\n\n| Entrada | Salida esperada |\n|---------|-----------------|\n",
                                            ["\n---", "\n\n---"])
                test_rows = [t.strip() for t in tests_raw.split('\n') if t.strip().startswith('|')]
                tests = []
                for tr in test_rows:
                    cells = [c.strip() for c in tr.strip('|').split('|')]
                    if len(cells) >= 2 and cells[0] != 'ejemplo':
                        tests.append(f"{cells[0]} | {cells[1]}")
                if not tests:
                    tests = ["0 | 0", "1 | 1", "2 | 2"]

                # Fallback for empty/boilerplate pasos
                if not p1 or len(p1) < 30:
                    p1 = f"**Análisis del problema:** {title}. Identifica la entrada, salida, y casos límite. Diseña una estrategia de solución."
                if not p2 or len(p2) < 30:
                    p2 = f"**Implementación:** Traduce el análisis a código en cada lenguaje. Sigue la estructura definida y maneja edge cases."
                if not p3 or len(p3) < 30:
                    p3 = "**Complejidad:** Analiza el tiempo y espacio requeridos por tu solución. **Aplicaciones:** este patrón aparece en problemas similares del mundo real."

            # Get code for all 4 languages
            # Use the clean title (without "RETO:" prefix and emoji) for DB lookup
            clean_title = re.sub(r'^.*?RETO:\s*', '', title).strip()
            codes = {}
            for lang in LANGUAGES:
                try:
                    code = get_code(clean_title, lang)
                    if not code:
                        code = f"# {lang} solution for {clean_title}\n# TODO: implement"
                    codes[lang] = code
                except Exception as e:
                    print(f"   ⚠️  Error getting {lang} code: {e}")
                    codes[lang] = f"# {lang} solution (fallback)"

            # Build new MDX
            difficulty_display = difficulty
            new_mdx = build_mdx(slug, title, desc, p1, p2, p3, big_o_time, big_o_space, tests, codes, difficulty_display)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_mdx)
            kept += 1
            print(f"   ✅ Rewritten")

        except Exception as e:
            errors.append((filename, str(e)))
            print(f"   ❌ ERROR: {e}")

    print(f"\n{'='*60}")
    print(f"📊 Results: {kept} kept + rewritten, {drafted} drafted, {len(errors)} errors")
    for fname, err in errors:
        print(f"   ❌ {fname}: {err}")


if __name__ == "__main__":
    main()
