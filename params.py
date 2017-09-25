print 'STARTING...\n'
__author__ = 'SHostetter'

# set up base globals
FOLDER = r'C:\Users\SHostetter\Desktop\GIT\CLION' # working directory
DB_HOST = 'Dotdevpgsql01.dot.nycnet' # database host
DB_NAME = 'RIS_TRAINING'# CRASHDATA' #'RIS_TRAINING' # database name
LION = 'lion' # LION segment table
NODE = 'node' # LION node table
RPL = 'tbl_rpl' # LION RPL database table
RPL_TXT = 'RPL.txt' # raw LION RPL text file 
VERSION = '16d' # LION verion number
PRECINCTS = 'districts_police_precincts' # police precincts table w geom
BOROUGHS = 'districts_boroughs' # borough boundary table w geom
HIGHWAYS = True
SRID = 2263

# _____________________________________________________________________________________________________
# global dictionaries
nodeStreetNames = {}  # {node: set(street)}
nodeIsIntersection = {}  # {node: True or False}
nodeNextSteps = {}  # {node: {street: fromNode, toNode}}
segmentBlocks = {}  # {segmentID: fromMaster, toMaster}
node_master = {}  # {node: masterid}
clusterIntersections = {}  # {sorted-street-names: [set([nodes]), masterID]}
# if split:
# clusterIntersections = {}#{sorted-street-names: [
# [set([nodes]), masterID]
# [set([nodes]), masterID]
# ]}
mfts = []
coordFromMaster = {}  # {master: [x,y]
# minor datastores - can be deleted after use?
streetSet = []
mft1Dict = {}  # mft: [segmentid, segmentid]
altGraph = {}  # node: [[other end of street node, segmentid], [other end of street node, segmentid]]