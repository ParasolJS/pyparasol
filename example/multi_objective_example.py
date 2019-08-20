# importing PyParasol
from PyParasol import PyParasol

# creating PyParasol object
# *note: the tab title, html file name and grid status can all be set when making the PyParasol object,
#   but for this example they were done using the set functions separately to demonstrate functionality
myParasol = PyParasol(link_plots_status=True, page_title='Lower Rio Grande Valley case study')

# setting application attributes
myParasol.setTabTitle("LRGV Analysis")
myParasol.setHTMLFileName("lrgv.html")
myParasol.setGridStatus(True)

# setting up objective and decision headers
objectives = ['rel. (-)', 'crit. rel. (-)', 'leases (#)', 'surplus (af)', 'cost ($)', 'dropped (af)', 'cost var. (-)',
              'dr. trans. ($)']
decisions = ['rights (af)', 'opt. low (af)', 'opt. high (af)', 'xi (-)', 'alpha 1-4 (-)', 'beta 1-4 (-)',
             'alpha 5-12 (-)', 'beta 5-12 (-)', 'cost ($)', 'dropped (af)', 'cost var. (-)', 'dr. trans. ($)']

# adding the objectives and decisions plots
myParasol.addPlot(file_name='data/lrgv.csv', plot_id='obj_plot', plot_title='Objectives', axes_layout=objectives)
myParasol.addPlot(file_name='data/lrgv.csv', plot_id='dec_plot', plot_title='Decisions', axes_layout=decisions)

# setting plot attributes
# *note how setting the plot_id_list to both the plots and setting plot_id_list to None sets the attribute to both plots
myParasol.setColorCluster(True, number_colors=3, plot_id_list=None)
myParasol.setPlotAlpha(.65, plot_id_list=['obj_plot', 'dec_plot'])

# displaying plot
myParasol.show()
