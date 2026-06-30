# Skill: Expandir guías "De 0 a 100"

## Formato y estructura de los posts `guia-0-100-*.mdx`

Cada guía debe seguir esta estructura. Target: **~2000–4000 líneas** por guía, con código real, explicaciones profundas, fuentes documentadas y progresión real 0–100.

## Frontmatter

```yaml
---
draft: false
title: "Guía de {Tecnología}: De 0 a 100"
description: "{Descripción ambiciosa: desde fundamentos hasta producción, con ecosistema, frameworks, proyectos y recursos en español.}"
pubDate: "2017-06-11"
tags: ["{tag}", "guia", "{categoria}"]
image: "img/guia_0_100_{tag}_cover-1200.webp"
author: "Jorge Beneyto Castelló"
---
```

## Template estándar por concepto

Cada sección técnica (secciones 5 a 15) debe aplicar este sub-formato para cada sub-concepto:

```
### {Concepto}

#### ¿Qué es?
- Definición en lenguaje llano + definición formal
- Analogía del mundo real
- 🔗 Enlace a Wikipedia / MDN / glosario

#### Sintaxis básica
- Código mínimo ejecutable, listo para copiar y pegar
- Tabla de variantes (si aplica)

#### 🧪 Cómo probarlo
- Mini‑script autónomo: `python3 -c "..."` / `node -e "..."`
- Test unitario con el framework estándar (pytest, Jest, JUnit, etc.)
- Template de test para este concepto concreto
- Ejemplo de aserciones básicas

#### 💡 Memoria y rendimiento
- Cuánto ocupa en memoria, stack vs heap
- Complejidad Big O (si aplica: acceso, búsqueda, inserción, borrado)
- Tips de optimización específicos del concepto
- ⚠️ Posibles fugas de memoria / efectos secundarios

#### ✅ Buenas prácticas
- Lo idiomático recomendado
- ⚠️ Errores frecuentes
- ❌ Antipatrones
- Cómo escala esta práctica en proyectos grandes

#### 🏗️ Metodología
- ¿Cuándo usarlo y cuándo NO?
- Alternativas según escala del proyecto (script → microservicio → monolito)
- Relación con otros paradigmas

#### 🔗 Para saber más
- 2-4 enlaces externos variados (oficial, tutorial, vídeo, artículo en profundidad)
```

## Secciones obligatorias (22)

### 1. ¿Qué es {Tecnología}?
- Origen, creador, año de creación
- Filosofía / paradigma(s) que soporta
- Casos de uso principales (con empresas reales si aplica)
- Fuente: sitio oficial, Wikipedia

### 2. ¿Cómo empezar? Instalación en todos los entornos
- Windows (instalador, winget, WSL)
- macOS (Homebrew, Xcode tools)
- Linux (apt, dnf, pacman)
- Gestor de versiones (nvm, sdkman, rustup, pyenv, etc.)
- Docker (Dockerfile mínimo)
- Alias útiles para el día a día
- Verificación con `--version` y "Hola Mundo"

### 3. Primeros pasos y configuración del entorno
- REPL / intérprete interactivo si existe
- Hola Mundo
- Estructura de proyecto
- Editores recomendados → [IDEs y Editores de Código](/posts/resources/#ides-y-editores-de-codigo) (VSCode, JetBrains, Neovim) + extensiones
- Config inicial: linters, formatters, type checkers
- Gestión de dependencias (npm, cargo, pip, maven, go modules, etc.)

### 4. Paradigmas de programación
Qué paradigmas soporta el lenguaje con ejemplo breve de cada uno:
- **Imperativo / procedural** — secuencia de instrucciones, variables mutables
- **Orientado a objetos** — clases, objetos, herencia, polimorfismo
- **Funcional** — funciones puras, inmutabilidad, higher-order functions, pattern matching
- **Declarativo** — qué hacer vs cómo hacerlo (SQL, configs)
- **Reactivo** — streams, observables, flujos de datos (si aplica)
- Tabla: "Paradigma | Soporte nativo | Librerías | Ejemplo"
- ¿Cuál es el paradigma principal del lenguaje? ¿Cuál se recomienda para empezar?

### 5. Tipos de datos y variables
- **Sistema de tipos**: estático/dinámico, fuerte/débil, inferencia, nominal/estructural
- **Primitivos**: int, float, bool, char, string — tamaño en memoria, precisiones
- **Compuestos**: arrays, lists, tuples, maps, sets, structs, enums
- **Mutabilidad**: mutable vs inmutable, constantes, final/val/const/let
- **Nullabilidad**: null/nil/none/undefined, Option/Maybe, null safety
- **Memoria**: stack vs heap, boxing/unboxing, value vs reference types
- **Type casting**: implícito, explícito, coerción, conversiones seguras
- Tabla de tipos con tamaño, rango, mutabilidad

### 6. Control de flujo y modularidad
- **Condicionales**: if/else, switch/match/when, ternarios, pattern matching en condicionales
- **Bucles**: for, while, do-while, for-in, for-of, iteradores, comprehensions
- **Control de flujo avanzado**: break/continue, labeled breaks, early returns, guard
- **Excepciones**: try/catch/finally, throw/raise, checked vs unchecked, Result vs exceptions
- **Módulos y paquetes**: imports/exports, namespaces, visibilidad (pub/private/internal)
- **Organización**: archivos, carpetas, módulos, proyectos multi-archivo
- Tabla: "Estructura | Sintaxis | Ejemplo"

### 7. Sistema de archivos (File System I/O)
- **Lectura/escritura**: archivos de texto, binarios, JSON, CSV, YAML, TOML
- **Directorios**: listar, crear, borrar, mover, recorrer árbol
- **Streams**: lectura/escritura por fragmentos, pipes, buffering
- **Rutas**: relativa vs absoluta, path manipulation, separadores por SO
- **Permisos**: lectura/escritura/ejecución, owner/group/world
- **Watch**: observar cambios en archivos/directorios
- **Temp files**: archivos y directorios temporales
- Ejemplo completo: lectura de un directorio, procesamiento de archivos CSV, escritura de resultados

### 8. Algoritmos y estructuras de datos
- **Búsqueda**: lineal, binaria, en colecciones (find, filter)
- **Ordenación**: sort nativo, estable vs inestable, comparadores personalizados
- **Estructuras nativas**: listas/arrays, pilas, colas, diccionarios, conjuntos
- **Estructuras de la stdlib**: colas con prioridad, árboles, grafos, LRU cache
- **Complejidad**: Big O de las operaciones principales del lenguaje (acceso, búsqueda, inserción, borrado — tabla)
- **Algoritmos de la stdlib**: funciones incorporadas para transformar colecciones (map, reduce, filter, groupBy, etc.)
- Ejemplo: ordenar un array de objetos por múltiples criterios

### 9. Conceptos clave del lenguaje (la sección más pesada)
Cada concepto debe incluir:
- Explicación clara de qué es
- Código de ejemplo ejecutable
- Analogía con otras tecnologías si aplica
- Peculiaridades propias del lenguaje

**Conceptos a cubrir (adaptar por lenguaje):**

| Concepto | Lenguajes donde aplica |
|---|---|
| Variables y memoria | Todos (stack vs heap, mutabilidad, boxing) |
| Tipado | Estático/dinámico, fuerte/débil, inferencia |
| Decoradores / anotaciones | Python, Java, TypeScript |
| POO (clases, herencia, interfaces) | Java, Kotlin, C#, TypeScript, Ruby, PHP, Dart, Swift, Python |
| Propiedades / getters/setters | C#, Kotlin, Python, Swift, Ruby |
| Genéricos / templates | Java, Kotlin, C#, TypeScript, Rust, Go (1.18+), Swift |
| Traits / interfaces / protocols | Rust, Go, TypeScript, Java, Swift |
| Gestión de errores | Todos (exceptions vs Result vs Option) |
| Async / await | Todos los modernos |
| Memoria y garbage collection | Java, C#, Go, Ruby, Python, JavaScript |
| Ownership / borrowing | Rust (único) |
| Canales / goroutines | Go (único) |
| Pattern matching | Rust, Kotlin, Swift, TypeScript, C# |
| Null safety | Kotlin, Swift, TypeScript, Rust, Dart |
| Mixins / extension methods | Dart, Kotlin, C#, Ruby |
| Macros / metaprogramación | Rust, Ruby, Elixir, Lisp |
| Structs vs clases | Rust, C#, Swift, Go |

### 10. POO y patrones de diseño
- Ejemplo completo (sistema multimedia: clases base, herencia, interfaces, composición)
- Demostrar: herencia, encapsulación, polimorfismo, composición, mixins
- Incluir: `@dataclass` / `record` / `data class`, métodos mágicos / operator overloading
- Patrones con ejemplos (adaptar al lenguaje):
  - Strategy (funciones como ciudadanos de primera clase)
  - Observer (eventos/signals)
  - Factory (registro dinámico)
  - Singleton (módulos, objetos companion)
  - Adapter (duck typing / interfaces)
  - Builder (para objetos complejos)
- Tabla "Patrón | En {Lenguaje}"

### 11. Polimorfismo en detalle
- Subtipado (herencia)
- Paramétrico (genéricos)
- Ad-hoc (overloading, traits, interfaces)
- Duck typing / structural typing si aplica
- Código de ejemplo para cada tipo

### 12. Interacción con contenido multimedia
- **Imágenes**: formatos (PNG, JPEG, WebP, AVIF, SVG), lectura/escritura, redimensionar, convertir
- **Video**: formatos, codecs, procesamiento de frames, extraer audio
- **Audio**: formatos, reproducción, análisis básico (waveform, espectro)
- **GIFs**: crear, editar, optimizar, extraer frames
- **Canvas/gráficos**: dibujo 2D, gráficos por computadora, visualización
- **Librerías** específicas del lenguaje para cada tipo multimedia
- Tabla: "Tipo | Librería | Formatos | Async | Ejemplo mínimo"

### 13. Bases de datos (si aplica)
- ORMs y drivers populares
  - SQLAlchemy / Prisma / Diesel / GORM / Entity Framework / Hibernate / ActiveRecord
  - Async drivers
  - NoSQL (MongoDB, Redis, Cassandra)
- Migraciones
- Ejemplo CRUD

### 14. WebSockets y mensajería (si aplica)
- Librerías de WebSocket
- MQTT / RabbitMQ / Kafka
- Server-Sent Events
- Ejemplo servidor + cliente

### 15. Concurrencia y paralelismo
- Modelo del lenguaje (threads, async, goroutines, actors)
- Comparativa threading vs async vs multiprocessing
- Librerías que mejoran el rendimiento
- Tabla "¿Cuál usar?" por escenario
- GIL / event loop / work-stealing según el lenguaje

### 16. Testing y calidad

Tipos de test y frameworks disponibles en {Tecnología}:

#### Frameworks y herramientas
| Framework | Propósito | Async? | CLI | Template |
|-----------|-----------|--------|-----|----------|
| {ej: pytest} | {unitario} | {sí/no} | {comando} | {enlace a template} |

#### Cómo testear cada concepto
(Por cada concepto de las secciones 5-15, dar el patrón de test específico)
- **Variables y tipos** → aserciones simples, type narrowing en tests
- **Control de flujo** → cobertura de ramas, boundary testing
- **POO** → mocks, stubs, fixtures, factories en tests
- **Async** → test con timeouts, falsificación de reloj
- **File I/O** → temp directories, fixtures de archivos
- **Red** → mock servers, HTTP interceptors

#### Parametrización
- Test parametrizados (pytest.mark.parametrize, Jest.each, JUnit @ParameterizedTest)
- Property-based testing (Hypothesis, fast-check, QuickTheories)
- Fuzzing básico

#### Cobertura y CI
- Herramientas de cobertura (coverage.py, c8/codecov, JaCoCo)
- Integración con GitHub Actions
- Umbrales recomendados

#### Mini‑scripts de verificación
- Script autónomo por concepto que el lector pueda ejecutar para validar que lo entendió
- Cada mini‑script incluye: enunciado, solución esperada, test que lo verifica
- Template de mini‑script disponible en `scripts/templates/` (por crear)

### 17. Conceptos avanzados parametrizados

Contenido parametrizado según la tecnología. Seleccionar los que apliquen:

| Tecnología | Concepto avanzado | Por qué es el siguiente paso natural |
|---|---|---|
| Docker | Kubernetes, Docker Swarm, Compose en producción | Orquestación multi‑contenedor |
| Python | asyncio profundo, C extensions, profile-guided optimization | Performance y concurrencia real |
| JavaScript | Web Workers, WASM, Server Components, Structured Clone | Cómputo en cliente y server |
| TypeScript | advanced types, template literal types, conditional types | Tipado de precisión quirúrgica |
| Java | Project Loom (virtual threads), GraalVM, JMM, JMH benchmarking | Concurrencia y native image |
| Kotlin | Coroutines flow/channels, multiplatform, Compose | Async y shared code |
| C# | Source Generators, NativeAOT, Span\<T\>/Memory\<T\>, Channels | Rendimiento extremo |
| Go | go:generate, pprof, cgo, WASM, govulncheck | Tooling y ecosistema |
| Rust | unsafe, FFI, embedded no_std, WASM, Pin, async traits | Sistemas y WASM |
| Swift | Swift concurrency (actors, async sequences), SwiftUI, macros | UI y concurrencia moderna |
| Dart | isolates, FFI, Wasm, flutter web | Rendimiento y nativo |
| Ruby | Ractor, Fiber Scheduler, YJIT, pattern matching | Concurrencia real |
| PHP | Fibers, FFI, preloading, async PHP (ReactPHP, Amp, Swoole) | Concurrencia y rendimiento |
| Astro | view transitions, server islands, content collections avanzado, i18n | Riqueza de UI y datos |
| Markdown/MDX | Remark plugins, MDX custom components, AST manipulation | Procesamiento avanzado |

Cada concepto avanzado debe incluir:
- Enlace a documentación oficial
- Mini tutorial de inicio
- Proyecto ejemplo

### 18. Escala de aprendizaje 0–100 (7 niveles)
Cada nivel debe incluir:
- Lista de conceptos a aprender (referenciando las secciones anteriores)
- Proyecto concreto con código que integre file system + algoritmos + testing + BD + red
- Referencia a conceptos clave del lenguaje

Niveles:
- **0–15**: Fundamentos (sintaxis, variables, tipos, condicionales, bucles, file system básico)
- **15–30**: Estructuras de datos, funciones, colecciones, algoritmos de búsqueda/ordenación
- **30–45**: POO, módulos, errores, genéricos, patrones, multimedia básico
- **45–60**: Testing (unitario + integración + parametrización), logging, tooling, empaquetado, file system avanzado, procesamiento por lotes
- **60–75**: Web APIs, async, BD, WebSockets, multimedia streaming
- **75–90**: Producción, Docker, CI/CD, patrones, procesamiento multimedia avanzado
- **90–100**: Arquitectura, sistemas distribuidos, performance, algoritmos complejos

### 19. Proyecto final integrador

Proyecto concreto que combine, como mínimo:
- File system I/O
- Algoritmo / estructura de datos
- POO o módulos
- Testing (unitario + integración)
- Red o BD

El proyecto debe:
- Ser ejecutable de principio a fin
- Incluir tests automatizados
- Incluir documentación
- Tener un template disponible en `scripts/templates/` (por crear)

### 20. Canales y recursos en español
- Canales de YouTube (mínimo 5)
- Comunidades (Reddit, Discord, Telegram)
- Repositorios GitHub destacados
- Blogs / newsletters

### 21. Hacks y tips de productividad
- Mínimo 8 tips con código
- Atajos, herramientas, patterns poco conocidos
- Configuraciones recomendadas
- Cómo debuggear file system, multimedia, concurrencia

### 22. Referencias y documentación oficial
- Links a docs oficiales
- PEPs / RFCs / JEPs / KIPs relevantes
- Fuentes de esta guía (mínimo 15, con URLs reales)
  - Documentación oficial
  - Libros recomendados
  - Blogs técnicos
  - Comunidades (Reddit, HN)
  - Especificaciones del lenguaje

## Reglas de estilo

1. **NO mencionar IA** — no decir "generado por IA", "hecho con IA", etc.
2. **NO atar al blog/astro** — las guías deben ser standalone
3. **Código real ejecutable** — cada snippet debe poder copiarse y ejecutarse
4. **Fuentes reales** — todas las URLs deben ser sitios reales y conocidos
5. **Español** — todo el contenido en español, incluídos comentarios de código
6. **Progresión real 0–100** — cada nivel debe ser alcanzable desde el anterior
7. **Analogías** — cuando un concepto es complejo, compararlo con algo que el lector ya conozca
8. **Tablas** — usar tablas para listar librerías, frameworks, comparativas
9. **Sin markdown excesivo** — no abusar de `<div>`, mantener MDX limpio
10. **File system en todos** — todo lenguaje tiene stdlib para I/O, incluir sí o sí
11. **Multimedia solo si aplica** — lenguajes de scripting tienen más librerías; sistemas embebidos/no estándar, omitir
12. **Todo progresivo** — cada sección referencia a las anteriores, construye sobre lo ya explicado
13. **Código testeable** — todo snippet debe poder ejecutarse y verificarse con un test
14. **Enlaces externos obligatorios** — cada concepto (¿Qué es?) debe tener al menos 1 enlace externo
15. **Mini‑scripts de verificación** — incluir al menos un script autónomo por sección que el lector pueda ejecutar para validar su comprensión
16. **Adaptación por tecnología** — no forzar conceptos que no aplican. Para tecnologías no‑lenguaje (Docker, Astro, Markdown/MDX), omitir secciones sin contenido significativo y reinterpretar otras (ej: Docker "patrones" = multi‑stage builds, redes overlay; Astro "POO" = componentes/server islands)
17. **Enlace al post "Hola Mundo"** — si la guía es de un lenguaje/tecnología que aparece en `src/content/posts/hola.mdx`, buscar la sección correspondiente (por nombre de tecnología) y añadir al inicio de la sección 3 (Primeros pasos) un párrafo como: `Si prefieres ver directamente el "Hola Mundo" en {Tecnología}, consulta [El Atlas del Hola Mundo](/posts/hola/#{sección}).` Solo aplica a guías de tipo *código* (lenguajes de programación, frameworks, tecnologías con sintaxis), no a guías conceptuales (Docker, Markdown/MDX).
18. **Referencia a IDEs en resources.mdx** — en sección 3 (Primeros pasos), no listar manualmente los IDEs/editorres. Enlazar a la sección `#ides-y-editores-de-codigo` de `/posts/resources/`. Solo mencionar los nombres (VSCode, JetBrains, Neovim) sin descripciones largas.

## Orden de ejecución recomendado

1. Python (guía de referencia)
2. JavaScript
3. TypeScript
4. Java
5. Kotlin
6. C# / .NET
7. Go
8. Rust
9. Swift
10. Dart
11. Ruby
12. PHP
13. Astro
14. Docker
15. Markdown/MDX
