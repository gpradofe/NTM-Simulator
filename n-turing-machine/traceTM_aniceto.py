import collections  # Import the collections module for specialized container datatypes
import argparse

# Define a class for a new Turing Machine
class NewTuringMachine:
    """This class represents a new Turing Machine, initialized with a given input file."""
    def __init__(self, input_file):
        """
        Initialize a NewTuringMachine instance with the given input file.

        This constructor reads the input file and sets up the initial configuration of the Turing machine,
        including its name, states, alphabets, start, accept, reject states, and transition rules.

        Parameters:
        input_file (str): Path to the file containing the Turing machine's configuration.
        """
        # Initialize instance variables for machine properties
        self.machine_name = ''         # Name of the Turing machine
        self.states = ''               # Set of states in the Turing machine
        self.input_alphabet = ''       # Alphabet used for input
        self.tape_alphabet = ''        # Alphabet used for the tape
        self.start_state = ''          # Starting state of the machine
        self.accept_state = ''         # State(s) where machine will accept the input
        self.reject_state = ''         # State(s) where machine will reject the input
        self.transitions = []          # List of transition rules

        # Read and parse the input file to initialize the Turing Machine
        self.parse_input(input_file)

    def parse_input(self, input_file):
        """
        Parse the input file and set up the Turing machine configuration.

        This method reads from the input file, extracting the Turing machine's properties like its name, 
        states, input and tape alphabets, start, accept, and reject states, and the transition rules.

        Parameters:
        input_file (str): Path to the file containing the Turing machine's configuration.
        """
        sections = []  # List to store different sections of the input file
        with open(input_file, 'r') as opened_file:  # Open the file for reading
            for line in opened_file:  # Iterate through each line in the file
                # Split the line by commas, strip whitespace, and filter out empty strings
                sections.append([x for x in line.strip().split(',') if x])

        # Assign the parsed values to instance variables
        self.machine_name = sections[0]  # Assign machine name
        self.states = sections[1]        # Assign states
        self.input_alphabet = sections[2]  # Assign input alphabet
        self.tape_alphabet = sections[3]   # Assign tape alphabet
        self.start_state = sections[4][0]  # Assign start state (first element)
        self.accept_state = sections[5]    # Assign accept state(s)
        self.reject_state = sections[6]    # Assign reject state(s)
        self.transitions = sections[7:]    # Assign transition rules

    def decompose_transition(self):
        """
        Decompose transition rules into a more accessible format.

        This method restructures the transition rules of the Turing machine for easier access and manipulation.
        It converts the list of transitions into a dictionary format keyed by state, allowing for more efficient
        lookup of transitions for each state.

        Returns:
        dict: A dictionary where each key is a state, and the value is a list of transitions for that state.
        """
        transition_dict = collections.defaultdict(list)  # Create a default dictionary for transitions
        for state in self.transitions:
            # Check if transition rule is valid and belongs to a known state
            if len(state[0]) == 2 and state[0] in self.states:
                # Map the state to its transitions
                transition_dict[state[0]].append(state[1:])
        return transition_dict  # Return the dictionary of transitions

# Define a class for the Turing Machine Simulator
class TuringMachineSimulator:
    """This class simulates the operation of a Turing machine using a computation tree."""
    def __init__(self, turing_machine):
        """
        Initialize the TuringMachineSimulator instance with a Turing machine.

        This constructor sets up the simulator with a specific Turing machine, preparing it for running simulations
        based on the Turing machine's configuration.

        Parameters:
        turing_machine (NewTuringMachine): The Turing machine to be simulated.
        """
        self.turing_machine = turing_machine  # Turing Machine to be simulated

    # Method to compute the computation tree of the Turing machine
    def compute_tree(self, input_string, states_map):
        """
        Compute the computation tree of the Turing machine for a given input string.

        This method simulates the operation of the Turing machine on an input string and constructs a computation
        tree that represents the transitions of the machine's states. The method limits the depth of the computation
        to prevent infinite loops.

        Parameters:
        input_string (str): The input string for the Turing machine simulation.
        states_map (dict): A dictionary of states and their corresponding transitions.

        Returns:
        list or tuple: A computation tree representing the Turing machine's operation, and the final state 
                    (accept or reject) if reached within the depth limit.
        """
        computation_tree = [[[self.turing_machine.start_state, -1, -1, input_string, 0]]]
        depth = -1  # Initialize depth of computation

        # Loop to simulate the Turing machine computation for a limited depth (max 15)
        while depth < 15:
            depth += 1  # Increment depth
            current_level = []  # Current level in computation tree
            next_node = 'na'  # Placeholder for the next node
            # Iterate through each state in the last level of the computation tree
            for track_pindex, state in enumerate(computation_tree[-1]):
                node, pheight, pindex, input_string, str_index = state

                # Check transitions for the current state
                for child in states_map[node]:
                    # Extend input string with a blank symbol if needed
                    if str_index >= len(input_string):
                        input_string += '_'
                    # Check for a matching transition
                    if child[0] == input_string[str_index]:  # Match found
                        # Save original input string for later restoration
                        temp = input_string
                        # Convert string to list for manipulation
                        input_string = list(input_string)
                        # Apply the transition (write symbol)
                        input_string[str_index] = child[2] if len(child) >= 3 else input_string[str_index]
                        # Convert list back to string
                        input_string = ''.join(input_string)
                        # Determine the direction of head movement
                        direction = 1 if len(child) >= 3 and child[3] == 'R' else -1
                        next_node = child[1]  # Next state
                        # Append new state to the current level of computation tree
                        current_level.append([next_node, len(computation_tree) - 1, track_pindex, input_string, str_index + direction])
                        # Restore original input string for the next iteration
                        input_string = temp
                    else:
                        # If no match, transition to reject state
                        current_level.append([self.turing_machine.reject_state[0], len(computation_tree) - 1, track_pindex, input_string, str_index])
            # Append the current level to the computation tree
            computation_tree.append(current_level)

            # Check for termination conditions
            if computation_tree[-1] == []:
                return self.turing_machine.reject_state  # No further states to process
            if next_node == self.turing_machine.accept_state[0]:
                return computation_tree, self.turing_machine.accept_state[0]  # Accept state reached
            elif next_node == 'na':
                return computation_tree, self.turing_machine.reject_state[0]  # No applicable transition (reject)
        return computation_tree  # Return the computation tree if depth limit reached

    # Method to calculate the path length in the computation tree
    def compute_path_len(self, computation_tree):
        """
        Calculate the path length in the computation tree.

        This method traces the path from the accept state (if reached) back to the start state in the computation
        tree, calculating the length of this path.

        Parameters:
        computation_tree (list of lists): The computation tree of the Turing machine.

        Returns:
        list: The path from the accept state to the start state in reverse order.
        """
        path = []  # List to store the path
        flag = False  # Flag to indicate if accept state is found
        # Start from the last node in the computation tree
        height, index = computation_tree[-1][-1][1], computation_tree[-1][-1][2]
        # Iterate backwards through the computation tree
        for level in computation_tree[::-1]:
            for state in level:
                # Check if current state is an accept state
                if state[0] == self.turing_machine.accept_state[0]:
                    # Update height and index to trace back the path
                    height, index = state[1], state[2]
                    # Append the accept state to the path
                    path.append(self.turing_machine.accept_state[0])
                    flag = True  # Set flag to indicate accept state found
                    break
            # Break out of the loop if accept state is found
            if flag:
                break
        # Trace back the path from the accept state to the start state
        while height != -1 and index != -1:
            # Append each state in the path
            path.append(computation_tree[height][index][0])
            # Update height and index for the previous state
            height, index = computation_tree[height][index][1], computation_tree[height][index][2]
        return path[::-1]  # Return the path in the correct order

    # Method to configure the output based on the computation tree
    def set_output(self, computation_tree):
        """
        Configures and returns the output of a Turing Machine based on its computation tree.

        This method traverses the computation tree of the Turing Machine in reverse. It looks for the 
        accept state, then formats and collects the output from the computation tree based on the 
        transitions and states encountered.

        Parameters:
        computation_tree (list of lists): A nested list representing the computation tree of the Turing Machine.
                                          Each element in this nested list represents a state with its details.

        Returns:
        list: A list of strings representing the formatted output of the Turing Machine's computation.
        """
        # Initialize an empty list to store the output.
        output_list = []
        # A flag used to break out of nested loops when a condition is met.
        flag = False
        # Initialize an empty list to store the answer.
        ans = []
        # Extract the height and index of the last element in the computation tree.
        height, index = computation_tree[-1][-1][1], computation_tree[-1][-1][2]

        # Iterate in reverse through the computation tree.
        for level in computation_tree[::-1]:
            for state in level:
                # Check if the current state is the Turing Machine's accept state.
                if state[0] == self.turing_machine.accept_state[0]:
                    # Update height and index to the current state's position.
                    height, index = state[1], state[2]
                    # Add the formatted state information to 'ans' list.
                    ans.append(state[3][:state[4]] + f'[{state[0]}]' + state[3][state[4]:])
                    # Add the accept state to 'output_list'.
                    output_list.append(self.turing_machine.accept_state[0])
                    # Set the flag to True to indicate the accept state was found.
                    flag = True
                    break
            # If the accept state was found, exit the outer loop.
            if flag:
                break

        # Iterate through the computation tree based on the updated height and index.
        while height != -1 and index != -1:
            # Extract the head position, current string, and current state.
            head = computation_tree[height][index][4]
            cur_string = computation_tree[height][index][3]
            cur_state = computation_tree[height][index][0]
            # Format the output based on the position of the head.
            if head == 0:
                output = f'[{cur_state}]' + cur_string
            else:
                output = cur_string[:head] + f'[{cur_state}]' + cur_string[head:]
            # Add the formatted output to 'ans' list.
            ans.append(output)
            # Add the current state to 'output_list'.
            output_list.append(computation_tree[height][index][0])
            # Update height and index for the next iteration.
            height, index = computation_tree[height][index][1], computation_tree[height][index][2]
        # Return the list containing the formatted output.
        return ans


    def compute_transitions(self, computation_tree):
        """
        Calculates and returns the total number of transitions in the computation tree of a Turing Machine.

        This method counts each node in the computation tree as a single transition, providing 
        the total number of transitions that have occurred during the computation process.

        Parameters:
        computation_tree (list of lists): A nested list representing the computation tree of the Turing Machine.
                                          Each element in this nested list represents a state with its details.

        Returns:
        int: The total number of transitions in the Turing Machine's computation tree.
        """
        # Initialize a counter for the number of transitions.
        size = 0
        # Iterate through each level of the computation tree.
        for level in computation_tree:
            # Iterate through each node in the current level.
            for node in level:
                # Increment the counter for each node (transition).
                size += 1
        # Return the total count of transitions.
        return size

def main():
    """Main function to execute the Turing machine simulation."""

    # Parsing command line arguments
    parser = argparse.ArgumentParser(description="Turing Machine Simulator")
    parser.add_argument('input_file', type=str, help='Input file for the Turing Machine')
    parser.add_argument('input_string', type=str, help='Input string to process')
    args = parser.parse_args()

    input_file = args.input_file
    input_string = args.input_string

    turing_machine = NewTuringMachine(input_file)
    simulator = TuringMachineSimulator(turing_machine)
    states_map = turing_machine.decompose_transition()
    computation_tree, status = simulator.compute_tree(input_string, states_map)

    size = simulator.compute_transitions(computation_tree)
    path = simulator.compute_path_len(computation_tree)
    ans = simulator.set_output(computation_tree)

    # Enhanced output formatting
    output_lines = []
    output_lines.append('==== Turing Machine Simulation Output ====')
    output_lines.append(f'Machine Name: {turing_machine.machine_name[0]}')
    output_lines.append(f'Input String: {input_string}')
    output_lines.append(f'Total Transitions Traced: {size - 2}')
    result = 'accepted' if status == turing_machine.accept_state[0] else 'rejected'
    output_lines.append(f'String {result} in {len(path) - 1} steps')
    output_lines.append('---- Computation Steps ----')
    for s in ans[::-1]:
        output_lines.append(f'  {s}')

    # Append to the output file instead of overwriting
    output_filename = f'{turing_machine.machine_name[0]}_output'
    with open(output_filename, 'a') as file:  # Use 'a' mode for append
        for line in output_lines:
            print(line)
            file.write(line + '\n')

if __name__ == '__main__':
    main()


