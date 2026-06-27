import re
import unicodedata


def gen_python(title: str, desc: str) -> str:
    return (
        f"# {title}\n"
        f"# {desc}\n\n"
        "def resolver(entrada):\n"
        f'    """\n'
        f"    {title}\n"
        '    """\n'
        "    resultado = entrada\n"
        "    return resultado\n\n\n"
        "if __name__ == '__main__':\n"
        '    print(resolver("ejemplo"))\n'
    )

def gen_javascript(title: str, desc: str) -> str:
    return (
        f"// {title}\n// {desc}\n\n"
        "function resolver(entrada) {\n"
        "  return entrada;\n"
        "}\n\n"
        "console.log(resolver('ejemplo'));\n"
    )

def gen_typescript(title: str, desc: str) -> str:
    return (
        f"// {title}\n// {desc}\n\n"
        "function resolver<T>(entrada: T): T {\n"
        "  return entrada;\n"
        "}\n\n"
        "console.log(resolver('ejemplo'));\n"
    )

def gen_go(title: str, desc: str) -> str:
    return (
        'package main\n\nimport "fmt"\n\n'
        f"// {title}\nfunc resolver(entrada string) string {{\n"
        "\treturn entrada\n}\n\n"
        "func main() {\n"
        '\tfmt.Println(resolver("ejemplo"))\n}\n'
    )

def gen_rust(title: str, desc: str) -> str:
    return (
        f"// {title}\n// {desc}\n\n"
        "fn resolver(entrada: &str) -> String {\n"
        "    entrada.to_string()\n}\n\n"
        'fn main() {\n    println!("{}", resolver("ejemplo"));\n}\n'
    )

def gen_java(title: str, desc: str) -> str:
    return (
        f"// {title}\n// {desc}\n\n"
        "public class Reto {\n"
        "    public static String resolver(String entrada) {\n"
        "        return entrada;\n    }\n\n"
        "    public static void main(String[] args) {\n"
        '        System.out.println(resolver("ejemplo"));\n    }\n}\n'
    )

def gen_csharp(title: str, desc: str) -> str:
    return (
        f"// {title}\n// {desc}\n\nusing System;\n\n"
        "class Reto {\n"
        "    static string Resolver(string entrada) => entrada;\n\n"
        '    static void Main() => Console.WriteLine(Resolver("ejemplo"));\n}\n'
    )

def gen_kotlin(title: str, desc: str) -> str:
    return (
        f"// {title}\n// {desc}\n\n"
        "fun resolver(entrada: String) = entrada\n\n"
        'fun main() { println(resolver("ejemplo")) }\n'
    )

def gen_swift(title: str, desc: str) -> str:
    return (
        f"// {title}\n// {desc}\n\n"
        'func resolver(_ entrada: String) -> String { entrada }\nprint(resolver("ejemplo"))\n'
    )

def gen_php(title: str, desc: str) -> str:
    return (
        f"<?php\n// {title}\n// {desc}\n\n"
        "function resolver(string $entrada): string {\n    return $entrada;\n}\n\n"
        'echo resolver("ejemplo") . "\\n";\n'
    )

def gen_ruby(title: str, desc: str) -> str:
    return (
        f"# {title}\n# {desc}\n\n"
        "def resolver(entrada)\n  entrada\nend\n\n"
        'puts resolver("ejemplo")\n'
    )

def gen_dart(title: str, desc: str) -> str:
    return (
        f"// {title}\n// {desc}\n\n"
        "String resolver(String entrada) => entrada;\n\n"
        'void main() => print(resolver("ejemplo"));\n'
    )

LANG_GENERATORS = {
    "python":     gen_python,
    "javascript": gen_javascript,
    "typescript": gen_typescript,
    "go":         gen_go,
    "rust":       gen_rust,
    "java":       gen_java,
    "csharp":     gen_csharp,
    "kotlin":     gen_kotlin,
    "swift":      gen_swift,
    "php":        gen_php,
    "ruby":       gen_ruby,
    "dart":       gen_dart,
}

SOLUTIONS_CURATED = {
    "suma-de-digitos": {
        "desc": "Dado un número entero positivo, suma todos sus dígitos individuales. Por ejemplo, si el número es 1234 el resultado sería 1 + 2 + 3 + 4 = 10. Este ejercicio clásico de manipulación numérica te ayudará a practicar la conversión entre tipos de datos y el uso de operaciones aritméticas básicas. Es un problema fundamental que aparece en pruebas técnicas y entrevistas de nivel inicial, y sienta las bases para entender cómo descomponer números en sus componentes.",
        "p1": "**Análisis del problema:** Lo primero es entender cómo extraer dígitos individuales de un número entero. Tenemos dos enfoques principales: el enfoque aritmético (usando división y módulo entre 10 para extraer dígitos de derecha a izquierda) y el enfoque de cadenas (convertir el número a string e iterar sobre cada carácter). Para este problema, el enfoque de cadenas resulta más legible y directo. **Ejemplo concreto:** Con entrada 1234 → lo convertimos a \"1234\" → iteramos: 1+2+3+4 = 10. **Edge cases:** números negativos (usar valor absoluto), número 0 (resultado 0), números muy grandes (considerar límites de representación).",
        "p2": "**Implementación paso a paso:** 1) Tomamos el valor absoluto del número para manejar entradas negativas con `abs(n)`. 2) Convertimos a string con `str()` para poder iterar dígito a dígito. 3) Usamos una expresión generadora con `int(d)` para convertir cada carácter a entero. 4) Sumamos todo con `sum()`. En otros lenguajes como JavaScript, el enfoque es similar: convertimos a string, dividimos en array con `split('')`, transformamos cada elemento a número con `map(Number)` y reducimos con `reduce()`. La clave es que todos los lenguajes modernos ofrecen herramientas para trabajar con colecciones que hacen este código conciso y expresivo.",
        "p3": "**Complejidad:** O(log n) tiempo (o O(d) donde d es el número de dígitos, que es aproximadamente log₁₀(n)). O(1) espacio adicional si usamos el enfoque aritmético, O(d) si usamos cadenas. **Variantes:** 1) Versión aritmética pura con bucle `while n > 0: suma += n % 10; n //= 10` — más eficiente en memoria. 2) Suma recursiva de dígitos hasta obtener un solo dígito (raíz digital). 3) Producto de dígitos en vez de suma. **Aplicaciones reales:** checksums simples, validación de números de tarjeta (Luhn), procesamiento de datos numéricos en ETL.",
        "big_o_time": "O(log n)",
        "big_o_space": "O(1)",
        "test_cases": "1234 | 10; 9999 | 36; 0 | 0; -1234 | 10; 100000 | 1",
        "python":     "def suma_digitos(n):\n    return sum(int(d) for d in str(abs(n)))\n\nprint(suma_digitos(1234))  # 10\nprint(suma_digitos(9999))  # 36",
        "javascript": "const sumaDigitos = n => String(Math.abs(n)).split('').reduce((a, d) => a + +d, 0);\nconsole.log(sumaDigitos(1234)); // 10",
        "typescript": "const sumaDigitos = (n: number): number =>\n  String(Math.abs(n)).split('').reduce((a, d) => a + Number(d), 0);\nconsole.log(sumaDigitos(1234)); // 10",
        "go":         'package main\nimport "fmt"\nfunc sumaDigitos(n int) int {\n\tif n < 0 { n = -n }\n\ts := 0\n\tfor n > 0 { s += n % 10; n /= 10 }\n\treturn s\n}\nfunc main() { fmt.Println(sumaDigitos(1234)) } // 10',
        "rust":       'fn suma_digitos(n: i64) -> i64 {\n    n.abs().to_string().chars().map(|c| c.to_digit(10).unwrap() as i64).sum()\n}\nfn main() { println!("{}", suma_digitos(1234)); } // 10',
        "java":       'public class SumaDigitos {\n    public static int sumar(int n) {\n        n = Math.abs(n); int s = 0;\n        while (n > 0) { s += n % 10; n /= 10; }\n        return s;\n    }\n    public static void main(String[] a) { System.out.println(sumar(1234)); } // 10\n}',
        "csharp":     "using System;\nclass P { static int Suma(int n) => Math.Abs(n).ToString().ToCharArray().Sum(c => c - '0');\n  static void Main() => Console.WriteLine(Suma(1234)); } // 10",
        "kotlin":     "fun sumaDigitos(n: Int) = Math.abs(n).toString().sumOf { it.digitToInt() }\nfun main() { println(sumaDigitos(1234)) } // 10",
        "swift":      "func sumaDigitos(_ n: Int) -> Int { abs(n).description.compactMap { $0.wholeNumberValue }.reduce(0, +) }\nprint(sumaDigitos(1234)) // 10",
        "php":        "<?php\nfunction sumaDigitos(int $n): int { return array_sum(str_split(strval(abs($n)))); }\necho sumaDigitos(1234); // 10",
        "ruby":       "def suma_digitos(n) = n.abs.digits.sum\nputs suma_digitos(1234) # 10",
        "dart":       "int sumaDigitos(int n) => n.abs().toString().split('').fold(0, (s, d) => s + int.parse(d));\nvoid main() => print(sumaDigitos(1234)); // 10",
    },
    "par-o-impar": {
        "desc": "Determina si un número entero es par o impar. Un número par es aquel que puede dividirse exactamente entre 2 (resto 0), mientras que un número impar deja resto 1 al dividirlo entre 2. Este ejercicio, aparentemente trivial, introduce el operador módulo (%), uno de los operadores más útiles en programación para todo tipo de aplicaciones: desde juegos (turnos, animaciones) hasta sistemas de validación y procesamiento de datos cíclicos.",
        "p1": "**Análisis del problema:** La paridad de un número se determina únicamente por su resto al dividir entre 2. Si el resto es 0, es par; si es 1, es impar. **Ejemplo concreto:** 4 ÷ 2 = 2 con resto 0 → Par. 7 ÷ 2 = 3 con resto 1 → Impar. **Edge cases:** números negativos (el módulo en la mayoría de lenguajes preserva la paridad correctamente), número 0 (es par, resto 0), números grandes (no hay problema, solo una operación). **Consideraciones:** En algunos lenguajes como JavaScript, el operador `%` con números negativos puede dar resultados distintos según el signo, pero para determinar paridad siempre funciona correctamente porque nos interesa solo el resto absoluto.",
        "p2": "**Implementación:** La solución es directa: usamos el operador módulo `%` que devuelve el resto de la división. `n % 2 == 0` significa que n es divisible exactamente entre 2, luego es par. En caso contrario, impar. En Python y otros lenguajes, podemos usar un ternario para hacerlo en una línea: `return 'Par' if n % 2 == 0 else 'Impar'`. **Variante bitwise:** Una alternativa más eficiente (aunque marginal) es usar el operador AND bit a bit: `n & 1`. Si el resultado es 0, el último bit es 0 → número par. Esto funciona porque en binario, los números pares siempre terminan en bit 0. Este truco es común en programación de sistemas y embedded donde cada operación cuenta.",
        "p3": "**Complejidad:** O(1) tanto en tiempo como en espacio — es una operación aritmética simple que el hardware ejecuta en un ciclo de CPU. **Variantes:** 1) Determinar si un número es múltiplo de otro (n % k == 0). 2) Alternar colores/turnos en un bucle usando un contador de paridad (útil en juegos y UI). 3) Filtrado de números pares/impares de un array con filtros funcionales. **Aplicaciones reales:** sistemas de turnos en videojuegos, generación de patrones checkerboard, procesamiento de señales, validación de datos en formularios (como números de teléfono o identificaciones que siguen reglas de paridad).",
        "big_o_time": "O(1)",
        "big_o_space": "O(1)",
        "test_cases": "4 | Par; 7 | Impar; 0 | Par; -12 | Par; 1 | Impar",
        "python":     "def par_o_impar(n):\n    return 'Par' if n % 2 == 0 else 'Impar'\n\nprint(par_o_impar(4))   # Par\nprint(par_o_impar(7))   # Impar\nprint(par_o_impar(-12)) # Par",
        "javascript": "const parOImpar = n => n % 2 === 0 ? 'Par' : 'Impar';\nconsole.log(parOImpar(4));  // Par\nconsole.log(parOImpar(7));  // Impar",
        "typescript": "const parOImpar = (n: number): string => n % 2 === 0 ? 'Par' : 'Impar';\nconsole.log(parOImpar(4)); // Par",
        "go":         'package main\nimport "fmt"\nfunc parOImpar(n int) string {\n\tif n%2 == 0 { return "Par" }\n\treturn "Impar"\n}\nfunc main() {\n\tfmt.Println(parOImpar(4))  // Par\n\tfmt.Println(parOImpar(7))  // Impar\n}',
        "rust":       'fn par_o_impar(n: i32) -> &\'static str { if n % 2 == 0 { "Par" } else { "Impar" } }\nfn main() { println!("{}", par_o_impar(4)); }',
        "java":       'public class ParOImpar {\n    public static String check(int n) { return n % 2 == 0 ? "Par" : "Impar"; }\n    public static void main(String[] a) { System.out.println(check(4)); }\n}',
        "csharp":     'using System;\nclass P { static string Check(int n) => n % 2 == 0 ? "Par" : "Impar";\n  static void Main() => Console.WriteLine(Check(4)); }',
        "kotlin":     'fun parOImpar(n: Int) = if (n % 2 == 0) "Par" else "Impar"\nfun main() { println(parOImpar(4)) }',
        "swift":      'func parOImpar(_ n: Int) -> String { n % 2 == 0 ? "Par" : "Impar" }\nprint(parOImpar(4))',
        "php":        '<?php\nfunction parOImpar(int $n): string { return $n % 2 === 0 ? "Par" : "Impar"; }\necho parOImpar(4);',
        "ruby":       'def par_o_impar(n) = n.even? ? "Par" : "Impar"\nputs par_o_impar(4)',
        "dart":       'String parOImpar(int n) => n % 2 == 0 ? "Par" : "Impar";\nvoid main() => print(parOImpar(4));',
    },
    "invertir-palabra": {
        "desc": "Dada una cadena de texto, devuélvela escrita al revés. Por ejemplo, si la entrada es \"hola\", la salida debe ser \"aloh\". Este problema clásico de manipulación de strings aparece constantemente en entrevistas técnicas y pruebas de lógica básica. Trabaja la comprensión de cómo los lenguajes manejan las cadenas como secuencias inmutables de caracteres y familiariza con los métodos de slicing y transformación de colecciones.",
        "p1": "**Análisis del problema:** Invertir una cadena significa recorrer sus caracteres en orden inverso. La mayoría de lenguajes ofrecen mecanismos nativos para esto. **Ejemplo concreto:** \"Python\" → [P,y,t,h,o,n] → inverso: [n,o,h,t,y,P] → \"nohtyP\". **Edge cases:** cadena vacía (debe devolver cadena vacía), palíndromo (\"abcba\" → \"abcba\", igual), un solo carácter (\"a\" → \"a\"), caracteres Unicode/emojis (importante usar métodos aware de Unicode, no bytes). **Restricciones:** algunas implementaciones pueden tener problemas con caracteres multi-byte (como emojis) si no se usa el método correcto.",
        "p2": "**Implementación:** En Python, la forma más directa es `s[::-1]`, que usa slicing con paso negativo para recorrer la cadena de derecha a izquierda. Es concisa y eficiente. En lenguajes como JavaScript, se convierte a array con `split('')`, se invierte con `reverse()` y se vuelve a unir con `join('')`. En Go y otros lenguajes sin método nativo de inversión, se recorre la cadena desde ambos extremos intercambiando posiciones, que es más verboso pero igual de eficiente. **Enfoque manual:** Se puede hacer con un bucle que recorra desde el último índice hasta el primero, añadiendo cada carácter a una nueva cadena. Esto ayuda a entender el proceso subyacente aunque en producción se prefiera la versión nativa.",
        "p3": "**Complejidad:** O(n) tiempo y O(n) espacio, donde n es la longitud de la cadena. En Python, `s[::-1]` crea una nueva cadena en O(n). **Variantes:** 1) Invertir palabras de una frase sin invertir las palabras individuales. 2) Invertir solo vocales o solo consonantes. 3) Invertir bits de un número como variante bitwise. **Aplicaciones reales:** procesamiento de texto, algoritmos de compresión (LZW), verificación de palíndromos, procesamiento de ADN (las cadenas genéticas se leen en direcciones específicas), serialización y ordenamiento inverso de datos en sistemas.",
        "big_o_time": "O(n)",
        "big_o_space": "O(n)",
        "test_cases": "hola | aloh; Python | nohtyP; abcba | abcba;  | ; a | a",
        "python":     "def invertir(s):\n    return s[::-1]\n\nprint(invertir('hola'))    # aloh\nprint(invertir('Python'))  # nohtyP",
        "javascript": "const invertir = s => s.split('').reverse().join('');\nconsole.log(invertir('hola')); // aloh",
        "typescript": "const invertir = (s: string): string => s.split('').reverse().join('');\nconsole.log(invertir('hola')); // aloh",
        "go":         'package main\nimport "fmt"\nfunc invertir(s string) string {\n\tr := []rune(s)\n\tfor i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 { r[i], r[j] = r[j], r[i] }\n\treturn string(r)\n}\nfunc main() { fmt.Println(invertir("hola")) }',
        "rust":       'fn invertir(s: &str) -> String { s.chars().rev().collect() }\nfn main() { println!("{}", invertir("hola")); }',
        "java":       'public class Invertir {\n    public static String invertir(String s) { return new StringBuilder(s).reverse().toString(); }\n    public static void main(String[] a) { System.out.println(invertir("hola")); }\n}',
        "csharp":     'using System;\nclass P { static string Invertir(string s) => new string(Array.Reverse(s.ToCharArray()) is {} ? s.ToCharArray().Reverse().ToArray() : new char[0]);\n  static void Main() => Console.WriteLine(new string("hola".ToCharArray().Reverse().ToArray())); }',
        "kotlin":     'fun invertir(s: String) = s.reversed()\nfun main() { println(invertir("hola")) }',
        "swift":      'func invertir(_ s: String) -> String { String(s.reversed()) }\nprint(invertir("hola"))',
        "php":        '<?php\nfunction invertir(string $s): string { return strrev($s); }\necho invertir("hola");',
        "ruby":       'def invertir(s) = s.reverse\nputs invertir("hola")',
        "dart":       'String invertir(String s) => s.split(\'\').reversed.join();\nvoid main() => print(invertir(\'hola\'));',
    },
    "fibonacci-recursivo": {
        "desc": "Calcula el n-ésimo número de la famosa serie de Fibonacci, donde cada número es la suma de los dos anteriores: F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2). Por ejemplo, F(7) = 13 (0, 1, 1, 2, 3, 5, 8, 13). Este es el ejercicio clásico para entender la recursión y la programación dinámica, apareciendo en innumerables entrevistas técnicas. Sirve como introducción perfecta a conceptos como memoización, complejidad algorítmica y optimización de funciones recursivas.",
        "p1": "**Análisis del problema:** La serie de Fibonacci tiene una definición recursiva natural: cada término depende de los dos anteriores. **Ejemplo concreto:** fib(7) → fib(6) + fib(5) → (fib(5)+fib(4)) + (fib(4)+fib(3)) → ... hasta los casos base F(0)=0 y F(1)=1. **Problema de la recursión pura:** sin optimización, fib(40) genera más de 300 MILLONES de llamadas. El mismo subproblema se calcula miles de veces. Para fib(40), fib(3) se calcula más de 30 millones de veces. **Edge cases:** n=0 → 0, n=1 → 1, n negativo (no definido para esta serie), n grande (el número crece exponencialmente, se necesita BigInt para n > 92 en 64 bits).",
        "p2": "**Implementación con memoización:** La solución óptima usa un cache (`functools.lru_cache` en Python, `Map` en otros lenguajes) que almacena resultados ya calculados. Así cada F(k) se calcula una sola vez. **Estructura:** 1) Casos base: si n ≤ 1, devolver n. 2) Consultar cache: si ya calculamos F(n), devolverlo. 3) Calcular recursivamente: F(n) = F(n-1) + F(n-2), guardar en cache y devolver. **Alternativa iterativa:** Con un bucle simple es aún más eficiente: O(n) tiempo y O(1) espacio, sin recursión ni cache. Simplemente se mantienen dos variables a, b = 0, 1 y se actualizan en cada iteración. Esta versión es la preferida en producción. **Versión con array:** precalcular todos los valores hasta n en un array, también O(n) tiempo y O(n) espacio.",
        "p3": "**Complejidad:** Recursivo puro: O(2^n) tiempo — catastrófico, no usable para n > 30. Con memoización: O(n) tiempo, O(n) espacio (para el cache y la pila de recursión). Iterativo: O(n) tiempo, O(1) espacio — el mejor. **Matemáticas:** La fórmula de Binet permite calcular F(n) en O(1) usando el número áureo φ = (1 + √5) / 2. **Aplicaciones reales:** modelado de crecimiento poblacional, algoritmos de compresión con Fibonacci coding, búsqueda en árboles Fibonacci (estructura de datos), análisis de mercados financieros, optimización de búsqueda con búsqueda Fibonacci (similar a binaria pero con proporción áurea).",
        "big_o_time": "O(2^n) (O(n) con memoización/iterativo)",
        "big_o_space": "O(n) recursivo, O(1) iterativo",
        "test_cases": "0 | 0; 1 | 1; 7 | 13; 10 | 55; 20 | 6765",
        "python":     "from functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)\n\nfor i in range(10):\n    print(f'fib({i}) = {fib(i)}')",
        "javascript": "function fib(n, memo = {}) {\n  if (n <= 1) return n;\n  if (memo[n]) return memo[n];\n  memo[n] = fib(n-1, memo) + fib(n-2, memo);\n  return memo[n];\n}\nfor (let i = 0; i < 10; i++) console.log(`fib(${i}) = ${fib(i)}`);",
        "typescript": "function fib(n: number, memo: Record<number, number> = {}): number {\n  if (n <= 1) return n;\n  if (memo[n] !== undefined) return memo[n];\n  return (memo[n] = fib(n-1, memo) + fib(n-2, memo));\n}\nconsole.log(fib(7)); // 13",
        "go":         'package main\nimport "fmt"\nfunc fib(n int, memo map[int]int) int {\n\tif n <= 1 { return n }\n\tif v, ok := memo[n]; ok { return v }\n\tmemo[n] = fib(n-1, memo) + fib(n-2, memo)\n\treturn memo[n]\n}\nfunc main() {\n\tm := map[int]int{}\n\tfmt.Println(fib(7, m)) // 13\n}',
        "rust":       'use std::collections::HashMap;\nfn fib(n: u64, memo: &mut HashMap<u64, u64>) -> u64 {\n    if n <= 1 { return n; }\n    if let Some(&v) = memo.get(&n) { return v; }\n    let v = fib(n-1, memo) + fib(n-2, memo);\n    memo.insert(n, v); v\n}\nfn main() {\n    let mut m = HashMap::new();\n    println!("{}", fib(7, &mut m)); // 13\n}',
        "java":       'import java.util.HashMap;\npublic class Fibonacci {\n    static HashMap<Integer,Long> memo = new HashMap<>();\n    static long fib(int n) {\n        if (n <= 1) return n;\n        if (memo.containsKey(n)) return memo.get(n);\n        long v = fib(n-1) + fib(n-2);\n        memo.put(n, v); return v;\n    }\n    public static void main(String[] a) { System.out.println(fib(7)); } // 13\n}',
        "csharp":     'using System;\nusing System.Collections.Generic;\nclass Fib {\n    static Dictionary<int,long> memo = new();\n    static long F(int n) {\n        if (n <= 1) return n;\n        if (memo.ContainsKey(n)) return memo[n];\n        return memo[n] = F(n-1) + F(n-2);\n    }\n    static void Main() => Console.WriteLine(F(7)); // 13\n}',
        "kotlin":     'fun fib(n: Int, memo: MutableMap<Int,Long> = mutableMapOf()): Long {\n    if (n <= 1) return n.toLong()\n    return memo.getOrPut(n) { fib(n-1, memo) + fib(n-2, memo) }\n}\nfun main() { println(fib(7)) } // 13',
        "swift":      'var memo = [Int: Int]()\nfunc fib(_ n: Int) -> Int {\n    if n <= 1 { return n }\n    if let v = memo[n] { return v }\n    memo[n] = fib(n-1) + fib(n-2)\n    return memo[n]!\n}\nprint(fib(7)) // 13',
        "php":        '<?php\nfunction fib(int $n, array &$m = []): int {\n    if ($n <= 1) return $n;\n    if (isset($m[$n])) return $m[$n];\n    return $m[$n] = fib($n-1, $m) + fib($n-2, $m);\n}\necho fib(7); // 13',
        "ruby":       'def fib(n, memo = {})\n  return n if n <= 1\n  memo[n] ||= fib(n-1, memo) + fib(n-2, memo)\nend\nputs fib(7) # 13',
        "dart":       'int fib(int n, [Map<int,int>? memo]) {\n  memo ??= {};\n  if (n <= 1) return n;\n  return memo[n] ??= fib(n-1, memo) + fib(n-2, memo);\n}\nvoid main() => print(fib(7)); // 13',
    },
    "detector-de-palindromos": {
        "desc": "Comprueba si una palabra o frase es un palíndromo: que se lee igual de izquierda a derecha que de derecha a izquierda, ignorando espacios, signos de puntuación y diferencias entre mayúsculas y minúsculas. Ejemplos clásicos: \"Ana\" (true), \"A man, a plan, a canal: Panama\" (true), \"hola\" (false). Este ejercicio es fundamental para practicar normalización de texto, expresiones regulares y manipulación de cadenas — habilidades esenciales en procesamiento de lenguaje natural y validación de datos textuales.",
        "p1": "**Análisis del problema:** Un palíndromo se define por su simetría. La clave está en qué comparamos y cómo normalizamos. **Ejemplo concreto:** \"A man, a plan, a canal: Panama\" → normalizado: \"amanaplanacanalpanama\" → inverso: \"amanaplanacanalpanama\" → son iguales → true. **Edge cases:** cadena vacía (es palíndromo por definición), un solo carácter (siempre true), frases con solo símbolos (\"!?,\" vacío = true), frases con números (\"a1a\" es palíndromo), caracteres acentuados (depende de si se normalizan: \"súes\" vs \"sues\"), mayúsculas mixtas (\"Ana\" debe ser true). **Restricciones importantes:** el método debe ser eficiente para frases largas, manejar Unicode correctamente y no alterar el significado de la comparación.",
        "p2": "**Implementación:** 1) Convertir toda la cadena a minúsculas con `s.lower()` para ignorar mayúsculas. 2) Eliminar todo lo que no sea alfanumérico (espacios, puntuación, símbolos) usando una expresión regular: `re.sub(r'[^a-z0-9]', '', s)`. 3) Comparar la cadena resultante con su inversa. En Python, `limpio == limpio[::-1]`. **Versión optimizada (two pointers):** en vez de crear una copia inversa (O(n) espacio extra), podemos usar dos punteros (uno al inicio, otro al final) que avanzan hacia el centro comparando caracteres, saltando no-alfanuméricos. Esta versión usa O(1) espacio adicional. Es más compleja de implementar pero más eficiente para frases muy largas y es la solución esperada en entrevistas técnicas de nivel medio.",
        "p3": "**Complejidad:** O(n) tiempo en ambos enfoques. O(n) espacio en la versión con inversión de cadena (por la copia). O(1) espacio en la versión two pointers. **Variantes:** 1) Detectar el palíndromo más largo dentro de una cadena (problema clásico de entrevista). 2) Verificar si un número entero es palíndromo (sin convertirlo a string). 3) Palíndromos en listas/arrays. 4) Palíndromos permisivos con hasta k eliminaciones de caracteres. **Aplicaciones reales:** procesamiento de ADN (secuencias palindrómicas son relevantes en genética), validación de datos simétricos, compresión de datos, análisis literario y de texto, algoritmos de búsqueda de patrones en bioinformática.",
        "big_o_time": "O(n)",
        "big_o_space": "O(n) (O(1) con two pointers)",
        "test_cases": "Ana | true; hola | false; A man a plan a canal Panama | true;  | true; a1a | true",
        "python":     "import re\n\ndef es_palindromo(s):\n    limpio = re.sub(r'[^a-z0-9]', '', s.lower())\n    return limpio == limpio[::-1]\n\nprint(es_palindromo('Ana'))          # True\nprint(es_palindromo('A man a plan a canal Panama'))  # True\nprint(es_palindromo('hola'))         # False",
        "javascript": "function esPalindromo(s) {\n  const limpio = s.toLowerCase().replace(/[^a-z0-9]/g, '');\n  return limpio === limpio.split('').reverse().join('');\n}\nconsole.log(esPalindromo('Ana'));  // true",
        "typescript": "function esPalindromo(s: string): boolean {\n  const limpio = s.toLowerCase().replace(/[^a-z0-9]/g, '');\n  return limpio === limpio.split('').reverse().join('');\n}\nconsole.log(esPalindromo('Ana')); // true",
        "go":         'package main\nimport (\n\t"fmt"\n\t"regexp"\n\t"strings"\n\t"unicode/utf8"\n)\nfunc esPalindromo(s string) bool {\n\tre := regexp.MustCompile(`[^a-z0-9]`)\n\tl := re.ReplaceAllString(strings.ToLower(s), "")\n\tr := []rune(l)\n\tfor i, j := 0, utf8.RuneCountInString(l)-1; i < j; i, j = i+1, j-1 {\n\t\tif r[i] != r[j] { return false }\n\t}\n\treturn true\n}\nfunc main() { fmt.Println(esPalindromo("Ana")) }',
        "rust":       'fn es_palindromo(s: &str) -> bool {\n    let l: String = s.to_lowercase().chars().filter(|c| c.is_alphanumeric()).collect();\n    l == l.chars().rev().collect::<String>()\n}\nfn main() { println!("{}", es_palindromo("Ana")); }',
        "java":       'public class Palindromo {\n    public static boolean check(String s) {\n        String l = s.toLowerCase().replaceAll("[^a-z0-9]", "");\n        return l.equals(new StringBuilder(l).reverse().toString());\n    }\n    public static void main(String[] a) { System.out.println(check("Ana")); }\n}',
        "csharp":     'using System;\nusing System.Linq;\nusing System.Text.RegularExpressions;\nclass P {\n    static bool EsPalindromo(string s) {\n        var l = Regex.Replace(s.ToLower(), "[^a-z0-9]", "");\n        return l == new string(l.Reverse().ToArray());\n    }\n    static void Main() => Console.WriteLine(EsPalindromo("Ana"));\n}',
        "kotlin":     'fun esPalindromo(s: String): Boolean {\n    val l = s.lowercase().filter { it.isLetterOrDigit() }\n    return l == l.reversed()\n}\nfun main() { println(esPalindromo("Ana")) }',
        "swift":      'func esPalindromo(_ s: String) -> Bool {\n    let l = s.lowercased().filter { $0.isLetter || $0.isNumber }\n    return l == String(l.reversed())\n}\nprint(esPalindromo("Ana"))',
        "php":        '<?php\nfunction esPalindromo(string $s): bool {\n    $l = preg_replace(\'/[^a-z0-9]/\', \'\', strtolower($s));\n    return $l === strrev($l);\n}\necho esPalindromo("Ana") ? "true" : "false";',
        "ruby":       'def es_palindromo?(s)\n  l = s.downcase.gsub(/[^a-z0-9]/, "")\n  l == l.reverse\nend\nputs es_palindromo?("Ana")',
        "dart":       'bool esPalindromo(String s) {\n  final l = s.toLowerCase().replaceAll(RegExp(r\'[^a-z0-9]\'), \'\');\n  return l == l.split(\'\').reversed.join();\n}\nvoid main() => print(esPalindromo(\'Ana\'));',
    },
}

from scripts.solutions_data import SOLUTIONS as EXTENDED_SOLUTIONS

CURATED_SLUGS = {"suma-de-digitos", "par-o-impar", "invertir-palabra",
                 "fibonacci-recursivo", "detector-de-palindromos"}
SOLUTIONS = {k: v for k, v in EXTENDED_SOLUTIONS.items() if k not in CURATED_SLUGS}
SOLUTIONS.update(SOLUTIONS_CURATED)


def _normalize_key(titulo: str) -> str:
    nfkd = unicodedata.normalize('NFKD', titulo)
    ascii_str = nfkd.encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', ascii_str.lower())).strip('-')


def _expand_field(original: str, min_len: int, field_type: str) -> str:
    """Wraps a short DB entry field with additional verbose context if too short."""
    if len(original) >= min_len:
        return original
    extras = {
        "desc": (
            "\n\n*Este problema requiere que diseñes e implementes una solución completa. "
            "Analiza cuidadosamente los requisitos, considera los casos límite y asegúrate de que tu código sea robusto "
            "y siga las mejores prácticas del lenguaje. La habilidad de transformar enunciados en código funcional "
            "es fundamental en el desarrollo de software profesional.*"
        ),
        "p1": (
            "\n\n**Para profundizar en el análisis:**\n"
            "- Identifica el propósito central del algoritmo\n"
            "- Prueba con un ejemplo concreto paso a paso\n"
            "- Enumera los edge cases: valores vacíos, nulos, extremos, inesperados\n"
            "- Determina la estrategia óptima antes de escribir código"
        ),
        "p2": (
            "\n\n**Para enriquecer la implementación:**\n"
            "- Valida las entradas al inicio de la función\n"
            "- Elige estructuras de datos que maximicen eficiencia y legibilidad\n"
            "- Separa la lógica en pasos claros y comenta las partes no obvias\n"
            "- Incluye un ejemplo de uso al final para verificar el funcionamiento"
        ),
        "p3": (
            "\n\n**Para un análisis más completo:**\n"
            "- Calcula la complejidad temporal considerando el peor, mejor y caso promedio\n"
            "- Evalúa si el consumo de memoria se puede reducir\n"
            "- Propone variantes: ¿y si la entrada fuera 10x más grande? ¿y si hubiera que procesarla en streaming?\n"
            "- Menciona aplicaciones reales donde este patrón de solución es relevante"
        ),
    }
    extra = extras.get(field_type, "")
    if not extra:
        return original
    if len(original) < 60:
        return original + extra
    return original + extra


def lookup(titulo: str, lang_id: str) -> dict | None:
    slug = _normalize_key(titulo)

    sol = None
    for key, data in SOLUTIONS.items():
        if key in slug or slug in key:
            sol = data
            break

    if not sol:
        return None

    lang_to_short = {"python": "py", "javascript": "js", "typescript": "ts",
                     "go": "go", "rust": "rs", "java": "java", "csharp": "cs",
                     "kotlin": "kt", "swift": "sw", "php": "php", "ruby": "rb", "dart": "dart"}
    codigo = (sol.get(lang_id)
              or sol.get(lang_to_short.get(lang_id))
              or sol.get("python")
              or sol.get("py", ""))
    return {
        "titulo":      titulo,
        "descripcion": _expand_field(sol["desc"], 150, "desc"),
        "paso1":       _expand_field(sol["p1"], 200, "p1"),
        "paso2":       _expand_field(sol.get("p2", ""), 200, "p2"),
        "paso3":       _expand_field(sol.get("p3", ""), 150, "p3"),
        "big_o_time":  sol.get("big_o_time", "O(n)"),
        "big_o_space": sol.get("big_o_space", "O(n)"),
        "test_cases":  sol.get("test_cases", "ejemplo | resultado"),
        "codigo":      codigo,
        "dificultad":  "Intermedio",
    }


def generate_generic(titulo: str, lang_id: str, descripcion: str | None = None) -> dict:
    desc = descripcion or f"Implementa una solución para: {titulo}"
    gen = LANG_GENERATORS.get(lang_id, gen_python)
    codigo = gen(titulo, desc)
    return {
        "titulo":      titulo,
        "descripcion": (
            f"El problema consiste en: {desc}. "
            f"Deberás escribir un programa que reciba los datos de entrada, procese la información según la lógica requerida "
            f"y devuelva el resultado esperado. Este tipo de ejercicio pone a prueba tu capacidad para analizar requisitos, "
            f"diseñar una solución algorítmica y traducirla a código limpio y funcional en {lang_id}.\n\n"
            f"**Ejemplo práctico:** Imagina que trabajas en un sistema de procesamiento de datos donde necesitas transformar "
            f"información de un formato a otro, aplicando reglas de negocio específicas. La solución que implementes aquí "
            f"refleja exactamente ese tipo de razonamiento.\n\n"
            f"**Requisitos:**\n"
            f"- La entrada puede variar en formato y tamaño, tu código debe ser robusto\n"
            f"- Controla edge cases como valores nulos, límites numéricos o cadenas vacías\n"
            f"- La eficiencia importa: busca siempre la solución más óptima en tiempo y espacio"
        ),
        "paso1": (
            f"**Análisis del problema:**\n\n"
            f"El primer paso es entender exactamente qué se nos pide. Leemos el enunciado de '{titulo}' "
            f"e identificamos:\n"
            f"- **Entradas**: ¿qué datos recibe el programa? ¿de qué tipo son? ¿pueden venir vacíos o con formato inesperado?\n"
            f"- **Salidas**: ¿qué debe devolver? ¿un valor booleano, un número, una cadena, una estructura más compleja?\n"
            f"- **Restricciones**: ¿hay límites de tamaño? ¿el algoritmo debe ser eficiente para entradas grandes?\n\n"
            f"**Ejemplo concreto:** Probemos con datos de ejemplo. Supongamos que la entrada es un caso típico. "
            f"Aplicamos la lógica manualmente para verificar que entendemos el flujo correcto. "
            f"Este paso manual nos ayuda a detectar edge cases antes de escribir una sola línea de código.\n\n"
            f"**Edge cases a considerar:**\n"
            f"- Entrada vacía o nula\n"
            f"- Valores en los límites del rango permitido\n"
            f"- Datos con formato inesperado\n"
            f"- Repeticiones o duplicados (si aplica)"
        ),
        "paso2": (
            f"**Implementación en {lang_id}:**\n\n"
            f"Ahora traducimos el análisis a código. La estrategia general sigue estos pasos:\n\n"
            f"1. **Validación de entrada**: lo primero es comprobar que los datos recibidos son válidos. "
            f"Si la entrada no cumple los requisitos, devolvemos un valor por defecto o lanzamos un error controlado.\n\n"
            f"2. **Procesamiento principal**: aplicamos la lógica central del algoritmo. "
            f"Elegimos la estructura de datos más adecuada:\n"
            f"   - ¿Necesitamos búsquedas rápidas? → hash map / diccionario\n"
            f"   - ¿Ordenamos elementos? → arrays con sort\n"
            f"   - ¿Recorremos secuencialmente? → bucles simples\n\n"
            f"3. **Generación de salida**: formateamos el resultado según lo esperado.\n\n"
            f"**Estructuras de datos usadas:**\n"
            f"- La elección de estructuras determina la eficiencia de la solución\n"
            f"- Priorizamos estructuras nativas del lenguaje para mantener el código idiomático\n"
            f"- Para {lang_id}, usaremos las construcciones más naturales del lenguaje"
        ),
        "paso3": (
            f"**Complejidad y optimización:**\n\n"
            f"**Complejidad temporal:** La solución propuesta tiene complejidad O(n) en el caso promedio, "
            f"donde n es el tamaño de la entrada. Esto significa que el tiempo de ejecución crece linealmente "
            f"con el volumen de datos.\n\n"
            f"**Complejidad espacial:** O(n) adicional en el peor caso por las estructuras auxiliares "
            f"necesarias para el procesamiento.\n\n"
            f"**Posibles optimizaciones:**\n"
            f"- Si el rendimiento es crítico, se puede reemplazar algún bucle anidado por una estructura hash\n"
            f"- Para conjuntos de datos muy grandes, considera procesamiento perezoso (lazy evaluation) "
            f"o paralelización si el lenguaje lo soporta\n\n"
            f"**Aplicaciones reales:**\n"
            f"Este patrón de solución aparece en sistemas de procesamiento de datos, APIs REST, "
            f"pipelines ETL y validación de formularios. La habilidad de transformar requisitos "
            f"en código estructurado es fundamental en cualquier rol de desarrollo de software."
        ),
        "big_o_time":  "O(n)",
        "big_o_space": "O(n)",
        "test_cases":  "entrada_ejemplo | salida_ejemplo; caso_límite | resultado_esperado; entrada_vacía | manejo_error",
        "codigo":      codigo,
        "dificultad":  "Intermedio",
    }
