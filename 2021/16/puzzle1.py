# Custom input
input_data = """620080001611562C8802118E34"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Functions

def bin_to_str(bin_str):
    bin_str = bin_str[2:]

    while len(bin_str) < 4:
        bin_str = '0' + bin_str
    
    return bin_str

def hex_to_bin(hex_string):
    bin_string = ""

    for hex in hex_string:
        bin_string += bin_to_str(bin(int(hex, 16)))
    
    return bin_string

def read_literal_value(packet):
    value_bin = ""

    index = 0

    while index < len(packet):
        value_bin += packet[index+1:index+5]

        if packet[index] == '0': # First bit is 0 => Stop reading
            index += 5
            break

        index += 5

    return index, int(value_bin, 2)

def decode_packet(packet, versions, values):
    if len(packet) > 0 and int(packet, 2) != 0:
        print('')
        print(packet)

        version, type_ID = int(packet[:3], 2), int(packet[3:6], 2)
        print(f"Version: {version}, Type ID: {type_ID}")

        versions.append(version)

        if type_ID == 4: # Literal value
            length, value = read_literal_value(packet[6:]) # Remove header
            print("Literal value", value)

            values.append(value)

            decode_packet(packet[6+length:], versions, values)

        else: # Operator
            length_type_ID = packet[6]

            if length_type_ID == '0': # Sub-packets contained by the packet
                length_sub_packet = int(packet[7:22], 2) # Next 15 bits
                print("Sub packet length", length_sub_packet)

                decode_packet(packet[22:22+length_sub_packet], versions, values) # Decode the sub package

                decode_packet(packet[22+length_sub_packet:], versions, values)

            else: # Sub-packets immediately contained
                nb_sub_packets = int(packet[7:18], 2) # Next 11 bits

                print("Sub packet number", nb_sub_packets)

                decode_packet(packet[18:], versions, values)
                

# Code


packet = hex_to_bin(input_data[0])

versions = []
values = []

decode_packet(packet, versions, values)

print('')
print(f"Versions: {versions}")
print(f"Total: {sum(versions)}")
#print(f"Values: {values}")


