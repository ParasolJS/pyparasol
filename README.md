# PyParasol
PyParasol is a way to easily write Parasol applications from python. 
PyParasol doesn't require any knowledge of html, css or starting local servers.
From PyParasol you can add your data to the application, set different plot 
attributes and display your Parasol application all from within one simple Python script.

### Refer to https://github.com/ParasolJS/parasol-es for more information on what Parasol does.
parasol.css, d3.v5.min.js, parasol.standalone.js all come from the parasol-es repository.
### Python Dependencies
-	pandas
# API
**PyParasol(page_title=””, tab_title=”PyParasol”, attach_grid_status=False, link_plots_status=True, output_html_file_name=”parasol.html”)**
-	Creates Parasol object.
-	page_title gets called through setPageTitle(), default is a blank string (no title will be displayed).
-	tab_title gets called through setTabTitle(), default is “PyParasol”.
-	attach_grid_status gets called through setGridStatus(), default is False.
-	link_plots_status gets called through setLinkedStatus(), default is True.
-	output_html_file_name gets sent through setHTMLFileName(), default is “parasol.html”.

**PyParasol.addPlot(file_name, plot_id, plot_title=None, columns_to_hide=None, axes_layout=None, plot_color=None, brushed_color=None, plot_alpha=None, brushed_alpha=None, reorderable_status=True)**
-	This is the main function for adding a plot and styling it. All parcoords options will be included in this function.
-	file_name is the associated .csv file that the data for the plot will come from. 
-	plot_id is required since it is how all other functions will refer to the plot, the plot_id can be numerical or can be a name. 
-	plot_title is optional and if entered it will be the title above the plot on the Parasol application. 
-	columns_to_hide (list) needs to be entered as a list of column headers relating to columns in the data file and is optional. This optional parameter sets which columns from the inputted data file you don’t want to show.
-	axes_layout (list) needs to be entered as a list of column headers relating to the columns in the data file and is optional. This parameter specifies exactly which columns from the inputted data file you want to have showing in the plot. Something important to note is that **axes_layout will override columns_to_hide.**
-	plot_color (string): the color of the data in the plot, entered as a 6 character hex value.
-	brushed_color (string): the color of the data in the plot when brushed, entered as a 6 character hex value.
-	plot_alpha (float): the alpha value of the plot, entered as a float between 0 and 1.
-	brushed_alpha (float): the alpha value of the plot when brushed, entered as a float between 0 and 1.
-	reorderable_status (boolean): determines the status of setting the reorderable attribute to the plot.

**PyParasol.setPageTitle(page_title)**
-	page_title: string.
-	Sets the title of Parasol application webpage, which will be displayed at the top of the Parasol application.

**PyParasol.setTabTitle(tab_title)**
-	tab_title: string.
-	Sets the tab name of the Parasol application webpage.

**PyParasol.setReorderableStatus(reorder_status, plot_id_list=None)**
-	reorder_status: boolean.
-	Changes the reorderable status to reorder_status for the plot ID’s listed in plot_id_list. If plot_id_list is set as none, it will change the status for all plots.

**PyParasol.setPlotAlpha(plot_alpha, plot_id_list=None)**
-	plot_alpha: float in the range (0, 1].
-	Sets the alpha to new_alpha for the plot ID’s listed in plot_id_list. If plot_id_list is set as none, it will change the attribute for all plots.

**PyParasol.setAlphaOnBrushed(alpha_on_brushed, plot_id_list=None)**
-	alpha_on_brushed: float in the range (0, 1].
-	Sets the alpha on brushed attribute to alpha_on_brushed for all plots listed in plot_id_list. If plot_id_list is set to none, it will change the attribute for all plots.

**PyParasol.setPlotColor(plot_color, plot_id_list=None)**
-	plot_color: 6 character hex color code (string).
-	Sets the color attribute to plot_color for all plots listed in plot_id_list. If plot_id_list is set to none, it will change the attribute for all plots.
-	**Setting the color of a plot will override any color clustering.**

**PyParasol.setBrushedColor(brushed_color, plot_id_list=None)**
-	brushed_color: 6 character hex color code (string).
-	Sets the color on brushed attribute to brushed_color for all plots listed in plot_id_list. If plot_id_list is set to none, it will change the attribute for all plots.

**PyParasol.setGridStatus(grid_status)**
-	grid_status: boolean.
-	Sets the grid status of the parasol application. If grid_status is set to true, it will display a grid, if set to false, it will not display a grid.
-	The grid will be linked to the linked data if the linked attribute is set to true.

**PyParasol.setHTMLFileName(new_html_file_name)**
-	new_html_file_name: string.
-	Sets the name of the html file that will be written when calling the compile function.
-	Defaults to parasol.html.

**PyParasol.setLinkedStatus(linked_status, plot_id_list=None)**
-	linked_stauts: boolean, plot_id_list: list.
-	Sets the status of if you want to link plots together and if you want to link the grid. 
-	**If the linked status is never set, the linked status will default to true.**
-	**plot_id_list specifies which plots you want to link together. If it is set to none, all plots will be linked if linked_status is set to true. This is the default.**

**PyParasol.setColorCluster(cluster_status, variables_to_cluster=None, number_colors=4, plot_id_list=None)**
-	cluster_status: boolean, variables_to_cluster: list, number_colors: integer, plot_id_list: list.
-	cluster_status is a Boolean which determines if color clustering will be turned on or off.
-	variables_to_cluster determines which variabes, defined as column headers from the data file, to base the color clustering on. If set to none, which is default, it will cluster based on all variables. Do not cluster qualitative variables.
-	number_colors determines how many different color groups will be made when clustering.
-	plot_id_list determines which plots will have color clustering. If set to none, all plots will use the same color clustering.
-	**Note: it is only possible to have one cluster statement, if multiple setColorCluster calls are made, only the last one will be used.**

**PyParasol.assignWeightedSums(variable_list, associated_weights, plot_id_list=None)**
-	variable_list: list, associated_weights: list, plot_id_list: list.
-	variable_list determines which variables will have weight associated with them for creating a weighted sum axes.
-	associated_weights determines what weights each variable will have.
-	variable_list and associated_weights need to be lists of the exact same length, as each variable in variable_list will have the associated weight of the corresponding index in associated_weights.
-	plot_id_list determines which plots will have an associated weight axes added on, if set to None, the weighted sum attribute will be assigned to all plots.
-	Note: just calling this function will turn on the weighted sum axes

**PyParasol.setVariableScale(variable_list, scale_list, plot_id_list=None)**
-	variable_list: list, scale_list: list, plot_id_list: list.
-	This function allows the user to control the lower and upper limit that will be displayed on each variables’ axes.
-	variable_list determines which variables will have a scale associated with them. Okay to enter as a single data point.
-	scale_list determines the lower and upper limits of the data of the corresponding variable name in variable_list. Each scale object needs to be a list of length two in the form, [minimum, maximum]. It is okay to enter a single scale item if there is only a single variable name, other wise it has to be entered as a list of lists, for example [[min1, max1], [min2, max2]].
-	plot_id_list determines which plots will have the variable scales attribute associated with. If set to None, attribute will be set to all plots.

**PyParasol.compile(html_file_name=None)**
-	html_file_name: string
-	if html_file_name is not none, calls setHTMLFileName() with html_file_name
-	Compiles all plots and user settings into the final html file and saves it to the the html file that was previously set by the user, or defaults to parasol.html.
-	Any changes made after calling compile() won’t be incorporated into the final Parasol application.

**PyParasol.startLocalServer(port=8000)**
-	port: integer
-	This function starts a localhost server at the port, defaulted to 8000, that the user can use to see the Parasol application.
-	**Note: once this function has been called it will go on forever; any code after calling this function will not be called. It is recommended to call displayWebpage() before calling this function if the user intends to automatically open up the Parasol application.**

**PyParasol.displayWebpage(port=8000)**
-	port: integer
-	Opens up the localhost webpage with the predetermined html file name and the port that is specified.

**PyParasol.show(port=8000)**
-	port: integer
-	With this function a user can easily display the Parasol application after finishing setting all attributes. This is the recommended function.
-	Combines compile(), startLocalServer(port) and displayWebpage() into one function. Calling show(port) will allow a user to compile their html file, start a local server and automatically open up the webpage with one function for simplicity. 
-	Read displayWebpage() and startLocalServer() for information about port parameter.

# Acknowledgements
PyParasol and Parasol were created the by the Kasprzyk Research Group at the University Of Colorado Boulder