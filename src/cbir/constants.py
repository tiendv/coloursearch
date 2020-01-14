K = 35

FIELD_NAMES = ['c_0_100_100', 'c_45_100_100', 'c_90_100_100', 'c_135_100_100', 'c_180_100_100',
               'c_225_100_100', 'c_270_100_100', 'c_315_100_100', 'c_0_50_100', 'c_45_50_100',
               'c_90_50_100', 'c_135_50_100', 'c_180_50_100', 'c_225_50_100', 'c_270_50_100',
               'c_315_50_100', 'c_0_100_50', 'c_45_100_50', 'c_90_100_50', 'c_135_100_50',
               'c_180_100_50', 'c_225_100_50', 'c_270_100_50', 'c_315_100_50', 'c_0_50_50',
               'c_45_50_50', 'c_90_50_50', 'c_135_50_50', 'c_180_50_50', 'c_225_50_50',
               'c_270_50_50', 'c_315_50_50', 'c_0_0_100', 'c_0_0_50', 'c_0_0_0']

METHODS = {
    'Fuzzy Color Histogram': 'fuzzy_color_histogram',
    'Color Coherence Vector': 'color_coherence_vector',
    'Color Correlogram': 'color_correlogram',
    'Cumulative Color Histogram': 'cumulative_color_histogram'
}

THUMBNAIL_IMAGE_HEIGHT = 256
MAX_IMAGE_WIDTH = MAX_IMAGE_HEIGHT = 512
MAX_RETRIEVAL_IMAGE_WIDTH = MAX_RETRIEVAL_IMAGE_HEIGHT = 32

NUMBER_OF_CCV_COLORS = 128
NUMBER_OF_COLORS = 512
NUMBER_OF_COARSE_COLORS = 4096
NUMBER_OF_FINE_COLORS = 64
M = 1.9

# K-means clustering
K_IN_K_MEANS = 8
