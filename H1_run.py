#%%
import numpy as np
import openmc
import pandas as pd

import sys
sys.path.append('/Users/user1/Documents/Summer Internship 2022/Python code/openmc/H1')

#%%
from utils.data_load import gamma_bins, neutron_bins

# Specifying cross_sections.xml location - environmental variable does not work
# for jupyter kernel for some reason

def main(n, N):

    openmc.Materials.cross_sections = "/Users/user1/Downloads/jeff33_hdf5/cross_sections.xml"

    #################################

    # Specifying materials

    H = openmc.Material(name="Hydrogen")
    H.add_nuclide("H1", 1.0)
    H.set_density("atom/cm3", 2e22)

    Nitrogen = openmc.Material(name="Nitrogen")
    Nitrogen.add_nuclide("N14", 1.0)
    Nitrogen.set_density("atom/cm3", 1e19)

    Materials = openmc.Materials([H, Nitrogen])
    Materials.export_to_xml('run_files/materials.xml')
    # openmc.plot_xs(H, "total")


    # Creating model geometry
    ball_exterior = openmc.Sphere(r=15)
    detector_inner = openmc.Sphere(r=16.3)
    detector_outer = openmc.Sphere(r=16.8, boundary_type='vacuum')

    ball = -ball_exterior 
    a_layer = +ball_exterior & -detector_inner
    detect = -detector_outer

    H_ball = openmc.Cell(name="ball", fill=H, region=ball)
    air_layer = openmc.Cell(fill=Nitrogen, region=a_layer)
    detector = openmc.Cell(fill=Nitrogen, region=detect)

    Universe = openmc.Universe(cells=[H_ball, air_layer, detector])
    Geometry = openmc.Geometry(Universe)
    Geometry.export_to_xml('run_files/geometry.xml')


    # Creating a plot for visualisation purposes

    plot_xy = openmc.Plot()
    plot_xy.width = (34, 34)
    plot_xy.pixels = (300, 300)
    plot_xz = openmc.Plot()
    plot_xz.width = (34, 34)
    plot_xz.pixels = (300, 300)
    plot_xz.basis = "xz"
    vox_plot = openmc.Plot()
    vox_plot.type = "voxel"
    vox_plot.width = (300, 300, 300)
    vox_plot.pixels = (200, 200, 200)

    # plot_xy.color_by = 'material'
    Plots = openmc.Plots([plot_xy, plot_xz, vox_plot])
    Plots.export_to_xml('run_files/plots.xml')
    # openmc.plot_geometry(cwd='run_files') # UNCOMMENT THIS WHEN YOU WANT TO SEE YOUR GEOMETRY REFRESHED


    # Defining settings

    settings = openmc.Settings()
    settings.run_mode = "fixed source"
    settings.particles = 10**(N-1)
    settings.batches = 10

    source = openmc.Source()
    #source.particle = "photon"
    source.space = openmc.stats.Point()
    source.angle = openmc.stats.Isotropic()
    # Set source energy distribution by changing n
    energy_dist_objects = [openmc.stats.Discrete(0.025, 1.0),
                        openmc.stats.Uniform(1e-5, 0.414),
                        openmc.stats.Uniform(1.38403e7, 1.41907e7)]
    source.energy = energy_dist_objects[n-1]
    settings.source = source

    settings.temperature = {'default': 293.6}
    settings.photon_transport = True
    settings.electron_treatment = 'led'
    settings.export_to_xml('run_files/settings.xml')


    # Specifying tallies

    particle_filter_n = openmc.ParticleFilter(['neutron'])
    particle_filter_g = openmc.ParticleFilter(['photon'])
    gamma_energy_filter = openmc.EnergyFilter(gamma_bins)
    neutron_energy_filter = openmc.EnergyFilter(neutron_bins)
    cell_filter = openmc.CellFilter([detector.id])

    flux_tally_g = openmc.Tally()
    current_tally_g = openmc.Tally()
    flux_tally_n = openmc.Tally()
    current_tally_n = openmc.Tally()
    
    flux_tally_g.filters = [gamma_energy_filter, particle_filter_g, cell_filter]
    flux_tally_g.scores = ["flux"]
    flux_tally_n.filters = [neutron_energy_filter, particle_filter_n, cell_filter]
    flux_tally_n.scores = ["flux"]

    surface_filter = openmc.SurfaceFilter(ball_exterior)
    current_tally_g.filters = [gamma_energy_filter, particle_filter_g, surface_filter]
    current_tally_g.scores = ["current"]
    current_tally_n.filters = [neutron_energy_filter, particle_filter_n, surface_filter]
    current_tally_n.scores = ["current"]


    Tally = openmc.Tallies([flux_tally_g, current_tally_g,
                            flux_tally_n, current_tally_n])
    Tally.export_to_xml('run_files/tallies.xml')

    ##########################
    # running

    openmc.run(cwd='run_files')  

def post_processing(n, N):

    with openmc.StatePoint("run_files/statepoint.10.h5") as statepoint:
        gamma_energy_filter = openmc.EnergyFilter(gamma_bins)
        neutron_energy_filter = openmc.EnergyFilter(neutron_bins)

        tallyfg = statepoint.get_tally(scores=['flux'], filters=[gamma_energy_filter])
        tallyfn = statepoint.get_tally(scores=['flux'], filters=[neutron_energy_filter])
        tallycg = statepoint.get_tally(scores=['current'], filters=[gamma_energy_filter])
        tallycn = statepoint.get_tally(scores=['current'], filters=[neutron_energy_filter])

    df_fg = tallyfg.get_pandas_dataframe()
    df_fn = tallyfn.get_pandas_dataframe()
    df_cg = tallycg.get_pandas_dataframe()
    df_cn = tallycn.get_pandas_dataframe()

    fg = df_fg['mean'].values
    fn = df_fn['mean'].values
    cg = df_cg['mean'].values
    cn = df_cn['mean'].values

    # Storing output values for later data processing

    gamma_bins_df = df_fg[["energy low [eV]", 'energy high [eV]']]
    neutron_bins_df = df_fn[["energy low [eV]", 'energy high [eV]']]
    gamma_vals = pd.DataFrame(np.array([fg, cg]).transpose(), columns=["fg", "cg"])
    neutron_vals = pd.DataFrame(np.array([fn, cn]).transpose(), columns=["fn", "cn"])
    output_g = pd.concat([gamma_bins_df, gamma_vals], axis=1)
    output_n = pd.concat([neutron_bins_df, neutron_vals], axis=1)

    output_g.to_csv(f"data/processed/output_{n}g_e{N}.csv")
    output_n.to_csv(f"data/processed/output_{n}n_e{N}.csv")

if __name__ == '__main__':
    # Set source energy distribution by changing n. N is power of 10 number of particles.
    n = 3
    N = 8
    main(n, N)
    post_processing(n, N)



 # %%
