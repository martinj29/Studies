# Create section :
mdb.models['Model-plein'].HomogeneousSolidSection(material='Aluminium_7075_T6', name='Section-1', thickness=None)

# assign section
mdb.models['Model-plein'].parts['Pied pale'].Set(cells=mdb.models['Model-plein'].parts['Pied pale'].cells.getSequenceFromMask(('[#1 ]', ), ), name='Set-3')
mdb.models['Model-plein'].parts['Pied pale'].SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=mdb.models['Model-plein'].parts['Pied pale'].sets['Set-3'], sectionName='Section-1', thicknessAssignment=FROM_SECTION)


# create and submit job

mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-plein', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='job_MP', nodalOutputPrecision=SINGLE, 
    numCpus=4, numDomains=4, numGPUs=0, queue=None, resultsFormat=ODB, scratch=
    '', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
mdb.jobs['job_MP'].submit(consistencyChecking=OFF)
mdb.jobs[''].waitForCompletion()


##########################################

x_values = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

for x in x_values :
    # Copie du modèle
    model_name = 'Model-plein_'+str(x)
    mdb.Model(name=model_name, objectToCopy=mdb.models['Model-plein'])
	# Modif de x
    mdb.models[model_name].ConstrainedSketch(name='__edit__', objectToCopy=mdb.models[model_name].parts['Pale'].features['Partition face-1'].sketch)
    mdb.models[model_name].parts['Pale'].projectReferencesOntoSketch(sketch=mdb.models[model_name].sketches['__edit__'], upToFeature=mdb.models['Model-plein'].parts['Pale'].features['Partition face-1'])
    mdb.models[model_name].sketches['__edit__'].dimensions[1].setValues(value = x)
    mdb.models[model_name].parts['Pale'].features['Partition face-1'].setValues(sketch=mdb.models[model_name].sketches['__edit__'])
    mdb.models[model_name].parts['Pale'].regenerate()
	
    mdb.models[model_name].rootAssembly.regenerate()
    mdb.models[model_name].parts['Pale'].generateMesh()
	# Creation du Job
    job_name = "job_"+model_name
    mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
        explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
        memory=90, model=model_name, modelPrint=OFF, 
        multiprocessingMode=DEFAULT, name=job_name, nodalOutputPrecision=SINGLE, 
        numCpus=2, numDomains=4, numGPUs=0, queue=None, scratch=
        '', userSubroutine='', waitHours=0, waitMinutes=0)
    # Lancement du Job
    mdb.jobs[job_name].submit(consistencyChecking=OFF)
    mdb.jobs[job_name].waitForCompletion()

##########################################
	
from odbAccess import *

nom_jobs = ["job_Model-plein_"+str(x)+'.odb' for x in [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]]
with open('Resultat_Bout_de_pale.csv','w') as csvfile:
    for nom_job in nom_jobs:
        odbFile = openOdb(path=nom_job)
        nframes = len(odbFile.steps['Step-1'].frames)
        subset = odbFile.rootAssembly.nodeSets['BOUT_DE_PALE']
        buff = odbFile.steps['Step-1'].frames[nframes-1].fieldOutputs['U'].getSubset(region=subset).values
        print(buff[0].magnitude)
        fichier = csv.writer(csvfile, delimiter=';',lineterminator='\n')
        fichier.writerow( [nom_job,str(buff[0].magnitude)] )
		
		