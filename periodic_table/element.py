import numpy as np
import matplotlib.patheffects as PathEffects
import betterplotlib as bpl

class ColorChange(object):
    """Plot item that can have its color changed to be paler, or totally hidden
    from view."""
    def __init__(self, plot_item, fade_zorder_change=-10):
        """
        Initialize the object

        :param plot_item: Matplotlib object that will be modified
        :param fade_zorder_change: How much to decrease the zorder when the color
                                   is faded.
        """
        self.faded = False
        self.hidden = False
        self.fade_zorder_change = fade_zorder_change

        self.plot_item = plot_item

        # Then figure out what the functions to modify the color are. This depends
        # on what kind of matplotlib object we have
        try:
            self.get_color = self.plot_item.get_color
            self._set_color_base = self.plot_item.set_color
        except AttributeError:
            # for facecolor the thing it returns is a different format, so
            # we have to parse it to make it play nice with the other functions.
            # It also depends on what kind of thing we have, strangely
            if len(self.plot_item.get_facecolor()) == 1:
                # This returns an array with an array of an RGBA tuple. We extract
                # the inner array and ignore alpha
                self.get_color = lambda: self.plot_item.get_facecolor()[0][0:3]
            elif len(self.plot_item.get_facecolor()) == 4:
                # here there is no outer array, so we just ignore alpha
                self.get_color = lambda: self.plot_item.get_facecolor()[0:3]

            self._set_color_base = self.plot_item.set_facecolor

        # Then set functions to modify the alpha
        self.get_alpha = self.plot_item.get_alpha
        self.set_alpha = self.plot_item.set_alpha
        self.original_alpha = self.get_alpha()

        # ... and zorder
        self.get_zorder = self.plot_item.get_zorder
        self.set_zorder = self.plot_item.set_zorder

        # Then calculate what color and zorder will be used when the object is faded.
        # We store this now, but it can be modified later if the object's color is
        # directly changed by the user
        self.original_color = self.get_color()
        self.faded_color = bpl.fade_color(self.original_color)
        self.original_zorder = self.get_zorder()
        self.faded_zorder = self.original_zorder + self.fade_zorder_change

    def fade(self):
        """
        Turn this object to it's faded color and zorder.

        :return: None, but the color and zorder are modified
        """
        if not self.faded:  # don't do anything if already faded
            self.faded = True
            # change to the faded colors and zorder
            self._set_color_base(self.faded_color)
            self.set_zorder(self.faded_zorder)


    def unfade(self):
        """
        Returns the object to its original color and zorder

        :return: None, but the color and zorder are modified.
        """
        if self.faded:  # if not currently faded, this does nothing
            self.faded = False
            self._set_color_base(self.original_color)
            self.set_zorder(self.original_zorder)

    def hide(self):
        """
        Hide this object by setting its alpha to zero.

        :return: None
        """
        if not self.hidden:  # don't do anything if already hidden
            self.hidden = True
            self.original_alpha = self.get_alpha()
            self.set_alpha(0)

    def unhide(self):
        """
        Unhide this object by reverting its alpha value back to the original.
        :return:
        """
        if self.hidden:  # if not currently hidden, this does nothing
            self.hidden = False
            self.set_alpha(self.original_alpha)

    def set_color(self, color):
        """This function can be used to set the color of the object.

        If the object is currently faded the color will be set with the faded version
        of the color supplied, with the original color stored and ready to be
        be applied later. Otherwise the supplied color is just set

        :param color: color to be used as the original color
        """
        self.original_color = color
        self.faded_color = bpl.fade_color(color)
        if self.faded:
            self._set_color_base(self.faded_color)
        else:
            self._set_color_base(self.original_color)


def box_fraction_line(frac):
    """
    Calculate a line that is above a given fraction of the unit square.

    Consider what I'll call the unit square, which is the square defined by the
    vertices (0,0), (1,0), (1,1), (0.1). We want to draw a line of unit slope
    that splits the square into two parts: one with area `frac` below the line,
    and one with area `1-frac` above the line. This calculates that line.

    :param frac: Fraction of the unit square to enclose below the line
    :type frac: float
    :return: Function containing the equation of the line.
    :rtype: function
    """
    if not 0 <= frac <= 1.0:
        raise ValueError("Frac must be between zero and one.")

    # Since we have a line of slope one, the only thing we need to determine
    # is the intercept. Working out the math is needed to determine this. I
    # did this on scratch paper. Due to the geometry, the integral of the area
    # has different forms depending on whether the fraction enclosed is more or
    # less than 0.5.
    if frac < 0.5:
        b = (-2 + np.sqrt(4 - 4 * (1 - 2 * frac))) / 2.0
    else:
        b = (2 - np.sqrt(4 - 4 * (2 * frac - 1))) / 2.0
    return lambda x: max(min(x + b, 1.0), 0.0)


class Element(object):
    fontsize = 30

    # The colors used for each source will be shared by the class.
    colors = {"bb":       "#D7E5CC",
              "cr":       "#C3DDFA",
              "snia":     "#fe9443",
              "snii":     "#FEE844",
              "r":        "#AFBF75",
              "s":        "#73A0CC",
              "decay":    "#DDCCDD",
              "unstable": "#CCCCCC"}
    colors["agb"] = colors["s"]

    def __init__(self, number, symbol, row, column,
                 frac_bb=0.0, frac_cr=0.0,
                 frac_snia=0.0, frac_snii=0.0, frac_agb=0.0,
                 frac_s=0.0, frac_r=0.0,
                 frac_decay=0.0, frac_unstable=0.0):
        """
        Set up the Element class

        :param number: Elemental number (number of protons)
        :param symbol: Two letter symbol for the element
        :param row: Row of the periodic table where this element is located.
        :param column: Column of the periodic table where this element is location.
        :param frac_bb: Fraction of this element's abundance that comes from the Big Bang
        :param frac_cr: Fraction of this element's abundance that comes from cosmic
                        ray spallation.
        :param frac_snia: Fraction of this element's abundance that comes from SNIa
        :param frac_snii: Fraction of this element's abundance that comes from SNII
        :param frac_agb: Fraction of this element's abundance that comes from nuclear
                         burning in low mass stars.
        :param frac_s: Fraction of this element's abundance that comes from S process
        :param frac_r: Fraction of this element's abundance that comes from R process
        :param frac_decay: Fraction of this element's abundance that comes from
                           nuclear decay
        :param frac_unstable: This will be 1.0 if the element is not naturally occuring
        """
        # Set up the element's basic info. We mess around with the indices a little to
        # match our table's setup.
        self.number = number
        self.symbol = symbol
        self.row_flip = row
        self.row = 11 - row
        self.column = column

        # We can hide or highlight this element, but to start neither will be true.
        self.hidden = False
        self.highlight = False

        # setup which sources contributed to this element
        self.fracs = {"bb":       frac_bb,
                      "cr":       frac_cr,
                      "snii":     frac_snii,
                      "snia":     frac_snia,
                      "agb":      frac_agb,
                      "s":        frac_s,
                      "r":        frac_r,
                      "decay":    frac_decay,
                      "unstable": frac_unstable}

        # Then double check this
        total_fracs = sum(self.fracs.values())
        if not np.isclose(total_fracs, 1):
            raise ValueError("Fractions don't sum to 1.")
        for frac in self.fracs.values():
            if frac < 0 or frac > 1:
                raise ValueError("Fractions must be between 0 and 1.")

        # None of the sources will be initially shown on the table.
        self.shown = {source:False for source in self.colors}
        self.fills = dict()

        # note that here we don't call setup, since we don't know which axis to put
        # this element on yet.

    def setup(self, ax):
        """
        Add this element to the given axis

        :param ax: Axis to add this element to.
        :return: None
        """
        # When we highlight the element, the text for the name will be white, with a
        # black outline. We need to have a separate text object for this.
        highlight_color = "white"
        highlight_text = ax.add_text(x=self.column + 0.5,
                                     y=self.row + 0.65,
                                     text=self.symbol,
                                     coords="data",
                                     fontsize=self.fontsize,
                                     color=highlight_color,
                                     horizontalalignment="center",
                                     verticalalignment="center",
                                     zorder=100)
        highlight_text.set_path_effects([PathEffects.withStroke(linewidth=5,
                                             foreground=bpl.almost_black)])
        self.ax_name_highlight = ColorChange(highlight_text)
        # This highlighted name is originally hidden.
        self.ax_name_highlight.hide()

        # When it's not highlighted, the text is just black. This is basiclly the same
        # as highlight_text, just without the highlight
        name = ax.add_text(x=self.column + 0.5,
                           y=self.row + 0.65,
                           text=self.symbol,
                           coords="data",
                           color=bpl.almost_black,
                           fontsize=self.fontsize,
                           horizontalalignment="center",
                           verticalalignment="center",
                           zorder=100)
        self.ax_name = ColorChange(name)

        # The number is never highlighted
        num = ax.add_text(x=self.column + 0.5,
                          y=self.row + 0.25,
                          text=self.number,
                          color=bpl.almost_black,
                          coords="data", fontsize=0.6 * self.fontsize,
                          horizontalalignment="center",
                          verticalalignment="center")
        self.ax_num = ColorChange(num)

        # Then draw the box around the element. This is just a square.
        box = ax.plot([self.column, self.column, self.column+1, self.column+1, self.column],
                      [self.row, self.row+1, self.row+1, self.row, self.row],
                      c=bpl.almost_black,
                      lw=5, zorder=100)
        # We do store these box segmments so they can be faded later.
        self.box_list = [ColorChange(segment) for segment in box]

        self.ax_name_highlight.hide()

        # fill the box white. This will be the base that's seen when the sources are
        # hidden.
        self.white_fill = ax.fill_between(x=[self.column, self.column+1],
                                          y1=self.row,
                                          y2=self.row+1,
                                          color="white", alpha=0.5, zorder=-100)

        # then fill the rest
        self.box_fill(ax)
        # hide all the fills to start
        for fills in self.fills.values():
            fills.hide()


    def show_source(self, source):
        """
        Show the fill indicating how much of this element came from a given source

        :param source: Which source to show
        :return: None
        """
        self.shown[source] = True
        try:
            self.fills[source].unhide()
        except KeyError:   # this source isn't present.
            # We don't have objects for sources with zero contribution, so we don't
            # raise an error
            pass

    def unshow_source(self, source):
        """
        Hide the fill indicating how much of this element came from a given soure

        :param source: Which source to show
        :return: None
        """
        self.shown[source] = False
        try:
            self.fills[source].hide()
        except KeyError:  # this source isn't present.
            # We don't have objects for sources with zero contribution, so we don't
            # raise an error
            pass

    def highlight_bool(self, source):
        """
        Internal function to calculate whether an element has more than 50% contribution
        from a given source

        This is only needed to handle the "low_mass" source, which is both S process
        and AGB.

        :param source: Which source to check if it needs to be highlighted
        :return: Whether or not this source has a greater than 50$ contribution.
        :rtype: bool
        """
        if source is None:
            return False
        else:
            highlight_threshold = 0.5
            # low mass has a special check
            if source == "low mass":
                return (self.fracs["AGB"] > highlight_threshold
                        or self.fracs["S"] > highlight_threshold)
            else:
                return self.fracs[source] > highlight_threshold

    def highlight_source(self, source):
        """
        Highlight the element name if there is a greater than 50% contribution from
        the given source.

        :param source: Which source to highlight
        :return: None, but the highlight text is activated
        """
        self.highlight = self.highlight_bool(source)

        if self.highlight:
            self.ax_name_highlight.unhide()
            self.ax_name.hide()
        else:
            self.ax_name_highlight.hide()
            self.ax_name.unhide()

    def fade(self):
        """
        Fade this element, including all parts of it (name, box, fills)
        :return: None
        """
        self.faded = True
        for segment in self.box_list:
            segment.fade()
        self.ax_name_highlight.fade()
        self.ax_name.fade()
        self.ax_num.fade()

        for fill in self.fills.values():
            fill.fade()

    def unfade(self):
        """
        Unade this element, including all parts of it (name, box, fills)
        :return: None
        """
        self.faded = False
        for segment in self.box_list:
            segment.unfade()
        self.ax_name_highlight.unfade()
        self.ax_name.unfade()
        self.ax_num.unfade()

        for fill in self.fills.values():
            fill.unfade()

    def box_fill(self, ax):
        """
        Fill in all the polygons that represent the fractions that come from all sources

        :param ax: Axis to do this on
        :return: None, but the fills are made
        """
        # then add certain sources. Here are the rules:
        # BB: full (except He and Li)
        # CR: full (except Li)
        # R: always on top
        # S: always on bottom
        # SNIa: Always on bottom
        # SNII: Always on top
        # AGB: Always on bottom

        # We do this as follows: For elements that are "under," we fill the entire box
        # with the representative color. Then for elements that are "over," we fill in
        # the section from the bottom to the needed line.

        top = ["bb", "cr", "r", "snii", "manmade"]
        bottom = ["agb", "s", "snia"]

        # setup some x and y values for the plotting
        x_left = self.column
        x_right = x_left + 1
        y_bottom = self.row
        y_top = y_bottom + 1

        n_points = 1000
        xs = np.linspace(x_left, x_right, n_points)
        # the line function needs values between 0 and 1.
        base_xs = np.linspace(0, 1, n_points)

        # He and Li are special cases with 3 important elements. Handle those first
        if self.symbol == "He":
            # Start with the bottom bb line
            bb_line = [y_bottom + box_fraction_line(self.fracs["bb"])(x)
                       for x in base_xs]
            # Then the AGB line will be in the middle. We can use the total fraction
            # of BB and AGB to get this
            total_agb_frac = self.fracs["bb"] + self.fracs["agb"]
            agb_line = [y_bottom + box_fraction_line(total_agb_frac)(x)
                        for x in base_xs]
            # Then the rest will be snii

            # We can fill this all in
            bb = ax.fill_between(x=xs, y1=y_bottom, y2=bb_line, lw=0,
                                 color=self.colors["bb"], zorder=1)
            agb = ax.fill_between(x=xs, y1=bb_line, y2=agb_line, lw=0,
                                  color=self.colors["agb"], zorder=1)
            snii = ax.fill_between(x=xs, y1=agb_line, y2=y_top, lw=0,
                                   color=self.colors["snii"], zorder=1)

            self.fills["snii"] = ColorChange(snii)
            self.fills["agb"] = ColorChange(agb)
            self.fills["bb"] = ColorChange(bb)


        elif self.symbol == "Li":
            # Start with the bottom bb line
            bb_line = [y_bottom + box_fraction_line(self.fracs["bb"])(x)
                       for x in base_xs]
            # Then the AGB line will be in the middle. We can use the total fraction
            # of BB and AGB to get this
            total_agb_frac = self.fracs["bb"] + self.fracs["agb"]
            agb_line = [y_bottom + box_fraction_line(total_agb_frac)(x)
                       for x in base_xs]
            # Then the rest will be cosmic rays

            # We can fill this all in
            bb = ax.fill_between(x=xs, y1=y_bottom, y2=bb_line, lw=0,
                                 color=self.colors["bb"], zorder=1)
            agb = ax.fill_between(x=xs, y1=bb_line, y2=agb_line, lw=0,
                                 color=self.colors["agb"], zorder=1)
            cr = ax.fill_between(x=xs, y1=agb_line, y2=y_top, lw=0,
                                 color=self.colors["cr"], zorder=1)

            self.fills["cr"] = ColorChange(cr)
            self.fills["agb"] = ColorChange(agb)
            self.fills["bb"] = ColorChange(bb)

        else:
            # go through the ones on top first
            for source in self.fracs:
                if self.fracs[source] == 0:
                    continue

                if source in top:
                    # We can calculate the line needed for the 1-fraction, then fill
                    # from the top to that line
                    line_func = box_fraction_line(1.0 - self.fracs[source])
                    line_ys = [min(y_bottom + line_func(x), y_top) for x in base_xs]

                    fill = ax.fill_between(x=xs, y1=line_ys, y2=y_top,
                                           lw=0, color=self.colors[source], zorder=1)
                    self.fills[source] = ColorChange(fill)
                else:  # in under
                    line_ys = [y_bottom + box_fraction_line(self.fracs[source])(x)
                               for x in base_xs]
                    fill = ax.fill_between(x=xs, y1=y_bottom, y2=line_ys,
                                           lw=0, color=self.colors[source], zorder=1)
                    self.fills[source] = ColorChange(fill)