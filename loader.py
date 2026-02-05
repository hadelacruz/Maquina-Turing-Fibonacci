
import yaml
from turing_machine import TuringMachine


def load_from_yaml(filename):

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {filename}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error al parsear el archivo YAML: {e}")
    
    # Extraer componentes de la definición
    states = data.get('states', [])
    input_alphabet = data.get('input_alphabet', [])
    tape_alphabet = data.get('tape_alphabet', [])
    initial_state = data.get('initial_state', '')
    final_states = data.get('final_states', [])
    blank_symbol = data.get('blank_symbol', '_')
    
    # Procesar transiciones
    transitions_list = data.get('transitions', [])
    transitions = {}
    
    for trans in transitions_list:
        from_state = trans['from_state']
        read_symbol = trans['read']
        to_state = trans['to_state']
        write_symbol = trans['write']
        move = trans['move']
        
        # Crear entrada en el diccionario de transiciones
        key = (from_state, read_symbol)
        value = (to_state, write_symbol, move)
        transitions[key] = value
    
    # Crear y retornar la máquina
    machine = TuringMachine(
        states=states,
        input_alphabet=input_alphabet,
        tape_alphabet=tape_alphabet,
        initial_state=initial_state,
        final_states=final_states,
        transitions=transitions,
        blank_symbol=blank_symbol
    )
    
    # TODO: Agregar validación completa del archivo de definición
    
    return machine


def load_from_file(filename):

    if filename.endswith('.yaml') or filename.endswith('.yml'):
        return load_from_yaml(filename)
    else:
        return load_from_yaml(filename)
