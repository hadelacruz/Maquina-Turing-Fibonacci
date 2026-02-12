import time

import matplotlib.pyplot as plt
import numpy as np

from loader import load_from_file
from simulator import TuringSimulator


def run_analysis(machine_file="fibonacci_new.yaml", test_values=None, max_steps=100000):
    if test_values is None:
        test_values = list(range(0, 11))
    
    print("=" * 60)
    print("ANÁLISIS EMPÍRICO - MÁQUINA DE TURING FIBONACCI")
    print("=" * 60)
    
    # Cargar máquina
    try:
        machine = load_from_file(machine_file)
        print(f"Máquina cargada: {machine_file}\n")
    except Exception as e:
        print(f"Error al cargar la máquina: {e}")
        return None
    
    # Ejecutar pruebas
    results = {
        'n_values': [],
        'steps': [],
        'times': [],
        'outputs': []
    }
    
    print("Ejecutando pruebas...")
    print("-" * 60)
    print(f"{'n':>5} | {'Entrada':>15} | {'Pasos':>10} | {'Tiempo (s)':>12} | {'Salida':>15}")
    print("-" * 60)
    
    for n in test_values:
        input_string = "1" * n
        
        # Crear simulador sin verbose para pruebas batch
        simulator = TuringSimulator(machine, input_string, verbose=False)
        
        start_time = time.perf_counter()
        result = simulator.run(max_steps=max_steps)
        elapsed_time = time.perf_counter() - start_time
        
        results['n_values'].append(n)
        results['steps'].append(result['step_count'])
        results['times'].append(elapsed_time)
        results['outputs'].append(result['tape_content'])
        
        # Interpretar salida como número de Fibonacci
        fib_result = result['tape_content'].count('1') if result['tape_content'] else 0
        
        print(f"{n:>5} | {input_string or '(vacía)':>15} | {result['step_count']:>10} | {elapsed_time:>12.6f} | {fib_result:>15}")
    
    print("-" * 60)
    print()
    
    return results


def plot_analysis(results, output_file="analysis_plot.png"):
    if results is None:
        print("No hay resultados para graficar.")
        return
    
    n_values = np.array(results['n_values'])
    steps = np.array(results['steps'])
    times = np.array(results['times'])
    
    # Crear figura con dos subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # --- Gráfico 1: Pasos vs n ---
    ax1.scatter(n_values, steps, color='blue', label='Datos observados', zorder=5)
    
    # Regresión polinomial para pasos
    if len(n_values) > 2:
        # Probar diferentes grados de polinomio
        best_degree = find_best_polynomial_degree(n_values, steps)
        coeffs = np.polyfit(n_values, steps, best_degree)
        poly = np.poly1d(coeffs)
        
        # Línea de regresión
        x_smooth = np.linspace(min(n_values), max(n_values), 100)
        y_smooth = poly(x_smooth)
        ax1.plot(x_smooth, y_smooth, 'r-', label=f'Regresión (grado {best_degree})', linewidth=2)
        
        # Mostrar ecuación
        equation = format_polynomial(coeffs)
        ax1.text(0.05, 0.95, f'p(n) = {equation}', transform=ax1.transAxes, 
                fontsize=9, verticalalignment='top', 
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    ax1.set_xlabel('Tamaño de entrada (n)', fontsize=12)
    ax1.set_ylabel('Número de pasos', fontsize=12)
    ax1.set_title('Complejidad: Pasos vs Entrada', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # --- Gráfico 2: Tiempo vs n ---
    ax2.scatter(n_values, times * 1000, color='green', label='Datos observados', zorder=5)
    
    # Regresión polinomial para tiempo
    if len(n_values) > 2:
        times_ms = times * 1000
        best_degree_time = find_best_polynomial_degree(n_values, times_ms)
        coeffs_time = np.polyfit(n_values, times_ms, best_degree_time)
        poly_time = np.poly1d(coeffs_time)
        
        y_smooth_time = poly_time(x_smooth)
        ax2.plot(x_smooth, y_smooth_time, 'r-', label=f'Regresión (grado {best_degree_time})', linewidth=2)
    
    ax2.set_xlabel('Tamaño de entrada (n)', fontsize=12)
    ax2.set_ylabel('Tiempo de ejecución (ms)', fontsize=12)
    ax2.set_title('Tiempo de Ejecución vs Entrada', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Gráfico guardado en: {output_file}")
    
    # Mostrar análisis de complejidad
    print_complexity_analysis(n_values, steps)
    
    plt.show()


def find_best_polynomial_degree(x, y, max_degree=5):
    best_degree = 1
    best_r2 = -np.inf
    
    for degree in range(1, min(max_degree + 1, len(x))):
        coeffs = np.polyfit(x, y, degree)
        poly = np.poly1d(coeffs)
        y_pred = poly(x)
        
        # Calcular R²
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        
        if ss_tot > 0:
            r2 = 1 - (ss_res / ss_tot)
            
            # Penalizar grados altos para evitar overfitting
            adjusted_r2 = r2 - (degree * 0.01)
            
            if adjusted_r2 > best_r2:
                best_r2 = adjusted_r2
                best_degree = degree
    
    return best_degree


def format_polynomial(coeffs):
    terms = []
    degree = len(coeffs) - 1
    
    for i, coef in enumerate(coeffs):
        power = degree - i
        if abs(coef) < 1e-10:
            continue
        
        if power == 0:
            terms.append(f"{coef:.2f}")
        elif power == 1:
            terms.append(f"{coef:.2f}n")
        else:
            terms.append(f"{coef:.2f}n^{power}")
    
    return " + ".join(terms) if terms else "0"


def print_complexity_analysis(n_values, steps):
    print("\n" + "=" * 60)
    print("ANÁLISIS DE COMPLEJIDAD")
    print("=" * 60)
    
    if len(n_values) < 3:
        print("Datos insuficientes para análisis.")
        return
    
    # Filtrar valores donde steps > 0
    valid_idx = [i for i in range(len(steps)) if steps[i] > 0]
    if len(valid_idx) < 3:
        print("Datos insuficientes para análisis.")
        return
    
    # Calcular ratios consecutivos
    ratios = []
    print("\nRatios de crecimiento consecutivos:")
    print("-" * 45)
    
    for i in range(1, len(valid_idx)):
        prev_i = valid_idx[i-1]
        curr_i = valid_idx[i]
        if steps[prev_i] > 0:
            ratio = steps[curr_i] / steps[prev_i]
            ratios.append(ratio)
            print(f"  n={n_values[curr_i]:>3}: {steps[curr_i]:>8} pasos (ratio: {ratio:.2f}x)")
    
    if len(ratios) < 2:
        print("Datos insuficientes para análisis.")
        return
    
    # Análisis del patrón de crecimiento
    # Ignorar primeros ratios (comportamiento inestable para n pequeños)
    stable_ratios = ratios[3:] if len(ratios) > 5 else ratios[1:] if len(ratios) > 2 else ratios
    
    avg_ratio = np.mean(stable_ratios) if stable_ratios else np.mean(ratios)
    std_ratio = np.std(stable_ratios) if stable_ratios else np.std(ratios)
    last_ratios = ratios[-3:] if len(ratios) >= 3 else ratios
    converging_ratio = np.mean(last_ratios)
    
    print("\n" + "-" * 45)
    print(f"Ratio promedio (valores estables): {avg_ratio:.3f}")
    print(f"Desviación estándar: {std_ratio:.3f}")
    print(f"Ratio convergente (últimos valores): {converging_ratio:.3f}")
    
    # Detectar tipo de crecimiento
    # Para exponencial: ratio constante > 1
    # Para polinomial O(n^k): ratio debería → 1 cuando n → ∞
    
    PHI_SQUARED = 2.618  # φ² ≈ (1.618)²
    
    print("\n" + "-" * 45)
    print("INTERPRETACIÓN:")
    
    # Si el ratio es aproximadamente constante y > 1.5, es exponencial
    # Usar el ratio de valores estables para la detección
    is_ratio_stable = std_ratio < 0.3 or (len(stable_ratios) >= 3 and np.std(stable_ratios[-3:]) < 0.2)
    
    if is_ratio_stable and avg_ratio > 1.8:
        # Verificar si coincide con φ² (caso Fibonacci)
        if abs(avg_ratio - PHI_SQUARED) < 0.5 or abs(converging_ratio - PHI_SQUARED) < 0.5:
            print(f"\n✓ Complejidad: O(φ^(2n)) ≈ O(2.618^n)")
            print(f"  Equivalente a: O(F(n)²) donde F(n) es el n-ésimo Fibonacci")
            print(f"\n  El ratio {converging_ratio:.3f} ≈ φ² = {PHI_SQUARED:.3f}")
            print(f"  Esto es característico de algoritmos que operan")
            print(f"  sobre los valores de Fibonacci (tamaño exponencial).")
        else:
            base = converging_ratio
            print(f"\n✓ Complejidad: O({base:.2f}^n) - Exponencial")
            print(f"  El ratio constante ≈{converging_ratio:.2f} indica crecimiento exponencial.")
    
    # Si el ratio decrece hacia 1, es polinomial
    elif converging_ratio < 1.3 and avg_ratio < 2:
        print(f"\n✓ Complejidad: O(n) - Lineal")
    elif converging_ratio < 1.8:
        print(f"\n✓ Complejidad: O(n log n) - Cuasilineal")
    else:
        # Intentar ajuste polinomial para estimar el grado
        log_n = np.log(np.array([n_values[i] for i in valid_idx[1:]]))
        log_steps = np.log(np.array([steps[i] for i in valid_idx[1:]]))
        
        # Regresión log-log para estimar el exponente
        if len(log_n) > 1:
            slope, _ = np.polyfit(log_n, log_steps, 1)
            print(f"\n⚠ Patrón no conclusivo. Análisis adicional:")
            print(f"  - Pendiente log-log: {slope:.2f}")
            if slope < 2.5:
                print(f"  - Sugiere O(n^{slope:.1f})")
            else:
                print(f"  - Probablemente exponencial con base ≈{converging_ratio:.2f}")
    
    print("\n" + "=" * 60)


def main():
    import sys

    # Valores de prueba por defecto
    test_values = list(range(0, 11))
    
    # Permitir especificar rango desde línea de comandos
    if len(sys.argv) > 1:
        try:
            max_n = int(sys.argv[1])
            test_values = list(range(0, max_n + 1))
        except ValueError:
            pass
    
    # Ejecutar análisis
    results = run_analysis(test_values=test_values)
    
    if results:
        plot_analysis(results)


if __name__ == "__main__":
    main()
