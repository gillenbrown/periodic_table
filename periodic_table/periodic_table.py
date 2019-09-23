import betterplotlib as bpl
import matplotlib.patheffects as PathEffects
import matplotlib.patches as patches

from .element import Element

bpl.presentation_style()

def _make_blank(fig, axs):
    # fig.patch.set_alpha(0.0)
    fig.set_facecolor("white")

    for ax in axs.flatten():
        ax.remove_labels("both")
        ax.equal_scale()
        for s in ax.spines.values():
            s.set_linewidth(0)
        ax.patch.set_alpha(0)
        ax.set_limits(0, 1, 0, 1)

def add_single_label(ax, x_idx, y_idx, text, color, highlight=False):
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
    ax.add_patch(rect)
    
    if highlight:
        highlight_color = "white" 
        txt = ax.add_text(x=x+dx_text, y=y+dy_text,
                          ha="center", va="center", zorder=3,
                          color=highlight_color,
                          text=text, fontsize=fontsize)
        txt.set_path_effects([PathEffects.withStroke(linewidth=4, foreground=bpl.almost_black)])
    else:        
        ax.add_text(x=x+dx_text, y=y+dy_text,
                    ha="center", va="center", zorder=3,
                    text=text, fontsize=fontsize)

def add_labels(fig, sources, highlight):
    ax_temp = fig.add_axes([0, 0, 1, 1], projection="bpl")
    ax_temp.remove_labels("both")
    for s in ax_temp.spines.values():
        s.set_linewidth(0)
    ax_temp.patch.set_alpha(0)
    ax_temp.set_limits(0, 20, 0, 12)
    
    if "BB" in sources:
        add_single_label(ax_temp, 0, 3, "Big Bang", elts[0].colors["BB"], "BB"==highlight)
    if "CR" in sources:
        add_single_label(ax_temp, 1, 3, "Cosmic Ray Spallation", elts[0].colors["CR"], "CR"==highlight)
    if "S" in sources or "AGB" in sources:
        highlight_flag = highlight == "AGB" or highlight == "S" or highlight == "low mass"
        add_single_label(ax_temp, 0, 2, "Low Mass Stars", elts[0].colors["S"], highlight_flag)
    if "SNII" in sources:
        add_single_label(ax_temp, 1, 2, "Exploding Massive Stars", elts[0].colors["SNII"], "SNII"==highlight)
    if "SNIa" in sources:
        add_single_label(ax_temp, 0, 1, "Exploding White Dwarfs", elts[0].colors["SNIa"], "SNIa"==highlight)
    if "R" in sources:
        add_single_label(ax_temp, 1, 1, "Merging Neutron Stars?", elts[0].colors["R"], "R"==highlight)
    if "decay" in sources:
        add_single_label(ax_temp, 0, 0, "Nuclear Decay", elts[0].colors["decay"], "decay"==highlight)
    if "unstable" in sources:
        add_single_label(ax_temp, 1, 0, "Not Naturally Occurring", elts[0].colors["unstable"], "unstable"==highlight)
        

    ax_temp.plot([3, 3.6666666, 3.666666, 4], [5.5, 5.5, 2.5, 2.5], lw=4, c=bpl.almost_black)
    ax_temp.plot([3, 3.3333333, 3.333333, 4], [4.5, 4.5, 1.5, 1.5], lw=4, c=bpl.almost_black)


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

def make_periodic_table(sources, highlight, savename=None, dpi=300):
    fig, axs = bpl.subplots(ncols=18+2, nrows=10+2, figsize=[20, 12],
                            gridspec_kw={"hspace":0, "wspace":0,
                                         "left": 0, "right": 1,
                                         "bottom": 0, "top": 1})

    _make_blank(fig, axs)

    for elt in elts:
        elt.box_fill(sources, axs, highlight)

    add_labels(fig, sources, highlight)

    if savename is not None:
        fig.savefig(savename, dpi=dpi)


#TODO: Finish cleaning up the Element class
#TODO: Make a Periodic Table class containing all the plotting stuff
#TODO: put the colors in the Periodic Table class, since that's where they
#      really belong
#TODO: Clean up the naming convention on things, especially the highlighting
#TODO: make the main plotting function cleaner, especially in how the
#      syntax for telling which sources to plot works
#TODO: maybe make AGB separate from S-process in the legend? C and N are unique
#TODO: instead of filling things in with white, have the code do the fill
#      above the 1-frac line. This only works for things with 2 sources, though
#TODO: have a check that all elements other than He and Li are only two sources
#      at most.
#TODO: add description to GitHub page
#TODO: allow user to customize names
#TODO: allow user to customize background color (none or white, at least)
#TODO: add multiple color schemes - pretty or visually distinct