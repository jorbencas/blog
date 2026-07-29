---
title: "Weekly Tech Recap W31"
description: "Esta semana, la IA sigue su curso imparable, pero con un giro notable hacia la practicidad y el código abierto, alejándose del hype inicial para centr"
pubDate: "2026-07-29"
author: "Jorge Beneyto Castelló"
image: "img/2026_w31_tech_recap/2026_w31_tech_recap_cover-1200.webp"
tags: ["tech", "IA", "DevOps", "Ciberseguridad"]
slug: "2026-w31-tech-recap"
draft: true
readingTime: 16720
categories: ["tech", "weekly-recap"]
---

## 🚀 Radiografía de la semana

Esta semana, la IA sigue su curso imparable, pero con un giro notable hacia la practicidad y el código abierto, alejándose del hype inicial para centrarse en herramientas concretas y modelos más accesibles. Paralelamente, el ecosistema DevOps consolida sus mejores prácticas con debates sobre la orquestación de Kubernetes, mientras el hardware enfrenta desafíos de coste y Microsoft introduce nuevas medidas de seguridad basadas en TPM que impactan a los usuarios. Una semana de consolidación y movimientos estratégicos.

### 1. Google Gemini 3.6 Flash: La velocidad de la IA al servicio del desarrollo (🤖 IA)
**El suceso:** Google lanzó Gemini 3.6 Flash, una iteración más rápida de su modelo de lenguaje, posicionándola como la opción de menor latencia y coste para tareas que exigen rapidez, como el desarrollo agéntico o el procesamiento en tiempo real.
**Impacto:** Este movimiento intensifica la carrera por la eficiencia en modelos fundacionales, obligando a los desarrolladores a elegir entre potencia bruta y agilidad. Marca una tendencia hacia LLMs especializados para casos de uso específicos, más allá del "modelo único para todo".

### 2. Despliegues en EKS: ArgoCD eclipsa a Terraform para la gestión de estado (🐳 DevOps)
**El suceso:** Se reitera que Terraform no es ideal para desplegar en EKS, sino para aprovisionar la infraestructura. ArgoCD, en su lugar, emerge como la herramienta preferida para la gestión del estado de aplicaciones dentro de Kubernetes, adoptando principios de GitOps.
**Impacto:** Esta distinción es crucial para adoptar un enfoque de GitOps puro, donde la configuración deseada del clúster reside en Git. Promueve flujos de trabajo de CI/CD más robustos y auditables, y reduce errores de configuración en entornos complejos como EKS.

### 3. Microsoft usará TPM para bloquear Windows pirateados: Seguridad por hardware (🔒 Ciberseguridad)
**El suceso:** A partir de agosto, Microsoft implementará el uso del chip TPM en PCs para bloquear por hardware las instalaciones de Windows que detecte como pirateadas. Esto busca reforzar la seguridad y la autenticidad del sistema operativo.
**Impacto:** Esta medida eleva la barrera contra el software no licenciado y podría tener implicaciones significativas para ciertos usuarios y mercados. Subraya la creciente integración de la seguridad a nivel de hardware y la lucha continua contra la piratería.

---

## 📋 Noticias por fuente

### 📰 Hacker News (1348 noticias)

- `💻 Tech` `📡 RSS` ChatGPT afirma que una IA rebelde atacó a más empresas (Wed, 29 Jul 2026 09:03:17 +0000)
- `💻 Tech` `📡 RSS` SQLite en Producción: Optimizando el Modo WAL, la Concurrencia y las Capas VFS (Wed, 29 Jul 2026 07:18:24 +0000)
- `💻 Tech` `📡 RSS` Más trucos de Tailscale para tu Kindle con jailbreak (Wed, 29 Jul 2026 04:58:46 +0000)
- `💻 Tech` `📡 RSS` Abriendo Windows: Portando RADV a Win32 (Wed, 29 Jul 2026 04:30:47 +0000)
- `💻 Tech` `📡 RSS` Interfaces de usuario de la Demo Scene (Wed, 29 Jul 2026 04:30:36 +0000)
- `💻 Tech` `📡 RSS` Transformer Transformer: Un modelo unificado para el codiseño de robots condicionado por el movimiento (Wed, 29 Jul 2026 03:52:29 +0000)
- `💻 Tech` `📡 RSS` ¡Viva la interfaz de Sockets! (Wed, 29 Jul 2026 02:25:29 +0000)
- `💻 Tech` `📡 RSS` Show HN: DSL de Datalog en Lean4 basado en Google Zanzibar para proyectos de IA (Wed, 29 Jul 2026 02:22:04 +0000)
- `💻 Tech` `📡 RSS` LearnVector – La empresa de IA de Andrew Ng que crea experiencias de aprendizaje personalizadas. (Wed, 29 Jul 2026 01:49:19 +0000)
- `💻 Tech` `📡 RSS` Show HN: Aprendiendo Rust escribiendo un compilador de Markdown a HTML. (Wed, 29 Jul 2026 01:04:30 +0000)

### 📰 Lobsters (271 noticias)

- `💻 Tech` `📡 RSS` User Interfaces of the Demo Scene (Wed, 29 Jul 2026 03:07:13 -0500)
- `💻 Tech` `📡 RSS` Writing Toy Software Is A Joy (2025) (Wed, 29 Jul 2026 00:14:46 -0500)
- `💻 Tech` `📡 RSS` Lobste.rs on Spinel (Tue, 28 Jul 2026 20:30:21 -0500)
- `💻 Tech` `📡 RSS` Manganin: tools matter (Tue, 28 Jul 2026 23:44:39 -0500)
- `💻 Tech` `📡 RSS` Why Rocq is better than Lean for program verification (Tue, 28 Jul 2026 16:16:29 -0500)
- `💻 Tech` `📡 RSS` The mean means nothing (Tue, 28 Jul 2026 13:53:28 -0500)
- `💻 Tech` `📡 RSS` Inside Zig's Incremental Compilation (Tue, 28 Jul 2026 09:14:06 -0500)
- `💻 Tech` `📡 RSS` Building (systems) software with Nix (Tue, 28 Jul 2026 08:10:24 -0500)
- `💻 Tech` `📡 RSS` Parallel JSON parsing on the GPU with compute shaders (Tue, 28 Jul 2026 09:39:46 -0500)
- `💻 Tech` `📡 RSS` I Designed A Custom PCB To Avoid Pressing A Button Three Times (Tue, 28 Jul 2026 08:33:00 -0500)

### 📰 InfoQ (114 noticias)

- `💻 Tech` `📡 RSS` Cloudflare Makes Internal DNS Generally Available (Wed, 29 Jul 2026 10:30:00 GMT)
- `💻 Tech` `📡 RSS` Presentation: Getting Rid of LeetCode Interviews in the World of AI (Wed, 29 Jul 2026 10:25:00 GMT)
- `💻 Tech` `📡 RSS` Article: Securing MCP in Production: Defense-in-Depth Beyond the Gateway (Wed, 29 Jul 2026 09:00:00 GMT)
- `💻 Tech` `📡 RSS` .NET 11 Preview 6 Modernises MAUI CollectionView and Android Shell (Wed, 29 Jul 2026 08:00:00 GMT)
- `💻 Tech` `📡 RSS` GitHub Introduces Default "Cooldown" Policy for Dependabot Version Updates (Tue, 28 Jul 2026 19:00:00 GMT)
- `💻 Tech` `📡 RSS` Grafana Assistant Expands to More Than 30 Data Sources (Tue, 28 Jul 2026 12:00:00 GMT)
- `💻 Tech` `📡 RSS` Presentation: The Future of Engineering: Mindsets That Matter When Code Isn’t Enough (Tue, 28 Jul 2026 11:10:00 GMT)
- `💻 Tech` `📡 RSS` Remix 3 Beta Preview Ditches React for a Web-Standards Full-Stack Framework (Tue, 28 Jul 2026 09:02:00 GMT)
- `💻 Tech` `📡 RSS` Article: The Hard-Stop Rule: From 3 HCM Monoliths to 120 Domain Microservices (Tue, 28 Jul 2026 09:00:00 GMT)
- `💻 Tech` `📡 RSS` AWS Launches Amazon GuardDuty Investigation Agent to Automate Threat Triage (Tue, 28 Jul 2026 07:14:00 GMT)

### 📰 MIT Tech Review AI (27 noticias)

- `💻 Tech` `📡 RSS` El Índice de Hype de la IA: IA sin glamour (Wed, 29 Jul 2026 08:42:57 +0000)
- `💻 Tech` `📡 RSS` Los trabajadores de chips de Samsung se están pasando a su rival SK Hynix (Tue, 28 Jul 2026 09:18:57 +0000)
- `💻 Tech` `📡 RSS` OpenAI calificó el ataque a Hugging Face como sin precedentes. Pero ya hemos estado aquí antes. (Mon, 27 Jul 2026 18:00:00 +0000)
- `💻 Tech` `📡 RSS` El camino hacia la superinteligencia artificial (Mon, 27 Jul 2026 12:00:00 +0000)
- `💻 Tech` `📡 RSS` Cerrando el ciclo de datos en el descubrimiento de fármacos impulsado por IA (Mon, 27 Jul 2026 11:40:16 +0000)
- `💻 Tech` `📡 RSS` Construyendo el entorno empresarial para IA agéntica (Mon, 27 Jul 2026 11:32:58 +0000)
- `💻 Tech` `📡 RSS` Cómo la IA ayuda a los científicos a diseñar la próxima generación de medicamentos (Thu, 23 Jul 2026 12:00:00 +0000)
- `💻 Tech` `📡 RSS` Advancing next-gen AI with materials science innovation (Tue, 21 Jul 2026 10:37:34 +0000)
- `💻 Tech` `📡 RSS` Los modelos de IA de China tienen al mundo de la IA de Trump en guerra consigo mismo (Mon, 20 Jul 2026 18:00:00 +0000)
- `💻 Tech` `📡 RSS` AI is more likely than humans to form biases when hiring (Mon, 20 Jul 2026 08:39:01 +0000)

### 📰 Search Engine Journal (135 noticias)

- `💻 Tech` `📡 RSS` Google’s Mueller: Fix Conflicting Metadata, Don’t Test It via @sejournal, @MattGSouthern (Wed, 29 Jul 2026 10:30:57 +0000)
- `💻 Tech` `📡 RSS` Google’s Illyes Unsure On Shifting unavailable_after Dates via @sejournal, @MattGSouthern (Wed, 29 Jul 2026 07:00:06 +0000)
- `💻 Tech` `📡 RSS` AI Recognizes 96% Of Brands But Mentions Almost None, New Study Finds (Wed, 29 Jul 2026 05:00:32 +0000)
- `💻 Tech` `📡 RSS` Google On SEO Impact Of URLs Injected Into HTML By CMS Platforms via @sejournal, @martinibuster (Wed, 29 Jul 2026 00:38:31 +0000)
- `💻 Tech` `📡 RSS` AI Opt-Out May Cost Sites A Google Top Stories Spot via @sejournal, @MattGSouthern (Tue, 28 Jul 2026 21:20:40 +0000)
- `💻 Tech` `📡 RSS` The Future Of Search & AI: What I Learned From Google’s Latest Earnings Call via @sejournal, @marie_haynes (Tue, 28 Jul 2026 19:00:06 +0000)
- `💻 Tech` `📡 RSS` Heavily AI-Flagged Pages Still Rank Across Google’s Top 10 via @sejournal, @MattGSouthern (Tue, 28 Jul 2026 18:06:52 +0000)
- `💻 Tech` `📡 RSS` Google Lost Its Scraping Case – Now You Have To Pick A Side On The Open Web via @sejournal, @slobodanmanic (Tue, 28 Jul 2026 17:30:13 +0000)
- `💻 Tech` `📡 RSS` Why Data Integrity Is The New Technical SEO: From Crawling To Trust via @sejournal, @alexmoss (Tue, 28 Jul 2026 14:30:34 +0000)
- `💻 Tech` `📡 RSS` Amazon Left US Google Shopping A Year Ago & Never Came Back via @sejournal, @brookeosmundson (Tue, 28 Jul 2026 12:00:43 +0000)

### 📰 Wired AI (405 noticias)

- `💻 Tech` `📡 RSS` Los mejores Switches Ethernet: Rápidos, Fiables y Seguros (Wed, 29 Jul 2026 10:30:00 +0000)
- `💻 Tech` `📡 RSS` Más errores tipográficos, menos guiones largos: Los escritores están creando una 'contracultura literaria' anti-IA (Wed, 29 Jul 2026 10:30:00 +0000)
- `💻 Tech` `📡 RSS` Cómo revivir un pozo geotérmico (Wed, 29 Jul 2026 10:00:00 +0000)
- `💻 Tech` `📡 RSS` Los Boomers no pueden dejar de regalar a sus nietos libros basura generados por IA (Wed, 29 Jul 2026 09:30:00 +0000)
- `💻 Tech` `📡 RSS` El nuevo modelo 3D de la NASA muestra que la Tierra es un amasijo irregular (Wed, 29 Jul 2026 09:30:00 +0000)
- `💻 Tech` `📡 RSS` Los nuevos contratos de los centros de detención de ICE declaran que las leyes estatales 'no se aplicarán' (Wed, 29 Jul 2026 09:00:00 +0000)
- `💻 Tech` `📡 RSS` Códigos promocionales de Therabody: 15% de descuento en julio de 2026 (Wed, 29 Jul 2026 05:00:00 +0000)
- `💻 Tech` `📡 RSS` Códigos promocionales de Braun: 15% de descuento en julio (Wed, 29 Jul 2026 05:00:00 +0000)
- `💻 Tech` `📡 RSS` El agente de IA rebelde de OpenAI hackeó más que solo Hugging Face. (Wed, 29 Jul 2026 00:15:30 +0000)
- `💻 Tech` `📡 RSS` Un error tipográfico envió a un gamer inocente a prisión por 18 meses (Tue, 28 Jul 2026 23:30:00 +0000)

### 📰 Dev.to (3854 noticias)

- `💻 Tech` `📡 RSS` Desarrollo impulsado por IA: Transformando los flujos de trabajo de software en 2026 (Wed, 29 Jul 2026 10:32:56 +0000)
- `💻 Tech` `📡 RSS` Automatizando la copia de seguridad de Dell PowerProtect en AWS: Un enfoque basado en Terraform (Wed, 29 Jul 2026 10:20:07 +0000)
- `💻 Tech` `📡 RSS` Deja de construir integraciones de IA personalizadas. Usa MCP en su lugar. (Wed, 29 Jul 2026 10:20:03 +0000)
- `💻 Tech` `📡 RSS` Terraform no debería desplegar en EKS. ArgoCD sí debería. (Wed, 29 Jul 2026 10:17:01 +0000)
- `💻 Tech` `📡 RSS` Prueba la voz antes de encargar el trabajo (Wed, 29 Jul 2026 10:15:11 +0000)
- `💻 Tech` `📡 RSS` El enlace estático de Go es un impuesto de seguridad del que nadie te advirtió (Wed, 29 Jul 2026 10:10:01 +0000)
- `💻 Tech` `📡 RSS` Pero _nosotros_ podemos reforzar Node.js contra la polución de prototipos (Wed, 29 Jul 2026 10:08:26 +0000)
- `💻 Tech` `📡 RSS` Facturación por suscripción: Los casos límite que la documentación de Stripe omite (Wed, 29 Jul 2026 10:00:47 +0000)
- `💻 Tech` `📡 RSS` La guía de búsqueda de IA de Google cambia el enfoque de Schema Markup a sitios web preparados para agentes (Wed, 29 Jul 2026 10:00:30 +0000)
- `💻 Tech` `📡 RSS` Crea un panel de monitorización del sistema con Python (Wed, 29 Jul 2026 10:00:10 +0000)

### 📰 Applesfera (185 noticias)

- `💻 Tech` Hoy en Apple TV, lo que parecía una comedia romántica más y ha terminado por darle un giro de 180º al género (2026-07-28T15:01:36Z)
- `💻 Tech` La cuarta y última temporada de Silo ya tiene fecha para cerrar la historia sin (demasiada) espera (2026-07-28T17:01:36Z)
- `💻 Tech` Sabíamos que Steve Jobs fue un visionario, pero no tanto. Se adelantó 40 años prediciendo cómo sería la inteligencia artificial (2026-07-28T16:01:36Z)
- `💻 Tech` Un reconocido analista augura el colapso de la inteligencia artificial y asegura que Apple "lo verá arder" desde la barrera (2026-07-28T14:01:36Z)
- `💻 Tech` Sara Carbonero avisa como madre y periodista: "El futuro de nuestros hijos no podemos dejárselo solo a un algoritmo" (2026-07-28T12:01:36Z)
- `💻 Tech` Persianistas y metalistas se ponen de acuerdo: “por esta zona de la casa estás tirando el frío del aire acondicionado” (2026-07-28T12:24:53Z)
- `💻 Tech` Comprar un iPhone o MacBook cambiará en Europa. No será lo único y la culpa la tiene un nuevo código QR obligatorio (2026-07-28T07:01:36Z)
- `💻 Tech` Apple lanza oficialmente iOS 26.6. Parece una actualización menor, pero puede ser crucial para que iOS 27 vaya bien en tu iPhone
- `💻 Tech` iOS 27 libera quita el freno a la memoria RAM para acercarlo más que nunca a un ordenador (2026-07-27T16:01:36Z)
- `💻 Tech` WhatsApp prueba un cambio en los chats del iPhone. Tienen un aire sospechoso a iMessage (2026-07-27T15:01:36Z)

### 📰 ADSL Zone (239 noticias)

- `💻 Tech` Telefónica confirma la tendencia y crece en ingresos y EBITDA durante los primeros seis meses del año (29 de julio, 2026 • 08:13)
- `💻 Tech` Los canales de fútbol de Orange TV vuelven a la normalidad: esto es lo que cambia de su parrilla (28 de julio, 2026 • 21:56)
- `💻 Tech` Uno de los móviles más potentes y deseados de Xiaomi Redmi tiene más de 150 € de descuento en AliExpress (28 de julio, 2026 • 21:08)
- `💻 Tech` A media hora de Madrid: el centro comercial que abrirá este año y que ya roza el 100 % de tiendas confirmadas (28 de julio, 2026 • 18:32)
- `💻 Tech` Quién quiere la Garmin Cirqa teniendo este Forerunner con pantalla AMOLED y GPS por el mismo precio gracias a PcComponentes (28 de julio, 2026 • 18:17)
- `💻 Tech` Adiós al 4K en Disney+: los clientes Premium denuncian el cambio y piden que les devuelvan el dinero (28 de julio, 2026 • 17:43)
- `💻 Tech` Camp Rock 3, más de Star Wars y otros estrenos destacados de Disney+ para agosto (28 de julio, 2026 • 14:39)
- `💻 Tech` MasOrange crece un 1,3% y supera los 3.700 millones durante los primeros seis meses del año (28 de julio, 2026 • 09:15)
- `💻 Tech` PcComponentes tiene el Mini PC perfecto si buscas 1TB y 32 GB de memoria RAM (27 de julio, 2026 • 21:06)
- `💻 Tech` Qué son las novias IA que China ha tenido que prohibir porque han hecho peligrar su índice de natalidad (27 de julio, 2026 • 20:02)

### 📰 MuyComputer (181 noticias)

- `💻 Tech` NoticiasHace 23 segundosOpenAI prepara su gran salto al hardwareOpenAI lleva varios años dejando claro que no quiere limitarse a desarrollar modelos y servicios que funcionen dentro de los...
- `💻 Tech` A FondoHace 50 minutosIA y tecnología contra incendios forestales
- `💻 Tech` NoticiasHace 1 minutoEl Galaxy Z TriFold regresará con más ambiciónCuando Samsung presentó el Galaxy Z TriFold a finales de 2025, lo hizo como uno de los dispositivos más ambiciosos...
- `💻 Tech` NoticiasHace 2 horasApple AI glasses: menos Vision Pro, más IA, 2027
- `💻 Tech` NoticiasHace 3 horasGTA VI y la sombra del downgrade gráfico: hay miedo, y está justificadoSi algo es demasiado bueno para ser cierto lo más probable es que no sea lo que aparenta. Esa es...
- `💻 Tech` NoticiasHace 28 segundosNuevo driver GeForce Game Ready y novedades RTX de la semanaNVIDIA ha lanzado un nuevo driver GeForce Game Ready que trae diferentes correcciones de errores y optimizaciones, y que ya...
- `💻 Tech` NoticiasHace 20 minutosOfertas por la vuelta al cole en PCSpecialist en PCs y portátiles
- `💻 Tech` NoticiasHace 2 horasRadeon RX 9050: especificaciones completas
- `💻 Tech` NoticiasHace 4 horasLas tarjetas gráficas GeForce RTX volverán a subir de precio por la crisis de la DRAM
- `💻 Tech` A FondoHace 3 minutosAnthropic, Google y OpenAI no quieren modelos de IA de peso abierto25 importantes empresas tecnológicas, organizaciones industriales y firmas de capital riesgo, han publicado una carta abierta instando a los responsables...

### 📰 ComputerHoy (242 noticias)

- `💻 Tech` ¿Puede la IA ayudar a automatizar tu casa? Los riesgos y beneficios de dejar tu hogar en sus manos
- `💻 Tech` Su pasión por el juego Skyrim le hizo pasar 18 meses en la cárcel: no tenía la culpa de nada
- `💻 Tech` El Ministerio de Ciencia y la ONCE regalan dos millones de gafas homologadas gratis para ver el eclipse del 12 de agosto: hay dos formas de conseguirlas
- `💻 Tech` Steve Jobs, cofundador de Apple: "El único problema de Microsoft es que no tienen absolutamente ningún gusto. Y no lo digo en broma, no se les ocurren ideas originales y no aportan mucha cultura a sus productos"
- `💻 Tech` VT Security, experto en Linux y ciberseguridad: "Hay un mundo más allá de Ubuntu y Arch... Existen usuarios súper atrincherados que desafían el tiempo con sus sistemas únicos"
- `💻 Tech` Nothing prepara su primer reloj inteligente: lo que sabemos del smartwatch con el que quiere plantar cara a Xiaomi y Samsung
- `💻 Tech` Dario Amodei, CEO de Anthropic, se defiende de las acusaciones: "Nunca hemos pedido prohibir los modelos de IA de código abierto"
- `💻 Tech` Si no ves las líneas de tráfico en Google Maps, no eres el único: el nuevo error de Google Maps no tiene solución (por ahora)
- `💻 Tech` Tendrás batería de sobra para todo el día y una pantalla sin reflejos: así es el ordenador que he probado varias semanas
- `💻 Tech` A partir de agosto Microsoft usará el chip TPM de los PC para bloquear por hardware los Windows pirateados

### 📰 Hipertextual (193 noticias)

- `💻 Tech` Los nuevos móviles de Samsung han copiado una de las funciones más útiles del iPhone
- `💻 Tech` Mira el genial tráiler de ‘Jumanji 3: Mundo abierto’, la última película de la saga
- `💻 Tech` Google Maps resuelve un fallo que podía meterte en un embotellamiento
- `💻 Tech` Samsung copia la función más polémica de las Ray-Ban Meta en sus nuevas gafas inteligentes
- `💻 Tech` Anthropic revela que Claude es capaz de romper el cifrado que protege a medio internet
- `💻 Tech` «Es inaceptable»: Xbox se pronuncia tras el caos por su caída mundial
- `💻 Tech` Apple prepara su respuesta al Google Nest Hub y el Amazon Echo Show, de la mano de Siri AI
- `💻 Tech` ¿Adiós a las operaciones de vista? Estas gafas inteligentes restauran la visión borrosa en pocos días
- `💻 Tech` ¿Cocina pequeña? Xiaomi ha lanzado un frigorífico con puertas francesas que puedes poner. Y encima es baratísimo
- `💻 Tech` GTA 6 dispara la fiebre de los vídeos falsos hechos con IA, que acumulan millones de reproducciones

### 📰 Hugging Face Blog (58 noticias)

- `💻 Tech` Visión General del Modelo FLUX 3: Modelos de Flujo Multimodales para la Predicción de Imagen, Video, Audio y Acción (2026-07-24T03:57:45)
- `💻 Tech` El modelo de pronóstico de IA del ECMWF es de código abierto: ahora hagamos que sea fácil de ejecutar. (2026-07-28T15:16:42)
- `💻 Tech` El estado de la simulación para la IA física: Una visión general (2026-07-21T20:00:27)
- `💻 Tech` La afluencia de modelos especializados en la clasificación de Open SLM. (2026-07-23T11:58:32)
- `💻 Tech` Hugging Face en AMD Instinct MI455X: Primeros resultados de Transformers (2026-07-23T21:56:43)
- `💻 Tech` POCKET: un modelo de 35 mil millones de parámetros que se ejecuta en tu iPhone — y en tu PC sin GPU (2026-07-23T04:14:44)
- `💻 Tech` Presentando Cosmos 3 Edgenvidia (2026-07-20T15:58:51)
- `💻 Tech` When will language models be good enough?craffel•4 days ago•5 (2026-07-16T20:17:17)
- `💻 Tech` Be Ready Before the Attack: A Practical Guide to Self-Hosting an Open Model for Cyber Defensejeffboudier•about 8 hours ago•5 (2026-07-20T18:51:06)
- `💻 Tech` Afina modelos de vídeo e imagen a escala con NVIDIA NeMo Automodel y 🤗 Diffusers (2026-07-17T15:57:54)

### 📰 Ars Technica (231 noticias)

- `💻 Tech` `📡 RSS` Audi tiene un nuevo buque insignia diseñado pensando en EE. UU.: El 2027 Q9 (Wed, 29 Jul 2026 01:00:36 +0000)
- `💻 Tech` `📡 RSS` Reaction wheel failures leave Swift rescue mission spinning in orbit (Tue, 28 Jul 2026 22:09:00 +0000)
- `💻 Tech` `📡 RSS` College lab class ends with 32 people on antibiotics for deadly germ exposure (Tue, 28 Jul 2026 21:49:52 +0000)
- `💻 Tech` `📡 RSS` We now have a better understanding how OpenAI hacked into Hugging Face (Tue, 28 Jul 2026 21:36:39 +0000)
- `💻 Tech` `📡 RSS` eBay pays $46M to journalists it targeted in bizarre harassment campaign (Tue, 28 Jul 2026 21:02:15 +0000)
- `💻 Tech` `📡 RSS` Study: Dinosaurs were charbroiled after Chicxulub impact (Tue, 28 Jul 2026 20:51:45 +0000)
- `💻 Tech` `📡 RSS` Philly suburb: Sure, build that data center—but first meet our 43 demands (Tue, 28 Jul 2026 20:43:19 +0000)
- `💻 Tech` `📡 RSS` Despite AI hype, Google's data shows workers aren't automating themselves away (Tue, 28 Jul 2026 20:20:20 +0000)
- `💻 Tech` `📡 RSS` Nueva aeronave bate récord volando 24 horas sin escalas de Australia a Francia (Tue, 28 Jul 2026 18:43:36 +0000)
- `💻 Tech` `📡 RSS` Juez bloquea la primera ley estatal que habría prohibido los mercados de predicción (Tue, 28 Jul 2026 18:31:13 +0000)

### 📰 TechCrunch (78 noticias)

- `💻 Tech` Cyera acuerda adquirir Oasis Security por 1.000 millones de dólares para salvaguardar la proliferación de agentes de IA. (2026-07-28T17:09:05-07:00)
- `💻 Tech` Fish Audio recauda 50 millones de dólares en financiación inicial para construir modelos de voz con IA para creadores y empresas (2026-07-28T07:00:00-07:00)
- `💻 Tech` Recursive Superintelligence firma un acuerdo de computación de 410 dólares con Amazon (2026-07-28T06:19:17-07:00)
- `💻 Tech` Dario Amodei de Anthropic responde: no se opone a los modelos de peso abierto, pero teme a la IA china (2026-07-27T17:13:33-07:00)
- `💻 Tech` Microsoft lanza su primer modelo de ciberseguridad, además de un nuevo sistema de ciberseguridad agéntico (2026-07-27T11:32:11-07:00)
- `💻 Tech` Monday.com es la última empresa tecnológica en culpar a la IA de los despidos — aquí hay otras 20 (2026-07-25T18:30:00-07:00)
- `💻 Tech` Una línea eléctrica caída expuso un problema creciente en los centros de datos de IA. Así es como se soluciona. (2026-07-25T06:05:00-07:00)
- `💻 Tech` How AI guardrails are impeding the work of offensive cybersecurity researchers (2026-07-23T18:00:00-07:00)
- `💻 Tech` OpenAI afirma que Hugging Face fue vulnerado por sus modelos de pre-lanzamiento (2026-07-21T13:56:55-07:00)
- `💻 Tech` X relanza una aplicación Android reconstruida tras un esfuerzo de un año (2026-07-20T12:37:39-07:00)

### 📰 MarkTechPost (88 noticias)

- `💻 Tech` Building Non-Interactive Agentic Coding Workflows with Moonshot AI’s Kimi CLI, JSONL Streaming, Testing, and Session Memory (2026-07-28T16:04:44-07:00)
- `💻 Tech` Fireworks AI Releases Fireworks Nexus: A Drop-In Routing and Cost-Control Layer That Moves Routine Coding Work to Open-Weight Models
- `💻 Tech` Microsoft AI Releases MAI-Cyber-1-Flash: A 5B-Active-Parameter Cyber Model That Pushes MDASH to 95.95% on CyberGym (2026-07-28T01:33:30-07:00)
- `💻 Tech` Deploying a 1-Bit Bonsai-27B Model with PrismML llama.cpp and OpenAI-Compatible Local Inference Workflows
- `💻 Tech` Kimi AI and kvcache-ai Open Sources ‘AgentENV’: A Distributed System that Powers Agentic Reinforcement Learning (RL) Training for Kimi K3 (2026-07-27T13:48:53-07:00)
- `💻 Tech` Designing Skill-Driven Financial Analysis Agents with Claude, Python, MCP Connectors, and Automated Deliverables (2026-07-27T11:08:24-07:00)
- `💻 Tech` Perplexity Releases pplx, a Single-Binary CLI That Puts Its Search API in the Terminal for Coding Agents
- `💻 Tech` KwaiKAT Team Releases KAT-Coder-V2.5: An Agentic Coding Model Trained on 100,000+ Verifiable Repository Environments (2026-07-26T03:46:19-07:00)
- `💻 Tech` Induction Labs Photon-1 Simulates Desktops, Plays Checkers, and Models Billiard Physics From One Pretraining Run
- `💻 Tech` FAIRChem v2 UMA for Multidomain Atomistic Simulation across Molecules, Catalysts, Materials, Vibrations, and Molecular Dynamics

### 📰 TechCrunch AI (187 noticias)

- `💻 Tech` `📡 RSS` Bot-detection startup Spur nabs $200M from Insight (Tue, 28 Jul 2026 21:29:34 +0000)
- `💻 Tech` `📡 RSS` La startup de MCP Runlayer acusa a Rippling de robar su idea de producto (Tue, 28 Jul 2026 20:45:12 +0000)
- `💻 Tech` `📡 RSS` Sam Altman está listo para desacelerar (Tue, 28 Jul 2026 20:17:08 +0000)
- `💻 Tech` `📡 RSS` Los centros de datos podrían enfrentar cortes de energía temporales para evitar apagones en la red eléctrica más grande de EE. UU. (Tue, 28 Jul 2026 15:42:26 +0000)
- `💻 Tech` `📡 RSS` Cursor realiza su mayor impulso en India hasta la fecha antes de la adquisición de SpaceX con precios localizados (Tue, 28 Jul 2026 04:30:00 +0000)
- `💻 Tech` `📡 RSS` Satya Nadella dice que las empresas que confían en una sola IA para todo podrían no sobrevivir (Mon, 27 Jul 2026 21:17:11 +0000)
- `💻 Tech` `📡 RSS` PSA: Your Claude shared chats and Artifacts may have ended up on Google (Mon, 27 Jul 2026 20:19:42 +0000)
- `💻 Tech` `📡 RSS` La brecha de seguridad de Hugging Face de OpenAI ha reavivado el debate sobre la alineación y el control (Mon, 27 Jul 2026 17:28:42 +0000)
- `💻 Tech` `📡 RSS` Los usuarios de Threads ya pueden chatear con Meta AI en sus DMs (Mon, 27 Jul 2026 16:45:24 +0000)
- `💻 Tech` `📡 RSS` Google’s AI search is rapidly becoming the default, new data shows (Mon, 27 Jul 2026 15:57:12 +0000)

### 📰 NVIDIA Blog (22 noticias)

- `💻 Tech` Cómputo potente tan compacto que es indispensable — Desarrolla IA en cualquier lugar con NVIDIA Jetson
- `💻 Tech` La supercomputadora de IA de NVIDIA entra en funcionamiento en la Escuela de Posgrado Naval
- `💻 Tech` Fabricado en Fort Worth: Wistron inaugura una planta de fabricación avanzada para producir sistemas de IA de NVIDIA
- `💻 Tech` En SIGGRAPH, NVIDIA avanza en gráficos y simulación con IA agéntica y física
- `💻 Tech` Bristol Myers Squibb construye la fábrica de IA más avanzada de la industria de las ciencias de la vida en NVIDIA Vera Rubin
- `💻 Tech` NVIDIA y Japón Llevan la IA y Robótica Full-Stack a Todas las Industrias
- `💻 Tech` Nemotron Labs: Cómo los modelos abiertos brindan a empresas y naciones una IA en la que pueden confiar, controlar y personalizar.
- `💻 Tech` NVIDIA Nemotron Achieves Benchmark-Leading Performance With LangChain Deep Agents Harness (2026-07-08T08:00:27-07:00)
- `💻 Tech` NVIDIA Desbloquea la Computación de IA a Escala, Invitando a Socios de Capital para Impulsar la Construcción de Infraestructura de IA
- `💻 Tech` NVIDIA y Socios Construyen en América, para América

### 📰 freeCodeCamp (64 noticias)

- `💻 Tech` Ingeniería de Prompt vs. Loop: Una guía para desarrolladores
- `💻 Tech` Una guía para la arquitectura moderna de formularios en React: TanStack Form + Zod + Shadcn
- `💻 Tech` El manual de pipelines ETL: Cómo construir un pipeline listo para producción en Python
- `💻 Tech` Cómo Diagnosticar Errores en Producción Cuando No Puedes Reproducirlos Localmente
- `💻 Tech` Cómo Usar Prompt Engineering y Context Engineering para Agentes de IA
- `💻 Tech` Cómo Construir un Agente de IA con Function Calling en Node.js Usando Google Gemini
- `💻 Tech` El Nuevo Stack para Agencias: Cómo las Empresas de Desarrollo Usan Claude, Cursor y Copilot en Producción
- `💻 Tech` Crea APIs a prueba de balas usando TypeScript en Express
- `💻 Tech` Product Experiment Counterfactual Methods for Estimating the Effects of AI Prompt Engineering
- `💻 Tech` Claude Certified Architect – Foundations: Prep for Anthropic's New Certification Exam

### 📰 The Decoder (44 noticias)

- `💻 Tech` Anthropic says its Mythos model found vulnerabilities in cryptographic algorithms that secure the internet
- `💻 Tech` Anthropic CEO Amodei doubles down on open-weight risk stance while insisting he never called for a ban
- `💻 Tech` Delhi High Court hands OpenAI a win by rejecting major Indian news agency's copyright injunction
- `💻 Tech` The AI coding tutor paradox grows as educators scramble to rethink how they test real skills
- `💻 Tech` Anthropic's Claude Opus 5 costs well below Fable 5 while matching or beating it across most benchmarks
- `💻 Tech` Microsoft's open-weight AI push is so obviously an Azure play it hurts
- `💻 Tech` Kimi K3 trails frontier US models by a wide margin on cyber exploits, and distillation may explain why
- `💻 Tech` One tampered ChatGPT link could spawn a rogue AI agent that took orders from an attacker every five minutes
- `💻 Tech` Google CEO Pichai says Gemini's next leap depends on building "much larger base models"
- `💻 Tech` Every frontier AI model tested by Britain's safety institute tried to cheat on cybersecurity evaluations

### 📰 Google AI Blog (20 noticias)

- `💻 Tech` `📡 RSS` Agentes Gestionados de la API de Gemini: 3.6 Flash, hooks y más (Tue, 28 Jul 2026 16:00:00 +0000)
- `💻 Tech` `📡 RSS` 5 formas en que el Modo IA en la Búsqueda te ayuda a disfrutar del mundo real (Tue, 28 Jul 2026 13:00:00 +0000)
- `💻 Tech` `📡 RSS` 5 maneras de organizar la cena definitiva con la Búsqueda de Google (Tue, 28 Jul 2026 13:00:00 +0000)
- `💻 Tech` `📡 RSS` 3 Google updates from Galaxy Unpacked 2026 (Wed, 22 Jul 2026 13:00:00 +0000)
- `💻 Tech` `📡 RSS` Connect more of your apps to Search (Thu, 16 Jul 2026 16:00:00 +0000)
- `💻 Tech` `📡 RSS` Create, edit and star in videos with two Google Vids updates (Thu, 16 Jul 2026 16:00:00 +0000)
- `💻 Tech` `📡 RSS` Celebrando 25 años de innovación en búsqueda visual (Tue, 14 Jul 2026 16:00:00 +0000)
- `💻 Tech` `📡 RSS` Ampliando los agentes gestionados en la Gemini API: tareas en segundo plano, MCP remoto y más (Tue, 07 Jul 2026 08:54:00 +0000)
- `💻 Tech` `📡 RSS` Las últimas noticias de IA que anunciamos en junio de 2026 (Wed, 01 Jul 2026 18:15:00 +0000)
- `💻 Tech` `📡 RSS` Educadores y líderes de la industria de la ciudad de Nueva York se reunieron en las oficinas de Google para dar forma al futuro de la IA en las aulas. (Wed, 01 Jul 2026 16:00:00 +0000)

### 📰 El País Tecnología (38 noticias)

- `💻 Tech` Amigos digitales con IA, la nueva amenaza para la salud mental de los adolescentes (2026-07-28T05:30:01+02:00)
- `💻 Tech` El problema de los clips ya está aquí: las IA pueden destruir el mundo sin querer (2026-07-26T05:30:01+02:00)
- `💻 Tech` Cuando el león de la IA se escapa de la jaula (2026-07-26T05:30:01+02:00)
- `💻 Tech` Cuando la inteligencia artificial pone a prueba el Pacto Verde Europeo (2026-07-25T05:30:01+02:00)
- `💻 Tech` Así funciona Kimi K3, la IA china que asusta a Silicon Valley (2026-07-23T05:30:01+02:00)
- `💻 Tech` Un nuevo modelo de OpenAI provoca un ataque “sin precedentes” contra otra plataforma de inteligencia artificial (2026-07-22T13:50:39+02:00)
- `💻 Tech` ‘Captchas’: ¿Ha logrado Google que todos entrenemos a su IA sin saberlo? (2026-07-22T05:30:01+02:00)
- `💻 Tech` Thais Ruiz de Alda, tecnóloga y abogada: “El ‘tecnobro’ es el primo del ‘cryptobro’” (2026-07-22T05:30:01+02:00)
- `💻 Tech` Cuando el conocimiento de internet ya no es suficiente: la IA les pone el ojo a las librerías de segunda mano (2026-07-21T05:30:00+02:00)
- `💻 Tech` Europa obliga a identificar la IA: quiénes y cómo deberán advertir que publican contenido artificial (2026-07-20T14:45:34+02:00)

### 📰 Smashing Magazine (8 noticias)

- `💻 Tech` Thinking Outside The Box: Digital Design In The AI Era (2026-07-28)
- `💻 Tech` Weaponizing And Defending The React Flight Protocol: Deserialization Sinks In RSCs (2026-07-21)
- `💻 Tech` When It Makes Sense To “Block” The Main Thread (2026-07-17)
- `💻 Tech` No, People Don’t Want More AI In Their Life (2026-07-15)
- `💻 Tech` Matching AI Modality To User Intent: Designing The Right Interface (2026-07-02)
- `💻 Tech` Designing With Uncertainty: How AI Supercharges Probabilistic Thinking (2026-06-16)
- `💻 Tech` How To Make Your Design System AI-Ready (2026-06-03)
- `💻 Tech` Algorithmic Theming Engines: Building Self-Correcting Color Systems Withcontrast-color() (2026-05-28)

### 📰 Stack Overflow Blog (22 noticias)

- `💻 Tech` `📡 RSS` You need reliable AI context for your site reliability​​​​‌﻿‍﻿​‍​‍‌‍﻿﻿‌﻿​‍‌‍‍‌‌‍‌﻿‌‍‍‌‌‍﻿‍​‍​‍​﻿‍‍​‍​‍‌﻿​﻿‌‍​‌‌‍﻿‍‌‍‍‌‌﻿‌​‌﻿‍‌​‍﻿‍‌‍‍‌‌‍﻿﻿​‍​‍​‍﻿​​‍​‍‌‍‍​‌﻿​‍‌‍‌‌‌‍‌‍​‍​‍​﻿‍‍​‍​‍‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​﻿‍‍​‍﻿﻿​‍﻿﻿‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍﻿﻿‌‍‍‌‌‍﻿‍‌﻿‌​‌‍‌‌‌‍﻿‍‌﻿‌​​‍﻿﻿‌‍‌‌‌‍‌​‌‍‍‌‌﻿‌​​‍﻿﻿‌‍﻿‌‌‍﻿﻿‌‍‌​‌‍‌‌​﻿﻿‌‌﻿​​‌﻿​‍‌‍‌‌‌﻿​﻿‌‍‌‌‌‍﻿‍‌﻿‌​‌‍​‌‌﻿‌​‌‍‍‌‌‍﻿﻿‌‍﻿‍​﻿‍﻿‌‍‍‌‌‍‌​​﻿﻿‌​﻿​‌​﻿​​​﻿‍‌​﻿‌​‌‍​‌‌‍​﻿​﻿‌﻿‌‍​‌​‍﻿‌‌‍‌‌‌‍​‍​﻿‌​‌‍‌‌​‍﻿‌​﻿‌​‌‍‌‍​﻿​﻿​﻿​‍​‍﻿‌​﻿‍​​﻿‍‌‌‍‌‍‌‍​‌​‍﻿‌​﻿‌‌​﻿​​‌‍‌‌​﻿‌﻿​﻿‌‍‌‍​‌​﻿​﻿‌‍‌​​﻿‍‌​﻿‌‌​﻿​﻿‌‍‌​​﻿‍﻿‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​﻿‍﻿‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​﻿﻿﻿‌‍​‍‌‍​‌‌﻿​﻿‌‍‌‌‌‌‌‌‌﻿​‍‌‍﻿​​﻿﻿‌‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​‍‌‌​﻿​﻿‌​​‌​‍‌‌​﻿​‍‌​‌‍​‍‌‌​﻿​‍‌​‌‍‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍‌‍‌‍‍‌‌‍‌​​﻿﻿‌​﻿​‌​﻿​​​﻿‍‌​﻿‌​‌‍​‌‌‍​﻿​﻿‌﻿‌‍​‌​‍﻿‌‌‍‌‌‌‍​‍​﻿‌​‌‍‌‌​‍﻿‌​﻿‌​‌‍‌‍​﻿​﻿​﻿​‍​‍﻿‌​﻿‍​​﻿‍‌‌‍‌‍‌‍​‌​‍﻿‌​﻿‌‌​﻿​​‌‍‌‌​﻿‌﻿​﻿‌‍‌‍​‌​﻿​﻿‌‍‌​​﻿‍‌​﻿‌‌​﻿​﻿‌‍‌​​‍‌‍‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​‍‌‍‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​‍‌‍‌﻿​​‌‍‌‌‌﻿​‍‌﻿​﻿‌﻿​​‌‍‌‌‌‍​﻿‌﻿‌​‌‍‍‌‌﻿‌‍‌‍‌‌​﻿﻿‌‌﻿​​‌﻿‌‌‌‍​‍‌‍﻿​‌‍‍‌‌﻿​﻿‌‍‍​‌‍‌‌‌‍‌​​‍​‍‌﻿﻿‌ (Tue, 28 Jul 2026 07:40:00 GMT)
- `💻 Tech` `📡 RSS` No Dumb Questions: What is the AI bottleneck? How does context engineering fix it?​​​​‌﻿‍﻿​‍​‍‌‍﻿﻿‌﻿​‍‌‍‍‌‌‍‌﻿‌‍‍‌‌‍﻿‍​‍​‍​﻿‍‍​‍​‍‌﻿​﻿‌‍​‌‌‍﻿‍‌‍‍‌‌﻿‌​‌﻿‍‌​‍﻿‍‌‍‍‌‌‍﻿﻿​‍​‍​‍﻿​​‍​‍‌‍‍​‌﻿​‍‌‍‌‌‌‍‌‍​‍​‍​﻿‍‍​‍​‍‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​﻿‍‍​‍﻿﻿​‍﻿﻿‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍﻿﻿‌‍‍‌‌‍﻿‍‌﻿‌​‌‍‌‌‌‍﻿‍‌﻿‌​​‍﻿﻿‌‍‌‌‌‍‌​‌‍‍‌‌﻿‌​​‍﻿﻿‌‍﻿‌‌‍﻿﻿‌‍‌​‌‍‌‌​﻿﻿‌‌﻿​​‌﻿​‍‌‍‌‌‌﻿​﻿‌‍‌‌‌‍﻿‍‌﻿‌​‌‍​‌‌﻿‌​‌‍‍‌‌‍﻿﻿‌‍﻿‍​﻿‍﻿‌‍‍‌‌‍‌​​﻿﻿‌​﻿‍‌​﻿​﻿‌‍​‍​﻿‌‍​﻿​‍‌‍‌‌​﻿‍‌​﻿​‌​‍﻿‌​﻿‍​‌‍‌‌‌‍​‍​﻿‍‌​‍﻿‌​﻿‌​​﻿‍​‌‍‌​‌‍‌‌​‍﻿‌‌‍​‍‌‍​‌​﻿‌​​﻿​‍​‍﻿‌‌‍​‍​﻿‌‌​﻿‌﻿​﻿‌​​﻿‌‍‌‍​﻿​﻿​﻿​﻿‌‍​﻿​​​﻿‌﻿​﻿​﻿​﻿​‍​﻿‍﻿‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​﻿‍﻿‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​﻿﻿﻿‌‍​‍‌‍​‌‌﻿​﻿‌‍‌‌‌‌‌‌‌﻿​‍‌‍﻿​​﻿﻿‌‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​‍‌‌​﻿​﻿‌​​‌​‍‌‌​﻿​‍‌​‌‍​‍‌‌​﻿​‍‌​‌‍‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍‌‍‌‍‍‌‌‍‌​​﻿﻿‌​﻿‍‌​﻿​﻿‌‍​‍​﻿‌‍​﻿​‍‌‍‌‌​﻿‍‌​﻿​‌​‍﻿‌​﻿‍​‌‍‌‌‌‍​‍​﻿‍‌​‍﻿‌​﻿‌​​﻿‍​‌‍‌​‌‍‌‌​‍﻿‌‌‍​‍‌‍​‌​﻿‌​​﻿​‍​‍﻿‌‌‍​‍​﻿‌‌​﻿‌﻿​﻿‌​​﻿‌‍‌‍​﻿​﻿​﻿​﻿‌‍​﻿​​​﻿‌﻿​﻿​﻿​﻿​‍​‍‌‍‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​‍‌‍‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​‍‌‍‌﻿​​‌‍‌‌‌﻿​‍‌﻿​﻿‌﻿​​‌‍‌‌‌‍​﻿‌﻿‌​‌‍‍‌‌﻿‌‍‌‍‌‌​﻿﻿‌‌﻿​​‌﻿‌‌‌‍​‍‌‍﻿​‌‍‍‌‌﻿​﻿‌‍‍​‌‍‌‌‌‍‌​​‍​‍‌﻿﻿‌ (Fri, 24 Jul 2026 16:00:00 GMT)
- `💻 Tech` `📡 RSS` Partnerships can keep open source sustainable​​​​‌﻿‍﻿​‍​‍‌‍﻿﻿‌﻿​‍‌‍‍‌‌‍‌﻿‌‍‍‌‌‍﻿‍​‍​‍​﻿‍‍​‍​‍‌﻿​﻿‌‍​‌‌‍﻿‍‌‍‍‌‌﻿‌​‌﻿‍‌​‍﻿‍‌‍‍‌‌‍﻿﻿​‍​‍​‍﻿​​‍​‍‌‍‍​‌﻿​‍‌‍‌‌‌‍‌‍​‍​‍​﻿‍‍​‍​‍‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​﻿‍‍​‍﻿﻿​‍﻿﻿‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍﻿﻿‌‍‍‌‌‍﻿‍‌﻿‌​‌‍‌‌‌‍﻿‍‌﻿‌​​‍﻿﻿‌‍‌‌‌‍‌​‌‍‍‌‌﻿‌​​‍﻿﻿‌‍﻿‌‌‍﻿﻿‌‍‌​‌‍‌‌​﻿﻿‌‌﻿​​‌﻿​‍‌‍‌‌‌﻿​﻿‌‍‌‌‌‍﻿‍‌﻿‌​‌‍​‌‌﻿‌​‌‍‍‌‌‍﻿﻿‌‍﻿‍​﻿‍﻿‌‍‍‌‌‍‌​​﻿﻿‌​﻿‌​​﻿‍‌​﻿‍‌​﻿​‍​﻿​‌​﻿​‍​﻿​​​﻿​‍​‍﻿‌​﻿​‌‌‍‌‍​﻿​﻿​﻿​‌​‍﻿‌​﻿‌​​﻿​​​﻿​﻿​﻿‌‍​‍﻿‌​﻿‍‌‌‍‌‍‌‍​‍​﻿‌﻿​‍﻿‌‌‍​‌​﻿‌﻿​﻿‍​​﻿‌‌​﻿‍​​﻿​‍​﻿‍​​﻿‌﻿​﻿​﻿​﻿​‌​﻿​﻿‌‍‌​​﻿‍﻿‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​﻿‍﻿‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​﻿﻿﻿‌‍​‍‌‍​‌‌﻿​﻿‌‍‌‌‌‌‌‌‌﻿​‍‌‍﻿​​﻿﻿‌‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​‍‌‌​﻿​﻿‌​​‌​‍‌‌​﻿​‍‌​‌‍​‍‌‌​﻿​‍‌​‌‍‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍‌‍‌‍‍‌‌‍‌​​﻿﻿‌​﻿‌​​﻿‍‌​﻿‍‌​﻿​‍​﻿​‌​﻿​‍​﻿​​​﻿​‍​‍﻿‌​﻿​‌‌‍‌‍​﻿​﻿​﻿​‌​‍﻿‌​﻿‌​​﻿​​​﻿​﻿​﻿‌‍​‍﻿‌​﻿‍‌‌‍‌‍‌‍​‍​﻿‌﻿​‍﻿‌‌‍​‌​﻿‌﻿​﻿‍​​﻿‌‌​﻿‍​​﻿​‍​﻿‍​​﻿‌﻿​﻿​﻿​﻿​‌​﻿​﻿‌‍‌​​‍‌‍‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​‍‌‍‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​‍‌‍‌﻿​​‌‍‌‌‌﻿​‍‌﻿​﻿‌﻿​​‌‍‌‌‌‍​﻿‌﻿‌​‌‍‍‌‌﻿‌‍‌‍‌‌​﻿﻿‌‌﻿​​‌﻿‌‌‌‍​‍‌‍﻿​‌‍‍‌‌﻿​﻿‌‍‍​‌‍‌‌‌‍‌​​‍​‍‌﻿﻿‌ (Fri, 24 Jul 2026 07:40:00 GMT)
- `💻 Tech` `📡 RSS` The future of development is full-stack​​​​‌﻿‍﻿​‍​‍‌‍﻿﻿‌﻿​‍‌‍‍‌‌‍‌﻿‌‍‍‌‌‍﻿‍​‍​‍​﻿‍‍​‍​‍‌﻿​﻿‌‍​‌‌‍﻿‍‌‍‍‌‌﻿‌​‌﻿‍‌​‍﻿‍‌‍‍‌‌‍﻿﻿​‍​‍​‍﻿​​‍​‍‌‍‍​‌﻿​‍‌‍‌‌‌‍‌‍​‍​‍​﻿‍‍​‍​‍‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​﻿‍‍​‍﻿﻿​‍﻿﻿‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍﻿﻿‌‍‍‌‌‍﻿‍‌﻿‌​‌‍‌‌‌‍﻿‍‌﻿‌​​‍﻿﻿‌‍‌‌‌‍‌​‌‍‍‌‌﻿‌​​‍﻿﻿‌‍﻿‌‌‍﻿﻿‌‍‌​‌‍‌‌​﻿﻿‌‌﻿​​‌﻿​‍‌‍‌‌‌﻿​﻿‌‍‌‌‌‍﻿‍‌﻿‌​‌‍​‌‌﻿‌​‌‍‍‌‌‍﻿﻿‌‍﻿‍​﻿‍﻿‌‍‍‌‌‍‌​​﻿﻿‌​﻿‌﻿‌‍‌​​﻿​﻿‌‍‌‍​﻿‍​‌‍​‌‌‍‌‌‌‍‌‌​‍﻿‌​﻿‍​​﻿​​​﻿‍​‌‍‌​​‍﻿‌​﻿‌​​﻿​﻿​﻿‌‍​﻿‌‍​‍﻿‌​﻿‍​​﻿​‍​﻿‌﻿​﻿​‌​‍﻿‌‌‍​﻿​﻿‌‍‌‍‌​‌‍​‍​﻿‌﻿​﻿‍​‌‍‌​​﻿​﻿​﻿‍​​﻿​‌​﻿​‌‌‍‌​​﻿‍﻿‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​﻿‍﻿‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​﻿﻿﻿‌‍​‍‌‍​‌‌﻿​﻿‌‍‌‌‌‌‌‌‌﻿​‍‌‍﻿​​﻿﻿‌‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​‍‌‌​﻿​﻿‌​​‌​‍‌‌​﻿​‍‌​‌‍​‍‌‌​﻿​‍‌​‌‍‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍‌‍‌‍‍‌‌‍‌​​﻿﻿‌​﻿‌﻿‌‍‌​​﻿​﻿‌‍‌‍​﻿‍​‌‍​‌‌‍‌‌‌‍‌‌​‍﻿‌​﻿‍​​﻿​​​﻿‍​‌‍‌​​‍﻿‌​﻿‌​​﻿​﻿​﻿‌‍​﻿‌‍​‍﻿‌​﻿‍​​﻿​‍​﻿‌﻿​﻿​‌​‍﻿‌‌‍​﻿​﻿‌‍‌‍‌​‌‍​‍​﻿‌﻿​﻿‍​‌‍‌​​﻿​﻿​﻿‍​​﻿​‌​﻿​‌‌‍‌​​‍‌‍‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​‍‌‍‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​‍‌‍‌﻿​​‌‍‌‌‌﻿​‍‌﻿​﻿‌﻿​​‌‍‌‌‌‍​﻿‌﻿‌​‌‍‍‌‌﻿‌‍‌‍‌‌​﻿﻿‌‌﻿​​‌﻿‌‌‌‍​‍‌‍﻿​‌‍‍‌‌﻿​﻿‌‍‍​‌‍‌‌‌‍‌​​‍​‍‌﻿﻿‌ (Tue, 21 Jul 2026 07:40:00 GMT)
- `💻 Tech` `📡 RSS` Developers who move fast still need to do it together​​​​‌﻿‍﻿​‍​‍‌‍﻿﻿‌﻿​‍‌‍‍‌‌‍‌﻿‌‍‍‌‌‍﻿‍​‍​‍​﻿‍‍​‍​‍‌﻿​﻿‌‍​‌‌‍﻿‍‌‍‍‌‌﻿‌​‌﻿‍‌​‍﻿‍‌‍‍‌‌‍﻿﻿​‍​‍​‍﻿​​‍​‍‌‍‍​‌﻿​‍‌‍‌‌‌‍‌‍​‍​‍​﻿‍‍​‍​‍‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​﻿‍‍​‍﻿﻿​‍﻿﻿‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍﻿﻿‌‍‍‌‌‍﻿‍‌﻿‌​‌‍‌‌‌‍﻿‍‌﻿‌​​‍﻿﻿‌‍‌‌‌‍‌​‌‍‍‌‌﻿‌​​‍﻿﻿‌‍﻿‌‌‍﻿﻿‌‍‌​‌‍‌‌​﻿﻿‌‌﻿​​‌﻿​‍‌‍‌‌‌﻿​﻿‌‍‌‌‌‍﻿‍‌﻿‌​‌‍​‌‌﻿‌​‌‍‍‌‌‍﻿﻿‌‍﻿‍​﻿‍﻿‌‍‍‌‌‍‌​​﻿﻿‌​﻿‍​​﻿‍​‌‍‌‍​﻿‌‌​﻿​‍‌‍‌​​﻿‌﻿‌‍​‍​‍﻿‌‌‍‌‌‌‍‌​​﻿​﻿​﻿‌‌​‍﻿‌​﻿‌​‌‍‌​​﻿​‍​﻿​﻿​‍﻿‌​﻿‍‌​﻿​​​﻿‌​‌‍‌‌​‍﻿‌‌‍‌‌​﻿​‌‌‍​﻿​﻿​﻿​﻿​​​﻿‌‍​﻿‍​​﻿‌‌​﻿​‍‌‍‌‌​﻿‌﻿​﻿‌﻿​﻿‍﻿‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​﻿‍﻿‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​﻿﻿﻿‌‍​‍‌‍​‌‌﻿​﻿‌‍‌‌‌‌‌‌‌﻿​‍‌‍﻿​​﻿﻿‌‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​‍‌‌​﻿​﻿‌​​‌​‍‌‌​﻿​‍‌​‌‍​‍‌‌​﻿​‍‌​‌‍‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍‌‍‌‍‍‌‌‍‌​​﻿﻿‌​﻿‍​​﻿‍​‌‍‌‍​﻿‌‌​﻿​‍‌‍‌​​﻿‌﻿‌‍​‍​‍﻿‌‌‍‌‌‌‍‌​​﻿​﻿​﻿‌‌​‍﻿‌​﻿‌​‌‍‌​​﻿​‍​﻿​﻿​‍﻿‌​﻿‍‌​﻿​​​﻿‌​‌‍‌‌​‍﻿‌‌‍‌‌​﻿​‌‌‍​﻿​﻿​﻿​﻿​​​﻿‌‍​﻿‍​​﻿‌‌​﻿​‍‌‍‌‌​﻿‌﻿​﻿‌﻿​‍‌‍‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​‍‌‍‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​‍‌‍‌﻿​​‌‍‌‌‌﻿​‍‌﻿​﻿‌﻿​​‌‍‌‌‌‍​﻿‌﻿‌​‌‍‍‌‌﻿‌‍‌‍‌‌​﻿﻿‌‌﻿​​‌﻿‌‌‌‍​‍‌‍﻿​‌‍‍‌‌﻿​﻿‌‍‍​‌‍‌‌‌‍‌​​‍​‍‌﻿﻿‌ (Fri, 17 Jul 2026 07:40:00 GMT)
- `💻 Tech` `📡 RSS` Your AI is only as responsible as you are​​​​‌﻿‍﻿​‍​‍‌‍﻿﻿‌﻿​‍‌‍‍‌‌‍‌﻿‌‍‍‌‌‍﻿‍​‍​‍​﻿‍‍​‍​‍‌﻿​﻿‌‍​‌‌‍﻿‍‌‍‍‌‌﻿‌​‌﻿‍‌​‍﻿‍‌‍‍‌‌‍﻿﻿​‍​‍​‍﻿​​‍​‍‌‍‍​‌﻿​‍‌‍‌‌‌‍‌‍​‍​‍​﻿‍‍​‍​‍‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​﻿‍‍​‍﻿﻿​‍﻿﻿‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍﻿﻿‌‍‍‌‌‍﻿‍‌﻿‌​‌‍‌‌‌‍﻿‍‌﻿‌​​‍﻿﻿‌‍‌‌‌‍‌​‌‍‍‌‌﻿‌​​‍﻿﻿‌‍﻿‌‌‍﻿﻿‌‍‌​‌‍‌‌​﻿﻿‌‌﻿​​‌﻿​‍‌‍‌‌‌﻿​﻿‌‍‌‌‌‍﻿‍‌﻿‌​‌‍​‌‌﻿‌​‌‍‍‌‌‍﻿﻿‌‍﻿‍​﻿‍﻿‌‍‍‌‌‍‌​​﻿﻿‌‌‍‌​​﻿‍​​﻿​‌​﻿‍​​﻿‌‍​﻿​​‌‍​‍​﻿‌﻿​‍﻿‌​﻿‌﻿‌‍​‍​﻿‌﻿​﻿​‍​‍﻿‌​﻿‌​‌‍​‍‌‍​‌​﻿‌‌​‍﻿‌​﻿‍​‌‍​‌‌‍‌​​﻿‌‌​‍﻿‌​﻿​﻿‌‍​‍​﻿‌﻿​﻿‌﻿‌‍‌‍‌‍‌​​﻿‍‌‌‍​‌​﻿‍​‌‍‌‌​﻿‍‌‌‍​‍​﻿‍﻿‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​﻿‍﻿‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​﻿﻿﻿‌‍​‍‌‍​‌‌﻿​﻿‌‍‌‌‌‌‌‌‌﻿​‍‌‍﻿​​﻿﻿‌‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​‍‌‌​﻿​﻿‌​​‌​‍‌‌​﻿​‍‌​‌‍​‍‌‌​﻿​‍‌​‌‍‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍‌‍‌‍‍‌‌‍‌​​﻿﻿‌‌‍‌​​﻿‍​​﻿​‌​﻿‍​​﻿‌‍​﻿​​‌‍​‍​﻿‌﻿​‍﻿‌​﻿‌﻿‌‍​‍​﻿‌﻿​﻿​‍​‍﻿‌​﻿‌​‌‍​‍‌‍​‌​﻿‌‌​‍﻿‌​﻿‍​‌‍​‌‌‍‌​​﻿‌‌​‍﻿‌​﻿​﻿‌‍​‍​﻿‌﻿​﻿‌﻿‌‍‌‍‌‍‌​​﻿‍‌‌‍​‌​﻿‍​‌‍‌‌​﻿‍‌‌‍​‍​‍‌‍‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​‍‌‍‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​‍‌‍‌﻿​​‌‍‌‌‌﻿​‍‌﻿​﻿‌﻿​​‌‍‌‌‌‍​﻿‌﻿‌​‌‍‍‌‌﻿‌‍‌‍‌‌​﻿﻿‌‌﻿​​‌﻿‌‌‌‍​‍‌‍﻿​‌‍‍‌‌﻿​﻿‌‍‍​‌‍‌‌‌‍‌​​‍​‍‌﻿﻿‌ (Tue, 14 Jul 2026 07:40:00 GMT)
- `💻 Tech` `📡 RSS` Building more than just an agent harness​​​​‌﻿‍﻿​‍​‍‌‍﻿﻿‌﻿​‍‌‍‍‌‌‍‌﻿‌‍‍‌‌‍﻿‍​‍​‍​﻿‍‍​‍​‍‌﻿​﻿‌‍​‌‌‍﻿‍‌‍‍‌‌﻿‌​‌﻿‍‌​‍﻿‍‌‍‍‌‌‍﻿﻿​‍​‍​‍﻿​​‍​‍‌‍‍​‌﻿​‍‌‍‌‌‌‍‌‍​‍​‍​﻿‍‍​‍​‍‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​﻿‍‍​‍﻿﻿​‍﻿﻿‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍﻿﻿‌‍‍‌‌‍﻿‍‌﻿‌​‌‍‌‌‌‍﻿‍‌﻿‌​​‍﻿﻿‌‍‌‌‌‍‌​‌‍‍‌‌﻿‌​​‍﻿﻿‌‍﻿‌‌‍﻿﻿‌‍‌​‌‍‌‌​﻿﻿‌‌﻿​​‌﻿​‍‌‍‌‌‌﻿​﻿‌‍‌‌‌‍﻿‍‌﻿‌​‌‍​‌‌﻿‌​‌‍‍‌‌‍﻿﻿‌‍﻿‍​﻿‍﻿‌‍‍‌‌‍‌​​﻿﻿‌‌‍‌​​﻿‌‌​﻿​﻿‌‍‌‍​﻿‍‌​﻿​﻿​﻿‌‌​﻿‍​​‍﻿‌​﻿​﻿‌‍​‍‌‍​‍​﻿​‍​‍﻿‌​﻿‌​‌‍‌‍​﻿‌‍​﻿‍‌​‍﻿‌‌‍​‌‌‍‌‌‌‍​‍‌‍‌‌​‍﻿‌‌‍‌​​﻿​﻿​﻿​‌‌‍‌​​﻿​‌​﻿‍‌​﻿‌‌​﻿​‍​﻿​‍‌‍​﻿‌‍‌​​﻿‌​​﻿‍﻿‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​﻿‍﻿‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​﻿﻿﻿‌‍​‍‌‍​‌‌﻿​﻿‌‍‌‌‌‌‌‌‌﻿​‍‌‍﻿​​﻿﻿‌‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​‍‌‌​﻿​﻿‌​​‌​‍‌‌​﻿​‍‌​‌‍​‍‌‌​﻿​‍‌​‌‍‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍‌‍‌‍‍‌‌‍‌​​﻿﻿‌‌‍‌​​﻿‌‌​﻿​﻿‌‍‌‍​﻿‍‌​﻿​﻿​﻿‌‌​﻿‍​​‍﻿‌​﻿​﻿‌‍​‍‌‍​‍​﻿​‍​‍﻿‌​﻿‌​‌‍‌‍​﻿‌‍​﻿‍‌​‍﻿‌‌‍​‌‌‍‌‌‌‍​‍‌‍‌‌​‍﻿‌‌‍‌​​﻿​﻿​﻿​‌‌‍‌​​﻿​‌​﻿‍‌​﻿‌‌​﻿​‍​﻿​‍‌‍​﻿‌‍‌​​﻿‌​​‍‌‍‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​‍‌‍‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​‍‌‍‌﻿​​‌‍‌‌‌﻿​‍‌﻿​﻿‌﻿​​‌‍‌‌‌‍​﻿‌﻿‌​‌‍‍‌‌﻿‌‍‌‍‌‌​﻿﻿‌‌﻿​​‌﻿‌‌‌‍​‍‌‍﻿​‌‍‍‌‌﻿​﻿‌‍‍​‌‍‌‌‌‍‌​​‍​‍‌﻿﻿‌ (Fri, 10 Jul 2026 07:40:00 GMT)
- `💻 Tech` `📡 RSS` What's left for infrastructure-as-code after AI moves in?​​​​‌﻿‍﻿​‍​‍‌‍﻿﻿‌﻿​‍‌‍‍‌‌‍‌﻿‌‍‍‌‌‍﻿‍​‍​‍​﻿‍‍​‍​‍‌﻿​﻿‌‍​‌‌‍﻿‍‌‍‍‌‌﻿‌​‌﻿‍‌​‍﻿‍‌‍‍‌‌‍﻿﻿​‍​‍​‍﻿​​‍​‍‌‍‍​‌﻿​‍‌‍‌‌‌‍‌‍​‍​‍​﻿‍‍​‍​‍‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​﻿‍‍​‍﻿﻿​‍﻿﻿‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍﻿﻿‌‍‍‌‌‍﻿‍‌﻿‌​‌‍‌‌‌‍﻿‍‌﻿‌​​‍﻿﻿‌‍‌‌‌‍‌​‌‍‍‌‌﻿‌​​‍﻿﻿‌‍﻿‌‌‍﻿﻿‌‍‌​‌‍‌‌​﻿﻿‌‌﻿​​‌﻿​‍‌‍‌‌‌﻿​﻿‌‍‌‌‌‍﻿‍‌﻿‌​‌‍​‌‌﻿‌​‌‍‍‌‌‍﻿﻿‌‍﻿‍​﻿‍﻿‌‍‍‌‌‍‌​​﻿﻿‌​﻿‌﻿‌‍‌‌‌‍​‍‌‍‌​​﻿‌﻿​﻿‌‍‌‍‌​​﻿​‍​‍﻿‌‌‍​﻿‌‍‌‌‌‍​‍‌‍​﻿​‍﻿‌​﻿‌​‌‍​‍​﻿‍​​﻿‍​​‍﻿‌​﻿‍​​﻿​‍‌‍‌‍​﻿‍‌​‍﻿‌​﻿​﻿‌‍‌​‌‍‌‍‌‍​‍​﻿​‍‌‍​﻿​﻿‍​‌‍​‍‌‍​﻿​﻿‌‌‌‍​﻿‌‍​‌​﻿‍﻿‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​﻿‍﻿‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​﻿﻿﻿‌‍​‍‌‍​‌‌﻿​﻿‌‍‌‌‌‌‌‌‌﻿​‍‌‍﻿​​﻿﻿‌‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​‍‌‌​﻿​﻿‌​​‌​‍‌‌​﻿​‍‌​‌‍​‍‌‌​﻿​‍‌​‌‍‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍‌‍‌‍‍‌‌‍‌​​﻿﻿‌​﻿‌﻿‌‍‌‌‌‍​‍‌‍‌​​﻿‌﻿​﻿‌‍‌‍‌​​﻿​‍​‍﻿‌‌‍​﻿‌‍‌‌‌‍​‍‌‍​﻿​‍﻿‌​﻿‌​‌‍​‍​﻿‍​​﻿‍​​‍﻿‌​﻿‍​​﻿​‍‌‍‌‍​﻿‍‌​‍﻿‌​﻿​﻿‌‍‌​‌‍‌‍‌‍​‍​﻿​‍‌‍​﻿​﻿‍​‌‍​‍‌‍​﻿​﻿‌‌‌‍​﻿‌‍​‌​‍‌‍‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​‍‌‍‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​‍‌‍‌﻿​​‌‍‌‌‌﻿​‍‌﻿​﻿‌﻿​​‌‍‌‌‌‍​﻿‌﻿‌​‌‍‍‌‌﻿‌‍‌‍‌‌​﻿﻿‌‌﻿​​‌﻿‌‌‌‍​‍‌‍﻿​‌‍‍‌‌﻿​﻿‌‍‍​‌‍‌‌‌‍‌​​‍​‍‌﻿﻿‌ (Wed, 08 Jul 2026 04:40:00 GMT)
- `💻 Tech` `📡 RSS`  Agent orchestration is so two-years ago​​​​‌﻿‍﻿​‍​‍‌‍﻿﻿‌﻿​‍‌‍‍‌‌‍‌﻿‌‍‍‌‌‍﻿‍​‍​‍​﻿‍‍​‍​‍‌﻿​﻿‌‍​‌‌‍﻿‍‌‍‍‌‌﻿‌​‌﻿‍‌​‍﻿‍‌‍‍‌‌‍﻿﻿​‍​‍​‍﻿​​‍​‍‌‍‍​‌﻿​‍‌‍‌‌‌‍‌‍​‍​‍​﻿‍‍​‍​‍‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​﻿‍‍​‍﻿﻿​‍﻿﻿‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍﻿﻿‌‍‍‌‌‍﻿‍‌﻿‌​‌‍‌‌‌‍﻿‍‌﻿‌​​‍﻿﻿‌‍‌‌‌‍‌​‌‍‍‌‌﻿‌​​‍﻿﻿‌‍﻿‌‌‍﻿﻿‌‍‌​‌‍‌‌​﻿﻿‌‌﻿​​‌﻿​‍‌‍‌‌‌﻿​﻿‌‍‌‌‌‍﻿‍‌﻿‌​‌‍​‌‌﻿‌​‌‍‍‌‌‍﻿﻿‌‍﻿‍​﻿‍﻿‌‍‍‌‌‍‌​​﻿﻿‌‌‍‌​​﻿‌‌​﻿​‍‌‍​‍​﻿​﻿​﻿​﻿​﻿‌​‌‍‌‌​‍﻿‌​﻿‌​​﻿​‍​﻿​﻿​﻿​﻿​‍﻿‌​﻿‌​‌‍‌‌​﻿‌﻿‌‍‌​​‍﻿‌‌‍​‌​﻿​‌​﻿​​‌‍​‍​‍﻿‌‌‍​‍‌‍‌‍‌‍​‍‌‍​‌​﻿​‌​﻿‌​​﻿‌﻿​﻿​‍‌‍​﻿​﻿​‍‌‍‌‍‌‍​‍​﻿‍﻿‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​﻿‍﻿‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​﻿﻿﻿‌‍​‍‌‍​‌‌﻿​﻿‌‍‌‌‌‌‌‌‌﻿​‍‌‍﻿​​﻿﻿‌‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​‍‌‌​﻿​﻿‌​​‌​‍‌‌​﻿​‍‌​‌‍​‍‌‌​﻿​‍‌​‌‍‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍‌‍‌‍‍‌‌‍‌​​﻿﻿‌‌‍‌​​﻿‌‌​﻿​‍‌‍​‍​﻿​﻿​﻿​﻿​﻿‌​‌‍‌‌​‍﻿‌​﻿‌​​﻿​‍​﻿​﻿​﻿​﻿​‍﻿‌​﻿‌​‌‍‌‌​﻿‌﻿‌‍‌​​‍﻿‌‌‍​‌​﻿​‌​﻿​​‌‍​‍​‍﻿‌‌‍​‍‌‍‌‍‌‍​‍‌‍​‌​﻿​‌​﻿‌​​﻿‌﻿​﻿​‍‌‍​﻿​﻿​‍‌‍‌‍‌‍​‍​‍‌‍‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​‍‌‍‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​‍‌‍‌﻿​​‌‍‌‌‌﻿​‍‌﻿​﻿‌﻿​​‌‍‌‌‌‍​﻿‌﻿‌​‌‍‍‌‌﻿‌‍‌‍‌‌​﻿﻿‌‌﻿​​‌﻿‌‌‌‍​‍‌‍﻿​‌‍‍‌‌﻿​﻿‌‍‍​‌‍‌‌‌‍‌​​‍​‍‌﻿﻿‌ (Tue, 07 Jul 2026 07:40:00 GMT)
- `💻 Tech` `📡 RSS` When the sensor starts thinking: SnortML, agentic AI, and the evolving architecture of intrusion detection​​​​‌﻿‍﻿​‍​‍‌‍﻿﻿‌﻿​‍‌‍‍‌‌‍‌﻿‌‍‍‌‌‍﻿‍​‍​‍​﻿‍‍​‍​‍‌﻿​﻿‌‍​‌‌‍﻿‍‌‍‍‌‌﻿‌​‌﻿‍‌​‍﻿‍‌‍‍‌‌‍﻿﻿​‍​‍​‍﻿​​‍​‍‌‍‍​‌﻿​‍‌‍‌‌‌‍‌‍​‍​‍​﻿‍‍​‍​‍‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​﻿‍‍​‍﻿﻿​‍﻿﻿‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍﻿﻿‌‍‍‌‌‍﻿‍‌﻿‌​‌‍‌‌‌‍﻿‍‌﻿‌​​‍﻿﻿‌‍‌‌‌‍‌​‌‍‍‌‌﻿‌​​‍﻿﻿‌‍﻿‌‌‍﻿﻿‌‍‌​‌‍‌‌​﻿﻿‌‌﻿​​‌﻿​‍‌‍‌‌‌﻿​﻿‌‍‌‌‌‍﻿‍‌﻿‌​‌‍​‌‌﻿‌​‌‍‍‌‌‍﻿﻿‌‍﻿‍​﻿‍﻿‌‍‍‌‌‍‌​​﻿﻿‌​﻿‌﻿​﻿‌‍‌‍​﻿​﻿‍‌​﻿‌﻿​﻿‌﻿​﻿​‌‌‍​‍​‍﻿‌​﻿​﻿​﻿‌​‌‍‌‌​﻿‌‍​‍﻿‌​﻿‌​‌‍‌​​﻿‍‌​﻿‍​​‍﻿‌​﻿‍​​﻿‌‍​﻿‌​​﻿​‌​‍﻿‌‌‍‌‌‌‍​﻿‌‍‌‌‌‍‌‍‌‍​﻿​﻿‌﻿​﻿​‌​﻿​‌‌‍‌‍​﻿​​‌‍‌‌‌‍‌‍​﻿‍﻿‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​﻿‍﻿‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​﻿﻿﻿‌‍​‍‌‍​‌‌﻿​﻿‌‍‌‌‌‌‌‌‌﻿​‍‌‍﻿​​﻿﻿‌‌‍‍​‌﻿‌​‌﻿‌​‌﻿​​‌﻿​﻿​‍‌‌​﻿​﻿‌​​‌​‍‌‌​﻿​‍‌​‌‍​‍‌‌​﻿​‍‌​‌‍‌‍​﻿‌‍﻿‌‌﻿​﻿​‍﻿‍‌﻿​﻿‌﻿‌​‌‍​‌‌‍​﻿‌‍‍﻿‌‍﻿﻿‌﻿‌‍‌‍‌‌‌﻿​‍‌‍‌‍‌‍﻿​‌‍﻿﻿‌﻿‌﻿​‍﻿‍‌‍​﻿‌‍﻿﻿​‍‌‍‌‍‍‌‌‍‌​​﻿﻿‌​﻿‌﻿​﻿‌‍‌‍​﻿​﻿‍‌​﻿‌﻿​﻿‌﻿​﻿​‌‌‍​‍​‍﻿‌​﻿​﻿​﻿‌​‌‍‌‌​﻿‌‍​‍﻿‌​﻿‌​‌‍‌​​﻿‍‌​﻿‍​​‍﻿‌​﻿‍​​﻿‌‍​﻿‌​​﻿​‌​‍﻿‌‌‍‌‌‌‍​﻿‌‍‌‌‌‍‌‍‌‍​﻿​﻿‌﻿​﻿​‌​﻿​‌‌‍‌‍​﻿​​‌‍‌‌‌‍‌‍​‍‌‍‌﻿‌​‌﻿‍‌‌﻿​​‌‍‌‌​﻿﻿‌‌‍​‍‌‍﻿​‌‍﻿﻿‌‍‌﻿‌‌​​‌‍﻿﻿‌﻿​﻿‌﻿‌​​‍‌‍‌﻿​​‌‍​‌‌﻿‌​‌‍‍​​﻿﻿‌‌﻿‌​‌‍‍‌‌﻿‌​‌‍﻿​‌‍‌‌​‍‌‍‌﻿​​‌‍‌‌‌﻿​‍‌﻿​﻿‌﻿​​‌‍‌‌‌‍​﻿‌﻿‌​‌‍‍‌‌﻿‌‍‌‍‌‌​﻿﻿‌‌﻿​​‌﻿‌‌‌‍​‍‌‍﻿​‌‍‍‌‌﻿​﻿‌‍‍​‌‍‌‌‌‍‌​​‍​‍‌﻿﻿‌ (Mon, 06 Jul 2026 15:23:34 GMT)

### 📰 Anthropic (23 noticias)

- `💻 Tech` 27 de julio de 2026AnunciosCognizant y Anthropic expanden su asociación para llevar Claude a clientes empresariales (Jul 27, 2026)
- `💻 Tech` 22 de julio de 2026 | Producto: Pregunta a Claude sobre el Índice Económico Anthropic (Jul 22, 2026)
- `💻 Tech` Anuncios del 21 de julio de 2026: Anthropic dona otros 20 millones de dólares a Public First Action (Jul 21, 2026)
- `💻 Tech` Solicita las becas de investigación de enfermedades raras de IA para la ciencia de Anthropic (Jul 20, 2026)
- `💻 Tech` 14 de julio de 2026 | Producto: Presentamos Claude para profesores. (Jul 14, 2026)
- `💻 Tech` Anthropic destina 10 millones de dólares a la investigación canadiense de IA (Jul 14, 2026)
- `💻 Tech` Estudio de Caso: UST lleva Claude a la IA física (9 de julio de 2026) (Jul 9, 2026)
- `💻 Tech` Inviting hard questionsAnnouncementsJul 9, 2026We’re asking the public for their hardest questions about AI, and committing to show our work as we address them. (Jul 9, 2026)
- `💻 Tech` Jul 9, 2026AnnouncementsBen Bernanke appointed to Anthropic’s Long-Term Benefit Trust (Jul 9, 2026)
- `💻 Tech` Anuncios: Presentamos una forma de reflexionar sobre cómo utilizas Claude (Jul 9, 2026)

### 📰 AWS ML (48 noticias)

- `💻 Tech` Beyond RAG: Task-aware knowledge compression for enterprise AI on AWS (2026-07-27T08:11:32-08:00)
- `💻 Tech` Deepgram enhances Amazon SageMaker AI support with AWS IAM Temporary Delegation (2026-07-27T08:07:44-08:00)
- `💻 Tech` Introducing Claude Opus 5 on AWS: Anthropic’s most capable Opus model (2026-07-24T09:59:03-08:00)
- `💻 Tech` Build an explainable next-best-product recommendation system for banking on AWS (2026-07-24T07:42:11-08:00)
- `💻 Tech` Get started with OpenAI GPT-5.6 Sol, Terra, and Luna on Amazon Bedrock (2026-07-24T07:40:08-08:00)
- `💻 Tech` Best practices for applying Amazon Bedrock Guardrails to code generation workflows (2026-07-23T15:03:44-08:00)
- `💻 Tech` Evaluating AI Agents: A production blueprint with Strands and AgentCore (2026-07-23T09:00:20-08:00)
- `💻 Tech` Building trade assistant: How Jefferies optimized front office trading operations with AI (2026-07-23T08:42:54-08:00)
- `💻 Tech` Detecting silent agent failures with Amazon Bedrock AgentCore optimization (2026-07-23T08:38:34-08:00)
- `💻 Tech` AI Teammates: how monday.com runs production AI agents on Amazon Bedrock (2026-07-22T07:54:28-08:00)

### 📰 Levante-EMV (43 noticias)

- `💻 Tech` La tecnologia i l’elogi de l’ociositat intel·ligent
- `💻 Tech` Agrobank Murcia (23/7/2026, 15:40:13)
- `💻 Tech` Los expertos en IA instan a pasar de la estrategia a la práctica (21/7/2026, 8:59:45)
- `💻 Tech` Brownie de chocolate gourmet con Teresa de Trufas Martínez | Milar (21/7/2026, 6:53:14)
- `💻 Tech` Edwards Lifesciences incorporará un centro de especialización en cardiopatías estructurales en su campus de Moncada (20/7/2026, 13:58:41)
- `💻 Tech` Cuando la victoria de España te pilla en pleno vuelo (20/7/2026, 10:35:42)
- `💻 Tech` Una mano biónica permite tocar el piano a personas con amputaciones (19/7/2026, 10:54:52)
- `💻 Tech` La gama SUV de Kia: una respuesta para cada forma de conducir (20/7/2026, 12:17:01)
- `💻 Tech` C. Valenciana
- `💻 Tech` Lista de espera para el carnet de conducir: las autoescuelas denuncian un sistema "colapsado"

### 📰 web.dev (7 noticias)

- `💻 Tech` `📡 RSS` New to the web platform in March (Fri, 27 Mar 2026 07:00:00 GMT)
- `💻 Tech` `📡 RSS` April 2026 Baseline monthly digest (Wed, 27 May 2026 07:00:00 GMT)
- `💻 Tech` `📡 RSS` March 2026 Baseline monthly digest (Tue, 14 Apr 2026 07:00:00 GMT)
- `💻 Tech` `📡 RSS` February 2026 Baseline monthly digest (Mon, 30 Mar 2026 07:00:00 GMT)
- `💻 Tech` `📡 RSS` January 2026 Baseline monthly digest (Mon, 02 Mar 2026 08:00:00 GMT)
- `💻 Tech` `📡 RSS` Navigation API - a better way to navigate, is now Baseline Newly Available (Tue, 17 Feb 2026 08:00:00 GMT)
- `💻 Tech` `📡 RSS` Interop 2026: Continuing to improve the web for developers (Thu, 12 Feb 2026 08:00:00 GMT)

### 📰 hacks.mozilla.org (11 noticias)

- `💻 Tech` `📡 RSS` Launching Interop 2025 (Thu, 13 Feb 2025 16:59:13 +0000)
- `💻 Tech` `📡 RSS` PACT: Anonymous Credentials for the Web (Tue, 23 Jun 2026 15:29:52 +0000)
- `💻 Tech` `📡 RSS` Announcing Web Serial Support in Firefox (Thu, 21 May 2026 18:00:05 +0000)
- `💻 Tech` `📡 RSS` Behind the Scenes Hardening Firefox with Claude Mythos Preview (Thu, 07 May 2026 16:01:21 +0000)
- `💻 Tech` `📡 RSS` Trustworthy JavaScript for the Open Web (Tue, 05 May 2026 15:49:11 +0000)
- `💻 Tech` `📡 RSS` Firefox Developer Edition and Beta: Try out Mozilla’s .rpm package! (Wed, 25 Mar 2026 16:17:11 +0000)
- `💻 Tech` `📡 RSS` Why is WebAssembly a second-class language on the web? (Thu, 26 Feb 2026 16:02:36 +0000)
- `💻 Tech` `📡 RSS` Goodbye innerHTML, Hello setHTML: Stronger XSS Protection in Firefox 148 (Tue, 24 Feb 2026 13:00:02 +0000)
- `💻 Tech` `📡 RSS` CRLite: Fast, private, and comprehensive certificate revocation checking in Firefox (Tue, 19 Aug 2025 16:03:19 +0000)
- `💻 Tech` `📡 RSS` Improving Firefox Stability in the Enterprise by Reducing DLL Injection (Tue, 25 Mar 2025 18:31:16 +0000)

### 📰 The Verge (6 noticias)

- `💻 Tech` Apple TV wants to go big (2025-11-23T13:00:00+00:00)
- `💻 Tech` Pasé una semana usando el teléfono Trump, es terrible. (2026-07-10T14:19:59+00:00)
- `💻 Tech` El servicio de cámaras para el hogar inteligente de Apple me está empezando a impresionar. (2026-06-16T12:00:00+00:00)
- `💻 Tech` Madison Square Garden’s surveillance system banned this fan over his T-shirt design
- `💻 Tech` Apple TV’s new horror series is scarier because it’s also hilarious
- `💻 Tech` The heist of iOS 26

### 📰 GitHub Engineering (3 noticias)

- `💻 Tech` `📡 RSS` El coste de decir sí ha cambiado (Fri, 17 Jul 2026 16:46:47 +0000)
- `💻 Tech` `📡 RSS` Mejores herramientas empeoraron la revisión de código de Copilot. Así es como la mejoramos realmente. (Fri, 10 Jul 2026 15:57:47 +0000)
- `💻 Tech` `📡 RSS` Automatizando la documentación entre repositorios con GitHub Agentic Workflows (Wed, 08 Jul 2026 21:11:56 +0000)

### 📰 Wired (8 noticias)

- `💻 Tech` Medio ambiente
- `💻 Tech` Health
- `💻 Tech` Climate
- `💻 Tech` Energy
- `💻 Tech` Space
- `💻 Tech` Physics and Math
- `💻 Tech` Biotech
- `💻 Tech` Psychology and Neuroscience

### 📰 MDN Blog (12 noticias)

- `💻 Tech` `📡 RSS` Introducing the MDN MCP server (Mon, 15 Jun 2026 00:00:00 +0000)
- `💻 Tech` `📡 RSS` Under the hood of MDN's new frontend (Wed, 8 Apr 2026 00:00:00 +0000)
- `💻 Tech` `📡 RSS` Image formats: Codecs and compression tools (Wed, 5 Nov 2025 00:00:00 +0000)
- `💻 Tech` `📡 RSS` A beginner-friendly guide to view transitions in CSS (Thu, 9 Oct 2025 00:00:00 +0000)
- `💻 Tech` `📡 RSS` Launching MDN's new front end (Tue, 19 Aug 2025 00:00:00 +0000)
- `💻 Tech` `📡 RSS` Image formats: Pixel data from encoders to decoders (Mon, 4 Aug 2025 00:00:00 +0000)
- `💻 Tech` `📡 RSS` Celebrating 20 years of MDN (Wed, 23 Jul 2025 00:00:00 +0000)
- `💻 Tech` `📡 RSS` Image formats: Color models for humans and devices (Tue, 6 May 2025 00:00:00 +0000)
- `💻 Tech` `📡 RSS` Default styles for h1 elements are changing (Fri, 11 Apr 2025 00:00:00 +0000)
- `💻 Tech` `📡 RSS` Implications of Global Privacy Control (Sat, 15 Mar 2025 00:00:00 +0000)

### 📰 Can I Use (5 noticias)

- `💻 Tech` `📡 RSS` New feature: Lazy loading via attribute for video & audio (2026-03-05T00:00:00+00:00)
- `💻 Tech` `📡 RSS` New feature: CSS Grid Lanes (2026-01-10T00:00:00+00:00)
- `💻 Tech` `📡 RSS` Site update: web-features now included + new feature list functionality (2025-10-11T12:30:39+00:00)
- `💻 Tech` `📡 RSS` New feature: CSS if() function (2025-07-18T00:00:00+00:00)
- `💻 Tech` `📡 RSS` New feature: View Transitions (cross-document) (2025-03-23T00:00:00+00:00)

### 📰 Chrome Developers (10 noticias)

- `💻 Tech` `📡 RSS` A developer toolkit to make your website agent-ready (Mon, 22 Jun 2026 07:00:00 GMT)
- `💻 Tech` `📡 RSS` Unlock runtime insights: Introducing third-party developer tools for Chrome DevTools for agents (Thu, 18 Jun 2026 07:00:00 GMT)
- `💻 Tech` `📡 RSS` What's New in WebGPU (Chrome 149-150) (Wed, 17 Jun 2026 07:00:00 GMT)
- `💻 Tech` `📡 RSS` Join the WebMCP origin trial (Tue, 09 Jun 2026 07:00:00 GMT)
- `💻 Tech` `📡 RSS` Seamless PWA origin migration: Change domains without losing users (Wed, 03 Jun 2026 07:00:00 GMT)
- `💻 Tech` `📡 RSS` Chrome 150 beta (Wed, 03 Jun 2026 07:00:00 GMT)
- `💻 Tech` `📡 RSS` What's new in DevTools (Chrome 149) (Tue, 02 Jun 2026 07:00:00 GMT)
- `💻 Tech` `📡 RSS` New in Chrome 149 (Tue, 02 Jun 2026 07:00:00 GMT)
- `💻 Tech` `📡 RSS` Build new features using built-in AI in Chrome (Tue, 26 May 2026 07:00:00 GMT)
- `💻 Tech` `📡 RSS` What's new in web extensions: I﻿/﻿O 2026 recap (Fri, 22 May 2026 07:00:00 GMT)

### 📰 Ars Technica AI (40 noticias)

- `💻 Tech` `📡 RSS` Los hackers pueden usar 9 de las herramientas de IA más populares para crear enormes botnets (Wed, 08 Jul 2026 07:00:51 +0000)
- `💻 Tech` `📡 RSS` Michigan registra un brote explosivo de parásito diarreico con más de 700 casos (Tue, 07 Jul 2026 22:29:00 +0000)
- `💻 Tech` `📡 RSS` La demanda energética de los centros de datos amenaza el plan “Made in America” de Trump (Tue, 07 Jul 2026 21:03:07 +0000)
- `💻 Tech` `📡 RSS` Un número sorprendentemente grande de personas podría tener un marcador para la alergia a la carne relacionada con garrapatas (Tue, 07 Jul 2026 20:32:39 +0000)
- `💻 Tech` `📡 RSS` SCOTUS permite a Texas aplicar una ley de tiendas de aplicaciones que Big Tech califica de “régimen de censura” (Tue, 07 Jul 2026 20:18:24 +0000)
- `💻 Tech` `📡 RSS` Bethesda, id Software reportedly hit hard by Microsoft layoffs (Tue, 07 Jul 2026 19:52:59 +0000)
- `💻 Tech` `📡 RSS` The Weather Channel aumenta los precios de suscripción de streaming hasta en 20 $ (Tue, 07 Jul 2026 18:29:24 +0000)
- `💻 Tech` `📡 RSS` Los días de la Nintendo Switch están contados, pero ¿cuál es ese número? (Tue, 07 Jul 2026 18:16:29 +0000)
- `💻 Tech` `📡 RSS` ¿Este coche de carreras está hecho de fibras vegetales, volcanes... y agua de mar? (Tue, 07 Jul 2026 16:45:18 +0000)
- `💻 Tech` `📡 RSS` Frente a los controles de exportación de EE. UU., DeepSeek de China planea fabricar sus propios chips (Tue, 07 Jul 2026 16:14:53 +0000)

### 📰 Google Search Central (12 noticias)

- `💻 Tech` `📡 RSS` See how content from social and video platforms performs on Google Search (Tue, 07 Jul 2026 00:00:00 +0000)
- `💻 Tech` `📡 RSS` Search Central Deep Dive Europe 2026: Apparently we're going to Barcelona (Mon, 06 Jul 2026 00:00:00 +0000)
- `💻 Tech` `📡 RSS` Help Us Pick the Next Stop in Europe for Search Central Live Deep Dive 2026! (Thu, 18 Jun 2026 00:00:00 +0000)
- `💻 Tech` `📡 RSS` Introducing Search Generative AI performance reports in Search Console (Wed, 03 Jun 2026 00:00:00 +0000)
- `💻 Tech` `📡 RSS` A new resource for optimizing for generative AI in Google Search (Fri, 15 May 2026 00:00:00 +0000)
- `💻 Tech` `📡 RSS` Introducing a new spam policy for "back button hijacking" (Mon, 13 Apr 2026 00:00:00 +0000)
- `💻 Tech` `📡 RSS` Search Central Live is Coming to Shanghai in 2026! (Thu, 02 Apr 2026 00:00:00 +0000)
- `💻 Tech` `📡 RSS` New Location for the Google Crawlers' IP Range Files (Tue, 31 Mar 2026 00:00:00 +0000)
- `💻 Tech` `📡 RSS` Inside Googlebot: demystifying crawling, fetching, and the bytes we process (Tue, 31 Mar 2026 00:00:00 +0000)
- `💻 Tech` `📡 RSS` Search Central Live Asia Pacific 2026: Get Ready for Sydney and more! (Fri, 20 Mar 2026 00:00:00 +0000)

### 📰 Fundación Carolina (10 noticias)

- `💻 Tech` La Fundación Carolina da la bienvenida a 59 becarios y becarias en la XXV edición de la Escuela de Verano de la UCM
- `💻 Tech` La secretaria de Estado de Cooperación Internacional clausura el curso de verano «Resistir la reacción: política, feminismo y cooperación iberoamericana»
- `💻 Tech` La activista mexicana Olimpia Coral Melo visita Madrid para participar en el Curso de Verano de Fundación Carolina
- `💻 Tech` El historiador y exbecario Herib Caballero, imparte una conferencia sobre la historia de Asunción en Casa de América
- `💻 Tech` Fundación Carolina y AECID presentan su programa de protección y formación para defensores de los Derechos Humanos
- `💻 Tech` La secretaria de Estado de Cooperación Internacional, Eva Granados, inaugura la XXI edición del Programa Jóvenes Líderes Iberoamericanos
- `💻 Tech` La Junta Rectora de Fundación Carolina celebra su 70ª sesión ordinaria
- `💻 Tech` Fundación Carolina abre la convocatoria de becas para sus Cursos de Verano 2026
- `💻 Tech` Mayki Gorosito recibe el III Premio Conchita Viera por su compromiso con la memoria y los derechos humanos
- `💻 Tech` La película Comandante Fritz, del cineasta cubano Pavel Giroud, ha sido galardonada con el Premio del Público en la 43ª edición del Miami Film Festival.

### 📰 HobbyConsolas (24 noticias)

- `💻 Tech` Los escaneos de Pokémon Go fueron utilizados para entrenar al sistema de navegación que se va a implementar en drones y otros robots destinados a la guerra (ACTUALIZADO)
- `💻 Tech` Los tres grandes fabricantes de RAM, Micron, Samsung y SK Hynix, son acusados de ''forzar'' la crisis de la memoria y ahora afrontarán una demanda colectiva
- `💻 Tech` Un desarrollador amateur trabaja en su propia versión de GTA 6 hecha con IA, y busca adelantar a Rockstar con sus progresos
- `💻 Tech` Unreal Engine 6 ya es una realidad, y empezará a probarse en los cosméticos de Fortnite: integración de IA con Claude y Gemini, nuevo lenguaje de programación y más detalles
- `💻 Tech` Valve confirma que Steam Machine y Steam Frame se pondrán a la venta en verano y explica el proceso de verificación de sus juegos
- `💻 Tech` Sega podría dar la sorpresa con una nueva consola portátil enfocada en juegos 2D, según un fabricante especializado en tecnología
- `💻 Tech` Anunciada ROG Xbox Ally X20, un nuevo modelo con pantalla OLED más grande y otros cambios para celebrar los 20 años de la marca ROG
- `💻 Tech` Clint Hocking, exdirector creativo de Assassin's Creed Hexe, confiesa haber usado la IA para aprender a programar, pero ChatGPT fue más un obstáculo que un tutor
- `💻 Tech` Final Fantasy VII Revelation: todo lo que se sabe del broche de oro de la trilogía y la gran despedida de Cloud, Tifa y compañía
- `💻 Tech` GTA 6 da alas a los especuladores: ya hay quien paga cifras loquísimas... ¡Por la reserva del juego!

### 📰 Azure AI (7 noticias)

- `💻 Tech` Meet Brain: The AI system behind Azure reliability (2026-07-02T09:00:00-07:00)
- `💻 Tech` From insight to action: The next phase of agentic cloud operations (2026-06-23T08:45:00-07:00)
- `💻 Tech` AI alone won’t change your business. The system running it will. (2026-06-02T12:15:57-07:00)
- `💻 Tech` Announcing Microsoft Discovery general availability and Microsoft Discovery app preview (2026-06-02T11:15:00-07:00)
- `💻 Tech` Advancing enterprise AI: New SAP on Azure announcements from SAP Sapphire 2026 (2026-05-12T11:00:00-07:00)
- `💻 Tech` Red Hat Summit 2026: Platform modernization and AI on Microsoft Azure Red Hat OpenShift (2026-05-11T12:00:00-07:00)
- `💻 Tech` Cloud Cost Optimization: Principles that still matter (2026-04-15T09:00:00-07:00)

### 📰 CSS-Tricks (1 noticias)

- `💻 Tech` The Siren Song of ariaNotify() (Jun 17, 2026)

### 📰 Moz Blog SEO (10 noticias)

- `💻 Tech` `📡 RSS` Cannibalization (Fri, 17 Sep 2021 00:00:00 -0700)
- `💻 Tech` `📡 RSS` Tackling 8,000 Title Tag Rewrites: A Case Study (Thu, 16 Sep 2021 00:00:00 -0700)
- `💻 Tech` `📡 RSS` How Our Website Conversion Strategy Increased Business Inquiries by 37% (Wed, 15 Sep 2021 00:00:00 -0700)
- `💻 Tech` `📡 RSS` How to Add Products to Your Google My Business Listing, Illustrated (Mon, 13 Sep 2021 00:00:00 -0700)
- `💻 Tech` `📡 RSS` The Three Bosses of SEO (Fri, 10 Sep 2021 00:00:00 -0700)
- `💻 Tech` `📡 RSS` Winning the Page Speed Race: How to Turn Your Clunker of a Website Into a Race Car (Wed, 08 Sep 2021 00:00:00 -0700)
- `💻 Tech` `📡 RSS` Responsive Search Ads: 5 Best Practices for Google Ads PPC Search Campaigns (Tue, 07 Sep 2021 00:00:00 -0700)
- `💻 Tech` `📡 RSS` How to Calculate Your SEO ROI Using Google Analytics (Mon, 06 Sep 2021 00:00:00 -0700)
- `💻 Tech` `📡 RSS` How to Use STAT to Find SEO Opportunities at Scale (Fri, 03 Sep 2021 00:00:00 -0700)
- `💻 Tech` `📡 RSS` The Guide to Targeted-Impact Link Building (Wed, 01 Sep 2021 00:00:00 -0700)

### 📰 DeepMind (1 noticias)

- `💻 Tech` Presentamos Gemini Omni. (May 2026)

### 📰 Genbeta (6 noticias)

- `💻 Tech` Así ha cambiado Internet en los 20 años transcurridos desde el lanzamiento de Genbeta
- `💻 Tech` Llega el primer sorteo exclusivo para suscriptores de Xataka Xtra: así puedes ganar un televisor LG QNED evo AI de 75”
- `💻 Tech` Lanzamos Xataka Xtra: tu experiencia en Xataka sube de nivel con newsletters exclusivas, sorteos, El Consultorio y más
- `💻 Tech` Un jefe boomer no entendía que sus empleados millennials no quisieran cargos directivos. Ellos tienen claras las razones
- `💻 Tech` Meta se ha puesto a la cabeza de la carrera de los agentes de IA adquiriendo Manus por 2.000 millones de dólares
- `💻 Tech` El Alzheimer ya no parece irreversible: la ciencia logra que cerebros con daños avanzados se recuperen por primera vez en animales

### 📰 GitHub Blog (10 noticias)

- `💻 Tech` From latency to instant: Modernizing GitHub Issues navigation performance
- `💻 Tech` How GitHub uses eBPF to improve deployment safety
- `💻 Tech` The uphill climb of making diff lines performant
- `💻 Tech` Agent-driven development in Copilot Applied Science
- `💻 Tech` Continuous AI for accessibility: How GitHub transforms feedback into inclusion
- `💻 Tech` How we rebuilt the search architecture for high availability in GitHub Enterprise Server
- `💻 Tech` From pixels to characters: The engineering behind GitHub Copilot CLI’s animated ASCII banner
- `💻 Tech` When protections outlive their purpose: A lesson on managing defense systems at scale
- `💻 Tech` Post-quantum security for SSH access on GitHub
- `💻 Tech` How GitHub engineers tackle platform problems


---

## 🎬 Videos destacados

_No hay videos destacados esta semana._

---

### 🛠️ Herramienta o Repo de la Semana

:::tip
**[uv](https://github.com/astral-sh/uv)** — Esta herramienta redefine la gestión de paquetes Python, reemplazando y consolidando funciones de pip, virtualenv y Poetry para un desarrollo más rápido y eficiente. Es una alternativa robusta que agiliza el flujo de trabajo en proyectos Python.
:::


---

## 🏁 En 30 segundos (TL;DR)

- IA entra en fase pragmática: Google lanza Gemini 3.6 Flash para alta velocidad, mientras el código abierto impulsa modelos más accesibles.
- DevOps se consolida en GitOps: ArgoCD se posiciona como el estándar para despliegues en EKS, priorizando la gestión de estado desde Git.
- `uv` revoluciona Python: Reemplaza y unifica pip, virtualenv y Poetry, prometiendo gestión de paquetes más rápida y eficiente.
- Seguridad hardware y precios: Microsoft bloqueará Windows pirata con TPM; el hardware enfrenta subidas de precio por la DRAM.

---

## 🔮 Qué esperar la próxima semana

:::warning
La tendencia hacia la "local-first" y el código abierto en IA, sumado a la maduración de plataformas DevOps, sugiere una mayor democratización del desarrollo de agentes autónomos y sistemas inteligentes. Esperemos más herramientas que faciliten la orquestación y el despliegue eficiente de estos sistemas, con un enfoque en la interoperabilidad y la capacidad de ejecución en entornos distribuidos.
:::

---

> **Nota del autor:** Me sorprendió la noticia de que ChatGPT afirmó que una IA rebelde atacó empresas, un claro ejemplo de las alucinaciones "creativas" que aún presentan los LLM cuando se les pide generar contenido periodístico. Esto refuerza la necesidad de una verificación humana rigurosa. También, el debate sobre Terraform vs. ArgoCD en EKS subraya una maduración importante en las arquitecturas de despliegue.

📡 **[Ver dashboard completo con todos los filtros](http://jorbencasdownloaderdocument.surge.sh)**