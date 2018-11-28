#Path
TRAIDATA_PATH = './data/uji/trainingData.csv'
VALIDATION_PATH = './data/uji/validationData.csv'

#DataSet Porperty
AP_COUNT = 520
LONGITUDE_INDEX = AP_COUNT
LATITUDE_INDEX = LONGITUDE_INDEX + 1
FLOOT_INDEX = LATITUDE_INDEX + 1
BUILDINGID_INDEX = FLOOT_INDEX + 1
SPACEID_INDEX = BUILDINGID_INDEX + 1
RELATIVEPOSITION_INDEX = SPACEID_INDEX + 1
USERID_INDEX = RELATIVEPOSITION_INDEX + 1
PHONEID_INDEX = USERID_INDEX + 1
TIMESTAMP_INDEX = PHONEID_INDEX + 1

#Device Normalize
PROXIMATE_THRESHOLD = 3
MIN_GAIN_DIFF = -20
MAX_GAIN_DIFF = 20

#Data Preprocess
BUILDINGID = 1
FLOORID = 1
RSSI_THRESHOLD = 80