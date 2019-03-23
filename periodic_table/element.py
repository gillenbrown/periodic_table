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
    return lambda xs: xs + b


class Element(object):
    def __init__(self, number, symbol, ax,
                 frac_bb=0.0, frac_cr=0.0,
                 frac_snia=0.0, frac_snii=0.0, frac_agb=0.0,
                 frac_s=0.0, frac_r=0.0,
                 frac_decay=0.0, frac_unstable=0.0):

        self.number = number
        self.symbol = symbol
        self.ax = ax

        self.elt_name_txt = None

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


    def fill_elt(self):
        self.ax.set_facecolor("w")
        self.ax.patch.set_alpha(1.0)
        # add the borders to the box
        lw = 5
        for s in self.ax.spines.values():
            s.set_linewidth(lw)

    def label_elt(self, highlight_source):
        if self.elt_name_txt is not None:
            self.elt_name_txt.remove()
            del self.elt_name_txt


        fontsize = 30

        highlight_threshold = 0.5
        if highlight_source == "":
            highlight = False
        elif highlight_source == "low mass":
            highlight = (self.fracs["AGB"] > highlight_threshold
                         or self.fracs["S"] > highlight_threshold)
        else:
            highlight = self.fracs[highlight_source] > highlight_threshold

        if highlight:
            highlight_color = "white"
            txt = self.ax.add_text(x=0.5, y=0.65, text=self.symbol,
                                   coords="axes", fontsize=fontsize,
                                   color=highlight_color,
                                   horizontalalignment="center",
                                   verticalalignment="center")
            txt.set_path_effects([PathEffects.withStroke(linewidth=5,
                                                         foreground=bpl.almost_black)])
            self.elt_name_txt = txt

        else:
            txt = self.ax.add_text(x=0.5, y=0.65, text=self.symbol,
                                   coords="axes", fontsize=fontsize,
                                   horizontalalignment="center",
                                   verticalalignment="center")
            self.elt_name_txt = txt

        self.ax.add_text(x=0.5, y=0.25, text=self.number,
                         coords="axes", fontsize=0.6 * fontsize,
                         horizontalalignment="center",
                         verticalalignment="center")



    def box_fill(self, sources, axs_array, highlight_source=""):
        # first make the empty cells
        self.box_no_fill(axs_array, highlight_source)

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

        ax = self._get_ax(axs_array)
        xs = [-1, 2]
        if self.symbol == "He":
            # Fill the background with SNII, then half of it with AGB,
            # then the normal BB fill
            if "SNII" in sources:
                ax.fill_between(x=xs, y1=[-1, -1], y2=[2, 2],
                                color=self.colors["SNII"], zorder=0)
            if "AGB" in sources:
                agb_color = self.colors["AGB"]
            else:
                agb_color = "white"
            ax.fill_between(x=xs, y1=[-1, -1], y2=[2, -1],
                            color=agb_color, zorder=1)

            if "BB" in sources:
                bb_color = self.colors["BB"]
            else:
                bb_color = "white"
            ax.fill_between(x=xs, y1=[-1, -1],
                            y2=box_fraction_line(self.fracs["BB"])(xs),
                            color=bb_color, zorder=2)

        elif self.symbol == "Li":
            # Fill in the whole thing with CR
            # then cover the bottom (BB + AGB) fraction with BB
            # then cover the bottom BB fraction with BB
            if "CR" in sources:
                ax.fill_between(x=xs, y1=[-1, -1], y2=[2, 2],
                                color=self.colors["CR"], zorder=0)
            if "AGB" in sources:
                agb_color = self.colors["AGB"]
            else:
                agb_color = "white"
            total_agb_frac = self.fracs["BB"] + self.fracs["AGB"]
            ax.fill_between(x=xs, y1=[-1, -1],
                            y2=box_fraction_line(total_agb_frac)(xs),
                            color=agb_color, zorder=1)

            if "BB" in sources:
                bb_color = self.colors["BB"]
            else:
                bb_color = "white"
            ax.fill_between(x=xs, y1=[-1, -1],
                            y2=box_fraction_line(self.fracs["BB"])(xs),
                            color=bb_color, zorder=2)

        else:
            # go through the ones on top first
            for source in self.fracs:
                if self.fracs[source] == 0:
                    continue

                if source in under:
                    if source in sources:
                        ax.fill_between(x=xs, y1=[-1, -1], y2=[2, 2],
                                        color=self.colors[source], zorder=0)
                else:  # in under
                    if source in sources:
                        color = self.colors[source]
                    else:
                        color = "white"
                    ax.fill_between(x=xs, y1=[-1, -1],
                                    y2=box_fraction_line(self.fracs[source])(xs),
                                    color=color, zorder=1)