import matplotlib
import numpy as np
import matplotlib.scale as mscale
import matplotlib.transforms as mtransforms
import matplotlib.ticker as mticker


class PowerScale(mscale.ScaleBase):
    name = 'power_scale'

    def __init__(self, axis, **kwargs):
        """Any keyword arguments passed to  ``set_xscale`` and
        ``set_yscale`` will be passed along to the scale's constructor.
        """
        mscale.ScaleBase.__init__(self)
        exponent = kwargs.pop('exponent', 1)
        nonpos = kwargs.pop('nonpos', 'clip')

        self.exponent = exponent
        self.nonpos = nonpos

    def get_transform(self):
       return self.PowerTransform(self.exponent, self.nonpos)

    def set_default_locators_and_formatters(self, axis):
        axis.set_major_locator(mticker.AutoLocator())
        axis.set_major_formatter(mticker.ScalarFormatter())
        axis.set_minor_locator(mticker.NullLocator())
        axis.set_minor_formatter(mticker.NullFormatter())


    class PowerTransform(mtransforms.Transform):
        """TODO: Docstring"""
        input_dims = 1
        output_dims = 1
        is_separable = True
        has_inverse = True

        def __init__(self, exponent, nonpos='clip'):
            mtransforms.Transform.__init__(self)
            self._clip = {"clip": True, "mask": False}[nonpos]
            self.exponent = exponent
            self.nonpos = nonpos

        def transform_non_affine(self, a):
            with np.errstate(divide="ignore", invalid="ignore"):
                out = a**self.exponent
                if self._clip:
                    out[a <= 0] = -1000
            return out

        def __str__(self):
            return "{}()".format(type(self).__name__, "clip" if self._clip else "mask")

        def inverted(self):
            return PowerScale.InvertedPowerTransform(self.exponent, self.nonpos)

    class InvertedPowerTransform(mtransforms.Transform):
        """TODO: Docstring"""
        input_dims = 1
        output_dims = 1
        is_separable = True
        has_inverse = True

        def __init__(self, exponent, nonpos='clip'):
            mtransforms.Transform.__init__(self)
            self._clip = {"clip": True, "mask": False}[nonpos]
            self.exponent = exponent

        def transform_non_affine(self, a):
            with np.errstate(divide="ignore", invalid="ignore"):
                out = a**(1/self.exponent)
                if self._clip:
                    out[a <= 0] = -1000
            return out

        def __str__(self):
            return "{}()".format(type(self).__name__, "clip" if self._clip else "mask")


mscale.register_scale(PowerScale)