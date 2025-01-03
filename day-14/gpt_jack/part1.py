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


def calculate_quadrants(positions, width, height):
    """Count robots in each quadrant."""
    center_x, center_y = width // 2, height // 2
    quadrants = [0, 0, 0, 0]  # Top-left, Top-right, Bottom-left, Bottom-right

    for x, y in positions:
        if x == center_x or y == center_y:
            continue  # Robots exactly on center lines don't count
        if x < center_x and y < center_y:
            quadrants[0] += 1  # Top-left
        elif x >= center_x and y < center_y:
            quadrants[1] += 1  # Top-right
        elif x < center_x and y >= center_y:
            quadrants[2] += 1  # Bottom-left
        else:
            quadrants[3] += 1  # Bottom-right

    return quadrants


def main():
    input_file = "input.txt"
    width, height = 101, 103  # Dimensions of the space
    steps = 100  # Time steps to simulate

    positions, velocities = parse_input(input_file)
    final_positions = simulate(positions, velocities, width, height, steps)
    quadrants = calculate_quadrants(final_positions, width, height)

    # Calculate the safety factor
    safety_factor = np.prod(quadrants)
    print("Safety Factor:", safety_factor)


if __name__ == "__main__":
    main()
