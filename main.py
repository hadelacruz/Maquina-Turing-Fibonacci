import sys

from loader import load_from_file
from simulator import TuringSimulator


def main():
    
    print("SIMULADOR DE MÁQUINA DE TURING - FIBONACCI")
    print("=" * 60)
    
    machine_file = "fibonacci_new.yaml"
    
    try:
        print(f"Cargando: {machine_file}...")
        machine = load_from_file(machine_file)
        print(f"- Máquina cargada exitosamente\n")
    except Exception as e:
        print(f"- Error al cargar la máquina: {e}")
        return
    
    # Verificar si se solicita análisis
    if len(sys.argv) > 1 and sys.argv[1] == "--analysis":
        run_batch_analysis(machine)
        return
    
    # Solicitar entrada
    print("CONFIGURACIÓN DE ENTRADA")
    print("=" * 60)
    print("\nConvención utilizada:")
    print("  - Entrada: n en notación unaria (n unos)")
    print("  - Salida: F(n) en notación unaria")
    print("  - Ejemplo: n=5 → '11111' → F(5)=5 → '11111'")
    
    if len(sys.argv) > 1:
        input_string = sys.argv[1]
    else:
        print("\nOpciones:")
        print("  1. Ingresar número decimal n (se convertirá a unario)")
        print("  2. Ingresar directamente en notación unaria")
        
        choice = input("\nSeleccione opción (1/2) [1]: ").strip()
        
        if choice == "2":
            input_string = input("Ingrese cadena unaria (ej: '111'): ")
        else:
            try:
                n = int(input("Ingrese número n: "))
                input_string = "1" * n
                print(f"- Convertido a unario: '{input_string}'")
            except ValueError:
                print("- Entrada inválida, usando n=0")
                input_string = ""
    
    print(f"\n{'='*60}")
    print(f"Entrada: n={len(input_string)} → '{input_string}'")
    print(f"{'='*60}\n")
    
    # Crear y ejecutar simulador
    verbose = "--quiet" not in sys.argv
    simulator = TuringSimulator(machine, input_string, verbose=verbose)
    
    try:
        results = simulator.run(max_steps=100000)
    except KeyboardInterrupt:
        print("\n\n- Simulación interrumpida por el usuario")
        return
    except Exception as e:
        print(f"\n\n- Error durante la simulación: {e}")
        return
    
    # Interpretar resultado
    print("\n" + "=" * 60)
    print("INTERPRETACIÓN DEL RESULTADO")
    print("=" * 60)
    
    n = len(input_string)
    output = results['tape_content']
    fib_result = output.count('1') if output else 0
    
    print(f"\n  Entrada n = {n}")
    print(f"  Salida en cinta: '{output}'")
    print(f"  Interpretación: F({n}) = {fib_result}")
    
    # Verificar contra valor esperado
    expected = fibonacci_iterative(n)
    if fib_result == expected:
        print(f"  ✓ Correcto! (esperado: {expected})")
    else:
        print(f"  ✗ Incorrecto (esperado: {expected})")
    
    # Análisis de complejidad
    print("\n" + "=" * 60)
    print("ANÁLISIS DE COMPLEJIDAD")
    print("=" * 60)
    
    steps = results['step_count']
    
    print(f"\nTamaño de entrada (n): {n}")
    print(f"Número de pasos: {steps}")
    
    if n > 0:
        ratio = steps / n
        print(f"Relación pasos/n: {ratio:.2f}")
        print(f"\n💡 Este dato ayuda a inferir la complejidad O(f(n))")
        print("   Ejecute con diferentes valores de n para ver el crecimiento.")
        print("   Use 'python analysis.py' para análisis empírico completo.")
    
    print("\n" + "=" * 60)
    print("- Simulación completada\n")


def fibonacci_iterative(n):
    """Calcula F(n) de forma iterativa para verificación."""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def run_batch_analysis(machine):
    """Ejecuta análisis batch para múltiples valores de n."""
    print("\n" + "=" * 60)
    print("ANÁLISIS BATCH")
    print("=" * 60)
    
    test_values = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    print(f"\n{'n':>5} | {'Entrada':>10} | {'Pasos':>8} | {'Resultado':>10} | {'Esperado':>10} | {'OK':>4}")
    print("-" * 60)
    
    for n in test_values:
        input_string = "1" * n
        simulator = TuringSimulator(machine, input_string, verbose=False)
        results = simulator.run(max_steps=100000)
        
        output = results['tape_content']
        fib_result = output.count('1') if output else 0
        expected = fibonacci_iterative(n)
        ok = "✓" if fib_result == expected else "✗"
        
        print(f"{n:>5} | {input_string or '(vacía)':>10} | {results['step_count']:>8} | {fib_result:>10} | {expected:>10} | {ok:>4}")
    
    print("-" * 60)
    print("\nPara análisis empírico con gráficos, ejecute: python analysis.py")


if __name__ == "__main__":
    main()
