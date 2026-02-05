
class TuringMachine:    
    def __init__(self, states, input_alphabet, tape_alphabet, 
                 initial_state, final_states, transitions, blank_symbol="_"):
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions  # {(estado, símbolo): (nuevo_estado, nuevo_símbolo, dirección)}
        self.blank_symbol = blank_symbol
        
        # TODO: Agregar validación completa de la definición formal
    
    def get_transition(self, current_state, current_symbol):
        return self.transitions.get((current_state, current_symbol), None)
    
    def is_final_state(self, state):
        return state in self.final_states
    
    def get_initial_state(self):
        return self.initial_state
    
    def get_blank_symbol(self):
        return self.blank_symbol
    
    def __str__(self):
        return f"TuringMachine(states={len(self.states)}, initial={self.initial_state}, final={self.final_states})"
