import time
from tape import Tape


class TuringSimulator:

    def __init__(self, turing_machine, input_string="", verbose=True):
  
        self.machine = turing_machine
        self.tape = Tape(input_string, turing_machine.get_blank_symbol())
        self.current_state = turing_machine.get_initial_state()
        self.step_count = 0
        self.verbose = verbose
        self.execution_time = 0
        
        # TODO: Limitar número máximo de pasos para evitar loops infinitos
    
    def step(self):
        # Verificar si estamos en estado final
        if self.machine.is_final_state(self.current_state):
            return False
        
        # Leer símbolo actual
        current_symbol = self.tape.read()
        
        # Buscar transición
        transition = self.machine.get_transition(self.current_state, current_symbol)
        
        if transition is None:
            # No hay transición definida, la máquina se detiene
            print(f"\n⚠ No hay transición definida para ({self.current_state}, '{current_symbol}')")
            return False
        
        # Aplicar transición
        new_state, new_symbol, direction = transition
        
        # Mostrar transición si verbose está activado
        if self.verbose:
            self.show_configuration()
            print(f"  → δ({self.current_state}, {current_symbol}) = ({new_state}, {new_symbol}, {direction})")
        
        # Ejecutar transición
        self.tape.write(new_symbol)
        self.tape.move(direction)
        self.current_state = new_state
        self.step_count += 1
        
        return True
    
    def run(self, max_steps=10000):

        print("=" * 60)
        print("INICIANDO SIMULACIÓN DE MÁQUINA DE TURING")
        print("=" * 60)
        print(f"Estado inicial: {self.current_state}")
        print(f"Entrada: {self.tape.get_full_content() or '(vacía)'}")
        print("=" * 60)
        print()
        
        start_time = time.time()
        
        # Ejecutar pasos
        while self.step_count < max_steps:
            if not self.step():
                break
        
        end_time = time.time()
        self.execution_time = end_time - start_time
        
        # Mostrar configuración final
        print("\n" + "=" * 60)
        print("CONFIGURACIÓN FINAL")
        print("=" * 60)
        self.show_configuration()
        
        # Resultados
        results = {
            'final_state': self.current_state,
            'step_count': self.step_count,
            'execution_time': self.execution_time,
            'tape_content': self.tape.get_full_content(),
            'halted': self.step_count < max_steps,
            'accepted': self.machine.is_final_state(self.current_state)
        }
        
        print("\n" + "=" * 60)
        print("RESULTADOS")
        print("=" * 60)
        print(f"Estado final: {results['final_state']}")
        print(f"Aceptado: {'✓ Sí' if results['accepted'] else '✗ No'}")
        print(f"Total de pasos: {results['step_count']}")
        print(f"Tiempo de ejecución: {results['execution_time']:.6f} segundos")
        print(f"Contenido final de la cinta: {results['tape_content'] or '(vacía)'}")
        print("=" * 60)
        
        # TODO: Comparar tiempo real vs número de transiciones
        
        return results
    
    def show_configuration(self):
        content, start_pos = self.tape.get_content()
        head_relative_pos = self.tape.get_head_position() - start_pos
        
        # Crear indicador de posición del cabezal
        pointer = " " * head_relative_pos + "^"
        
        print(f"\nPaso {self.step_count}:")
        print(f"  Estado: {self.current_state}")
        print(f"  Cinta:  {content}")
        print(f"          {pointer}")
        
        # TODO: Separar impresión de configuraciones del motor de simulación
    
    def get_step_count(self):
        return self.step_count
    
    def get_execution_time(self):
        return self.execution_time
