
#import VA One module
from VAOne import *
import traceback
try:

    if not pi_fIsInit():
        pi_fInit(); # Initialize API

    # get a reference to the current database
    db = pi_fNeoDatabaseGetCurrent()
    # get a reference to the current network
    network = pi_fNeoDatabaseGetNetwork(db)
    # get a reference to the current analysis environment
    env = pi_fNetworkGetAnalysisEnv(network)
    # see if the table called Sample Spectrum already exists
    SpecName = 'Test Damping5'
    # see if the table called Sample Spectrum already exists
    table = pi_fNeoDatabaseFindByName(db, pi_fFloatSpectralTableGetClassID(), SpecName)
    # if not,
    if table == None:
        # create the frequency domain
        fdom = pi_fFreqDomainCreateThirdOctave(16,8000)
        # create table in memory (not in database yet)
        # reference count = 1
        table=pi_fFloatSpectralTableCreate(SpecName, SPECTRUM_ATTENUATION_TL, 
            SPECTRUM_FORM_FREQUENCY, fdom)
        # correct the reference count of the new frequency domain
        pi_fDBElementUnref(pi_fConvertNeoPersistDBElement(pi_fConvertFreqDomainNeoPersist(fdom)))
        # add to the current database, reference count = 2
        pi_fDBElementAddToDatabase(pi_fConvertNeoPersistDBElement(pi_fConvertFloatSpectralFunctionNeoPersist(pi_fConvertFloatSpectralTableFloatSpectralFunction(table))), db)
        # remove extra table reference from memory
        pi_fDBElementUnref(pi_fConvertNeoPersistDBElement(pi_fConvertFloatSpectralFunctionNeoPersist(pi_fConvertFloatSpectralTableFloatSpectralFunction(table))))
        NumFreqs = pi_fFloatSpectralTableGetCount(table)
        # Write values to database
        for index in range(NumFreqs):
            v=2.0**(index/10.0)
            pi_fFloatSpectralTableSetValue(table, v, index)

            
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
