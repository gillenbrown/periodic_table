import numpy as np
import matplotlib.patheffects as PathEffects
import betterplotlib as bpl

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
        self.ax_name_highlight = ax.add_text(x=self.column + 0.5,
                                             y=self.row + 0.65,
                                             text=self.symbol,
                                             coords="data",
                                             fontsize=self.fontsize,
                                             color=highlight_color,
                                             horizontalalignment="center",
                                             verticalalignment="center",
                                             zorder=100)
        self.ax_name_highlight.set_path_effects([PathEffects.withStroke(linewidth=5,
                                             foreground=bpl.almost_black)])

        self.ax_name = ax.add_text(x=self.column + 0.5,
                                   y=self.row + 0.65,
                                   text=self.symbol,
                                   coords="data",
                                   fontsize=self.fontsize,
                                   horizontalalignment="center",
                                   verticalalignment="center",
                                   zorder=100)

        self.ax_num = ax.add_text(x=self.column + 0.5,
                                  y=self.row + 0.25,
                                  text=self.number,
                                  coords="data", fontsize=0.6 * self.fontsize,
                                  horizontalalignment="center",
                                  verticalalignment="center")

        self.box = ax.plot([self.column, self.column, self.column+1, self.column+1, self.column],
                           [self.row, self.row+1, self.row+1, self.row, self.row],
                           c=bpl.almost_black,
                           lw=5, zorder=100)

        self.ax_name_highlight.set_alpha(0)

        # # fill the base white
        # self.white_fill = ax.fill_between(x=[self.column, self.column+1],
        #                                   y1=self.row,
        #                                   y2=self.row+1,
        #                                   color="white", alpha=1.0, zorder=0)

        # then fill the rest
        self.box_fill(ax)

    def show_source(self, source):
        self.shown[source] = True
        try:
            self.fills[source].set_color(self.colors[source])
        except KeyError:
            pass

    def unshow_source(self, source):
        self.shown[source] = False
        try:
            self.fills[source].set_color("w")
        except KeyError:
            pass

    def highlight_source(self, source):
        if source is None:
            highlight = False
        else:
            highlight_threshold = 0.5
            if source == "low mass":
                highlight = (self.fracs["AGB"] > highlight_threshold
                             or self.fracs["S"] > highlight_threshold)
            else:
                highlight = self.fracs[source] > highlight_threshold

        # True is treated as 1
        self.ax_name_highlight.set_alpha(1.0*highlight)
        self.ax_name.set_alpha(1.0 * (not highlight))

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
            self.fills["SNII"] = ax.fill_between(x=xs, y1=base_ys,
                            y2=base_ys+1, color="w", zorder=1)
            self.fills["AGB"] = ax.fill_between(x=xs, y1=base_ys,
                            y2=base_ys + 1.0 - base_xs,
                            color="w", zorder=2)
            self.fills["S"] = self.fills["AGB"]
            self.fills["BB"] = ax.fill_between(x=xs, y1=base_ys,
                            y2=[self.row + box_fraction_line(self.fracs["BB"])(x) for x in base_xs],
                            color="w", zorder=3)

        elif self.symbol == "Li":
            # Fill in the whole thing with CR
            # then cover the bottom (BB + AGB) fraction with BB
            # then cover the bottom BB fraction with BB
            self.fills["CR"] = ax.fill_between(x=xs, y1=base_ys,
                            y2=base_ys+1,
                            color="w", zorder=1)
            total_agb_frac = self.fracs["BB"] + self.fracs["AGB"]
            self.fills["AGB"] = ax.fill_between(x=xs, y1=base_ys,
                            y2=[self.row + box_fraction_line(total_agb_frac)(x) for x in base_xs],
                            color="w", zorder=2)
            self.fills["BB"] = ax.fill_between(x=xs, y1=base_ys,
                            y2=[self.row + box_fraction_line(self.fracs["BB"])(x) for x in base_xs],
                            color="w", zorder=3)

        else:
            # go through the ones on top first
            for source in self.fracs:
                if self.fracs[source] == 0:
                    continue

                if source in under:
                    self.fills[source] = ax.fill_between(x=xs, y1=base_ys,
                                    y2=base_ys+1,
                                    color="w", zorder=1)
                else:  # in under
                    self.fills[source] = ax.fill_between(x=xs, y1=base_ys,
                                    y2=[self.row + box_fraction_line(self.fracs[source])(x) for x in base_xs],
                                    color="w", zorder=2)