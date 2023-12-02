class NTuringMachine:
    def __init__(self):
        # Initialize NTM components (states, transitions, etc.)
        self.states = set()
        self.transitions = {}  # Example format: {(state, symbol): [(next_state, write_symbol, move_dir), ...]}
        self.start_state = None
        self.accept_states = set()
        self.reject_states = set()
        

    def parse_csv(self, filepath):
        # Parse the TM definition from a CSV file
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            
            # Reading header lines
            machine_name = next(reader)[0]
            states = next(reader)[0].split(',')  # Assuming states are comma-separated
            input_alphabet = next(reader)[0].split(',')
            tape_alphabet = next(reader)[0].split(',')
            start_state = next(reader)[0]
            accept_state = next(reader)[0]
            reject_state = next(reader)[0]

            # Initialize NTM components
            self.states = set(states)
            self.input_alphabet = set(input_alphabet)
            self.tape_alphabet = set(tape_alphabet)
            self.start_state = start_state
            self.accept_states = set([accept_state])
            self.reject_states = set([reject_state])

            # Processing transitions
            self.transitions = {}
            for row in reader:
                current_state, symbol, next_state, write_symbol, move_dir = row
                key = (current_state, symbol)
                if key not in self.transitions:
                    self.transitions[key] = []
                self.transitions[key].append((next_state, write_symbol, move_dir))

            # Assign machine name as an attribute if needed
            self.machine_name = machine_name

    def run_ntm(self, input_string):
        # Run the NTM on the input string using breadth-first search
        # Initialize the tape with the input string and pad with blank symbols ('_')
        initial_tape = ['_'] + list(input_string) + ['_']
        initial_head_pos = 1  # Starting at the first character of the input string
        initial_config = (self.start_state, initial_tape, initial_head_pos)

        # Queue for BFS: each element is a tuple (state, tape, head position, path)
        queue = [(initial_config, [])]

        while queue:
            (state, tape, head_pos), path = queue.pop(0)

            # Check for accept state
            if state in self.accept_states:
                return "Accept", path + [(state, ''.join(tape), head_pos)]

            # Handle implicit reject state
            if state in self.reject_states or (state, tape[head_pos]) not in self.transitions:
                continue

            # Explore all possible transitions from the current configuration
            for next_state, write_symbol, move_dir in self.transitions[(state, tape[head_pos])]:
                new_tape = tape.copy()
                new_tape[head_pos] = write_symbol
                new_head_pos = head_pos + (1 if move_dir == 'R' else -1)

                # Ensure the head does not go off the tape
                if new_head_pos < 0 or new_head_pos >= len(new_tape):
                    continue

                new_config = (next_state, new_tape, new_head_pos)
                new_path = path + [(state, ''.join(tape), head_pos)]
                queue.append((new_config, new_path))

        return "Reject", None

    def get_next_configurations(self, config):
        # Generate all possible next configurations from the current configuration
        # based on the NTM's transition rules
        current_state, tape, head_pos = config
        current_symbol = tape[head_pos] if head_pos < len(tape) else '_'

        # Check if there are any transitions for the current state and symbol
        if (current_state, current_symbol) not in self.transitions:
            return []  # No transitions available

        next_configs = []
        for next_state, write_symbol, move_dir in self.transitions[(current_state, current_symbol)]:
            new_tape = tape.copy()
            new_tape[head_pos] = write_symbol  # Write the new symbol

            # Calculate the new head position
            new_head_pos = head_pos + (1 if move_dir == 'R' else -1)

            # Ensure the tape is extended if the head moves beyond the current tape
            if new_head_pos >= len(new_tape):
                new_tape.append('_')  # Append a blank symbol at the end
            elif new_head_pos < 0:
                new_head_pos = 0
                new_tape.insert(0, '_')  # Insert a blank symbol at the beginning

            next_configs.append((next_state, new_tape, new_head_pos))

        return next_configs

