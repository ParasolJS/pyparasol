# PyParasol
# For more information on PyParasol and for a full API, refer to https://github.com/ParasolJS/pyparasol

from combine_csv import combine_csv
from http.server import SimpleHTTPRequestHandler
from webbrowser import open as open_website
from socketserver import TCPServer


# this class contains all the options for a single plot, and a method for writing all the plot specific attributes
# instances of this class should not be made by the user, as there is no use for them except when called from
#   the PyParasol class.
# information about plot attributes can be found at https://github.com/ParasolJS/parasol-es/wiki/API-Reference
class _ParasolPlot:
    # plot data information
    file_name = None
    plot_id = None
    plot_title = None
    axes_layout = None
    columns_to_hide = None
    variables_to_scale_list = None
    variables_scale_limit_list=None

    # styling attributes
    alpha = None
    color = None
    alpha_on_brush = None
    color_on_brush = None
    reorderable = None

    def __init__(self, file_name, plot_id):
        # only plot data information gets set to defaults
        # styling attributes remain None unless changed
        self.file_name = file_name
        self.plot_id = plot_id
        self.plot_title = ""
        self.axes_layout = []
        self.columns_to_hide = []
        self.variables_to_scale_list = []
        self.variables_scale_limit_list = []

    # this function writes all the paracoord attributes specific to the plot
    def write_self_attributes(self, plot_id_number):
        final_html_lines = "\nps.charts[" + str(plot_id_number) + "]"

        # if there is a color set for that plot, adds the color attribute
        if self.color:
            final_html_lines += ".color('" + self.color + "')"

        # if there is an alpha set for that plot, adds the alpha attribute
        if self.alpha:
            final_html_lines += ".alpha(" + str(self.alpha) + ")"

        # if reorderable is true, adds reorderable keyword
        if self.reorderable:
            final_html_lines += ".reorderable()"

        # if brushed color was set, adds attribute
        if self.color_on_brush:
            final_html_lines += ".brushedColor('" + self.color_on_brush + "')"

        # if alpha on brushed was set, adds attribute
        if self.alpha_on_brush:
            final_html_lines += ".alphaOnBrushed(" + str(
                self.alpha_on_brush) + ")"

        if self.variables_to_scale_list:
            for variable, scale in zip(self.variables_to_scale_list, self.variables_scale_limit_list):
                final_html_lines += ".scale('" + str(variable) + "', " + str(scale) + ")"

        final_html_lines += ";"
        return final_html_lines


# the class parasol contains all attributes for a parasol plot as well as all methods for writing a parasol html file
# all class variables and functions with __ in front of them are intended to not be used by the user
class PyParasol:
    # list of individual parasol plots
    __parasol_plot_list = None

    # general data - not specific to a single plot
    __page_title = None
    __page_tab_title = None
    __attachGrid = None
    __html_file_name = None
    # linking plots data
    __link_plots = None
    __linked_plots_list = None
    # color clustering data
    __cluster_status = None
    __number_of_cluster_colors = None
    __plots_to_cluster_list = None
    __variables_to_cluster = None
    # weighted sums variables
    __weighted_variable_list = None
    __weighted_weight_list = None
    __weighted_plots_to_add_weights = None

    # button data
    # in the form of variable names and text data for button
    __button_variable_names = None
    __button_text_names = None

    def __init__(self,
                 page_title="",
                 tab_title="PyParasol",
                 attach_grid_status=False,
                 link_plots_status=True,
                 output_html_file_name="parasol.html"
                 ):
        self.__parasol_plot_list = []
        self.__button_variable_names = []
        self.__button_text_names = []
        self.__cluster_status = False
        # validating page title
        self.__page_title = page_title
        # setting tab title
        self.__page_tab_title = tab_title
        # setting grid status
        self.setGridStatus(attach_grid_status)
        # setting linked status
        self.setLinkedStatus(link_plots_status)
        # setting output html file name
        self.setHTMLFileName(output_html_file_name)

    # Adding csv file with data you want to be displayed as its own parallel plot
    # plot name is what the header name will be above the plot
    # if no plot title is specified, there won't be a title for the plot
    # the plot id is required and is how a user changes settings for that plot
    # columns to hide needs to be entered as a list of strings of column headers that you *DON'T* want displayed
    # *****SETTING AXES LAYOUT WILL OVERRIDE SETTING COLUMNS TO HIDE************
    def addPlot(self,
                file_name,
                plot_id,
                plot_title=None,
                columns_to_hide=None,
                axes_layout=None,
                plot_color=None,
                brushed_color=None,
                plot_alpha=None,
                brushed_alpha=None,
                reorderable_status=True
                ):

        # ensuring file exists
        temp = open(file_name, 'r')
        temp.close()

        # creating new parasol plot item
        new_plot = _ParasolPlot(file_name, str(plot_id))

        # adding all attributes if they exist
        if plot_title is not None:
            new_plot.plot_title = plot_title
        # axes layout list
        if axes_layout is not None:
            new_plot.axes_layout = axes_layout
        # columns to hide list
        if columns_to_hide is not None:
            new_plot.columns_to_hide = columns_to_hide
        # plot color
        plot_color = self.__validate_color__(plot_color)
        if plot_color != 0:
            new_plot.color = plot_color
        # plot alpha
        plot_alpha = self.__validate_alpha__(plot_alpha)
        if plot_alpha != 0:
            new_plot.alpha = plot_alpha
        # plot reorderable status
        if type(reorderable_status) != bool:
            new_plot.reorderable = True
        else:
            new_plot.reorderable = reorderable_status
        # brushed color
        brushed_color = self.__validate_color__(brushed_color)
        if brushed_color != 0:
            new_plot.color_on_brush = brushed_color
        # alpha on brushed
        brushed_alpha = self.__validate_alpha__(brushed_alpha)
        if brushed_alpha != 0:
            new_plot.alpha_on_brush = brushed_alpha

        # adding new parasol plot item to the list
        self.__parasol_plot_list.append(new_plot)

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@ PARASOL APPLICATION SETTINGS @@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # this function is for setting the name at the top of the parasol app page
    def setPageTitle(self, page_title):
        if type(page_title) != str:
            print("page title not set to a valid string")
            return
        self.__page_title = page_title

    # this function is for setting the title of the tab of the parasol app page
    def setTabTitle(self, tab_title):
        if type(tab_title) != str:
            print("tab title not set to a valid string")
            return
        self.__page_tab_title = tab_title

    # this function determines whether or not the plots will be reorderable
    def setReorderableStatus(self, reorder_status, plot_id_list=None):
        if type(reorder_status) is not bool:
            print('Set reorder status to True or False')
            return
        ids_to_change = self.__find_plot_index_from_id__(plot_id_list)
        if ids_to_change != 0:
            for plot_id in ids_to_change:
                self.__parasol_plot_list[plot_id].reorderable = reorder_status

    # this function sets the alpha level of the plots
    def setPlotAlpha(self, plot_alpha, plot_id_list=None):
        plot_alpha = self.__validate_alpha__(plot_alpha)
        if plot_alpha == 0:
            return
        ids_to_change = self.__find_plot_index_from_id__(plot_id_list)
        if ids_to_change != 0:
            for plot_id in ids_to_change:
                self.__parasol_plot_list[plot_id].alpha = plot_alpha

    # this function sets the brushed on alpha variable
    def setAlphaOnBrushed(self, alpha_on_brushed, plot_id_list=None):
        alpha_on_brushed = self.__validate_alpha__(alpha_on_brushed)
        if alpha_on_brushed == 0:
            return
        ids_to_change = self.__find_plot_index_from_id__(plot_id_list)
        if ids_to_change != 0:
            for plot_id in ids_to_change:
                self.__parasol_plot_list[plot_id].alpha_on_brush = alpha_on_brushed

    # this function determines whether or not there will be a grid of data attached
    def setGridStatus(self, grid_status):
        if type(grid_status) is not bool:
            print('Set grid status to True or False')
            return
        self.__attachGrid = grid_status

    # this function allows the user to set the file name of the outputted html file
    def setHTMLFileName(self, new_html_file_name):
        if self.__validate_file_name__(new_html_file_name, 'html'):
            print("html file name not valid")
            return
        self.__html_file_name = new_html_file_name

    # this function specifies whether or not to link the plots together
    # linked plots defaults to yes, so plots are interactive with eachother
    # linked charts list is optional and specifies which specific plots to list
    # if no linked chart list parameter is given, it will link all plots together
    # linked chart list needs to take in a list of integers representing plot numbers, starting at 0
    def setLinkedStatus(self, linked_status, plot_id_list=None):
        if type(linked_status) is not bool:
            print('Set linked status to True or False')
            return
        if plot_id_list is not None:
            plot_id_list = self.__find_plot_index_from_id__(plot_id_list)
            if plot_id_list != 0:
                self.__linked_plots_list = plot_id_list
        self.__link_plots = linked_status


    # this function sets the color of the plot
    # WARNING: setting an overall plot color will override a plot cluster
    def setPlotColor(self, plot_color, plot_id_list=None):
        plot_color = self.__validate_color__(plot_color)
        if plot_color == 0:
            return
        ids_to_change = self.__find_plot_index_from_id__(plot_id_list)
        if ids_to_change != 0:
            for plot_id in ids_to_change:
                self.__parasol_plot_list[plot_id].color = plot_color

    # this function sets the color when a plot is brushed
    def setBrushedColor(self, brushed_color, plot_id_list=None):
        brushed_color = self.__validate_color__(brushed_color)
        if brushed_color == 0:
            return
        ids_to_change = self.__find_plot_index_from_id__(plot_id_list)
        if ids_to_change != 0:
            for plot_id in ids_to_change:
                self.__parasol_plot_list[plot_id].color_on_brush = brushed_color

    # this function sets the color clustering functionality
    # plots to cluster needs to be entered as a list of integers associating plot number
    # if no variables to cluster attribute is added, it will cluster all of them
    def setColorCluster(self, cluster_status, variables_to_cluster=None, number_colors=4, plot_id_list=None):
        # validating inputs
        if type(cluster_status) is not bool:
            print('Set cluster status to True or False')
            return
        try:
            int(number_colors)
            if number_colors < 1:
                raise Exception('invalid number of colors')
        except Exception:
            print('set number of colors to a valid positive integer')
            return

        # validating variables to cluster if cluster status is true
        if cluster_status and variables_to_cluster is not None:
            variables_to_cluster = self.__validate_data_is_list_or_single__(variables_to_cluster, str)
            if variables_to_cluster == 0:
                print("set variables to cluster to a valid list of names, or a single name")
                return
        if plot_id_list is not None:
            plot_id_list = self.__find_plot_index_from_id__(plot_id_list)
            if plot_id_list != 0:
                self.__plots_to_cluster_list = plot_id_list

        # setting data
        self.__cluster_status = cluster_status
        self.__number_of_cluster_colors = number_colors
        self.__variables_to_cluster = variables_to_cluster

    # this function assigns weights to certain variables to make a weighted sums variable
    # variable list is a list of the variables that will have a weight associated to them
    # associated weights is the list of weights that correspond the variable list
    def assignWeightedSums(self, variable_list, associated_weights, plot_id_list=None):
        variable_list = self.__validate_data_is_list_or_single__(variable_list, str)
        associated_weights = self.__validate_data_is_list_or_single__(associated_weights, float)
        if variable_list == 0 or associated_weights == 0:
            print("error in variable list or associated weights list")
            return
        if len(variable_list) != len(associated_weights):
            print("variable list and associated weights list are not the same length")
            return
        self.__weighted_variable_list = variable_list
        self.__weighted_weight_list = associated_weights
        if plot_id_list is not None:
            plot_id_list = self.__find_plot_index_from_id__(plot_id_list)
            if plot_id_list != 0:
                self.__weighted_plots_to_add_weights = plot_id_list

    # this function assigns scales (lower and upper limits for axes) to a variable or list of variables
    # you can enter variables as a list of variables or one variable name
    # you can enter scale_list as one list [min, max] or a list of scale-lists: [[min1, max1], [min2, max2]]
    def setVariableScale(self, variable_list, scale_list, plot_id_list=None):
        variable_list = self.__validate_data_is_list_or_single__(variable_list, str)
        # validating that scale_list is a valid scale, or list of scales
        bad_data = False
        try:
            temp = scale_list[0][0]
            for scale in scale_list:
                # if scale isn't a list in the form [min, max]
                if len(scale) != 2:
                    bad_data = True
                scale = self.__validate_data_is_list_or_single__(scale, float)
                if scale == 0:
                    bad_data = True
        except Exception:
            scale_list = self.__validate_data_is_list_or_single__(scale_list, float)
            if scale_list == 0 or len(scale_list) != 2:
                bad_data = True
            scale_list = [scale_list]

        # if data is bad, exits function
        if bad_data:
            print("variable scale data inputted incorrectly")
            return
        if len(variable_list) != len(scale_list):
            print("variable list and scale list not the same length")
            return

        # changing scales for all entered ids
        ids_to_change = self.__find_plot_index_from_id__(plot_id_list)
        if ids_to_change != 0:
            for plot_id in ids_to_change:
                self.__parasol_plot_list[plot_id].variables_to_scale_list += variable_list
                self.__parasol_plot_list[plot_id].variables_scale_limit_list += scale_list

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@ BUTTON OPTIONS @@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # this function sets the optional export brushed data button
    def addExportBrushedButton(self):
        self.__button_text_names.append("Export Brushed Data")
        self.__button_variable_names.append("export_brushed")

    # this function sets the optional export marked data button
    def addExportMarkedButton(self):
        self.__button_text_names.append("Export Marked Data")
        self.__button_variable_names.append("export_marked")

    # this function sets the optional reset brushed data button
    def addResetBrushedButton(self):
        self.__button_text_names.append("Reset Brushed Data")
        self.__button_variable_names.append("reset_brushed")

    # this function sets the optional reset brushed data button
    def addResetMarkedButton(self):
        self.__button_text_names.append("Reset Marked Data")
        self.__button_variable_names.append("reset_marked")

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@ HELPER FUNCTIONS @@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # this function checks to see if inputted data is a list, or if it's a single piece of data it returns
    # the data as the only element inside a list
    # this function also checks to see that all inputted data is of the correct type
    # this function is set up so if a float is entered as the data type, it will validate integers
    @staticmethod
    def __validate_data_is_list_or_single__(input_data, data_type):
        if type(input_data) == list:
            for data in input_data:
                # validates if data type is float and input data is int
                if data_type == float and type(data) == int:
                    continue
                if type(data) != data_type:
                    return 0
            return input_data
        elif type(input_data) == data_type:
            return [input_data]
        # validates if data type is float and input data is int
        elif data_type == float and type(input_data) == int:
            return [input_data]
        else:
            return 0

    # this function validates a file name as a file and the correct extension
    # returns true if not validated, returns false if valid function name
    @staticmethod
    def __validate_file_name__(file_name, extension_type):
        if type(file_name) is not str:
            return True
        try:
            if file_name.split('.')[1] != extension_type:
                return True
        except Exception:
            return True
        return False

    # this function returns the plot index of a plot id name
    # if the plot id doesn't exist, returns 0
    # if the id_to_find_list is None, returns a list of all indices
    def __find_plot_index_from_id__(self, id_to_find_list):
        if id_to_find_list is None:
            # returns all indices
            id_index_list = list(range(len(self.__parasol_plot_list)))
            return id_index_list
        # if just a single data point was entered, turns it into a list
        if type(id_to_find_list) != list:
            id_to_find_list = [id_to_find_list]
        bad_data = False
        id_index_list = []
        for id_to_find in id_to_find_list:
            # validates that all id's inputted are actual ids that have been specified
            try:
                id_to_find = str(id_to_find)
                for plot_number in range(len(self.__parasol_plot_list)):
                    if self.__parasol_plot_list[plot_number].plot_id == id_to_find:
                        id_index_list.append(plot_number)
            except Exception:
                bad_data = True
        if bad_data:
            return 0
        else:
            return id_index_list

    # this function is used to validate a variable is a hex color
    @staticmethod
    def __validate_color__(color_variable):
        if color_variable is None:
            return None
        if type(color_variable) is not str:
            print("hex code not valid, setting to default")
            return 0
        # validating hex code is a six character string
        if color_variable[0] == "#":
            color_variable = color_variable[1:]
        if len(color_variable) != 6:
            print("hex code not valid, setting to default")
            return 0
        color_variable = '#' + color_variable
        return color_variable

    # this function validates than an alpha variable is valid
    @staticmethod
    def __validate_alpha__(alpha):
        if alpha is None:
            return None
        try:
            float(alpha)
        except BaseException:
            print("set the alpha to a valid decimal number")
            return 0
        if (0 < alpha <= 1) is False:
            print("set the alpha to a valid float between 0 and 1, (0,1]")
            return 0
        return alpha

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@ WRITING HTML CODE FUNCTIONS @@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # this function writes a line for making a button
    def __write_button_initial_line__(self, variable_name, text):
        final_html_line = "\n<button id='" + str(variable_name) + "'>" + str(text) + "</button>"
        return final_html_line

    # this function writes the initial lines for starting the button area
    def __write_button_setup_lines__(self):
        if self.__button_variable_names is None or self.__button_text_names is None:
            return ""
        final_html_lines = "\n<div class='widgets'>"
        for button_variable_name, button_text in zip(self.__button_variable_names, self.__button_text_names):
            final_html_lines += self.__write_button_initial_line__(button_variable_name, button_text)

        final_html_lines += "\n</div>"
        return final_html_lines

    # this function writes the html code for making the layout of the plots on the screen
    def __write_plot_body_lines__(self):
        # setting up plot id names
        plot_id_list = []
        for index in range(len(self.__parasol_plot_list)):
            plot_id_list.append("p" + str(index))

        final_html_lines = ""
        # adding header and data association to each file
        for plot in range(len(self.__parasol_plot_list)):
            final_html_lines += "\n<h2>" + self.__parasol_plot_list[plot].plot_title + "</h2>"
            final_html_lines += '\n<div id="' + plot_id_list[plot] + \
                                '" class="parcoords" style="height:200px; width:850px;"></div>'
        # adding grid for data at the bottom
        if self.__attachGrid:
            final_html_lines += '\n<div id="grid" style="width:100%;height:700px;" class="slickgrid-container"></div>'
        return final_html_lines

    # this function ends the body and starts the script lines
    def __write_end_body_start_script__(self, final_data_file):
        final_html_lines = '</body>'
        final_html_lines += '\n\n<script>'
        final_html_lines += "\nd3.csv('" + final_data_file + "')"
        final_html_lines += ".then(function(data) {"
        return final_html_lines

    # this function writes the end of a function
    def __write_function_end__(self):
        final_html_lines = "\n});"
        return final_html_lines

    # this function writes the end of the script section
    def __write_script_end__(self):
        final_html_lines = "\n</script>"
        return final_html_lines

    # this function sets up the titles, imports and styling settings
    def __write_setup_settings__(self):
        final_html_lines = '<!doctype html>\n<head>\n<meta content="text/html;charset=utf-8" http-equiv="Content-Type">'
        final_html_lines += '\n<meta content="utf-8" http-equiv="encoding">\n</head>'
        final_html_lines += '\n\n<title>' + self.__page_tab_title + '</title>'
        final_html_lines += '\n\n<link rel="stylesheet" type="text/css" href="parasol.css" >'
        final_html_lines += '\n<script src="d3.v5.min.js"></script>'
        final_html_lines += '\n<script src="parasol.standalone.js"></script>'
        final_html_lines += '\n\n<body>'
        final_html_lines += '\n<h1>' + self.__page_title + '</h1>\n'
        return final_html_lines

    # this function writes the parasol variable lines of code
    def __write_parasol_variable__(self):
        final_html_lines = "\nvar ps = Parasol(data)('.parcoords')"

        # adds attachgrid line if option is set to true
        if self.__attachGrid:
            final_html_lines += "\n.attachGrid({container: '#grid'})"

        # adds linked line if option is set to true
        final_html_lines += self.__write_linked_attribute_line__()

        # adds the clustering statements if set to true
        final_html_lines += self.__write_cluster_attribute_line__()

        # adds the weights variable if it exists
        final_html_lines += self.__write_weighted_sum_line__()

        # always adds the axes to hide line, if there is only one plot it will be an empty set
        # setting hideaxes or setaxeslayout *LAST* will override the other one
        final_html_lines += "\n.hideAxes(axes_to_hide)"
        final_html_lines += "\n.setAxesLayout(axes_layout)"

        final_html_lines += ";"
        return final_html_lines

    # this function writes all the attributes that are specific to plots
    # variables included: plot color, plot alpha
    def __write_specific_plot_attribute_lines__(self):
        final_html_lines = ""
        # loops through every plot that has been created
        for plot_id_number in self.__find_plot_index_from_id__(None):
            final_html_lines += self.__parasol_plot_list[plot_id_number].write_self_attributes(plot_id_number)
        return final_html_lines

    # this function writes the .linked attribute line if called
    def __write_linked_attribute_line__(self):
        final_html_line = ""
        # if the linked status is false, returns nothing
        if not self.__link_plots:
            return final_html_line
        # if there is a specific list of plots to link, adds them otherwise just adds all
        if self.__linked_plots_list is not None:
            final_html_line += "\n.linked(chartIDs = "
            final_html_line += str(self.__linked_plots_list)
            final_html_line += ")"
        else:
            final_html_line += "\n.linked()"
        return final_html_line

    # this function writes the .weightedSums line if called
    def __write_weighted_sum_line__(self):
        if self.__weighted_weight_list is None or self.__weighted_variable_list is None:
            return ""
        final_html_line = "\n.weightedSum({ weights:weights"
        if self.__weighted_plots_to_add_weights is not None:
            final_html_line += ", displayIDs: " + str(self.__weighted_plots_to_add_weights)
        final_html_line += "})"

        return final_html_line

    # this function writes the .cluster line if called
    def __write_cluster_attribute_line__(self):
        # if status is set to false, returns nothing
        if not self.__cluster_status:
            return ""
        final_html_line = "\n.cluster({k: " + str(self.__number_of_cluster_colors)
        # if there are display ids set, writes them
        if self.__plots_to_cluster_list is not None:
            final_html_line += ", displayIDs: " + str(self.__plots_to_cluster_list)
        # if there are certain variables to cluster set, writes them
        if self.__variables_to_cluster is not None:
            final_html_line += ", vars: " + str(self.__variables_to_cluster)
        final_html_line += "})"
        return final_html_line

    # this function writes the weights variables for the weighted sum option
    def __write_weights_variable__(self):
        if self.__weighted_weight_list is None or self.__weighted_variable_list is None:
            return ""
        final_html_lines = "\nvar weights = {"
        for weighted_var_number in range(len(self.__weighted_weight_list)):
            final_html_lines += "\n'" + str(self.__weighted_variable_list[weighted_var_number]) + "': " + \
                                str(self.__weighted_weight_list[weighted_var_number]) + ","
        final_html_lines += "\n};"
        return final_html_lines

    # this function writes the axes_to_hide variable to display numerous plots of different data
    def __write_axes_to_hide__(self, header_list):
        final_html_lines = "\nvar axes_to_hide = {"
        # for each plot, it adds the headers of every other data set besides itself
        for plot_number in range(len(header_list)):
            final_html_lines += "\n" + str(plot_number) + ": ["
            # adds any headers to hide that were specified
            for header_to_hide in self.__parasol_plot_list[plot_number].columns_to_hide:
                final_html_lines += '"' + header_to_hide + '", '
            # loops through every plots header list for each plot
            for plot_headers_number in range(len(header_list)):
                # skips iteration so the headers of a plot don't get added to the plots own axes-to-hide list
                if plot_headers_number == plot_number:
                    continue
                # if two plots have the same data set, skips so all data doesn't get erased
                if self.__parasol_plot_list[plot_number].file_name == self.__parasol_plot_list[plot_headers_number].file_name:
                    continue
                # if the current header list isn't for the current plot, adds the header lists to axes to hide
                for header in range(len(header_list[plot_headers_number])):
                    final_html_lines += '"' + header_list[plot_headers_number][header] + '", '
            final_html_lines += ']'
            if plot_number != len(header_list) - 1:
                final_html_lines += ','
        final_html_lines += "\n};"
        return final_html_lines

    # this function writes the axes layout variable to specify order, which variables to display
    def __write_axes_layout__(self):
        final_html_lines = "\nvar axes_layout = {"
        for plot in range(len(self.__parasol_plot_list)):
            if self.__parasol_plot_list[plot].axes_layout:
                final_html_lines += "\n" + str(plot) + ": "
                final_html_lines += str(self.__parasol_plot_list[plot].axes_layout)
                if plot != len(self.__parasol_plot_list) - 1:
                    final_html_lines += ","

        final_html_lines += "\n};"
        return final_html_lines

    # this function writes a button declaration line
    def __write_button_action_lines__(self, button_variable_name, action_item_line):
        final_html_lines = "\nd3.select('#" + str(button_variable_name) + "').on('click',function() {"
        final_html_lines += str(action_item_line)
        final_html_lines += self.__write_function_end__()
        return final_html_lines

    # this function is the master function for assigning buttons to their actions
    def __write_button_action_master__(self):
        # if there are no buttons, skips
        if self.__button_text_names is None or self.__button_variable_names is None:
            return ""
        final_html_lines = ""
        # loops through all variable names
        for button_variable_name in self.__button_variable_names:
            # gets buttons action and then writes the full button action function
            action = self.__get_button_action__(button_variable_name)
            if action is not None:
                final_html_lines += self.__write_button_action_lines__(button_variable_name, action)

        return final_html_lines

    # this function contains the inventory for assigning button variable names with their actions
    def __get_button_action__(self, variable_name):
        # @@@@@@@@ BUTTON ACTION INVENTORY @@@@@@@@@
        if variable_name == "export_brushed":
            action = "\nps.exportData(type='brushed')"
        elif variable_name == "export_marked":
            action = "\nps.exportData(type='marked')"
        elif variable_name == "reset_brushed":
            action = "\nps.resetSelections('brushed')"
        elif variable_name == "reset_marked":
            action = "\nps.resetSelections('marked')"
        else:
            action = None

        return action

    # this is the master function for writing all parasol html file lines
    # some of the functions are always called even if they won't do anything based on user options
    #   in that case, the function simply returns a blank string ""
    def __write_parasol_html_file__(self, header_list, final_data_file):
        html_final = ""
        html_final += self.__write_setup_settings__()
        html_final += self.__write_button_setup_lines__()
        html_final += self.__write_plot_body_lines__()
        html_final += self.__write_end_body_start_script__(final_data_file)
        html_final += self.__write_axes_to_hide__(header_list)
        html_final += self.__write_axes_layout__()
        html_final += self.__write_weights_variable__()
        html_final += self.__write_parasol_variable__()
        html_final += self.__write_specific_plot_attribute_lines__()
        html_final += self.__write_button_action_master__()
        html_final += self.__write_function_end__()
        html_final += self.__write_script_end__()

        return html_final

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@ FINISHING PLOT AND DISPLAYING PLOT @@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # this function starts the local server for the parallel plot and opens the web page
    def startLocalServer(self, port=8000):
        localhost_server = TCPServer(("", port), SimpleHTTPRequestHandler)
        localhost_server.serve_forever()

    # this function opens up the webpage that's specified as the html file name, call after starting local server
    def displayWebpage(self, port=8000):
        open_website("http://localhost:" + str(port) + "/" + self.__html_file_name)

    # this functions is used to display the parallel plot once set up and styling has been finished
    # this function is the same as compile except it *ALSO* creates a local server and opens the parasol window
    def show(self,
             port=8000
             ):
        # compiles the html and csv output files
        compile_success = self.compile()

        # if compiling failed, exits function
        if compile_success == 0:
            return

        # opens up webpage first since any code following starting the server won't be run
        self.displayWebpage(port)

        # starts local server at specified port
        self.startLocalServer(port)

        return

    # this function compiles the parasol html file and the output csv file
    # this function *DOES NOT* start a local server and run open a parasol window, it just creates it
    def compile(self, html_file_name=None):
        # assigns new html file name if one is specified
        if html_file_name is not None:
            self.setHTMLFileName(html_file_name)

        # if there is no data that has been added yet, exits program
        if len(self.__parasol_plot_list) == 0:
            print("no data files have been specified, will not compile")
            return 0
        # checking to see if all files are the same
        # also compiles list of all file names
        all_files_are_same = True
        file_name_list = []
        temp_file_name = self.__parasol_plot_list[0].file_name
        for plot_number in range(len(self.__parasol_plot_list)):
            file_name_list.append(self.__parasol_plot_list[plot_number].file_name)
            if self.__parasol_plot_list[plot_number].file_name != temp_file_name:
                all_files_are_same = False

        # setting up combined csv data file
        # if all files are the same (or there is only one file), uses data file as output data
        if all_files_are_same:
            output_data_file_name = self.__parasol_plot_list[0].file_name
            header_list = []
            for plot_number in range(len(self.__parasol_plot_list)):
                header_list.append([])
        # if there are numerous data files, combines them
        else:
            output_data_file_name = "output_data.csv"
            header_list = combine_csv(file_name_list, output_data_file_name)

        # writing the html file
        html_file = self.__write_parasol_html_file__(header_list, output_data_file_name)

        # writing the html file contents to the actual html file
        if self.__html_file_name is None:
            # if no html file name is specified, sets to default
            self.__html_file_name = "parasol.html"
        with open(self.__html_file_name, 'w') as html_output:
            html_output.write(html_file)

        return 1
