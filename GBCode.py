import numpy as np

class POSCAR:
    """ Python Class for VASP POSCAR """

    def __init__(self, file_path='POSCAR'):
        self.file_path = file_path
        self.scale_factor = None
        self.lattice_vectors = None
        self.atom_species = None
        self.atom_counts = None
        self.atom_coordinates_direct = None
        self.read_poscar()

    def read_poscar(self):
        """ Read VASP POSCAR file """
        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        self.scale_factor = float(lines[1])
        self.lattice_vectors = np.empty((3, 3))

        # Extract lattice vectors
        for i in range(3):
            self.lattice_vectors[i] = np.array(list(map(float, lines[i + 2].split()))) * self.scale_factor

        # Extract atom species and counts
        self.atom_species = lines[5].split()
        atom_counts_line = list(map(int, lines[6].split()))
        self.atom_counts = np.array(atom_counts_line)

        # Extract atom coordinates
        atom_coordinates = []
        for line in lines[8:]:
            parts = line.split()
            if len(parts) == 3:
                atom_coordinates.append(parts[:3])

        self.atom_coordinates_direct = np.array(atom_coordinates, dtype=float)

    def rotate_atoms(self, angle_degrees, radius):
        """ Rotate atoms around the [001] axis by a specified angle if within a given radius from the center in the x-y plane """
        angle_rad = np.radians(angle_degrees)
        rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad), 0],
                                    [np.sin(angle_rad), np.cos(angle_rad), 0],
                                    [0, 0, 1]])

        # Calculate center in x-y plane
        center_x = np.mean(self.atom_coordinates_direct[:, 0])
        center_y = np.mean(self.atom_coordinates_direct[:, 1])

        rotated_coords_after_rotation = []

        for coord in self.atom_coordinates_direct:
            distance = np.sqrt((coord[0] - center_x)**2 + (coord[1] - center_y)**2)  # Calculate distance from center in x-y plane
            if distance <= radius:
                # Translate the coordinate to have the center as origin, rotate, and translate back
                translated_coord = coord - np.array([center_x, center_y, 0])
                rotated_coord = np.dot(rotation_matrix, translated_coord)
                rotated_coords_after_rotation.append(rotated_coord + np.array([center_x, center_y, 0]))
            else:
                rotated_coords_after_rotation.append(coord)

        return np.array(rotated_coords_after_rotation)

    def save_rotated_atoms_to_file(self, rotated_coords):
        """ Save rotated atom coordinates to a file named 'output_POSCAR' """
        with open("output_POSCAR", "w") as file:
            with open(self.file_path, "r") as original_file:
                # Write the first 7 lines from the original POSCAR file
                for i in range(7):
                    file.write(original_file.readline())

                # Write the rotated atom coordinates starting from line 8
                file.write("Cartesian\n")
                for coord in rotated_coords:
                    file.write(' '.join(map(str, coord)) + '\n')

# Example usage
if __name__ == "__main__":
    poscar = POSCAR("POSCAR")

    # Rotate atoms around the [001] axis by 45 degrees within a radius of 100 in the x-y plane
    rotated_coords_after_rotation = poscar.rotate_atoms(45, 100)

    # Save rotated atom coordinates to 'output_POSCAR' file
    poscar.save_rotated_atoms_to_file(rotated_coords_after_rotation)

