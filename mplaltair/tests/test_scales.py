import matplotlib.pyplot as plt

def test_scales_clip_false():
    fig, ax = plt.subplots()
    ax.set_yscale('power_scale', exponent=2, nonpos="mask")