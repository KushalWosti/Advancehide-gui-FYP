import wave
import sys
def enc_sound(audio_scr1,cipher_msg):
    # read wave audio file
    with wave.open(audio_scr1, 'rb') as song:
        # Reading the frames and converting it into byte array
        frame_bytes = bytearray(list(song.readframes(song.getnframes())))
        # Appending dummy data to fill remaining bytes.
        secret_msg = cipher_msg + int((len(frame_bytes)-(len(cipher_msg)*8*8))/8) *'#'
        # Converting text into bit array
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in secret_msg])))
        # Replace LSB of each byte of the audio data by one bit from the text bit array
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 254) | bit
        # Get the modified bytes
        frame_modified = bytes(frame_bytes)
        return song, frame_modified

    # Write bytes to a new wave audio file
    with wave.open(audio_scr1, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)

def dec_sound(audio_scr2):
    song = wave.open(audio_scr2, mode='rb')
    # Converting audio to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    # Extract the LSB of each byte
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    # Convert byte array back to string
    string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
    # Cut off at the filler characters
    decoded = string.split("###")[0]
    return decoded