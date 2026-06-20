import whisper 
import sys
import io
import string
#import clip_video


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def transcribeVid(video_path: str):
    model = whisper.load_model("base")
    # whisper has different model specifications depending on what you want to do. won't put them all here but base is just to test, may need small or medium

    #Transcribe video file
    result = model.transcribe(video_path, temperature=0) #temperature can't be higher than 1.0(max randomness)
    
    return result["segments"] 

def wordMatch(segments, target_word):
    puncStrip = target_word.translate(str.maketrans('', '', string.punctuation))

    matches = []

    for segment in segments: # Whisper can return segments as dicts or namedtuples depending on version
        if isinstance(segment, dict):# This handles both formats to prevent TypeError on string indexing 
            # Dictonary format: access with bracket 
            text = segment['text']
            start = segment['start']
            end = segment['end']
        else:
            # Namedtuple format: access with dot
            text = segment.text
            start = segment.start
            end = segment.end
    if puncStrip.lower() in text.lower():
            matches.append({"start": start, "end": end})
            
    return matches 





#Testing block
""" if __name__ == "__main__": #same as func main() in Go
    video_file = "testvideo.mp4"

    print("Loading model...")
    segments = transcribeVid(video_file)
    matches = wordMatch(segments, "friends!")

    # if matches :
    #     clip_video.clipMatches("testvideo.mp4", matches, "outputmix.mp4")
    # else:
    #     print("No matches found")
    # print(f"Found {len(segments)} segments.")
    
    print()

    for i, segment in enumerate(segments):
        print(f"Segment {i}:")
        print(f"    Start:{segment['start']}s")
        print(f"    End:{segment['end']}s")
        print(f"    Text:{segment['text']}")
        print("-" * 30) 

    print() 
print(f"Found {len(matches)} matches: {matches}")  """


