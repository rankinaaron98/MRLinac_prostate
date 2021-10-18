
import os
import six
import radiomics
import pandas

from radiomics import featureextractor

ptPath = 'D:/data/Sarcoma/sarcomaRadiomics/radiomics/'
ptDir = os.listdir(ptPath)

paramPath = 'D:/data/Sarcoma/sarcomaRadiomics/ParamsSarcoma.yaml'
extractor = featureextractor.RadiomicsFeatureExtractor(paramPath)

for i in ptDir:
	if not 'txt' in i:
		scans = os.listdir(ptPath + str(i))

		for j in scans:
			if  os.path.exists(ptPath + i + '/' + j + '/' + i + '_' + j + '_NORMimage.nii'):
				print ('Processing patient: ' + i + '   scan: ' + j)	
				imageName = ptPath + i + '/' + j + '/' + i + '_' + j + '_NORMimage.nii'
				tmpResults = pandas.DataFrame()	
				
				if os.path.exists(ptPath + i + '/' + j + '/' + i + '_' + j + '_AD.nii'):
					maskName = ptPath + i + '/' + j + '/' + i + '_' + j + '_AD.nii'
					
					AD = pandas.Series(extractor.execute(imageName, maskName))
					AD.name = 'AD' + '_' + j
					tmpResults = tmpResults.append(AD)
						
				else:
					print ("Check segmentation list for AD")
				
				if os.path.exists(ptPath + i + '/' + j + '/' + i + '_' + j + '_JZ.nii'):
					maskName = ptPath + i + '/' + j + '/' + i + '_' + j + '_JZ.nii'
					
					JZ = pandas.Series(extractor.execute(imageName, maskName))
					JZ.name = 'JZ' + '_' + j
					tmpResults = tmpResults.append(JZ)
						
				else:
					print ("Check segmentation list for JZ")
				
				
				tmpResults.T.to_csv('D:/data/Sarcoma/sarcomaRadiomics/radiomicsResults/' + i + '_' + str(j) + '.csv')
				
					
