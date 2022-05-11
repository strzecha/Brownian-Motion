from brownian.simulation import Simulation

def main():
    sim = Simulation(800, 600, 500, 5)
    sim.run()

main()