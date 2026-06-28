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

## Secciones obligatorias (16)

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
- Editores recomendados (VSCode, JetBrains, Neovim) + extensiones
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

### 16. Escala de aprendizaje 0–100 (7 niveles)
Cada nivel debe incluir:
- Lista de conceptos a aprender (referenciando las secciones anteriores)
- Proyecto concreto con código que integre file system + algoritmos + multimedia + BD + red
- Referencia a conceptos clave del lenguaje

Niveles:
- **0–15**: Fundamentos (sintaxis, variables, tipos, condicionales, bucles, file system básico)
- **15–30**: Estructuras de datos, funciones, colecciones, algoritmos de búsqueda/ordenación
- **30–45**: POO, módulos, errores, genéricos, patrones, multimedia básico
- **45–60**: Testing, logging, tooling, empaquetado, file system avanzado, procesamiento por lotes
- **60–75**: Web APIs, async, BD, WebSockets, multimedia streaming
- **75–90**: Producción, Docker, CI/CD, patrones, procesamiento multimedia avanzado
- **90–100**: Arquitectura, sistemas distribuidos, performance, algoritmos complejos

### 17. Canales y recursos en español
- Canales de YouTube (mínimo 5)
- Comunidades (Reddit, Discord, Telegram)
- Repositorios GitHub destacados
- Blogs / newsletters

### 18. Hacks y tips de productividad
- Mínimo 8 tips con código
- Atajos, herramientas, patterns poco conocidos
- Configuraciones recomendadas
- Cómo debuggear file system, multimedia, concurrencia

### 19. Referencias y documentación oficial
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
