import numpy as np


# Define a class for the 3D truss FEM solver to keep it modular and reusable
class Truss3D_FEM:
    def __init__(self, nodes, elements, E, A, forces, fixed_nodes):
        # Initialize problem parameters
        self.nodes = nodes  # List of node coordinates [(x1, y1, z1), ...]
        self.elements = elements  # List of element connectivity [(node_i, node_j), ...]
        self.E = E  # Modulus of elasticity (Pa)
        self.A = A  # Cross-sectional area (m^2)
        self.forces = forces  # External forces [(node, fx, fy, fz), ...]
        self.fixed_nodes = fixed_nodes  # List of fixed node indices
        self.num_nodes = len(nodes)
        self.dof_per_node = 3  # Degrees of freedom per node (x, y, z)
        self.total_dof = self.num_nodes * self.dof_per_node

    def local_stiffness_matrix(self, elem):
        # Extract nodes of the element
        n1, n2 = self.elements[elem]
        x1, y1, z1 = self.nodes[n1]
        x2, y2, z2 = self.nodes[n2]

        # Calculate element length
        L = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

        # Direction cosines
        cx = (x2 - x1) / L
        cy = (y2 - y1) / L
        cz = (z2 - z1) / L

        # Local stiffness matrix for 3D bar element: k = (EA/L) * [c^2]
        k_factor = (self.E * self.A) / L
        k_local = k_factor * np.array([
            [cx * cx, cx * cy, cx * cz, -cx * cx, -cx * cy, -cx * cz],
            [cx * cy, cy * cy, cy * cz, -cx * cy, -cy * cy, -cy * cz],
            [cx * cz, cy * cz, cz * cz, -cx * cz, -cy * cz, -cz * cz],
            [-cx * cx, -cx * cy, -cx * cz, cx * cx, cx * cy, cx * cz],
            [-cx * cy, -cy * cy, -cy * cz, cx * cy, cy * cy, cy * cz],
            [-cx * cz, -cy * cz, -cz * cz, cx * cz, cy * cz, cz * cz]
        ])
        return k_local

    def assemble_global_stiffness(self):
        # Initialize global stiffness matrix
        K_global = np.zeros((self.total_dof, self.total_dof))

        # Loop over all elements to assemble global stiffness
        for elem in range(len(self.elements)):
            k_local = self.local_stiffness_matrix(elem)
            n1, n2 = self.elements[elem]
            # Degrees of freedom for the two nodes (3 DOF each)
            dof = [n1 * 3, n1 * 3 + 1, n1 * 3 + 2, n2 * 3, n2 * 3 + 1, n2 * 3 + 2]
            # Add local stiffness contributions to global matrix
            for i in range(6):
                for j in range(6):
                    K_global[dof[i], dof[j]] += k_local[i, j]
        return K_global

    def apply_boundary_conditions(self, K_global, F_global):
        # Reduce system by removing fixed DOFs
        free_dof = []
        fixed_dof = []
        for node in range(self.num_nodes):
            if node in self.fixed_nodes:
                fixed_dof.extend([node * 3, node * 3 + 1, node * 3 + 2])
            else:
                free_dof.extend([node * 3, node * 3 + 1, node * 3 + 2])

        # Partition stiffness matrix and force vector
        K_ff = K_global[np.ix_(free_dof, free_dof)]
        F_f = F_global[free_dof]
        return K_ff, F_f, free_dof, fixed_dof

    def solve_displacements(self):
        # Assemble global stiffness matrix
        K_global = self.assemble_global_stiffness()

        # Assemble global force vector
        F_global = np.zeros(self.total_dof)
        for node, fx, fy, fz in self.forces:
            F_global[node * 3] = fx
            F_global[node * 3 + 1] = fy
            F_global[node * 3 + 2] = fz

        # Apply boundary conditions
        K_ff, F_f, free_dof, fixed_dof = self.apply_boundary_conditions(K_global, F_global)

        # Solve for displacements (u = K^-1 * F)
        u_f = np.linalg.solve(K_ff, F_f)

        # Reconstruct full displacement vector
        u_global = np.zeros(self.total_dof)
        for i, dof in enumerate(free_dof):
            u_global[dof] = u_f[i]
        return u_global, K_global, F_global, free_dof, fixed_dof

    def compute_reactions(self, K_global, u_global, F_global, fixed_dof):
        # Reaction forces: R = K * u - F (only at fixed DOFs)
        reactions = K_global @ u_global - F_global
        return reactions[fixed_dof]

    def compute_stresses(self, u_global):
        # Calculate stress in each element
        stresses = []
        for elem in range(len(self.elements)):
            n1, n2 = self.elements[elem]
            x1, y1, z1 = self.nodes[n1]
            x2, y2, z2 = self.nodes[n2]
            L = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
            cx = (x2 - x1) / L
            cy = (y2 - y1) / L
            cz = (z2 - z1) / L

            # Displacements at element nodes
            u1 = u_global[n1 * 3:n1 * 3 + 3]
            u2 = u_global[n2 * 3:n2 * 3 + 3]

            # Axial displacement along element
            delta = (-cx * u1[0] - cy * u1[1] - cz * u1[2]) + (cx * u2[0] + cy * u2[1] + cz * u2[2])
            strain = delta / L
            stress = self.E * strain
            stresses.append(stress)
        return stresses


# Default problem setup
def main():
    # Define nodes [(x, y, z)]
    # nodes = [
    #     (12, -3, -4),  # Node 1
    #     (0, 0, 0),  # Node 2
    #     (12, -3, -7),  # Node 3
    #     (14, 6, 0),  # Node 4
    # ]

    nodes = [
        (0,0,0),
        (60,0,0),
        (30,40,0),
        (30,60,0)
    ]

    # Define elements [(node_i, node_j)]
    # elements = [
    #     (0, 1),  # Element between node 1 and 2
    #     (0, 2),  # Element between node 1 and 3
    #     (0, 3)  # Element between node 1 and 4
    # ]

    elements = [
        (0,2),
        (1,2),
        (2,3)
    ]

    # Material properties
    # E = 210e9  # Modulus of elasticity (210 GPa)
    # A = 10e-4  # Cross-sectional area (10^-4 m^2)

    A = 50*10e-4
    E = 210e9

    # External forces [(node, fx, fy, fz)]
    # forces = [(0, 20e3, 0, 0)]  # 20 kN in x-direction at node 1
    forces = [(2,50e3,-100e3,0)]
    # Fixed nodes (pin supports at nodes 2, 3, 4)
    # fixed_nodes = [1, 2, 3]  # Node indices (0-based)
    fixed_nodes = [0,1,3]
    # Create and solve FEM problem
    fem = Truss3D_FEM(nodes, elements, E, A, forces, fixed_nodes)
    u_global, K_global, F_global, free_dof, fixed_dof = fem.solve_displacements()

    # Compute reactions and stresses
    reactions = fem.compute_reactions(K_global, u_global, F_global, fixed_dof)
    stresses = fem.compute_stresses(u_global)

    # Output results
    print("Nodal Displacements (m):")
    for i in range(fem.num_nodes):
        print(f"Node {i + 1}: x={u_global[i * 3]:.6e}, y={u_global[i * 3 + 1]:.6e}, z={u_global[i * 3 + 2]:.6e}")

    print("\nReaction Forces (N):")
    for i, dof in enumerate(fixed_dof):
        node = dof // 3 + 1
        direction = ['x', 'y', 'z'][dof % 3]
        print(f"Node {node} ({direction}): {reactions[i]:.2f}")

    print("\nElement Stresses (Pa):")
    for i, stress in enumerate(stresses):
        print(f"Element {i + 1}: {stress:.2e}")


if __name__ == "__main__":
    main()