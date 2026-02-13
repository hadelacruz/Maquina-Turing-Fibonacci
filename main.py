import sys

from loader import load_from_file
from simulator import TuringSimulator


def run_single_simulation():
    
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
        print(f"  Correcto! (esperado: {expected})")
    else:
        print(f"  Incorrecto (esperado: {expected})")
    
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
        print(f"\n Este dato ayuda a inferir la complejidad O(f(n))")
        print("   Ejecute con diferentes valores de n para ver el crecimiento.")
        print("   Use 'python analysis.py' para análisis empírico completo.")
    
    print("\n" + "=" * 60)
    print(" Simulación completada")
    print("=" * 60)


def fibonacci_iterative(n):
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


def run_tests():
    """Ejecuta la suite completa de tests"""
    from test_fib import test_fibonacci_sequence
    
    print("\n" + "=" * 60)
    print("EJECUTANDO TESTS DE FIBONACCI")
    print("=" * 60 + "\n")
    
    test_fibonacci_sequence()
    
    print("\n" + "=" * 60)
    print(" TESTS COMPLETADOS")
    print("=" * 60)


def run_full_analysis():
    """Ejecuta el análisis de complejidad y genera gráficos"""
    from analysis import run_analysis, plot_analysis
    
    print("\n" + "=" * 60)
    print("ANÁLISIS DE COMPLEJIDAD")
    print("=" * 60 + "\n")
    
    print("Ejecutando simulaciones para n=0 hasta n=10...")
    results = run_analysis()
    
    if results:
        print("\nGenerando gráficos...")
        plot_analysis(results)
        print("\n" + "=" * 60)
        print(" Análisis completado. Revisa los gráficos generados.")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print(" Error durante el análisis.")
        print("=" * 60)


def show_machine_info():
    """Muestra información sobre la máquina de Turing cargada"""
    try:
        machine = load_from_file('fibonacci_new.yaml')
        
        print("\n" + "=" * 60)
        print("INFORMACIÓN DE LA MÁQUINA DE TURING")
        print("=" * 60)
        print(f"\nEstados: {len(machine.states)}")
        print(f"Alfabeto de entrada: {machine.input_alphabet}")
        print(f"Alfabeto de cinta: {machine.tape_alphabet}")
        print(f"Estado inicial: {machine.initial_state}")
        print(f"Estados finales: {machine.final_states}")
        print(f"Número de transiciones: {len(machine.transitions)}")
        print(f"Símbolo blanco: '{machine.blank_symbol}'")
        print("\n" + "=" * 60)
        
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'fibonacci_new.yaml'")
    except Exception as e:
        print(f"Error: {str(e)}")


def run_all():
    """Ejecuta todas las funcionalidades en secuencia"""
    print("\n" + "=" * 60)
    print("EJECUCIÓN COMPLETA")
    print("=" * 60)
    
    # 1. Tests
    run_tests()
    input("\nPresiona Enter para continuar con el análisis...")
    
    # 2. Análisis
    run_full_analysis()
    input("\nPresiona Enter para continuar con una simulación...")
    
    # 3. Simulación individual
    run_single_simulation()
    
    print("\n" + "=" * 60)
    print(" EJECUCIÓN COMPLETA FINALIZADA")
    print("=" * 60)


def print_menu():
    """Imprime el menú principal"""
    print("\n" + "=" * 60)
    print("  SIMULADOR DE MÁQUINA DE TURING - FIBONACCI")
    print("=" * 60)
    print("\n1. Ejecutar simulación individual")
    print("2. Ejecutar tests completos")
    print("3. Ejecutar análisis de complejidad")
    print("4. Mostrar información de la máquina")
    print("5. Ejecutar todo (tests + análisis + simulación)")
    print("0. Salir")
    print("\n" + "=" * 60)


def main():
    """Punto de entrada principal con menú interactivo"""
    
    # Si hay argumentos de línea de comandos, ejecutar modo antiguo
    if len(sys.argv) > 1:
        run_single_simulation()
        return
    
    while True:
        print_menu()
        
        choice = input("Seleccione una opción: ").strip()
        
        if choice == '1':
            run_single_simulation()
        elif choice == '2':
            run_tests()
        elif choice == '3':
            run_full_analysis()
        elif choice == '4':
            show_machine_info()
        elif choice == '5':
            run_all()
        elif choice == '0':
            print("\n¡Hasta luego!")
            sys.exit(0)
        else:
            print("\n Opción inválida. Por favor seleccione una opción válida.")
        
        print("\n" + "-" * 60)
        input(">>> Presiona Enter para volver al menú principal... ")


if __name__ == "__main__":
    main()
