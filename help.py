#import VA One module
from VAOne import *
# import traceback
try:
    # Sets the name of the model to be created/read
    va1model = 'Example.va1'
    # check for API initialization
    if not pi_fIsInit():
        pi_fInit() # Initialize API
    # Obtain pointer associated with a new database
    db = pi_fNeoDatabaseCreate(True)
    # Set this database as the current database
    pi_fNeoDatabaseSetCurrent(db)
    # Set filename associated with this database
    pi_fNeoDatabaseSetFileSpec(db, va1model)
    # If the database file doesn't exist on disk then create it
    if not pi_fNeoDatabaseExistsOnDisk(db):
        # Try to create the database on disk
        if not pi_fNeoDatabaseCreateOnDisk(db):
            pi_fNeoDatabaseDispose(db) # Deallocates the database
            raise Exception("Cannot create file on disk.")
        # Try to open the database
        if not pi_fNeoDatabaseOpenReadWrite(db):
            pi_fNeoDatabaseDispose(db) # Deallocates the database
            raise Exception("Cannot open database.")
        # next 3 steps create valid .va1 file
        # creates a unit system
        unitsys = pi_fUnitSysCreate("SI","kg","m","s",1,1,1)
        # creates the environment
        env = pi_fAnalysisEnvCreate(unitsys)
        # creates the network
        net = pi_fNetworkCreate("Example", env)
    else:
        if not pi_fNeoDatabaseOpenReadWrite(db): # Try to open the database
            pi_fNeoDatabaseDispose(db) # Deallocates the database
            raise Exception("Cannot open database.")

	# Create coordinate arrays for the points to be created
    x=[0,0.2,0.5,1]
    y=[0,0.05,0.02,-0.02]
    z=[1,1.25,1.5,2]

	# Create four nodes from arrays x, y, z
    NodeList=new_CNode3DArray(4)
    for index in range(4):
         CNode3DArray_setitem(NodeList,index,pi_fNode3DCreate(index, x[index], y[index],z[index]))
	# Create an orientation node
    ReferenceNode = pi_fNode3DCreate(5,1.0,2.5,1.0)
	# Create the beam
    NewBeam = pi_fBeamCreate('New Beam', NodeList, 4, ReferenceNode)
	# Add the beam to the current network
    db = pi_fNeoDatabaseGetCurrent()
    Network = pi_fNeoDatabaseGetNetwork(db)
    pi_fNetworkAddNetElm(Network, pi_fConvertBeamNetElm(NewBeam))
			
    # in the end of the code If changes are to be saved
    # they should be commited to the database 
    pi_fNeoDatabaseCommit(db, False)
    # the file should be properly closed
    pi_fNeoDatabaseClose(db)
    # the database should be deallocated from memory
    pi_fNeoDatabaseDispose(db)
except:
    if pi_fIsInit():
        db = pi_fNeoDatabaseGetCurrent()
        if pi_fNeoDatabaseIsOpen(db):
            pi_fNeoDatabaseClose(db)
            pi_fNeoDatabaseDispose(db)
    raise