# Máquina de Turing - Fibonacci

Simulador de una Máquina de Turing que calcula la secuencia de Fibonacci en notación unaria.

## Descripción

Este proyecto implementa un simulador de Máquina de Turing determinista que, dado un número `n` en notación unaria (`111` = 3), calcula `F(n)` (el n-ésimo número de Fibonacci) y lo escribe en la cinta en notación unaria.

## Video

[![Ver video](https://img.youtube.com/vi/HJk6L2nPIa8/0.jpg)](https://youtu.be/HJk6L2nPIa8)


## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/hadelacruz/Maquina-Turing-Fibonacci.git
   cd Maquina-Turing-Fibonacci
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Menú interactivo
```bash
python main.py
```

### Secuencia de Fibonacci
```
F(0) = 0
F(1) = 1
F(n) = F(n-1) + F(n-2)  para n >= 2

Secuencia: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...
```

## Estructura del Proyecto

```
Maquina-Turing-Fibonacci/
├── main.py              # Menú principal interactivo
├── turing_machine.py    # Definición de la Máquina de Turing
├── tape.py              # Implementación de la cinta infinita
├── simulator.py         # Motor de simulación
├── loader.py            # Cargador de configuración YAML
├── analysis.py          # Análisis de complejidad empírica
├── test_fib.py          # Tests de verificación
├── fibonacci_new.yaml   # Definición de la MT
└── requirements.txt     # Dependencias
```

### Ejemplo: F(4) = 3

```
Entrada:     1111           (n=4)
Inicial:     1111$#1        (a=0, b=1)
Iteración 1: X111$1#1       (a=1, b=1)
Iteración 2: XX11$1#11      (a=1, b=2)
Iteración 3: XXX1$11#111    (a=2, b=3)
Iteración 4: XXXX$111#11111 (a=3, b=5)
Limpieza:    XXXX$___111    
Resultado:   111 = 3
```

## Complejidad

La complejidad temporal es aproximadamente **O(F(n)²)** debido a las operaciones de copia y desplazamiento en la cinta.

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

## Configuración YAML

La máquina se define en `fibonacci_new.yaml`:

```yaml
states:
  - q0         # Estado inicial
  - q_accept   # Estado de aceptación
  - ...

input_alphabet:
  - '1'

tape_alphabet:
  - '1', 'X', 'Y', 'Z', 'W'
  - '$', '#'
  - '_'

transitions:
  - from_state: q0
    read: '1'
    to_state: q1
    write: '1'
    move: R
```

## Autores

- Universidad del Valle de Guatemala
- hadelacruz 
- Jose Auyón
- Daniel Juárez

---

Proyecto desarrollado para el curso de Algoritmos
