class KTapeTuringMachine:
    def __init__(self, num_tapes, transitions, initial_state, name):
        self.num_tapes = num_tapes
        self.transitions = transitions
        self.tapes = [['*'] for _ in range(num_tapes)]
        self.heads = [0 for _ in range(num_tapes)]
        self.current_state = initial_state
        self.name = name

    def move_head(self, tape_index, direction):
        if direction == 'L':
            self.heads[tape_index] = max(0, self.heads[tape_index] - 1)
        elif direction == 'R':
            self.heads[tape_index] += 1
            if self.heads[tape_index] == len(self.tapes[tape_index]):
                self.tapes[tape_index].append('*')
        # 'S' (Stay) option leaves the head in the same position

    def read_tape(self, tape_index):
        return self.tapes[tape_index][self.heads[tape_index]]

    def write_tape(self, tape_index, symbol):
        if symbol != '*':  # '*' means do not change
            self.tapes[tape_index][self.heads[tape_index]] = symbol

    def get_tape_heads_symbols(self):
        return [self.read_tape(i) for i in range(self.num_tapes)]

    def execute_transition(self):
        tape_heads_symbols = self.get_tape_heads_symbols()
        for key in self.transitions:
            if key[0] == self.current_state and all(x == y or y == '*' for x, y in zip(tape_heads_symbols, key[1:])):
                new_state, replacements, movements = self.transitions[key]
                self.current_state = new_state
                for i in range(self.num_tapes):
                    self.write_tape(i, replacements[i])
                    self.move_head(i, movements[i])
                return True
        return False

    def simulate(self):
        print(f"{self.name} Simulation Start")
        step = 0
        while self.execute_transition():
            print(f"Step {step}: State={self.current_state}")
            for i in range(self.num_tapes):
                tape_with_head = ''.join([self.tapes[i][j] if j != self.heads[i] else f'[{self.tapes[i][j]}]' for j in range(len(self.tapes[i]))])
                print(f"Tape {i + 1}: {tape_with_head}")
            step += 1
        print("Simulation complete")

# Define transitions for a binary increment machine
transitions = {
    # State, Tape 1, Tape 2 -> New State, [Replace Tape 1, Replace Tape 2], [Move Tape 1, Move Tape 2]
    ("start", "1", "*"): ("continue", ["*", "*"], ["L", "S"]),
    ("start", "0", "*"): ("end", ["1", "*"], ["S", "S"]),
    ("start", "*", "*"): ("end", ["1", "*"], ["S", "S"]),
    ("continue", "1", "*"): ("continue", ["0", "*"], ["L", "S"]),
    ("continue", "0", "*"): ("end", ["1", "*"], ["S", "S"]),
    ("continue", "*", "*"): ("end", ["1", "*"], ["S", "S"])
}

# Re-initialize the machine with the corrected transitions
machine = KTapeTuringMachine(num_tapes=2, transitions=transitions, initial_state="start", name="Binary Increment Machine")

# Prepare the tape with a binary number (e.g., '101')
machine.tapes[0] = list("101")[::-1]  # Reverse the input

# Run the simulation again
machine.simulate()

machine2 = KTapeTuringMachine(num_tapes=2, transitions=transitions, initial_state="start", name="Binary Increment Machine 2")
machine2.tapes[0] = list("111")[::-1]

# Test case 3: Incrementing the binary number '1010' (should result in '1011')
machine3 = KTapeTuringMachine(num_tapes=2, transitions=transitions, initial_state="start", name="Binary Increment Machine 3")
machine3.tapes[0] = list("1010")[::-1]

# Running the test cases
print("Running Test Case 2")
machine2.simulate()
print("\nRunning Test Case 3")
machine3.simulate()