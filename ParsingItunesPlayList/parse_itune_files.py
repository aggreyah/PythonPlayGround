import plistlib
def findDuplicates(fileName):
    print(f"Finding duplicate files in {fileName}...")
    #read in a playlist
    plist = plistlib.readPlist(fileName)
    #get the tracks from the tracks dictionary
    tracks = plist['Tracks']
    #create a track name dictionary
    trackNames = {}
    #iterate through the tracks
    for trackId, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            #look for existing entries
            if name in trackNames:
                #if name and duration match, increament the count
                #round the track length to the nearest second
                if duration // 1000 == trackNames[name][0] // 1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count + 1)
                else:
                    #add dictionary entry as a tuple (duration, count)
                    trackNames[name] = (duration, 1)
        except:
            #ignore
            pass
    
    #store duplicates as (name, count) tuples
    duplicates = []
    for key, value in trackNames.items():
        if value[1] > 1:
            duplicates.append((value[1], key))

    #save duplicates to a file
    if len(duplicates) > 0:
        print(f"Found {len(duplicates)} duplicates. Track names saved to dup.txt")
    else:
        print("No duplicate tracks found!")

    duplicates_file = open("duplicates_file.txt", "w")
    for value in duplicates:
        duplicates_file.write(f"{value[0]} {value[1]}\n")
    duplicates_file.close()