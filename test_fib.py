from loader import load_from_file
from simulator import TuringSimulator

machine = load_from_file('fibonacci_new.yaml')
expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

print("Testing F(0) to F(10):")
for n in range(11):
    input_str = '1' * n
    sim = TuringSimulator(machine, input_str, verbose=False)
    results = sim.run(max_steps=50000)
    output = results['tape_content']
    count = output.count('1') if output else 0
    status = "OK" if count == expected[n] else "FAIL"
    print(f"F({n})={count} (expected={expected[n]}) [{status}] steps={results['step_count']}")
