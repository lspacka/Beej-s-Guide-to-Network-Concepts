# p.48 y 55
# https://chatgpt.com/share/68acc8c7-5080-8005-b78c-96ee6bf1382b

import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2
BYTES = 5

def usage():
    print("usage: wordclient.py server port", file=sys.stderr)

packet_buffer = b''

# Return the next word packet from the stream.
# The word packet consists of the encoded word length followed by the
# UTF-8-encoded word.
# Returns None if there are no more words, i.e. the server has hung up.
def get_next_word_packet(s):
    global packet_buffer

    while True:
        # if buffer starts with a complete packet
        if len(packet_buffer) >= WORD_LEN_SIZE:
            length = int.from_bytes(packet_buffer[:WORD_LEN_SIZE], 'big')

            if len(packet_buffer) >= WORD_LEN_SIZE + length:
                # extract the packet data
                packet = packet_buffer[:WORD_LEN_SIZE+length]
                # strip the packet data off the front of the buffer
                packet_buffer = packet_buffer[WORD_LEN_SIZE+length:]
                return packet
            
        data = s.recv(BYTES)
        if not data:
            s.close()
            return None
        packet_buffer += data

def extract_word(word_packet):
    word_packet = word_packet[WORD_LEN_SIZE:]
    word_packet = word_packet.decode()

    return word_packet

# Do not modify:

def main(argv):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    print("Getting words:")

    while True:
        word_packet = get_next_word_packet(s)

        if word_packet is None:
            break

        word = extract_word(word_packet)
        
        print(f"    {word}")
        
    s.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))