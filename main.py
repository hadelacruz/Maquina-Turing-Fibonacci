import sys
from loader import load_from_file
from simulator import TuringSimulator


def main():
    
    print("SIMULADOR DE MÁQUINA DE TURING - FIBONACCI")
    print("=" * 60)
    
    machine_file = "fibonacci.yaml"
    
    try:
        print(f"Cargando: {machine_file}...")
        machine = load_from_file(machine_file)
        print(f"- Máquina cargada exitosamente\n")
    except Exception as e:
        print(f"- Error al cargar la máquina: {e}")
        return
    
    # Solicitar entrada
    print("CONFIGURACIÓN DE ENTRADA")
    print("=" * 60)
    
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
    # TODO: Permitir deshabilitar verbose desde línea de comandos
    simulator = TuringSimulator(machine, input_string, verbose=True)
    
    try:
        results = simulator.run(max_steps=100000)
    except KeyboardInterrupt:
        print("\n\n- Simulación interrumpida por el usuario")
        return
    except Exception as e:
        print(f"\n\n- Error durante la simulación: {e}")
        return
    
    # Análisis adicional
    print("\n" + "=" * 60)
    print("ANÁLISIS DE COMPLEJIDAD")
    print("=" * 60)
    
    n = len(input_string)
    steps = results['step_count']
    
    print(f"\nTamaño de entrada (n): {n}")
    print(f"Número de pasos: {steps}")
    
    if n > 0:
        ratio = steps / n
        print(f"Relación pasos/n: {ratio:.2f}")
        print(f"\n💡 Este dato ayuda a inferir la complejidad O(f(n))")
        print("   Ejecute con diferentes valores de n para ver el crecimiento.")
    
    print("\n" + "=" * 60)
    print("- Simulación completada\n")
    
    # TODO: Mejorar visualización del análisis empírico
    # TODO: Implementar otras convenciones numéricas (binario)
    

def run_batch_analysis():

    # TODO: Implementar análisis batch para múltiples valores de n
    pass


if __name__ == "__main__":
    main()
