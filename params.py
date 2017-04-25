

print 'STARTING...\n'
__author__ = 'SHostetter'

# set up base globals
FOLDER = '' # working directory
DB_HOST = '' # database host
DB_NAME = '' # database name
LION = '' # LION segment table
NODE = '' # LION node table
RPL = '' # LION RPL database table
RPL_TXT = '' # raw LION RPL text file 
VERSION = '' # LION verion number
PRECINCTS = '' # police precincts table w geom
BOROUGHS = '' # borough boundary table w geom
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