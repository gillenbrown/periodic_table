import betterplotlib as bpl
import matplotlib.patheffects as PathEffects
import matplotlib.patches as patches

from .element import Element, ColorChange

bpl.set_style(font="Avenir", fontweight="medium")

# Element fractions come from Jennifer Johnson
# https://science.sciencemag.org/content/363/6426/474
# specifically table S1
# https://science.sciencemag.org/content/sci/suppl/2019/01/30/363.6426.474.DC1/aau9540-Johnson-SM.pdf
elts = [
    Element(1, "H", 1, 1, frac_bb=1.00),
    Element(2, "He", 1, 18, frac_bb=0.90, frac_snii=0.05, frac_agb=0.05),
    Element(3, "Li", 2, 1, frac_bb=0.25, frac_agb=0.6, frac_cr=0.15),
    Element(4, "Be", 2, 2, frac_cr=1.00),
    Element(5, "B", 2, 13, frac_cr=1.00),
    Element(6, "C", 2, 14, frac_agb=0.75, frac_snii=0.25),
    Element(7, "N", 2, 15, frac_agb=0.75, frac_snii=0.25),
    Element(8, "O", 2, 16, frac_snii=1.0),
    Element(9, "F", 2, 17, frac_snii=1.0),
    Element(10, "Ne", 2, 18, frac_snii=1.0),
    Element(11, "Na", 3, 1, frac_snii=1.0),
    Element(12, "Mg", 3, 2, frac_snii=0.99, frac_snia=0.01),
    Element(13, "Al", 3, 13, frac_snii=1.0),
    Element(14, "Si", 3, 14, frac_snii=0.70, frac_snia=0.30),
    Element(15, "P", 3, 15, frac_snii=0.97, frac_snia=0.03),
    Element(16, "S", 3, 16, frac_snii=0.57, frac_snia=0.43),
    Element(17, "Cl", 3, 17, frac_snii=0.83, frac_snia=0.17),
    Element(18, "Ar", 3, 18, frac_snii=0.56, frac_snia=0.44),
    Element(19, "K", 4, 1, frac_snii=0.81, frac_snia=0.19),
    Element(20, "Ca", 4, 2, frac_snii=0.50, frac_snia=0.50),
    Element(21, "Sc", 4, 3, frac_snii=0.81, frac_snia=0.19),
    Element(22, "Ti", 4, 4, frac_snii=0.34, frac_snia=0.66),
    Element(23, "V", 4, 5, frac_snii=0.26, frac_snia=0.74),
    Element(24, "Cr", 4, 6, frac_snii=0.24, frac_snia=0.76),
    Element(25, "Mn", 4, 7, frac_snii=0.18, frac_snia=0.82),
    Element(26, "Fe", 4, 8, frac_snii=0.32, frac_snia=0.68),
    Element(27, "Co", 4, 9, frac_snii=0.32, frac_snia=0.68),
    Element(28, "Ni", 4, 10, frac_snii=0.29, frac_snia=0.71),
    Element(29, "Cu", 4, 11, frac_snii=0.42, frac_snia=0.58),
    Element(30, "Zn", 4, 12, frac_snii=0.44, frac_snia=0.56),
    Element(31, "Ga", 4, 13, frac_snii=1.0),
    Element(32, "Ge", 4, 14, frac_snii=1.0),
    Element(33, "As", 4, 15, frac_snii=1.0),
    Element(34, "Se", 4, 16, frac_snii=1.0),
    Element(35, "Br", 4, 17, frac_snii=1.0),
    Element(36, "Kr", 4, 18, frac_snii=1.0),
    Element(37, "Rb", 5, 1, frac_snii=1.0),
    Element(38, "Sr", 5, 2, frac_s=0.87, frac_snii=0.13),
    Element(39, "Y", 5, 3, frac_s=0.92, frac_snii=0.08),
    Element(40, "Zr", 5, 4, frac_s=0.84, frac_snii=0.16),
    Element(41, "Nb", 5, 5, frac_s=0.85, frac_r=0.15),
    Element(42, "Mo", 5, 6, frac_s=0.62, frac_r=0.38),
    Element(43, "Tc", 5, 7, frac_unstable=1.0),
    Element(44, "Ru", 5, 8, frac_s=0.33, frac_r=0.67),
    Element(45, "Rh", 5, 9, frac_s=0.14, frac_r=0.86),
    Element(46, "Pd", 5, 10, frac_s=0.46, frac_r=0.54),
    Element(47, "Ag", 5, 11, frac_s=0.20, frac_r=0.80),
    Element(48, "Cd", 5, 12, frac_s=0.53, frac_r=0.47),
    Element(49, "In", 5, 13, frac_s=0.36, frac_r=0.64),
    Element(50, "Sn", 5, 14, frac_s=0.70, frac_r=0.30),
    Element(51, "Sb", 5, 15, frac_s=0.25, frac_r=0.75),
    Element(52, "Te", 5, 16, frac_s=0.58, frac_r=0.42),
    Element(53, "I", 5, 17, frac_s=0.05, frac_r=0.95),
    Element(54, "Xe", 5, 18, frac_s=0.17, frac_r=0.83),
    Element(55, "Cs", 6, 1, frac_s=0.15, frac_r=0.85),
    Element(56, "Ba", 6, 2, frac_s=0.81, frac_r=0.19),
    Element(57, "La", 9, 4, frac_s=0.62, frac_r=0.38),
    Element(58, "Ce", 9, 5, frac_s=0.76, frac_r=0.24),
    Element(59, "Pr", 9, 6, frac_s=0.49, frac_r=0.51),
    Element(60, "Nd", 9, 7, frac_s=0.60, frac_r=0.40),
    Element(61, "Pm", 9, 8, frac_unstable=1.0),
    Element(62, "Sm", 9, 9, frac_s=0.30, frac_r=0.70),
    Element(63, "Eu", 9, 10, frac_s=0.06, frac_r=0.94),
    Element(64, "Gd", 9, 11, frac_s=0.15, frac_r=0.85),
    Element(65, "Tb", 9, 12, frac_s=0.07, frac_r=0.93),
    Element(66, "Dy", 9, 13, frac_s=0.15, frac_r=0.85),
    Element(67, "Ho", 9, 14, frac_s=0.08, frac_r=0.92),
    Element(68, "Er", 9, 15, frac_s=0.17, frac_r=0.83),
    Element(69, "Tm", 9, 16, frac_s=0.13, frac_r=0.87),
    Element(70, "Yb", 9, 17, frac_s=0.33, frac_r=0.67),
    Element(71, "Lu", 9, 18, frac_s=0.20, frac_r=0.80),
    Element(72, "Hf", 6, 4, frac_s=0.56, frac_r=0.44),
    Element(73, "Ta", 6, 5, frac_s=0.41, frac_r=0.59),
    Element(74, "W", 6, 6, frac_s=0.56, frac_r=0.44),
    Element(75, "Re", 6, 7, frac_s=0.09, frac_r=0.91),
    Element(76, "Os", 6, 8, frac_s=0.09, frac_r=0.91),
    Element(77, "Ir", 6, 9, frac_s=0.01, frac_r=0.99),
    Element(78, "Pt", 6, 10, frac_s=0.05, frac_r=0.95),
    Element(79, "Au", 6, 11, frac_s=0.06, frac_r=0.94),
    Element(80, "Hg", 6, 12, frac_s=0.61, frac_r=0.39),
    Element(81, "Tl", 6, 13, frac_s=0.76, frac_r=0.24),
    Element(82, "Pb", 6, 14, frac_s=0.87, frac_r=0.13),
    Element(83, "Bi", 6, 15, frac_s=0.26, frac_r=0.74),
    Element(84, "Po", 6, 16, frac_unstable=1.0),
    Element(85, "At", 6, 17, frac_unstable=1.0),
    Element(86, "Rn", 6, 18, frac_unstable=1.0),
    Element(87, "Fr", 7, 1, frac_unstable=1.0),
    Element(88, "Ra", 7, 2, frac_unstable=1.0),
    Element(89, "Ac", 10, 4, frac_unstable=1.0),
    Element(90, "Th", 10, 5, frac_r=1.0),
    Element(91, "Pa", 10, 6, frac_unstable=1.0),
    Element(92, "U", 10, 7, frac_r=1.0),
    Element(93, "Np", 10, 8, frac_unstable=1.0),
    Element(94, "Pu", 10, 9, frac_r=1.0),
    Element(95, "Am", 10, 10, frac_unstable=1.0),
    Element(96, "Cm", 10, 11, frac_unstable=1.0),
    Element(97, "Bk", 10, 12, frac_unstable=1.0),
    Element(98, "Cf", 10, 13, frac_unstable=1.0),
    Element(99, "Es", 10, 14, frac_unstable=1.0),
    Element(100, "Fm", 10, 15, frac_unstable=1.0),
    Element(101, "Md", 10, 16, frac_unstable=1.0),
    Element(102, "No", 10, 17, frac_unstable=1.0),
    Element(103, "Lr", 10, 18, frac_unstable=1.0),
    Element(104, "Rf", 7, 4, frac_unstable=1.0),
    Element(105, "Db", 7, 5, frac_unstable=1.0),
    Element(106, "Sg", 7, 6, frac_unstable=1.0),
    Element(107, "Bh", 7, 7, frac_unstable=1.0),
    Element(108, "Hs", 7, 8, frac_unstable=1.0),
    Element(109, "Mt", 7, 9, frac_unstable=1.0),
    Element(110, "Ds", 7, 10, frac_unstable=1.0),
    Element(111, "Rg", 7, 11, frac_unstable=1.0),
    Element(112, "Cn", 7, 12, frac_unstable=1.0),
    Element(113, "Nh", 7, 13, frac_unstable=1.0),
    Element(114, "Fl", 7, 14, frac_unstable=1.0),
    Element(115, "Mc", 7, 15, frac_unstable=1.0),
    Element(116, "Lv", 7, 16, frac_unstable=1.0),
    Element(117, "Ts", 7, 17, frac_unstable=1.0),
    Element(118, "Og", 7, 18, frac_unstable=1.0),
]


class SourceLabels(object):
    """
    Class holding the labels that go at the top of the table.
    """

    def __init__(self, ax, x_idx, y_idx, text, color):
        """
        Initialize these labels

        :param ax: Axis where these labels willbe placed
        :param x_idx: The x index in the grid of labels. This is not the element
                      position, this is the index among the labls.
        :param y_idx: The y index in the grid of labels. This is not the element
                      position, this is the index among the labls.
        :param text: What text to put in this box.
        :param color: What color to make this box.
        """
        # initialize the attributes about the state of this label.
        self.shown = False
        self.highlight = False
        self.ax = ax

        fontsize = 27

        # Then figure out where to put the label. We do some math based on the available
        # spacing, then figure out where to put this one
        # idx starts from bottom left
        spacing = 0.25
        # The X space for these labels goes from 3 to 13.
        x_0 = 3
        x_1 = 13
        # we need 3 spaces: left, right, center
        width_rect = ((x_1 - x_0) - 3 * spacing) / 2.0

        # Y space goes from 8 to 11
        y_0 = 8
        y_1 = 11
        # we need 4 spaces: bottom, inbetween the 3 labels. No space at top, it aligns
        # with the top of the figure.
        height_rect = ((y_1 - y_0) - 4 * spacing) / 4.0

        # The text needs to be offset by half the box size
        dx_text = width_rect / 2.0
        dy_text = height_rect / 2.0

        # Then figure out where the lower left corner of the box is
        x = x_0 + spacing * (x_idx + 1) + width_rect * x_idx
        y = y_0 + spacing * (y_idx + 1) + height_rect * y_idx

        # Then we can add the box to the plot. Note that we have to make the edge line
        # separately, since the fade functions only handle facecolor of the box.
        rect = patches.Rectangle(
            (x, y),
            width_rect,
            height_rect,
            fill=True,
            facecolor=color,
            linewidth=0,
            alpha=1.0,
            zorder=2,
        )
        self.ax.add_patch(rect)

        lines = ax.plot(
            [x, x, x + width_rect, x + width_rect, x],
            [y, y + height_rect, y + height_rect, y, y],
            lw=1,
            color=bpl.almost_black,
        )

        # store these as color change objects
        self.box = ColorChange(rect)
        self.box_lines = [ColorChange(l) for l in lines]

        # Then add the text for the highlight
        highlight_color = "white"
        txt_hl = self.ax.add_text(
            x=x + dx_text,
            y=y + dy_text,
            ha="center",
            va="center",
            zorder=3,
            color=highlight_color,
            text=text,
            fontsize=fontsize,
        )
        txt_hl.set_path_effects(
            [PathEffects.withStroke(linewidth=4, foreground=bpl.almost_black)]
        )
        # Setting the ColorChange for the highted text is tricky. We should use both
        # the main object (although I don't think it will matter becase it is white),
        # but also the path effect that is highlighted.
        self.text_hl_stroke = ColorChange(txt_hl._path_effects[0])
        self.text_hl = ColorChange(txt_hl)
        # hide it initially. This hides the stroke too.
        self.text_hl.hide()

        # then add the regular text.
        txt = self.ax.add_text(
            x=x + dx_text,
            y=y + dy_text,
            ha="center",
            va="center",
            zorder=3,
            text=text,
            fontsize=fontsize,
        )
        self.text = ColorChange(txt)

        # The labels are initially hidden
        self.unshow()

    def show(self):
        """
        Show this label on the axis.

        :return: None
        """
        self.shown = True
        self.box.unhide()
        for line in self.box_lines:
            line.unhide()

        if self.highlight:
            self.highlight_on()
        else:
            self.highlight_off()

    def unshow(self):
        """
        Unshow this label on the axis

        :return: None
        """
        self.shown = False
        self.text.hide()
        self.text_hl.hide()
        self.box.hide()
        for line in self.box_lines:
            line.hide()

    def highlight_on(self):
        """
        Highlight the text on this label

        :return: None
        """
        self.highlight = True
        if self.shown:  # only highlight the text if the label is already shown.
            self.text_hl.unhide()
            self.text.hide()

    def highlight_off(self):
        """
        Turn off the highlighting on this label

        :return: None
        """
        self.highlight = False
        if self.shown:  # only unhighlight the text if the label is already shown.
            self.text_hl.hide()
            self.text.unhide()

    def fade(self, to_print=False):
        """
        Fade all attributes on this label

        :return: None
        """
        self.text_hl.fade()
        self.text_hl_stroke.fade()
        self.text.fade()
        self.box.fade()
        for line in self.box_lines:
            line.fade()

    def unfade(self):
        """
        Unfade all attributes on this label

        :return: None
        """
        self.text_hl.unfade()
        self.text_hl_stroke.unfade()
        self.text.unfade()
        self.box.unfade()
        for line in self.box_lines:
            line.unfade()


class PeriodicTable(object):
    def __init__(
        self,
        label_bb="Big Bang",
        label_cr="Cosmic Ray Spallation",
        label_agb="Low Mass Stars",
        label_snii="Exploding Massive Stars",
        label_snia="Exploding White Dwarfs",
        label_r="Merging Neutron Stars?",
        label_unstable="Not Naturally Occurring",
        color_bb="#D7E5CC",
        color_cr="#C3DDFA",
        color_snia="#fe9443",
        color_snii="#FEE844",
        color_r="#AFBF75",
        color_agb="#73A0CC",
        color_unstable="#CCCCCC",
    ):
        """
        Set up the periodic table figure and axes.
        """
        # set the element color scheme. This attribute is shared by all members of the
        # element class, so it will be applied to all.
        elts[0].set_scheme(
            color_bb,
            color_cr,
            color_snia,
            color_snii,
            color_r,
            color_agb,
            color_unstable,
        )

        # The periodic table layout has 18 columns and 9 rows (counting Lanthanides and
        # Actinides separately). I'll add spacing columns on the left and right, top and
        # bottom, plus between the Lanthanides and Actinides and the rest of the table.
        # we make the figure 1 inch per square. There will be no space on the outside.
        fig, ax = bpl.subplots(
            figsize=[20, 12],
            tight_layout=False,
            gridspec_kw={
                "hspace": 0,
                "wspace": 0,
                "left": 0,
                "right": 1,
                "bottom": 0,
                "top": 1,
            },
        )

        self._fig = fig
        self._ax = ax

        # make the background of the figure transparent
        self._fig.patch.set_alpha(0.0)
        self._fig.set_facecolor("white")

        # remove all the labels from the axes
        self._ax.remove_labels("both")
        # make the limits match the figure size, then use equal scale to make sure the
        # element squares are actually square
        self._ax.set_limits(0, 20, 0, 12)
        self._ax.equal_scale()
        # get rid of the spines on the outside
        for s in self._ax.spines.values():
            s.set_linewidth(0)
        # and make the overall axis transparent.
        self._ax.patch.set_alpha(0)

        # add the lines connecting the Lanthanides and Actinides
        l1 = self._ax.plot(
            [3, 3.6666666, 3.666666, 4],
            [5.5, 5.5, 2.5, 2.5],
            lw=4,
            c=bpl.almost_black,
            zorder=-1000,
        )
        l2 = self._ax.plot(
            [3, 3.3333333, 3.333333, 4],
            [4.5, 4.5, 1.5, 1.5],
            lw=4,
            c=bpl.almost_black,
            zorder=-1000,
        )
        self._connector_lines = [ColorChange(segment) for segment in l1 + l2]

        # add the labels
        self._labels = dict()
        self._labels["bb"] = SourceLabels(self._ax, 0, 3, label_bb, color_bb)
        self._labels["cr"] = SourceLabels(self._ax, 1, 3, label_cr, color_cr)
        self._labels["s"] = SourceLabels(self._ax, 0, 2, label_agb, color_agb)
        self._labels["agb"] = self._labels["s"]
        self._labels["snii"] = SourceLabels(self._ax, 1, 2, label_snii, color_snii)
        self._labels["snia"] = SourceLabels(self._ax, 0, 1, label_snia, color_snia)
        self._labels["r"] = SourceLabels(self._ax, 1, 1, label_r, color_r)
        self._labels["unstable"] = SourceLabels(
            self._ax, 0, 0, label_unstable, color_unstable
        )

        # have a dictionary showing which sources are visible
        self.sources_on = {label: False for label in self._labels}

        # Then add each of the elements
        for elt in elts:
            elt.setup(self._ax)

    def highlight_source(self, source):
        """
        Highlight this source throughout the table.

        This will highlight the elements that are primarily from this source, as well
        as the label at the top

        :param source: Source to highlight
        :return: None
        """
        # Check all the labels
        for label in self._labels:
            # low mass is a separate thing
            if source == "low mass":
                label_source = "agb"
            else:
                label_source = source
            # then actually do the checking
            if label == label_source.lower():
                self._labels[label].highlight_on()
            else:
                self._labels[label].highlight_off()

        # Then the elements
        for elt in elts:
            elt.highlight_source(source.lower())

    def unhighlight_all_sources(self):
        """
        Get rid of all highlighting on the table.

        :return: None
        """
        # go through the labels.
        for label in self._labels:
            self._labels[label].highlight_off()
        # then the elements
        for elt in elts:
            elt.highlight_source(None)

    def show_source(self, *args):
        """
        Add the element fills and labels for a given source

        :param args: As many sources as you want to add.
        :return: None
        """
        sources = [item.lower() for item in args]
        # there is a separate low mass label that is both AGB and S
        if "low mass" in sources:
            sources.append("s")
            sources.append("agb")
            sources.remove("low mass")

        # then add these to our dictionary. This also does the error checking
        for source in sources:
            if source not in self.sources_on:
                raise ValueError("Source {} not correct.".format(source))
            self.sources_on[source] = True

        # add the labels
        for source in sources:
            self._labels[source].show()

        # Then show all the elements
        for elt in elts:
            for source in sources:
                elt.show_source(source)

    def unshow_source(self, *args):
        """
        Hide the elemental fills and labels for a given source

        :param args: As many sources as you want to unshow
        :return: None
        """
        sources = [item.lower() for item in args]
        # there is a separate low mass label that is both AGB and S
        if "low mass" in sources:
            sources.append("s")
            sources.append("agb")
            sources.remove("low mass")

        # then add these to our dictionary. This also does the error checking
        for source in sources:
            if source not in self.sources_on:
                raise ValueError("Source {} not correct.".format(source))
            self.sources_on[source] = False

        # go through the labels. We have to be careful about AGB and S process. We want
        # the label if either of those is present
        for source in sources:
            if source in ["agb", "s"]:
                if self.sources_on["agb"] is False and self.sources_on["s"] is False:
                    self._labels[source].unshow()
            # otherwise we just remove it
            else:
                self._labels[source].unshow()

        # then do the elements
        for elt in elts:
            for source in sources:
                elt.unshow_source(source)

    def show_all_sources(self):
        """
        Show all sources on the table.

        This is just a wrapper around `show_source`

        :return: None
        """
        self.show_source("bb", "cr", "s", "agb", "snii", "snia", "r", "unstable")

    def unshow_all_sources(self):
        """
        Show all sources on the table.

        This is just a wrapper around `unshow_source`

        :return: None
        """
        self.unshow_source("bb", "cr", "s", "agb", "snii", "snia", "r", "unstable")

    def isolate_elt(self, *args):
        """
        Isolate a given element by fading all other elements.

        :param args: As many elements as you want to isolate.
        :return: None
        """
        # fade the Lanthanide and Actinide lines
        for l in self._connector_lines:
            l.fade()

        # fade all labels
        for label in self._labels:
            self._labels[label].fade()

        # then fade the elements that are not listed
        for elt in elts:
            if elt.symbol not in args:
                elt.fade()
            else:
                elt.unfade()

    def isolate_elt_label(self, *args):
        """
        Isolate a given element by fading all other elements. This also fades all the
        labels other than the ones that are primary in the elements isolated.

        :param args: As many elements as you want to isolate.
        :return: None
        """
        # first use the fade_elt to fade the elements and all labels, then unfade
        # the label of interest
        self.isolate_elt(*args)

        for label in self._labels:
            for elt in elts:
                if elt.symbol in args and elt.highlight_bool(label):
                    self._labels[label].unfade()

    def unisolate_all_elts(self):
        """
        Unfade all elements and labels

        :return: None
        """
        # Lanthanide and Actinide lines
        for l in self._connector_lines:
            l.unfade()

        # source labels
        for label in self._labels.values():
            label.unfade()

        # elements
        for elt in elts:
            elt.unfade()

    def save(self, savename):
        """
        Save the plot

        :param savename: Path or filename to save the plot to
        :return: None
        """
        self._fig.savefig(savename)

    def get_figure(self):
        """
        Returns the figure, so it can be shown in a Jupyter notebook

        Not much use for this otherwise.

        :return: Figure object
        """
        return self._fig
