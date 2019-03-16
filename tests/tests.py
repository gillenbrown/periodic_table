import pytest

from periodic_table import Element, box_fraction_line

from scipy import integrate
import numpy as np

np.random.seed(0)

def test_fracs_in_range():
    with pytest.raises(ValueError):
        Element("H", 1, 1, 1, frac_bb=-0.1)
    with pytest.raises(ValueError):
        Element("H", 1, 1, 1, frac_agb=1.1)
    Element("H", 1, 1, 1, frac_bb=1.0)  # no error

def test_fracs_sum_to_one():
    with pytest.raises(ValueError):
        Element("H", 1, 1, 1, frac_bb=0.1)
    with pytest.raises(ValueError):
        Element("H", 1, 1, 1, frac_r=0.8)
    Element("H", 1, 1, 1, frac_bb=1.0)  # no error

def test_fraction_line_zero():
    # the real test here is whether the area under the curve integrates to
    # the proper value. We get the function returned, and integrate it along
    # the box used to represent an element, which is the unit square (ie square
    # with the lower right corner at (0,0) and side length of 1.

    def integrand(xs, frac):
        line_func = box_fraction_line(frac)
        # get rid of negative values to keep the integrand in the square
        ys = np.maximum(line_func(xs), 0)
        # then get rid of things above 1
        ys = np.minimum(ys, 1)
        return ys

    # get random fractions to test the integration for, including zero and one
    for frac in np.concatenate(([0, 1], np.random.uniform(0, 1, 100))):
        result = integrate.quad(integrand, 0, 1, args=(frac))[0]
        assert np.isclose(result, frac, rtol=0, atol=1E-6)
