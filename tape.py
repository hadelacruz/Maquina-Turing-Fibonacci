class Tape:
    
    def __init__(self, initial_content="", blank_symbol="_"):

        self.blank_symbol = blank_symbol
        self.tape = {}  # Diccionario para almacenar símbolos
        self.head_position = 0  # Posición inicial del cabezal
        
        # Cargar contenido inicial
        for i, symbol in enumerate(initial_content):
            self.tape[i] = symbol
            
        # TODO: Optimizar representación de la cinta para entradas grandes
    
    def read(self):
        return self.tape.get(self.head_position, self.blank_symbol)
    
    def write(self, symbol):

        if symbol == self.blank_symbol:
            # Si escribimos el símbolo blanco, lo eliminamos del diccionario
            # para mantener la cinta compacta
            if self.head_position in self.tape:
                del self.tape[self.head_position]
        else:
            self.tape[self.head_position] = symbol
    
    def move_left(self):
        self.head_position -= 1
    
    def move_right(self):
        self.head_position += 1
    
    def move(self, direction):

        if direction == 'L':
            self.move_left()
        elif direction == 'R':
            self.move_right()
        elif direction == 'S':
            pass  # Sin movimiento
        else:
            raise ValueError(f"Dirección inválida: {direction}")
    
    def get_content(self, show_range=20):
        if not self.tape:
            # Cinta vacía, mostrar rango alrededor del cabezal
            start = self.head_position - show_range
            end = self.head_position + show_range
        else:
            # Determinar rango basado en contenido
            min_pos = min(min(self.tape.keys()), self.head_position - 5)
            max_pos = max(max(self.tape.keys()), self.head_position + 5)
            start = min_pos
            end = max_pos
        
        content = ""
        for i in range(start, end + 1):
            content += self.tape.get(i, self.blank_symbol)
        
        return content, start
    
    def get_head_position(self):
        return self.head_position
    
    def get_full_content(self):
        if not self.tape:
            return self.blank_symbol
        
        min_pos = min(self.tape.keys())
        max_pos = max(self.tape.keys())
        
        content = ""
        for i in range(min_pos, max_pos + 1):
            content += self.tape.get(i, self.blank_symbol)
        
        return content.strip(self.blank_symbol)
