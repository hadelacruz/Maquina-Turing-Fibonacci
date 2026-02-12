# 🔢 Máquina de Turing - Fibonacci

Simulador de una Máquina de Turing que calcula la secuencia de Fibonacci en notación unaria.

## 📋 Descripción

Este proyecto implementa un simulador de Máquina de Turing determinista que, dado un número `n` representado en notación unaria (como `n` unos: `111` = 3), calcula `F(n)` (el n-ésimo número de Fibonacci) y lo escribe en la cinta también en notación unaria.

### Secuencia de Fibonacci
```
F(0) = 0
F(1) = 1
F(n) = F(n-1) + F(n-2)  para n ≥ 2

Secuencia: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...
```

## 🏗️ Estructura del Proyecto

```
📁 Maquina-Turing-Fibonacci/
├── 📄 main.py              # Punto de entrada principal
├── 📄 turing_machine.py    # Definición de la Máquina de Turing
├── 📄 tape.py              # Implementación de la cinta infinita
├── 📄 simulator.py         # Motor de simulación
├── 📄 loader.py            # Cargador de configuración YAML
├── 📄 analysis.py          # Análisis de complejidad empírica
├── 📄 test_fib.py          # Tests de verificación
├── 📄 fibonacci_new.yaml   # Definición de la MT (configuración actual)
├── 📄 fibonacci.yaml       # Definición original (referencia)
└── 📄 requirements.txt     # Dependencias
```

## 🚀 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/hadelacruz/Maquina-Turing-Fibonacci.git
   cd Maquina-Turing-Fibonacci
   ```

2. **Crear entorno virtual (opcional pero recomendado)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Uso

### Ejecución básica
```bash
python main.py
```

Se te pedirá ingresar un valor de `n` y el programa calculará `F(n)`.

### Modo verbose (paso a paso)
Para ver cada transición de la máquina:
```bash
python main.py --verbose
```

### Tests
Ejecutar la suite de pruebas para verificar `F(0)` a `F(10)`:
```bash
python test_fib.py
```

### Análisis de complejidad
```bash
python analysis.py
```

## 🔧 Cómo funciona

### Representación en la cinta
La cinta utiliza la siguiente estructura:
```
[contador]$[zona a]#[zona b]
```

- **contador**: `n` unos que se van marcando con `X` en cada iteración
- **$**: separador entre contador y área de trabajo
- **zona a**: almacena `F(i-1)` durante la iteración `i`
- **#**: separador entre a y b
- **zona b**: almacena `F(i)` durante la iteración `i`

### Ejemplo: F(4) = 3

```
Entrada:     1111           (n=4 en unario)
Inicial:     1111$#1        (a=0, b=1)

Iteración 1: X111$1#1       (a=1, b=1)
Iteración 2: XX11$1#11      (a=1, b=2)
Iteración 3: XXX1$11#111    (a=2, b=3)
Iteración 4: XXXX$111#11111 (a=3, b=5)

Limpieza:    XXXX$___111    
Resultado:   111 = 3 ✓
```

### Algoritmo de cada iteración
Para transformar `(a, b)` → `(b, a+b)`:

1. **Marcar b**: Convertir `1` → `Y` en zona b (preservar b_old)
2. **Copiar a → b**: Por cada `1` en a, agregar `1` al final de b
3. **Borrar a**: Eliminar zona a
4. **Copiar Y → a**: Mover los `Y` (b_old) a la zona a
5. **Restaurar**: Convertir `Y` → `1`

## 📊 Complejidad

| n | F(n) | Pasos |
|---|------|-------|
| 0 | 0    | 1     |
| 1 | 1    | 3     |
| 2 | 1    | 15    |
| 3 | 2    | 56    |
| 4 | 3    | 122   |
| 5 | 5    | 238   |
| 6 | 8    | 469   |
| 7 | 13   | 967   |
| 8 | 21   | 2,123 |
| 9 | 34   | 4,924 |
| 10| 55   | 11,922|

La complejidad temporal es aproximadamente **O(F(n)²)** debido a las operaciones de copia y desplazamiento en la cinta.

## 📝 Configuración YAML

La máquina se define en `fibonacci_new.yaml` con la siguiente estructura:

```yaml
states:
  - q0         # Estado inicial
  - q_accept   # Estado de aceptación
  - ...        # Estados intermedios

input_alphabet:
  - '1'        # Entrada en unario

tape_alphabet:
  - '1', 'X', 'Y', 'Z', 'W'  # Símbolos de trabajo
  - '$', '#'                  # Separadores
  - '_'                       # Blanco

transitions:
  - from_state: q0
    read: '1'
    to_state: q1
    write: '1'
    move: R
  # ... más transiciones
```

## 🧪 Verificación

Los valores calculados corresponden a la secuencia de Fibonacci estándar:

```
F(0)=0 ✓   F(5)=5 ✓
F(1)=1 ✓   F(6)=8 ✓
F(2)=1 ✓   F(7)=13 ✓
F(3)=2 ✓   F(8)=21 ✓
F(4)=3 ✓   F(9)=34 ✓
           F(10)=55 ✓
```

## 📚 Referencias

- [Turing Machine - Wikipedia](https://en.wikipedia.org/wiki/Turing_machine)
- [Fibonacci Sequence - Wikipedia](https://en.wikipedia.org/wiki/Fibonacci_sequence)
- Michael Sipser, *Introduction to the Theory of Computation*

## 👤 Autor

**hadelacruz** - Universidad del Valle de Guatemala
**Jose Auyón** 
---

*Proyecto desarrollado para el curso de Algoritmos*
