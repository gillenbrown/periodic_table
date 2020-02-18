import betterplotlib as bpl
import matplotlib.patheffects as PathEffects
import matplotlib.patches as patches

from .element import Element, ColorChange

bpl.presentation_style()

elts = [Element(1,   "H",  1,  1,  frac_bb=1.0),
        Element(2,   "He", 1,  18, frac_bb=0.85, frac_snii=0.075, frac_agb=0.075),
        Element(3,   "Li", 2,  1,  frac_bb=0.1, frac_agb=0.7, frac_cr=0.2),
        Element(4,   "Be", 2,  2,  frac_cr=1.0),
        Element(5,   "B",  2,  13, frac_cr=1.0),
        Element(6,   "C",  2,  14, frac_agb=0.7, frac_snii=0.3),
        Element(7,   "N",  2,  15, frac_agb=0.7, frac_snii=0.3),
        Element(8,   "O",  2,  16, frac_snii=1.0),
        Element(9,   "F",  2,  17, frac_snii=1.0),
        Element(10,  "Ne", 2,  18, frac_snii=1.0),
        Element(11,  "Na", 3,  1,  frac_snii=1.0),
        Element(12,  "Mg", 3,  2,  frac_snii=1.0),
        Element(13,  "Al", 3,  13, frac_snii=1.0),
        Element(14,  "Si", 3,  14, frac_snii=0.65, frac_snia=0.35),
        Element(15,  "P",  3,  15, frac_snii=0.95, frac_snia=0.05),
        Element(16,  "S",  3,  16, frac_snii=0.55, frac_snia=0.45),
        Element(17,  "Cl", 3,  17, frac_snii=0.75, frac_snia=0.25),
        Element(18,  "Ar", 3,  18, frac_snii=0.55, frac_snia=0.45),
        Element(19,  "K",  4,  1,  frac_snii=0.75, frac_snia=0.25),
        Element(20,  "Ca", 4,  2,  frac_snii=0.49, frac_snia=0.51),
        Element(21,  "Sc", 4,  3,  frac_snii=0.70, frac_snia=0.30),
        Element(22,  "Ti", 4,  4,  frac_snii=0.35, frac_snia=0.65),
        Element(23,  "V",  4,  5,  frac_snii=0.25, frac_snia=0.75),
        Element(24,  "Cr", 4,  6,  frac_snii=0.20, frac_snia=0.80),
        Element(25,  "Mn", 4,  7,  frac_snii=0.15, frac_snia=0.85),
        Element(26,  "Fe", 4,  8,  frac_snii=0.35, frac_snia=0.65),
        Element(27,  "Co", 4,  9,  frac_snii=0.35, frac_snia=0.65),
        Element(28,  "Ni", 4,  10, frac_snii=0.35, frac_snia=0.65),
        Element(29,  "Cu", 4,  11, frac_snii=0.48, frac_snia=0.52),
        Element(30,  "Zn", 4,  12, frac_snii=0.48, frac_snia=0.52),
        Element(31,  "Ga", 4,  13, frac_snii=1.0),
        Element(32,  "Ge", 4,  14, frac_snii=1.0),
        Element(33,  "As", 4,  15, frac_snii=1.0),
        Element(34,  "Se", 4,  16, frac_snii=1.0),
        Element(35,  "Br", 4,  17, frac_snii=1.0),
        Element(36,  "Kr", 4,  18, frac_snii=1.0),
        Element(37,  "Rb", 5,  1,  frac_snii=1.0),
        Element(38,  "Sr", 5,  2,  frac_s=0.90, frac_snii=0.1),
        Element(39,  "Y",  5,  3,  frac_s=0.95, frac_snii=0.05),
        Element(40,  "Zr", 5,  4,  frac_s=0.85, frac_snii=0.15),
        Element(41,  "Nb", 5,  5,  frac_s=0.90, frac_r=0.10),
        Element(42,  "Mo", 5,  6,  frac_s=0.55, frac_r=0.45),
        Element(43,  "Tc", 5,  7,  frac_decay=1.0),
        Element(44,  "Ru", 5,  8,  frac_s=0.35, frac_r=0.65),
        Element(45,  "Rh", 5,  9,  frac_s=0.20, frac_r=0.80),
        Element(46,  "Pd", 5,  10, frac_s=0.45, frac_r=0.55),
        Element(47,  "Ag", 5,  11, frac_s=0.20, frac_r=0.80),
        Element(48,  "Cd", 5,  12, frac_s=0.55, frac_r=0.45),
        Element(49,  "In", 5,  13, frac_s=0.35, frac_r=0.65),
        Element(50,  "Sn", 5,  14, frac_s=0.70, frac_r=0.30),
        Element(51,  "Sb", 5,  15, frac_s=0.25, frac_r=0.75),
        Element(52,  "Te", 5,  16, frac_s=0.60, frac_r=0.40),
        Element(53,  "I",  5,  17, frac_s=0.05, frac_r=0.95),
        Element(54,  "Xe", 5,  18, frac_s=0.20, frac_r=0.80),
        Element(55,  "Cs", 6,  1,  frac_s=0.20, frac_r=0.80),
        Element(56,  "Ba", 6,  2,  frac_s=0.80, frac_r=0.20),
        Element(57,  "La", 9,  4,  frac_s=0.60, frac_r=0.40),
        Element(58,  "Ce", 9,  5,  frac_s=0.75, frac_r=0.25),
        Element(59,  "Pr", 9,  6,  frac_s=0.51, frac_r=0.49),
        Element(60,  "Nd", 9,  7,  frac_s=0.55, frac_r=0.45),
        Element(61,  "Pm", 9,  8,  frac_decay=1.0),
        Element(62,  "Sm", 9,  9,  frac_s=0.25, frac_r=0.75),
        Element(63,  "Eu", 9,  10, frac_s=0.05, frac_r=0.95),
        Element(64,  "Gd", 9,  11, frac_s=0.15, frac_r=0.85),
        Element(65,  "Tb", 9,  12, frac_s=0.10, frac_r=0.90),
        Element(66,  "Dy", 9,  13, frac_s=0.15, frac_r=0.85),
        Element(67,  "Ho", 9,  14, frac_s=0.10, frac_r=0.90),
        Element(68,  "Er", 9,  15, frac_s=0.18, frac_r=0.82),
        Element(69,  "Tm", 9,  16, frac_s=0.18, frac_r=0.82),
        Element(70,  "Yb", 9,  17, frac_s=0.30, frac_r=0.70),
        Element(71,  "Lu", 9,  18, frac_s=0.20, frac_r=0.80),
        Element(72,  "Hf", 6,  4,  frac_s=0.55, frac_r=0.45),
        Element(73,  "Ta", 6,  5,  frac_s=0.40, frac_r=0.60),
        Element(74,  "W",  6,  6,  frac_s=0.55, frac_r=0.45),
        Element(75,  "Re", 6,  7,  frac_s=0.10, frac_r=0.90),
        Element(76,  "Os", 6,  8,  frac_s=0.15, frac_r=0.85),
        Element(77,  "Ir", 6,  9,  frac_s=0.02, frac_r=0.98),
        Element(78,  "Pt", 6,  10, frac_s=0.05, frac_r=0.95),
        Element(79,  "Au", 6,  11, frac_s=0.10, frac_r=0.90),
        Element(80,  "Hg", 6,  12, frac_s=0.60, frac_r=0.40),
        Element(81,  "Tl", 6,  13, frac_s=0.70, frac_r=0.30),
        Element(82,  "Pb", 6,  14, frac_s=0.85, frac_r=0.15),
        Element(83,  "Bi", 6,  15, frac_s=0.35, frac_r=0.65),
        Element(84,  "Po", 6,  16, frac_decay=1.0),
        Element(85,  "At", 6,  17, frac_decay=1.0),
        Element(86,  "Rn", 6,  18, frac_decay=1.0),
        Element(87,  "Fr", 7,  1,  frac_decay=1.0),
        Element(88,  "Ra", 7,  2,  frac_decay=1.0),
        Element(89,  "Ac", 10, 4,  frac_decay=1.0),
        Element(90,  "Th", 10, 5,  frac_r=1.0),
        Element(91,  "Pa", 10, 6,  frac_decay=1.0),
        Element(92,  "U",  10, 7,  frac_r=1.0),
        Element(93,  "Np", 10, 8,  frac_decay=1.0),
        Element(94,  "Pu", 10, 9,  frac_decay=1.0),
        Element(95,  "Am", 10, 10, frac_unstable=1.0),
        Element(96,  "Cm", 10, 11, frac_unstable=1.0),
        Element(97,  "Bk", 10, 12, frac_unstable=1.0),
        Element(98,  "Cf", 10, 13, frac_unstable=1.0),
        Element(99,  "Es", 10, 14, frac_unstable=1.0),
        Element(100, "Fm", 10, 15, frac_unstable=1.0),
        Element(101, "Md", 10, 16, frac_unstable=1.0),
        Element(102, "No", 10, 17, frac_unstable=1.0),
        Element(103, "Lr", 10, 18, frac_unstable=1.0),
        Element(104, "Rf", 7,  4,  frac_unstable=1.0),
        Element(105, "Db", 7,  5,  frac_unstable=1.0),
        Element(106, "Sg", 7,  6,  frac_unstable=1.0),
        Element(107, "Bh", 7,  7,  frac_unstable=1.0),
        Element(108, "Hs", 7,  8,  frac_unstable=1.0),
        Element(109, "Mt", 7,  9,  frac_unstable=1.0),
        Element(110, "Ds", 7,  10, frac_unstable=1.0),
        Element(111, "Rg", 7,  11, frac_unstable=1.0),
        Element(112, "Cn", 7,  12, frac_unstable=1.0),
        Element(113, "Nh", 7,  13, frac_unstable=1.0),
        Element(114, "Fl", 7,  14, frac_unstable=1.0),
        Element(115, "Mc", 7,  15, frac_unstable=1.0),
        Element(116, "Lv", 7,  16, frac_unstable=1.0),
        Element(117, "Ts", 7,  17, frac_unstable=1.0),
        Element(118, "Og", 7,  18, frac_unstable=1.0)
       ]

class SourceLabels(object):
    def __init__(self, ax, x_idx, y_idx, text, color):

        self.shown = False
        self.highlight = False
        self.ax = ax

        # idx starts from bottom left
        fontsize = 27

        spacing = 0.25

        # X space goes from 3 to 13.
        x_0 = 3
        x_1 = 13
        width_rect = ((x_1 - x_0) - 3 * spacing) / 2.0

        # Y space goes from 8 to 11
        y_0 = 8
        y_1 = 11
        height_rect = ((y_1 - y_0) - 4 * spacing) / 4.0

        dx_text = width_rect / 2.0
        dy_text = height_rect / 2.0

        x = x_0 + spacing * (x_idx + 1) + width_rect * x_idx
        y = y_0 + spacing * (y_idx + 1) + height_rect * y_idx

        if x_idx == 2:  # Make manmade go all the way over
            width_rect = 5 - spacing
            # This has to be done now so the position is calculated
            # properly previously

        rect = patches.Rectangle((x, y), width_rect, height_rect,
                                 fill=True, facecolor=color,
                                 linewidth=1, edgecolor=bpl.almost_black,
                                 alpha=1.0, zorder=2)
        self.ax.add_patch(rect)
        self.box = ColorChange(rect)

        highlight_color = "white"
        txt_hl = self.ax.add_text(x=x + dx_text, y=y + dy_text,
                                       ha="center", va="center", zorder=3,
                                       color=highlight_color,
                                       text=text, fontsize=fontsize)
        txt_hl.set_path_effects([PathEffects.withStroke(linewidth=4,
                                                     foreground=bpl.almost_black)])
        self.text_hl = ColorChange(txt_hl)
        self.text_hl.hide()

        txt = self.ax.add_text(x=x + dx_text, y=y + dy_text,
                                    ha="center", va="center", zorder=3,
                                    text=text, fontsize=fontsize)
        self.text = ColorChange(txt)

        self.unshow()

    def show(self):
        self.shown = True
        self.box.unhide()
        if self.highlight:
            self.highlight_on()
        else:
            self.highlight_off()

    def unshow(self):
        self.shown = False
        self.box.hide()
        self.text.hide()
        self.text_hl.hide()

    def highlight_on(self):
        self.highlight = True
        if self.shown:
            self.text_hl.unhide()
            self.text.hide()

    def highlight_off(self):
        self.highlight = False
        if self.shown:
            self.text_hl.hide()
            self.text.unhide()

    def fade(self):
        self.text_hl.fade()
        self.text.fade()
        self.box.fade()

    def unfade(self):
        self.text_hl.unfade()
        self.text.unfade()
        self.box.unfade()

class PeriodicTable(object):
    def __init__(self):
        self.__elts = elts
        fig, ax = bpl.subplots(figsize=[20, 12], tight_layout=False,
                               gridspec_kw={"hspace":0, "wspace":0,
                                            "left": 0, "right": 1,
                                            "bottom": 0, "top": 1})

        self._fig = fig
        self._ax = ax

        self._fig.patch.set_alpha(0.0)
        self._fig.set_facecolor("white")

        self._ax.remove_labels("both")
        self._ax.equal_scale()
        for s in self._ax.spines.values():
            s.set_linewidth(0)
        self._ax.patch.set_alpha(0)
        self._ax.set_limits(0, 20, 0, 12)

        # add the lines connecting the Lanthanides and Actinides
        l1 = self._ax.plot([3, 3.6666666, 3.666666, 4], [5.5, 5.5, 2.5, 2.5], lw=4,
                          c=bpl.almost_black, zorder=-1000)
        l2 = self._ax.plot([3, 3.3333333, 3.333333, 4], [4.5, 4.5, 1.5, 1.5], lw=4,
                          c=bpl.almost_black, zorder=-1000)
        self._connector_lines = [ColorChange(segment) for segment in l1 + l2]

        # add the labels
        self._labels = dict()
        self._labels["bb"] = SourceLabels(self._ax, 0, 3, "Big Bang", elts[0].colors["bb"])
        self._labels["cr"] = SourceLabels(self._ax, 1, 3, "Cosmic Ray Spallation", elts[0].colors["cr"])
        self._labels["s"] = SourceLabels(self._ax, 0, 2, "Low Mass Stars", elts[0].colors["s"])
        self._labels["agb"] = self._labels["s"]
        self._labels["snii"] = SourceLabels(self._ax, 1, 2, "Exploding Massive Stars", elts[0].colors["snii"])
        self._labels["snia"] = SourceLabels(self._ax, 0, 1, "Exploding White Dwarfs", elts[0].colors["snia"])
        self._labels["r"] = SourceLabels(self._ax, 1, 1, "Merging Neutron Stars?", elts[0].colors["r"])
        self._labels["decay"] = SourceLabels(self._ax, 0, 0, "Nuclear Decay", elts[0].colors["decay"])
        self._labels["unstable"] = SourceLabels(self._ax, 1, 0, "Not Naturally Occurring", elts[0].colors["unstable"])

        for elt in elts:
            elt.setup(self._ax)

    def highlight_source(self, source):
        for label in self._labels:
            if label == source.lower():
                self._labels[label].highlight_on()
            else:
                self._labels[label].highlight_off()

        for elt in elts:
            elt.highlight_source(source.lower())

    def unhighlight_all_sources(self):
        for label in self._labels:
            self._labels[label].highlight_off()

        for elt in elts:
            elt.highlight_source(None)

    def show_source(self, *args):
        sources = [item.lower() for item in args]
        for source in sources:
            if not source in self._labels:
                raise ValueError("Source {} not correct.".format(source))
            self._labels[source].show()

        for elt in elts:
            for source in sources:
                elt.show_source(source)

    def unshow_source(self, *args):
        sources = [item.lower() for item in args]
        for source in sources:
            if not source in self._labels:
                raise ValueError("Source {} not correct.".format(source))
            self._labels[source].unshow()

        for elt in elts:
            for source in sources:
                elt.unshow_source(source)

    def show_all_sources(self):
        self.show_source("bb", "cr", "s", "agb", "snii", "snia", "r", "decay",
                         "unstable")

    def unshow_all_sources(self):
        self.unshow_source("bb", "cr", "s", "agb", "snii", "snia", "r", "decay",
                           "unstable")

    def isolate_elt(self, *args, keep_labels=True):

        for l in self._connector_lines:
            l.fade()

        if keep_labels:
            for label in self._labels:
                fade_this = True
                for elt in elts:
                    if elt.symbol in args and elt.highlight_bool(label):
                        fade_this = False
                if fade_this:
                    self._labels[label].fade()
                else:
                    self._labels[label].unfade()

        for elt in elts:
            if elt.symbol not in args:
                elt.fade()
            else:
                elt.unfade()

    def unisolate_all_elts(self):
        for l in self._connector_lines:
            l.unfade()

        for label in self._labels.values():
            label.unfade()

        for elt in elts:
            elt.unfade()

    def save(self, savename):
        self._fig.savefig(savename)

    def get_figure(self):
        # for use in notebooks
        return self._fig


#TODO: Finish cleaning up the Element class
#TODO: Make a Periodic Table class containing all the plotting stuff
#TODO: put the colors in the Periodic Table class, since that's where they
#      really belong
#TODO: Clean up the naming convention on things, especially the highlighting
#TODO: maybe make AGB separate from S-process in the legend? C and N are unique
#TODO: have a check that all elements other than He and Li are only two sources
#      at most.
#TODO: add description to GitHub page
#TODO: allow user to customize names
#TODO: allow user to customize background color (none or white, at least)
#TODO: add multiple color schemes - pretty or visually distinct
#TODO: redo fractions! Removing the lines on the fill-between messed up the
#      fractions
#TODO: add alternate names for the sources
#TODO: make sure the outer border for the source names gets faded when needed