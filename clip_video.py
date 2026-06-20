from moviepy import VideoFileClip, concatenate_videoclips

def clipMatches(videoPath, matches, outputPath, buffer=0.5):
    if not matches:
        print("No matches found. No sorcery here")
        return
    print("Loading video...")
    originalClip = VideoFileClip(videoPath)

    clips = []

    for match in enumerate(matches):
        start = max(0, match['start'] - buffer)
        end = match['end'] + buffer

        #make sure it stays in video bounds
        if end > originalClip.duration:
            end = originalClip.duration

        #create subclip
        subclip = originalClip.subclipped(start, end)
        clips.append(subclip)

    print(f"Putting {len(clips)} clips together...")
    finalClip = concatenate_videoclips(clips)

    finalClip.write_videofile(outputPath, codec='libx264', audio_codec = 'aac')
    print(f"Writing output to {outputPath}")

    finalClip.close()
    originalClip.close()
    print("Fin")

