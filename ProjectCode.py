from __future__ import print_function
import os
import pandas
import SimpleITK as sitk
import matplotlib.pyplot as plt
from radiomics import featureextractor


outPath = "D:\\users\\Chelsea\\4D_data_complete\\"
parameterPath = "D:\\users\\Chelsea\\testRadiomics\\"

inputExhale_CSV = os.path.join(outPath, "exhaleCases.csv")
inputMC_CSV = os.path.join(outPath, "MCCases.csv")
inputMCMed_CSV = os.path.join(outPath, "MCMedCases.csv")
inputInhale_CSV = os.path.join(outPath, "inhaleCases.csv")

exhaleOutput = os.path.join(outPath, "exhale_radiomics_features.csv")
mcOutput = os.path.join(outPath, "MC_radiomics_features.csv")
mcMedOutput = os.path.join(outPath, "MCMed_radiomics_features.csv")
inhaleOutput = os.path.join(outPath, "inhale_radiomics_features.csv")

params = "D:\\users\\Chelsea\\testRadiomics\\Params.yaml"

def visualisation():
    
    im = sitk.ReadImage("D:\\users\\Chelsea\\4D_data_complete\\CT_exhale\\Patient04_50.nii") #read image file
    im = sitk.Cast(sitk.IntensityWindowing(im, windowMinimum = 0, windowMaximum = 1500),
                       sitk.sitkUInt8) #set level and window
    msk = sitk.ReadImage("D:\\users\\Chelsea\\4D_data_complete\\New_Masks\\mask_exhale\\Patient04_50.nii") #read mask file

   
    #for z in range(im.GetDepth()): #change to loop if want to visual all slices 
    ct_slice = sitk.GetArrayViewFromImage(im)[54,:,:] #zth slice (54th)
    mask_slice = sitk.GetArrayViewFromImage(msk)[54,:,:]
        
    nrow = ncol = 1
    fig, ax = plt.subplots(nrow,ncol)
    plt.axis('off')   
    cb = ax.imshow(ct_slice, interpolation=None, cmap='Greys_r', vmin = ct_slice.min(), vmax = ct_slice.max()) #plot ct slice
    cnt = ax.contour(mask_slice, alpha=1) #overlay mask as contour
    
         
    for c in cnt.collections:
        c.set_edgecolor("red")
        c.set_linewidth(0.5)
        fig.savefig("workflowfigurecontour.jpeg")   
        

# Use pandas to read and transpose ('.T') the input data
# The transposition is needed so that each column represents one test case. This is easier for iteration over
# the input cases
#before this point need a way of creating these csv files. 
flistsEx = pandas.read_csv(inputExhale_CSV).T
flistsMC = pandas.read_csv(inputMC_CSV).T
flistsIn = pandas.read_csv(inputInhale_CSV).T
flistsMCMed = pandas.read_csv(inputMCMed_CSV).T
if os.path.isfile(params):
    extractor = featureextractor.RadiomicsFeatureExtractor(params)
    

   
    #Disable all features except first order
    extractor.disableAllFeatures()
    
    #Enable all features in named class
    extractor.enableFeatureClassByName('glcm')
else:  # Parameter file not found, use hardcoded settings instead, extract all features
    settings = {}
    settings['binWidth'] = 25
    settings['resampledPixelSpacing'] = None  # [3,3,3]
    settings['interpolator'] = sitk.sitkBSpline
    settings['enableCExtensions'] = True
    settings['correctMask'] = True


    extractor = featureextractor.RadiomicsFeatureExtractor(**settings)

    extractor.disableAllFeatures()
    extractor.enableFeatureClassByName('glcm')
    

def exhaleExtraction():
    exhaleResults = pandas.DataFrame()
    for entry in flistsEx:  # Loop over all columns (i.e. the test cases)
        imageFilepath = flistsEx[entry]['Image']
        maskFilepath = flistsEx[entry]['Mask']
        label = flistsEx[entry].get('Label', None)
        
        print('image path:', imageFilepath) #check to see if image path is correct
        if str(label).isdigit():
          label = int(label)
        else:
          label = None
    
        if (imageFilepath is not None) and (maskFilepath is not None):
          featureVector = flistsEx[entry]  # This is a pandas Series
          featureVector['Image'] = os.path.basename(imageFilepath)
          featureVector['Mask'] = os.path.basename(maskFilepath)

        ex_result = pandas.Series(extractor.execute(imageFilepath, maskFilepath, label))
        featureVector = featureVector.append(ex_result) 
        featureVector.name = entry
          
        exhaleResults = exhaleResults.join(featureVector, how='outer')  # If feature extraction failed, results will be all NaN
        exhaleResults.T.to_csv(exhaleOutput, index=False, na_rep='NaN')
        
def mcExtraction():
    mcResults = pandas.DataFrame()
    for entry in flistsMC:  # Loop over all columns (i.e. the test cases)
        imagepath = flistsMC[entry]['Image']
        maskpath = flistsMC[entry]['Mask']
        label = flistsMC[entry].get('Label', None)
        
        print('image path:', imagepath)
        if str(label).isdigit():
          label = int(label)
        else:
          label = None
    
        if (imagepath is not None) and (maskpath is not None):
          featureVector = flistsMC[entry]  
          featureVector['Image'] = os.path.basename(imagepath)
          featureVector['Mask'] = os.path.basename(maskpath)
       
        mcResult = pandas.Series(extractor.execute(imagepath, maskpath, label))
        featureVector = featureVector.append(mcResult)
        featureVector.name = entry
          
        mcResults = mcResults.join(featureVector, how='outer')  
        mcResults.T.to_csv(mcOutput, index=False, na_rep='NaN')

def mcMedExtraction():
    mcMedResults = pandas.DataFrame()
    for entry in flistsMCMed:  
        imagepath = flistsMCMed[entry]['Image']
        maskpath = flistsMCMed[entry]['Mask']
        label = flistsMCMed[entry].get('Label', None)
        
        print('image path:', imagepath)
        if str(label).isdigit():
          label = int(label)
        else:
          label = None
    
        if (imagepath is not None) and (maskpath is not None):
          featureVector = flistsMCMed[entry]  
          featureVector['Image'] = os.path.basename(imagepath)
          featureVector['Mask'] = os.path.basename(maskpath)
       
        mcMedResult = pandas.Series(extractor.execute(imagepath, maskpath, label))
        featureVector = featureVector.append(mcMedResult)
        featureVector.name = entry
          
        mcMedResults = mcMedResults.join(featureVector, how='outer')  
        mcMedResults.T.to_csv(mcMedOutput, index=False, na_rep='NaN')

def inhaleExtraction():
    inhaleResults = pandas.DataFrame()
    for entry in flistsIn:  
        imagepath = flistsIn[entry]['Image']
        maskpath = flistsIn[entry]['Mask']
        label = flistsIn[entry].get('Label', None)
        
        print('image path:', imagepath)
        if str(label).isdigit():
          label = int(label)
        else:
          label = None
    
        if (imagepath is not None) and (maskpath is not None):
          featureVector = flistsIn[entry]  
          featureVector['Image'] = os.path.basename(imagepath)
          featureVector['Mask'] = os.path.basename(maskpath)
       
        inhaleResult = pandas.Series(extractor.execute(imagepath, maskpath, label))
        featureVector = featureVector.append(inhaleResult)
        featureVector.name = entry
          
        inhaleResults = inhaleResults.join(featureVector, how='outer')  
        inhaleResults.T.to_csv(inhaleOutput, index=False, na_rep='NaN')

   
#visualisation()
exhaleExtraction()
mcExtraction()
inhaleExtraction()
mcMedExtraction()