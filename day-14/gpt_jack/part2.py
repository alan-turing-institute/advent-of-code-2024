import numpy as np


def parse_input(file_path):
    """Parse the input file to extract positions and velocities."""
    positions = []
    velocities = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                p, v = line.split(" ")
                px, py = map(int, p[2:].split(","))
                vx, vy = map(int, v[2:].split(","))
                positions.append((px, py))
                velocities.append((vx, vy))
    return np.array(positions), np.array(velocities)


def simulate(positions, velocities, width, height, steps):
    """Simulate robot positions after a given number of steps."""
    for _ in range(steps):
        positions += velocities
        # Wrap around edges (teleportation)
        positions[:, 0] %= width
        positions[:, 1] %= height
    return positions


def find_easter_egg(positions, velocities, width, height):
    """Find the fewest seconds for the robots to display the Easter egg."""
    step = 0
    while True:
        # Map the robots to a grid
        grid = np.zeros((height, width), dtype=int)
        for x, y in positions:
            grid[y % height, x % width] += 1

        # Detect dense clusters in the grid
        cluster_detected = detect_dense_cluster(grid)
        if cluster_detected:
            print(f"Easter egg detected at step {step}:")
            print_grid(grid)
            return step

        # Update positions for the next step
        positions += velocities
        step += 1


def detect_dense_cluster(grid):
    """Check for dense clusters in the grid."""
    # Look for high-density regions in sub-grids
    subgrid_size = 20  # Size of the sub-grid to analyze
    density_threshold = 0.5  # Fraction of cells that must be occupied

    for y in range(0, grid.shape[0] - subgrid_size + 1, subgrid_size):
        for x in range(0, grid.shape[1] - subgrid_size + 1, subgrid_size):
            subgrid = grid[y : y + subgrid_size, x : x + subgrid_size]
            occupied = np.sum(subgrid > 0)
            total_cells = subgrid_size * subgrid_size
            if occupied / total_cells > density_threshold:
                return True
    return False


def print_grid(grid):
    """Print the current grid for visualization."""
    for row in grid:
        print("".join("#" if cell > 0 else "." for cell in row))


def main():
    input_file = "input.txt"
    width, height = 101, 103  # Dimensions of the space

    positions, velocities = parse_input(input_file)
    steps_to_easter_egg = find_easter_egg(positions, velocities, width, height)

    print("Fewest seconds to Easter egg:", steps_to_easter_egg)


if __name__ == "__main__":
    main()
