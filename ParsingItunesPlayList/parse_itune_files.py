import plistlib
import numpy as np
import matplotlib as pyplot


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

def findCommonTracks(fileNames):
    # a list of a set of track names
    trackNameSets = []
    for fileName in fileNames:
        # create a new set
        trackNames = set()
        # read in playlist
        plist = plistlib.readPlist(fileName)
        # get tracks
        tracks = plist['Tracks']
        # iterate through tracks
        for trackId, track in tracks.items():
            try:
                # add the track name to a set
                trackNames.add(track['Name'])
            except:
                # ignore
                pass
        # add to list
        trackNameSets.append(trackNames)
    # get the set of common tracks
    commonTracks = set.intersection(*trackNameSets)
    # write to file
    if len(commonTracks) > 0:
        common_tracks_file_handle = open("common_tracks.txt", "w")
        for value in commonTracks:
            value_string = f"{value}\n"
            common_tracks_file_handle.write(value_string.encode("UTF-8"))
        common_tracks_file_handle.close()
        print(f"{len(commonTracks)} common tracks found. Track names written to common_tracks.txt.")
    else:
        print("No common tracks!")


def plotStats(fileName):
    # read in a playlist
    plist = plistlib.readPlist(fileName)
    # get the tracks from the playlist
    tracks = plist['Tracks']
    ratings = []
    durations = []
    # iterate through the tracks
    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            # ignore
            pass
    # ensure that valid data was collected.
    if ratings == [] or durations == []:
        print(f"No valid Album Rating/Total Time data in {fileName}.")
        return
    
    # scatter plot
    x_axis_values = np.array(durations, np.int32)
    # convert to minutes
    x_axis_values = x_axis_values / 60000.0
    y_axis_values = np.array(ratings, np.int32)
    pyplot.subplot(2,1,1)
    pyplot.plot(x_axis_values, y_axis_values, 'o')
    pyplot.axis([0, 1.05*np.max(x_axis_values), -1, 110])
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Track rating')

    # plot histogram
    pyplot.subplot(2, 1, 2)
    pyplot.hist(x_axis_values, bins = 20)
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Count')

    # show plot
    pyplot.show()

