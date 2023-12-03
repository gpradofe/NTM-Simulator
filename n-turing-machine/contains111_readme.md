# README for Non-Deterministic Turing Machine - contains111

## Overview

This repository contains the implementation and documentation for a non-deterministic Turing machine (NTM) designed to detect the presence of the sequence "111" in a binary string. The machine's behavior, states, and transitions are defined in the `contains111.csv` file.

## File Description

- `contains111.csv`: This single file contains all the necessary information about the states, transitions, and actions of the Turing machine.

## Turing Machine Description

This non-deterministic Turing machine operates on a binary input tape and detects whether the sequence "111" is present in the tape. It uses a head to read and write on the tape and moves either left (L) or right (R) after each action.

## State Transitions and Actions

The Turing machine includes the following states and transitions as defined in `contains111.csv`:

- **States**: `q0` (initial state), `q1`, `q2`, `q3` (accept state), and `qreject` (reject state).
- **Transitions**:
  - In state `q0`, upon reading `0`, it stays in `q0` and moves right; upon reading `1`, it moves to `q1` and moves right.
  - In state `q1`, upon reading `0`, it transitions to `q0` and moves right; upon reading `1`, it moves to `q2` and moves right.
  - In state `q2`, upon reading `0`, it moves back to `q0` and moves right; upon reading `1`, it transitions to the accepting state `q3` and moves right.
  - State `q3` indicates the detection of the sequence "111", completing the process.
  - The `qreject` state is not utilized in this configuration.

## Input Tape and Expected Outcomes

### Example 1

- **Input Tape**: `010110`
- **Expected Outcome**: The machine remains in state `q0` and does not detect the sequence "111".

### Example 2

- **Input Tape**: `110111`
- **Expected Outcome**: The machine transitions to state `q3`, indicating that the sequence "111" is detected.

### Example 3

- **Input Tape**: `1110`
- **Expected Outcome**: The machine transitions to state `q3`, indicating that the sequence "111" is detected.

## Usage

To use this Turing machine, load the `contains111.csv` file into a Turing machine simulator capable of interpreting non-deterministic behaviors. Provide a binary string as the input tape, and the simulator will process the tape to determine the presence of the sequence "111".

## Notes

- Ensure that the simulator used is compatible with non-deterministic Turing machines.
- The behavior and transitions of the machine are solely determined by the `contains111.csv` file.
