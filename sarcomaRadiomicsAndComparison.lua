
function scandir(directory)
    local i, t, popen = 0, {}, io.popen
    for filename in popen('dir "'..directory..'" /o:n /b'):lines() do
        i = i + 1
        t[i] = filename
    end
    return t
end

function folderExists(strFolderName)
	local fileHandle, strError = io.open(strFolderName.."\\*.*","r")
	if fileHandle ~= nil then
		io.close(fileHandle)
		return true
	else
		if string.match(strError,"No such file or directory") then
			return false
		else
			return true
		end
	end
end

function clear()
  for i = 1, wm.scan.len do
    if not scan[i].data.empty then
      wm.scan[i]:clear()
    end
  end
  wm.Delineation:clear()
end

dataT = [[D:\data\Sarcoma\sarcomaRadiomics\Sarcoma MR images\]]

output = [[D:\data\Sarcoma\sarcomaRadiomics\radiomics\]]
headerFlag = true
file = io.output(output..[[result.txt]], 'a')

        
-- read folders
folderPatients = {}
folderPatients = scandir(dataT)

--load data
-- list patient folders
for i = 1, #folderPatients do
  folderVisits = {}
  folderVisits = scandir(dataT..folderPatients[i])
  
  --list visits
  for j = 1, #folderVisits do
    folderScans = {}
    folderScans = scandir(dataT..folderPatients[i]..[[\]]..folderVisits[j])
    
    --list scans
    for k = 1, #folderScans do
      PtImages = {}
      PtImages = scandir(dataT..folderPatients[i]..[[\]]..folderVisits[j]..[[\]]..folderScans[k])
      
      --check both sets of observers are present
      print("Processing patient "..i..[[,  ]]..folderPatients[i].." visit "..folderVisits[j].." scan "..folderScans[k])
      
      -- look for MR and structures and load
      MRflag = false
      for l = 1, #PtImages do
        if MRflag == false then
          if string.find(dataT..folderPatients[i]..[[\]]..folderVisits[j]..[[\]]..folderScans[k]..[[\]]..PtImages[l], 'MR') then
            wm.scan[1]:load([[DCM:]]..dataT..folderPatients[i]..[[\]]..folderVisits[j]..[[\]]..folderScans[k]..[[\]]..PtImages[l])
            MRflag = true
          end
        end
      end
      for l = 1, #PtImages do
        if string.find(dataT..folderPatients[i]..[[\]]..folderVisits[j]..[[\]]..folderScans[k]..[[\]]..PtImages[l], 'RS') then
          wm.Delineation:load([[DCM:]]..dataT..folderPatients[i]..[[\]]..folderVisits[j]..[[\]]..folderScans[k]..[[\]]..PtImages[l], wm.scan[1])
        end
      end
      
      -- find contours and burn
      flagContour1 = false; flagContour2 = false;
      
      wm.scan[2]:clear()
      for m = 1, wm.delineation.len do
        if string.find(wm.delineation[m-1].name, 'AD') then
          struc_1B = wm.Delineation[wm.delineation[m-1].name]
          wm.scan[2] = wm.scan[1]:burn(struc_1B, 255, true)
          flagContour1 = true
          break
        end
      end
      if flagContour1 == false then
        print("Patient "..i..[[,  ]]..folderPatients[i].." visit "..folderVisits[j].." scan "..folderScans[k]..[[AD contour not found]])
      end
      
      wm.scan[3]:clear()
      for m = 1, wm.delineation.len do
        if string.find(wm.delineation[m-1].name, 'JZ') then
          struc_1TB = wm.Delineation[wm.delineation[m-1].name]
          wm.scan[3] = wm.scan[1]:burn(struc_1TB, 255, true)
          flagContour2 = true
          break
        end
      end
      if flagContour2 == false then
        print("Patient "..i..[[,  ]]..folderPatients[i].." visit "..folderVisits[j].." scan "..folderScans[k]..[[JZ contour not found]])
      end
      
      
      if (flagContour1 == true and flagContour2 == true) then
      
        calcStats = true
        if calcStats == true then
          --Bladder stats
          --perfoms a surface distance calculation and converts to a histogram
          dist1B = field:new(); dist2B = field:new(); hist = field:new(); bladder1Dots = field:new(); bladder1Index = field:new(); bladder2Dots = field:new(); bladder2Index = field:new();
          AVS:FIELD_ISOSURFACE(wm.scan[2].data, bladder1Dots, bladder1Index, 128); AVS:FIELD_ISOSURFACE(wm.scan[3].data, bladder2Dots, bladder2Index, 128)
          AVS:SURF_DIST(bladder1Dots, bladder1Index, bladder2Dots, bladder2Index, dist1B)
          AVS:SURF_DIST(bladder2Dots, bladder2Index, bladder1Dots, bladder1Index, dist2B)
          dist1B:concat(dist2B, 1)
          
          -- performs stats
          AVS:FIELD_HIST(dist1B, hist, 0, 0, 256)
          bladder_mean = field:new(); bladder_sd = field:new()
          AVS:HISTOGRAM_STAT(hist,bladder_mean,3)  -- mean DTA
          AVS:HISTOGRAM_STAT(hist,bladder_sd,4)  -- SD of DTA
          
          -- Calculated the DSC
          DSCbladder = 0; DSCtmp = field:new()
          wm.scan[2].data:toshort(); wm.scan[3].data:toshort()
          AVS:FIELD_AND(wm.scan[2].data, wm.scan[3].data, DSCtmp)
          a = scan:new(); a.data = DSCtmp
          DSCbladder = (a:volume().value*2)/(wm.scan[2]:volume().value+wm.scan[3]:volume().value)
          
          --print("Bladder ", wm.scan[2]:volume().value, wm.scan[3]:volume().value, bladder_mean.value, bladder_sd.value, DSCbladder)
          
          -- save data to file
         
          if headerFlag == true then
            --header
            file:write([[Pt,visit,scan,AD,JZ,DTAmean,DTAsd,DSC]].."\n")
            headerFlag = false
            
          end
          
          file:write(folderPatients[i]..[[,]]..folderVisits[j]..[[,]]..folderScans[k]..[[,]]..wm.scan[2]:volume().value..[[,]]..wm.scan[3]:volume().value..[[,]]..bladder_mean.value..[[,]]..bladder_sd.value..[[,]]..DSCbladder.."\n")
        end
        
         -- save files for radiomics analysis
        saveNii = false
        if saveNii == true then
          radiomicsOutput = [[D:\data\Sarcoma\sarcomaRadiomics\radiomics\]]
          os.execute('mkdir '..radiomicsOutput..folderPatients[i])
          os.execute('mkdir '..radiomicsOutput..folderPatients[i]..[[\]]..folderVisits[j]..[[_]]..folderScans[k])
          
          -- need binary masks 1 and 0
          wm.scan[2] = wm.scan[2]/255; wm.scan[3] = wm.scan[3]/255; 
          
          wm.scan[1]:write_nifty(radiomicsOutput..folderPatients[i]..[[\]]..folderVisits[j]..[[_]]..folderScans[k]..[[\]]..folderPatients[i]..[[_]]..folderVisits[j]..[[_]]..folderScans[k]..[[_image.nii]])
          
          wm.scan[2]:write_nifty(radiomicsOutput..folderPatients[i]..[[\]]..folderVisits[j]..[[_]]..folderScans[k]..[[\]]..folderPatients[i]..[[_]]..folderVisits[j]..[[_]]..folderScans[k]..[[_AD.nii]])
          wm.scan[3]:write_nifty(radiomicsOutput..folderPatients[i]..[[\]]..folderVisits[j]..[[_]]..folderScans[k]..[[\]]..folderPatients[i]..[[_]]..folderVisits[j]..[[_]]..folderScans[k]..[[_JZ.nii]])
         
         
         ProcessMessages()
         collectgarbage()
        end
      
      end
    end
  end
end

io.close(file)  

print("Script finished")