import streamlit as st
import tempfile
import transcribe
from moviepy import VideoFileClip, concatenate_videoclips
import os



st.title("Sorcery")

uploadedFiles = st.file_uploader("Upload videos", accept_multiple_files=True, type="mp4")#figure out how to change 200mb message

st.info("Max file size 50MB per video. Processing time may vary")

targetWord = st.text_input("Enter your target word")

if uploadedFiles:
    maxSize = 50 * 1024 * 1024 #50MB in bytes

    for f in uploadedFiles:
        if f.size > maxSize:
            st.error(f"'{f.name}' is too large - ({f.size / 1024 / 1024:.1f}MB). Max 50MB")
            st.stop()

if st.button("Complie Video") and uploadedFiles and targetWord:
    allClips = []
    tempPathsRemoval = []
    newTempPaths = [] #to hold subclips so orginal tempfiles can be closed, was otherwise getting valueerror: i/o operation on closed file 

    progressBar = st.progress(0)

    totalFiles = len(uploadedFiles)

    for i, uploadedFile in enumerate(uploadedFiles):
        #Save to temp location to process
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp: #with is semantically equivalent to try -> expect -> finally. encapsulated for convenient reuse. however it is only used here to ensure the file handle is closed 
            tmp.write(uploadedFile.read())
            tempPath = tmp.name
            tempPathsRemoval.append(tempPath)
        try:
            #process
            segments = transcribe.transcribeVid(tempPath)
            matches = transcribe.wordMatch(segments, targetWord)

            if matches: #load clips
                tempClips = []
                for match in matches:
                    clip = VideoFileClip(tempPath)
                    subclip = clip.subclipped(max(0, match['start']) - 0.5, match['end'] + 0.5)

                    newTempFile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") #subclip to new temp file to break dependency on original - part of valueerror:  i/o problem
                    newTempPath = newTempFile.name
                    newTempFile.close()

                    subclip.write_videofile(newTempPath, codec='libx264', audio_codec='aac')

                    subclip.close()
                    clip.close() # explicitly close original clip to release OS handle 
                    
                    newTempPaths.append(newTempPath)
                    allClips.append(newTempPath)

            progressBar.progress((i + 1) / totalFiles)

        except Exception as e:

            st.error(f"Error prcessing {uploadedFile.name} : {e}")

            if os.path.exists(tempPath):
                os.remove(tempPath)
    
    if allClips:
        st.write("Combining clips...")
        finalClips = [VideoFileClip(path) for path in allClips]
        finalClip = concatenate_videoclips(finalClips) #passing strings causes attributeerror: 'str' object has no attribute 'duration'
        finalClip.write_videofile("clippy.mp4", codec='libx264', audio_codec='aac')

        for c in finalClips:
            c.close() #close individual clips
        finalClip.close() #clean up clips

        with open("clippy.mp4", "rb") as file:
            st.download_button("Download video", file, "clippy.mp4")

        
        #temp files were initially deleted in the finally block, however that stopped me from using the same video multiple times. now all temp files are deleted here
        for path in tempPathsRemoval + newTempPaths:
            try:
                if os.path.exists(path):
                    os.remove(path)  
            except OSError as e:
                st.warning(f"{e}")
    else:
        st.error("No matches found")
        for path in tempPathsRemoval:
            if os.path.exists(path):
                os.remove(path)