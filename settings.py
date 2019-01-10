# Path
DATA_SRC_DIR = './data/uji/'
TRAIDATA_PATH = DATA_SRC_DIR+'trainingData.csv'
VALIDATION_PATH = DATA_SRC_DIR+'validationData.csv'
MIDFILE_DIR = DATA_SRC_DIR+'midfile/'


# DataSet Porperty
AP_COUNT = 0
MSR_COUNT = 0
DEVICE_SET = set()

# Device Normalize
PROXIMATE_THRESHOLD = 3
MIN_GAIN_DIFF = -20
MAX_GAIN_DIFF = 20

# Data Preprocess
BUILDINGID = 1
FLOORID = 1
RSSI_THRESHOLD = 80
DEFAULT_RSSI = 100
MIN_VALID_RSSI = -80
POSITION_OFFSET = 20
SPACE_RANGE = [-POSITION_OFFSET, POSITION_OFFSET,
               POSITION_OFFSET, -POSITION_OFFSET]

# Cluster Param
AP_CLU_THRESHOLD = 0.1
LOC_CLU_THRESHOLD = 0.1

# Solve LDPL
# ERSGA
KNOWN_LOC_PERCENT = 0.2
POWER_MAX = -10
POWER_MIN = -50
POWER_SEARCH_STEP = 1
GAMMA_MAX = 60
GAMMA_MIN = 15
GAMMA_SEARCH_STEP = 1
GRID_DISTANCE_THRESHOLD = 1

# GA
SOLUTION_NUM = 50
GA_ROUND = 1
SELECT_PERCENT = 10
PICK_PERCENT = 20
RANDOM_PERCENT = 10
CROSS_PERCENT = 60
