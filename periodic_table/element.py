import numpy as np
import matplotlib.patheffects as PathEffects
from matplotlib import colors as mpl_colors
import betterplotlib as bpl

class ColorChange(object):
    """Plot item that can have its color changed to be paler, or totally hidden
    from view."""
    def __init__(self, plot_item, fade_zorder_change=-10):
        self.faded = False
        self.hidden = False
        self.fade_zorder_change = fade_zorder_change

        self.plot_item = plot_item

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

        self.get_alpha = self.plot_item.get_alpha
        self.set_alpha = self.plot_item.set_alpha
        self.original_alpha = self.get_alpha()
        self.hidden_alpha = 0

        self.get_zorder = self.plot_item.get_zorder
        self.set_zorder = self.plot_item.set_zorder

        self._set_internal_colors()
        self._set_internal_zorder()


    def _set_internal_colors(self):
        self.original_color = self.get_color()
        self.faded_color = bpl.fade_color(self.original_color)

    def _set_internal_zorder(self):
        self.original_zorder = self.get_zorder()
        self.faded_zorder = self.original_zorder + self.fade_zorder_change

    def fade(self):
        if not self.faded:  # don't do anything if already faded
            self._set_internal_colors()
            self._set_internal_zorder()
            self.faded = True
            self._set_color_base(self.faded_color)

            self.set_zorder(self.faded_zorder)


    def unfade(self):
        if self.faded:  # if not currently faded, this does nothing
            self.faded = False
            self._set_color_base(self.original_color)
            self.set_zorder(self.original_zorder)

    def hide(self):
        if not self.hidden:  # don't do anything if already hidden
            self.hidden = True
            self.original_alpha = self.get_alpha()
            self.set_alpha(self.hidden_alpha)

    def unhide(self):
        if self.hidden:  # if not currently hidden, this does nothing
            self.hidden = False
            self.set_alpha(self.original_alpha)

    def set_color(self, color):
        """This function can be used to set the color of the object. If the
        object is currently faded the color will be set with the faded version
        of the color supplied, with the original color stored and ready to be
        be applied later."""
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
    def __init__(self, number, symbol, row, column,
                 frac_bb=0.0, frac_cr=0.0,
                 frac_snia=0.0, frac_snii=0.0, frac_agb=0.0,
                 frac_s=0.0, frac_r=0.0,
                 frac_decay=0.0, frac_unstable=0.0):
        """

        :param number:
        :param symbol:
        :param row:
        :param column:
        :param frac_bb:
        :param frac_cr:
        :param frac_snia:
        :param frac_snii:
        :param frac_agb:
        :param frac_s:
        :param frac_r:
        :param frac_decay:
        :param frac_unstable:
        """
        self.number = number
        self.symbol = symbol
        self.row_flip = row
        self.row = 11 - row
        self.column = column

        self.hidden = False
        self.highlight = False

        self.fracs = {"BB":       frac_bb,
                      "CR":       frac_cr,
                      "SNII":     frac_snii,
                      "SNIa":     frac_snia,
                      "AGB":      frac_agb,
                      "S":        frac_s,
                      "R":        frac_r,
                      "decay":    frac_decay,
                      "unstable": frac_unstable}

        total_fracs = sum(self.fracs.values())
        if not np.isclose(total_fracs, 1):
            raise ValueError("Fractions don't sum to 1.")
        for frac in self.fracs.values():
            if frac < 0 or frac > 1:
                raise ValueError("Fractions must be between 0 and 1.")

        self.colors = {"BB":       "#D7E5CC",
                       "CR":       "#C3DDFA",
                       "SNIa":     "#fe9443",
                       "SNII":     "#FEE844",
                       "R":        "#AFBF75",
                       "S":        "#73A0CC",
                       "decay":    "#DDCCDD",
                       "unstable": "#CCCCCC"}
        self.colors["AGB"] = self.colors["S"]

        self.shown = {source:False for source in self.colors}
        self.fills = dict()

    def setup(self, ax):
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

        num = ax.add_text(x=self.column + 0.5,
                          y=self.row + 0.25,
                          text=self.number,
                          color=bpl.almost_black,
                          coords="data", fontsize=0.6 * self.fontsize,
                          horizontalalignment="center",
                          verticalalignment="center")
        self.ax_num = ColorChange(num)

        box = ax.plot([self.column, self.column, self.column+1, self.column+1, self.column],
                      [self.row, self.row+1, self.row+1, self.row, self.row],
                      c=bpl.almost_black,
                      lw=5, zorder=100)
        self.box_list = [ColorChange(segment) for segment in box]

        self.ax_name_highlight.hide()

        # # fill the base white, will be used to highlight
        # self.white_fill = ax.fill_between(x=[self.column, self.column+1],
        #                                   y1=self.row,
        #                                   y2=self.row+1,
        #                                   color="white", alpha=0.5, zorder=-100)

        # then fill the rest
        self.box_fill(ax)

    def show_source(self, source):
        self.shown[source] = True
        try:
            self.fills[source].set_color(self.colors[source])
        except KeyError:   # this source isn't present
            pass

    def unshow_source(self, source):
        self.shown[source] = False
        try:
            self.fills[source].set_color("w")
        except KeyError:  # this source isn't present
            pass

    def highlight_bool(self, source):
        if source is None:
            return False
        else:
            highlight_threshold = 0.5
            if source == "low mass":
                return (self.fracs["AGB"] > highlight_threshold
                        or self.fracs["S"] > highlight_threshold)
            else:
                return self.fracs[source] > highlight_threshold

    def highlight_source(self, source):
        if self.highlight_bool(source):
            self.ax_name_highlight.unhide()
            self.ax_name.hide()
        else:
            self.ax_name_highlight.hide()
            self.ax_name.unhide()

        self.highlight = self.highlight_bool(source)

    def fade(self):
        self.faded = True
        for segment in self.box_list:
            segment.fade()
        self.ax_name_highlight.fade()
        self.ax_name.fade()
        self.ax_num.fade()

        for fill in self.fills.values():
            fill.fade()

    def unfade(self):
        self.faded = False
        for segment in self.box_list:
            segment.unfade()
        self.ax_name_highlight.unfade()
        self.ax_name.unfade()
        self.ax_num.unfade()

        for fill in self.fills.values():
            fill.unfade()

    def box_fill(self, ax):
        # then add certain sources. Here are the rules:
        # BB: full (except He and Li)
        # CR: full (except Li)
        # R: always on top
        # S: always on bottom
        # SNIa: Always on bottom
        # SNII: Always on top
        # AGB: Always on bottom
        # Elements in the top can be done by filling the whole thing, then
        # filling the rest with the color of the rest (either white or the
        # actual color)
        under = ["BB", "CR", "R", "SNII", "manmade"]
        over = ["AGB", "S", "SNIa"]

        # xs = [-1, 2]
        n_points = 1000
        xs = np.linspace(self.column, self.column + 1, n_points)
        base_xs = np.linspace(0, 1, n_points)
        base_ys = np.ones(n_points) * self.row
        if self.symbol == "He":
            # Fill the background with SNII, then half of it with AGB,
            # then the normal BB fill
            snii = ax.fill_between(x=xs, y1=base_ys,
                            y2=base_ys+1, color="w", lw=0, zorder=1)
            agb = ax.fill_between(x=xs, y1=base_ys,
                                  y2=base_ys + 1.0 - base_xs,
                                  lw=0,
                                  color="w", zorder=2)
            bb = ax.fill_between(x=xs, y1=base_ys,
                            y2=[self.row + box_fraction_line(self.fracs["BB"])(x) for x in base_xs],
                                 lw=0,
                            color="w", zorder=3)

            self.fills["SNII"] = ColorChange(snii)
            self.fills["AGB"] = ColorChange(agb)
            self.fills["BB"] = ColorChange(bb)
            self.fills["S"] = self.fills["AGB"]

        elif self.symbol == "Li":
            # Fill in the whole thing with CR
            # then cover the bottom (BB + AGB) fraction with BB
            # then cover the bottom BB fraction with BB
            cr = ax.fill_between(x=xs, y1=base_ys,
                            y2=base_ys+1,
                                 lw=0, color="w", zorder=1)
            total_agb_frac = self.fracs["BB"] + self.fracs["AGB"]
            agb = ax.fill_between(x=xs, y1=base_ys,
                            y2=[self.row + box_fraction_line(total_agb_frac)(x) for x in base_xs],
                                  lw=0, color="w", zorder=2)
            bb = ax.fill_between(x=xs, y1=base_ys,
                            y2=[self.row + box_fraction_line(self.fracs["BB"])(x) for x in base_xs],
                                 lw=0, color="w", zorder=3)

            self.fills["CR"] = ColorChange(cr)
            self.fills["AGB"] = ColorChange(agb)
            self.fills["BB"] = ColorChange(bb)

        else:
            # go through the ones on top first
            for source in self.fracs:
                if self.fracs[source] == 0:
                    continue

                if source in under:
                    fill = ax.fill_between(x=xs, y1=base_ys,
                                    y2=base_ys+1,
                                           lw=0, color="w", zorder=1)
                    self.fills[source] = ColorChange(fill)
                else:  # in under
                    fill = ax.fill_between(x=xs, y1=base_ys,
                                    y2=[self.row + box_fraction_line(self.fracs[source])(x) for x in base_xs],
                                           lw=0, color="w", zorder=2)
                    self.fills[source] = ColorChange(fill)