import os

import imageio
import numpy as np

from periodic_table import PeriodicTable

this_dir = os.path.realpath(os.path.split(__file__)[0])
baseline_im_dir = this_dir + os.sep + "baseline_images" + os.sep
new_im_dir = this_dir + os.sep + "temporary_images" + os.sep

def image_similarity(im_1_path, im_2_path):
    """
    Compare two images to see if they are identical.

    :param im_1_path: Path of the first image. Should be a png.
    :type im_1_path: str
    :param im_2_path: Path of the second image. Should be a png.
    :type im_2_path: str
    :return: True if the images are identical, false if they are not.
    :rtype bool:
    """
    im_1 = imageio.imread(im_1_path)
    im_2 = imageio.imread(im_2_path)

    return abs(np.sum(im_1 - im_2)) < 1


def image_similarity_full(fig, image_name):
    new_img = new_im_dir + image_name
    baseline_img = baseline_im_dir + image_name

    fig.savefig(new_im_dir + image_name)

    try:
        matched = image_similarity(new_img, baseline_img)
    except OSError:
        raise IOError("Baseline image does not exist.")
    if matched:
        os.remove(new_img)
    return matched

# ------------------------------------------------------------------------------
#
# Testing
#
# ------------------------------------------------------------------------------
def test_blank():
    pt = PeriodicTable()
    assert image_similarity_full(pt.fig, "blank.png")

def test_bb():
    pt = PeriodicTable()
    pt.make_visible(bb=True)
    pt.highlight(bb=True)
    assert image_similarity_full(pt.fig, "bb_BB.png")

def test_bb_agb():
    pt = PeriodicTable()
    pt.make_visible(bb=True, agb=True)
    pt.highlight(agb=True)
    assert image_similarity_full(pt.fig, "bb_agb_AGB.png")

def test_bb_agb_snii():
    pt = PeriodicTable()
    pt.make_visible(bb=True, agb=True, snii=True)
    pt.highlight(snii=True)
    assert image_similarity_full(pt.fig, "bb_agb_snii_SNII.png")

def test_bb_agb_snii_snia():
    pt = PeriodicTable()
    pt.make_visible(bb=True, agb=True, snii=True, snia=True)
    pt.highlight(snia=True)
    assert image_similarity_full(pt.fig, "bb_agb_snii_snia_SNIA.png")

def test_bb_agb_snii_snia_s():
    pt = PeriodicTable()
    pt.make_visible(bb=True, agb=True, snii=True, snia=True, s=True)
    pt.highlight(s=True)
    assert image_similarity_full(pt.fig, "bb_agb_snii_snia_s_S.png")

def test_bb_agb_snii_snia_s_r():
    pt = PeriodicTable()
    pt.make_visible(bb=True, agb=True, snii=True, snia=True, s=True, r=True)
    pt.highlight(r=True)
    assert image_similarity_full(pt.fig, "bb_agb_snii_snia_s_r_R.png")

def test_bb_agb_snii_snia_s_r_cr():
    pt = PeriodicTable()
    pt.make_visible(bb=True, agb=True, snii=True, snia=True, s=True, r=True,
                    cr=True)
    pt.highlight(cr=True)
    assert image_similarity_full(pt.fig, "bb_agb_snii_snia_s_r_cr_CR.png")

def test_bb_agb_snii_snia_s_r_cr_decay():
    pt = PeriodicTable()
    pt.make_visible(bb=True, agb=True, snii=True, snia=True, s=True, r=True,
                    cr=True, decay=True)
    pt.highlight(decay=True)
    assert image_similarity_full(pt.fig, "bb_agb_snii_snia_s_r_cr_decay_DECAY.png")

def test_bb_agb_snii_snia_s_r_cr_decay_unstable():
    pt = PeriodicTable()
    pt.make_visible(bb=True, agb=True, snii=True, snia=True, s=True, r=True,
                    cr=True, decay=True, unstable=True)
    pt.highlight(unstable=True)
    assert image_similarity_full(pt.fig,  "bb_agb_snii_snia_s_r_cr_decay_unstable_UNSTABLE.png")

def test_full_bb():
    pt = PeriodicTable()
    pt.make_visible(bb=True, agb=True, snii=True, snia=True, s=True, r=True,
                    cr=True, decay=True, unstable=True)
    pt.highlight(bb=True)
    assert image_similarity_full(pt.fig, "full_bb.png")

def test_full_cr():
    pt = PeriodicTable()
    pt.make_visible(bb=True, agb=True, snii=True, snia=True, s=True, r=True,
                    cr=True, decay=True, unstable=True)
    pt.highlight(cr=True)
    assert image_similarity_full(pt.fig, "full_cr.png")

def test_full_lm():
    pt = PeriodicTable()
    pt.make_visible(bb=True, agb=True, snii=True, snia=True, s=True, r=True,
                    cr=True, decay=True, unstable=True)
    pt.highlight(low_mass=True)
    assert image_similarity_full(pt.fig, "full_lm.png")

def test_full_snii():
    pt = PeriodicTable()
    pt.make_visible(bb=True, agb=True, snii=True, snia=True, s=True, r=True,
                    cr=True, decay=True, unstable=True)
    pt.highlight(snii=True)
    assert image_similarity_full(pt.fig, "full_snii.png")

def test_full_snia():
    pt = PeriodicTable()
    pt.make_visible(bb=True, agb=True, snii=True, snia=True, s=True, r=True,
                    cr=True, decay=True, unstable=True)
    pt.highlight(snia=True)
    assert image_similarity_full(pt.fig, "full_snia.png")

def test_full_r():
    pt = PeriodicTable()
    pt.make_visible(bb=True, agb=True, snii=True, snia=True, s=True, r=True,
                    cr=True, decay=True, unstable=True)
    pt.highlight(r=True)
    assert image_similarity_full(pt.fig, "full_r.png")

def test_full_decay():
    pt = PeriodicTable()
    pt.make_visible(bb=True, agb=True, snii=True, snia=True, s=True, r=True,
                    cr=True, decay=True, unstable=True)
    pt.highlight(decay=True)
    assert image_similarity_full(pt.fig, "full_decay.png")

def test_full_unstable():
    pt = PeriodicTable()
    pt.make_visible(bb=True, agb=True, snii=True, snia=True, s=True, r=True,
                    cr=True, decay=True, unstable=True)
    pt.highlight(unstable=True)
    assert image_similarity_full(pt.fig, "full_unstable.png")

def test_full_none():
    pt = PeriodicTable()
    pt.make_visible(bb=True, agb=True, snii=True, snia=True, s=True, r=True,
                    cr=True, decay=True, unstable=True)
    assert image_similarity_full(pt.fig, "full_none.png")
