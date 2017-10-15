import wave
import os
import audioop
import logging

# input file
filepath = None

# output base directory
tempDir = None

validAudio = False

# Open file
audio = wave.open(filepath, 'rb')
print("Input Audio file")
print("Channels:\t\t" + str(audio.getnchannels()))
print("Samplerate:\t\t" + str(audio.getframerate()))
print("Sample Width:\t" + str(audio.getsampwidth()))


# Check if wave file needs processing
if audio.getnchannels() == 1 and audio.getframerate() == 8000:
    validAudio = True
    audio.close()
    print("Test Passed: %s" % os.path.basename(filepath))

# Process the file
if not validAudio:
    try:
        tempWav = wave.open(os.path.join(tempDir, os.path.basename(filepath)), 'wb')
        tempWav.setframerate(8000)
        tempWav.setnchannels(1)
        tempWav.setsampwidth(2)
        n_frames = audio.getnframes()
        data = audio.readframes(n_frames)
    except:
        logging.exception("Failed to read file.")
        # continue

    try:
        converted = audioop.ratecv(data, 2, audio.getnchannels(), audio.getframerate(), 8000, None)
        if audio.getnchannels() != 1:
            converted = audioop.tomono(converted[0], 2, 0.5, 0.5)
            tempWav.writeframes(converted)
        else:
            tempWav.writeframes(converted[0])
    except:
        logging.exception("Failed to downsample.")
        # continue

    print("Processed File")
    print("Channels:\t\t" + str(tempWav.getnchannels()))
    print("Samplerate:\t\t" + str(tempWav.getframerate()))
    print("Sample Width:\t" + str(tempWav.getsampwidth()))

    try:
        print("Processed File: " + os.path.basename(filepath))
        audio.close()
        tempWav.close()
    except:
        logging.exception("Failed to close files")
        # continue
