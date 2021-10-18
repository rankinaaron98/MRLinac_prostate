
import os
import six
import radiomics
import pandas

from radiomics import featureextractor

paramPath = "D:\\data\\Bladder\\motionStudy\\Params.yaml"

ptDir = os.listdir("D:\\data\\Bladder\\motionStudy\\radiomics")
#print (ptDir)

extractor = featureextractor.RadiomicsFeatureExtractor(paramPath)

for i in ptDir:
	scanWeeks = os.listdir("D:\\data\\Bladder\\motionStudy\\radiomics\\"+str(i))
	
	for j in scanWeeks:
		niiFiles = os.listdir("D:\\data\\Bladder\\motionStudy\\radiomics\\"+str(i)+"\\"+str(j))
		
		for k in niiFiles:
			tmpName = str(k)
			tmpName = tmpName[:-14]
			
			if "image" in k:
				print ("Processing: "+tmpName+"  Timepoint: "+j)	
				imageName = "D:\\data\\Bladder\\motionStudy\\radiomics\\"+str(i)+"\\"+str(j)+"\\"+str(k)
				#print ("image  "+imageName)
			
				tmpResults = pandas.DataFrame()	
				if os.path.exists("D:\\data\\Bladder\\motionStudy\\radiomics\\"+str(i)+"\\"+str(j)+"\\"+tmpName+"_"+j+"_1_TEtumorBed.nii"):
					maskName = "D:\\data\\Bladder\\motionStudy\\radiomics\\"+str(i)+"\\"+str(j)+"\\"+tmpName+"_"+j+"_1_TEtumorBed.nii"
					
					TEtumorBed = pandas.Series(extractor.execute(imageName, maskName))
					TEtumorBed.name = "TEtumorBed_"+tmpName[-1:]+"_"+j
					tmpResults = tmpResults.append(TEtumorBed)
					
				else:
					print ("Check segmentation list for TEtumorBed")
				
				if os.path.exists("D:\\data\\Bladder\\motionStudy\\radiomics\\"+str(i)+"\\"+str(j)+"\\"+tmpName+"_"+j+"_1_YPtumorBed.nii"):
					maskName = "D:\\data\\Bladder\\motionStudy\\radiomics\\"+str(i)+"\\"+str(j)+"\\"+tmpName+"_"+j+"_1_YPtumorBed.nii"
					
					YPtumorBed = pandas.Series(extractor.execute(imageName, maskName))
					YPtumorBed.name = "YPtumorBed_"+tmpName[-1:]+"_"+j
					tmpResults = tmpResults.append(YPtumorBed)
					
				else:
					print ("Check segmentation list for YPtumorBed")
				
				if os.path.exists("D:\\data\\Bladder\\motionStudy\\radiomics\\"+str(i)+"\\"+str(j)+"\\"+tmpName+"_"+j+"_1_TEbladderWall.nii"):
					maskName = "D:\\data\\Bladder\\motionStudy\\radiomics\\"+str(i)+"\\"+str(j)+"\\"+tmpName+"_"+j+"_1_TEbladderWall.nii"
					
					TEbladderWall = pandas.Series(extractor.execute(imageName, maskName))
					TEbladderWall.name = "TEbladderWall_"+tmpName[-1:]+"_"+j
					tmpResults = tmpResults.append(TEbladderWall)
					
				else:
					print ("Check segmentation list for TEbladderWall")
				
				if os.path.exists("D:\\data\\Bladder\\motionStudy\\radiomics\\"+str(i)+"\\"+str(j)+"\\"+tmpName+"_"+j+"_1_YPbladderWall.nii"):
					maskName = "D:\\data\\Bladder\\motionStudy\\radiomics\\"+str(i)+"\\"+str(j)+"\\"+tmpName+"_"+j+"_1_YPbladderWall.nii"
					
					YPbladderWall = pandas.Series(extractor.execute(imageName, maskName))
					YPbladderWall.name = "YPbladderWall_"+tmpName[-1:]+"_"+j
					tmpResults = tmpResults.append(YPbladderWall)
											
				else:
					print ("Check segmentation list for YPbladderWall")			
				
				tmpResults.T.to_csv("D:\\data\\Bladder\\motionStudy\\radiomicsResults\\"+tmpName+"_"+str(j)+".csv")
			
				
