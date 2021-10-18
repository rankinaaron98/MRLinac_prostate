import SimpleITK as sitk
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
import os

histmatch = True

url = 'D:/data/Sarcoma/sarcomaRadiomics/radiomics/'
scanType = 'T2' # T1 or T2

ptDir = os.listdir(url)


if histmatch:
    refPat = '264848839' # patient with T1 and T2 axial images
    refimage =  sitk.ReadImage(url + refPat + '/' + scanType + '_Axial/' + refPat + '_' + scanType + '_axial_image.nii' ) 
    result = sitk.GetArrayFromImage(refimage)
    plt.figure('reference histogram')
    result = result.flatten()
    refmax = result.max()
    print(refmax)

    plt.hist(result, bins=64, range= (1,refmax),facecolor='red', alpha=0.75,histtype = 'step', density=True)
    plt.xlabel('MR intensity')
    plt.ylabel('Percentage') 
    plt.savefig('D:/data/Sarcoma/sarcomaRadiomics/histograms/'+ refPat+ '_' + scanType + '_axial.png', dpi=300)


plt.figure('Histograms')
print (scanType)
for i in ptDir:
	scans = os.listdir(url + str(i))
	
	for j in scans:
		if scanType in str(j):
			print('Processing patient: ' + i + '   scan: ' + j)

			image = sitk.ReadImage(url + i + '/' + j + '/' + i + '_' + j + '_image.nii')
			if histmatch:
				matcher = sitk.HistogramMatchingImageFilter()
				matcher.SetNumberOfHistogramLevels(256)
				matcher.SetNumberOfMatchPoints(11)
				matcher.ThresholdAtMeanIntensityOn()
				image = matcher.Execute(image, refimage)
				sitk.WriteImage( image, url + i + '/' + j + '/' + i + '_' + j + '_NORMimage.nii' )
			result = sitk.GetArrayFromImage(image)

			if not histmatch:
				refmax = result.max()

			result = result.flatten()
			plt.hist(result, bins=64, range= (1,refmax),facecolor='red', alpha=0.75,histtype = 'step', density=True)
			plt.xlabel('MR intensity')
			plt.ylabel('Percentage')

			if histmatch:
				plt.savefig('D:/data/Sarcoma/sarcomaRadiomics/histograms/normHistograms/' + scanType + '/' + i + '_' + j + '.png', dpi=300)
			else:        
				plt.savefig('D:/data/Sarcoma/sarcomaRadiomics/histograms/rawHistograms/' + scanType + '/' + i + '_' + j + '.png', dpi=300)
			plt.show()
			
"""
for file in os.listdir(url):
    print(file)
    image = sitk.ReadImage(url + '/' + file)
    if histmatch:
        matcher = sitk.HistogramMatchingImageFilter()
        matcher.SetNumberOfHistogramLevels(256)
        matcher.SetNumberOfMatchPoints(11)
        matcher.ThresholdAtMeanIntensityOn()
        image = matcher.Execute(image, refimage)
        sitk.WriteImage( image, url + '_norm_HN/' + file )
    result = sitk.GetArrayFromImage(image)

    if not histmatch:
        refmax = result.max()

	result = result.flatten()
    plt.hist(result, bins=64, range= (1,refmax),facecolor='red', alpha=0.75,histtype = 'step', density=True)
plt.xlabel('MR intensity')
plt.ylabel('Percentage')

if histmatch:
    plt.savefig('T:/Eliana/PeterMbanu/results/figs/matched_histograms_ref'+ refPat+ '.png', dpi=300)
else:
    plt.savefig('T:/Eliana/PeterMbanu/results/figs/input_histograms.png', dpi=300)
plt.show()
"""