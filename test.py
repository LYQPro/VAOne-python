from VAOne import *
import traceback
try:
    # Sets the name of the model to be created/read
    va1model = 'Example.va1'
    # Check for API initialization
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
        # Try to open the database
        if not pi_fNeoDatabaseOpenReadWrite(db):
            pi_fNeoDatabaseDispose(db) # Deallocates the database
            raise Exception("Cannot open database.")
        # in the end of the code If changes are to be saved
        # they should be committed to the database
        pi_fNeoDatabaseCommit(db, False)
        # the file should be properly closed
        pi_fNeoDatabaseClose(db)
        # the database should be deallocated from memory
        pi_fNeoDatabaseDispose(db)
except:
    if pi_fIsInit:
        db = pi_fNeoDatabaseGetCurrent
    if pi_fNeoDatabaseIsOpen(db):
        pi_fNeoDatabaseClose(db)
        pi_fNeoDatabaseDispose(db)
    raise
