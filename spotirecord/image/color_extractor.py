"""
This module extracts the most important color out of an image.
Most of that is taken from https://github.com/davidkrantz/Colorfy/blob/master/spotify_background_color.py
"""
import numpy as np
import skimage
from sklearn.cluster import KMeans


def get_best_color(image_url, k=8, color_tol=10):
    """
    AUTHOR: David Krantz (https://github.com/davidkrantz)

    Returns a suitable background color for the given image.
    Uses k-means clustering to find `k` distinct colors in
    the image. A colorfulness index is then calculated for each
    of these colors. The color with the highest colorfulness
    index is returned if it is greater than or equal to the
    colorfulness tolerance `color_tol`. If no color is colorful
    enough, a gray color will be returned. Returns more or less
    the same color as Spotify in 80 % of the cases.
    Args:
        image_url: the url of the image for download
        k (int): Number of clusters to form.
        color_tol (float): Tolerance for a colorful color.
            Colorfulness is defined as described by Hasler and
            Süsstrunk (2003) in https://infoscience.epfl.ch/
            record/33994/files/HaslerS03.pdf.

    Returns:
        tuple: (R, G, B). The calculated background color.
    """
    img = skimage.io.imread(image_url)
    artwork = img.copy()
    img = img.reshape((img.shape[0] * img.shape[1], 3))

    clt = KMeans(n_clusters=k)
    clt.fit(img)
    centroids = clt.cluster_centers_

    colorfulness = [calc_colorfulness(color[0], color[1], color[2]) for color in centroids]
    max_colorful = np.max(colorfulness)
    if max_colorful < color_tol:
        # If not colorful, set to gray
        best_color = [230, 230, 230]
    else:
        # Pick the most colorful color
        best_color = centroids[np.argmax(colorfulness)]
    return int(best_color[0]), int(best_color[1]), int(best_color[2])


def calc_colorfulness(r, g, b):
    """
    AUTHOR: David Krantz (https://github.com/davidkrantz)

    Returns a colorfulness index of given RGB combination.
    Implementation of the colorfulness metric proposed by
    Hasler and Süsstrunk (2003) in https://infoscience.epfl.ch/
    record/33994/files/HaslerS03.pdf.
    Args:
        r (int): Red component.
        g (int): Green component.
        b (int): Blue component.
    Returns:
        float: Colorfulness metric.
    """
    rg = np.absolute(r - g)
    yb = np.absolute(0.5 * (r + g) - b)

    # Compute the mean and standard deviation of both `rg` and `yb`.
    rg_mean, rg_std = (np.mean(rg), np.std(rg))
    yb_mean, yb_std = (np.mean(yb), np.std(yb))

    # Combine the mean and standard deviations.
    std_root = np.sqrt((rg_std ** 2) + (yb_std ** 2))
    mean_root = np.sqrt((rg_mean ** 2) + (yb_mean ** 2))

    return std_root + (0.3 * mean_root)
