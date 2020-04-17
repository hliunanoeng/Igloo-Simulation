import os
from os.path import join
import numpy as np
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import dolfin as df

eps = 1e-9

# Define set up, corresponding to axon tunnel
dx_tunnel = 300.0  # um
dy_tunnel = 300.0
dz_tunnel = 5.0

x0 = -dx_tunnel / 2
y0 = -dy_tunnel / 2
z0 = 0.0

x1 = x0 + dx_tunnel
y1 = y0 + dy_tunnel
z1 = z0 + dz_tunnel

nx = 300  # Number of points in mesh. Larger number gives more accuracy, but is computationally demanding
ny = 300
nz = 10

sigma = 0.3  # Extracellular conductivity (S/m)


out_folder = 'S4_results'
fem_fig_folder = "S4_figs"
cross_section_fig_folder = "cross_section_figs"
sim_name = "S4"
[os.makedirs(f, exist_ok=True) for f in [out_folder, fem_fig_folder]]

V_center=[]

def plot_FEM_results(phi, t_idx):
    """ Plot the set-up, transmembrane currents and electric potential
    """

    x = np.linspace(x0, x1, nx)
    z = np.linspace(z0, z1, nz)
    y = np.linspace(y0, y1, ny)

    mea_x_values = np.zeros(len(x))

    for idx in range(len(x)):
        mea_x_values[idx] = phi(x[idx], 0, eps) #phi take 3D coordinates as the argument (x,y,z)
        if idx == 150:
            V_center.append(phi(x[idx], 0, eps))

    phi_plane_xz = np.zeros((len(x), len(z)))
    phi_plane_xy = np.zeros((len(x), len(y)))
    for x_idx in range(len(x)):
        for z_idx in range(len(z)):
            phi_plane_xz[x_idx, z_idx] = phi(x[x_idx], 0.0, z[z_idx])
        for y_idx in range(len(y)):
            try:
                phi_plane_xy[x_idx, y_idx] = phi(x[x_idx], y[y_idx], 0.0 + eps)
            except:
                phi_plane_xy[x_idx,y_idx]=0

    plt.close("all")
    fig = plt.figure(figsize=[18, 9])
    fig.subplots_adjust(hspace=0.9, bottom=0.07, top=0.97, left=0.2)

    ax_setup = fig.add_subplot(511, aspect=1, xlabel='x [$\mu$m]', ylabel='z [$\mu$m]',
                          title='Axon (green) and tunnel (gray)', xlim=[x0 - 5, x1 + 5], ylim=[z0 - 5, z1 + 5])

    axon_center_idx = np.argmin(np.abs(source_pos[:, 0] - 0))

    imem_max = np.max(np.abs(imem))
    ax_imem_temporal = fig.add_axes([0.05, 0.8, 0.08, 0.1], xlabel='Time [ms]', ylabel='nA',
                                    xlim=[0, tvec[-1]], ylim=[-imem_max, imem_max],
                          title='Transmembrane currents\n(x=0)')

    ax_imem_spatial = fig.add_subplot(512, xlabel=r'x [$\mu$m]', ylabel='nA',
                                      ylim=[-imem_max, imem_max],
                          title='Transmembrane currents across axon', xlim=[x0 - 5, x1 + 5])

    ax1 = fig.add_subplot(513, aspect=1, xlabel=r'x [$\mu$m]', ylabel=r'y [$\mu$m]',
                          title='Potential cross section (z=0)')

    ax2 = fig.add_subplot(514, aspect=1, xlabel=r'x [$\mu$m]', ylabel=r'z [$\mu$m]',
                          title='Potential cross section (y=0)')

    ax3 = fig.add_subplot(515, xlabel=r'x [$\mu$m]', ylabel='Potential [$\mu$V]',
                          ylim=[-1500, 1500], xlim=[x0 - 5, x1 + 5])
    ax3.set_yticks([-1500, -1000, -500, 0, 500, 1000, 1500])

    #  Draw set up with tunnel and axon
    rect = mpatches.Rectangle([x0, z0], dx_tunnel, dz_tunnel, ec="k", fc='0.8')
    ax_setup.add_patch(rect)

    ax_setup.plot(source_pos[:, 0], source_pos[:, 2], c='g', lw=2)
    ax_imem_temporal.plot(tvec, imem[axon_center_idx, :])
    ax_imem_temporal.axvline(tvec[t_idx], c='gray', ls="--")

    ax_imem_spatial.plot(source_pos[:, 0], imem[:, t_idx])

    img1 = ax1.imshow(phi_plane_xy.T, interpolation='nearest', origin='lower', cmap='bwr',
                      extent=(x[0], x[-1], y[0], y[-1]), vmax=1.5, vmin=-1.5)
    img2 = ax2.imshow(phi_plane_xz.T, interpolation='nearest', origin='lower', cmap='bwr',
                      extent=(x[0], x[-1], z[0], z[-1]), vmax=1.5, vmin=-1.5)

    cax = fig.add_axes([0.95, 0.5, 0.01, 0.1])

    plt.colorbar(img1, cax=cax, label="mV")
    l, = ax3.plot(x, mea_x_values*1000,  lw=2, c='k')

    plt.savefig(join(fem_fig_folder, 'results_{}_t_idx_{:04d}.png'.format(sim_name, t_idx)))

    plt.close("all")
    fig = plt.figure(figsize=[18, 9])
    ax1 = fig.add_subplot(111, aspect=1, xlabel=r'x [$\mu$m]', ylabel=r'y [$\mu$m]',
                          title='Potential cross section (z=0)')
    img1 = ax1.imshow(phi_plane_xy.T, interpolation='nearest', origin='lower', cmap='bwr',
                      extent=(x[0], x[-1], y[0], y[-1]), vmax=1.5, vmin=-1.5)
    cax = fig.add_axes([0.95, 0.5, 0.01, 0.1])

    plt.colorbar(img1, cax=cax, label="mV")
    plt.savefig(join(cross_section_fig_folder, 'results_{}_t_idx_{:04d}.png'.format(sim_name, t_idx)))

# Loading results from neural simulation, from running "python neural_simulation.py" in terminal
source_pos = np.load(join(out_folder, "source_pos.npy")) #a list of 3D-coordinate lists
imem = np.load(join(out_folder, "axon_imem.npy")) #the current at each location over the simulation time period
tvec = np.load(join(out_folder, "axon_tvec.npy")) #simulation time step
num_tsteps = imem.shape[1]
num_sources = source_pos.shape[0]

mesh = df.Mesh('S4.xml')
print("Number of cells in mesh: ", mesh.num_cells())
np.save(join(out_folder, "mesh_coordinates.npy"), mesh.coordinates())

domains = df.MeshFunction("size_t", mesh, 'S4_physical_region.xml')
boundaries = df.MeshFunction("size_t", mesh, 'S4_facet_region.xml')

V = df.FunctionSpace(mesh, "CG", 2)
dx = df.Measure("dx", domain=mesh, subdomain_data=domains)

# Define function space and basis functions
v = df.TestFunction(V)
u = df.TrialFunction(V)
a = df.inner(sigma * df.grad(u), df.grad(v)) * dx

# This corresponds to Neumann boundary conditions zero, i.e. all outer boundaries are insulating.
L = df.Constant(0) * v * dx

# Define Dirichlet boundary conditions at left, right, top and bottom  boundaries
bcs = [df.DirichletBC(V, 0.0, boundaries,1)]

for t_idx in range(num_tsteps):

    print("Time step {} of {}".format(t_idx, num_tsteps))
    phi = df.Function(V)
    A = df.assemble(a)
    b = df.assemble(L)

    [bc.apply(A, b) for bc in bcs]

    # Adding point sources (Dirac condition))from neural simulation
    for s_idx, s_pos in enumerate(source_pos):
        point = df.Point(s_pos[0], s_pos[1], s_pos[2])
        delta = df.PointSource(V, point, imem[s_idx, t_idx])
        delta.apply(b)

    df.solve(A, phi.vector(), b, 'cg', "ilu")

    np.save(join(out_folder, "phi_t_vec_{}.npy".format(t_idx)), phi.vector())

    plot_FEM_results(phi, t_idx)

V_center=np.array(V_center)
np.save(join(out_folder,"Voltage000.npy"),V_center)