from math import prod

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

def read_value(packet):
    bin_value = ""
    index = 0

    while index < len(packet):
        bin_value += packet[index+1:index+5]

        if packet[index] == '0': # First bit is 0 => Stop reading
            index += 5
            break

        index += 5

    return index, int(bin_value, 2)

def read_packet(packet, cursor, tree, parent=None):
    if len(packet[cursor[0]:]) >= 11: # minimal length for a packet
        #print(packet, '\n\n', cursor, f" ({packet[cursor[0]:]})", '\n\n')
        id = len(tree) # generate id for the current sub packet

        # sub packet of a packet
        if parent != None:
            tree[parent][1].add(id)
        
        # start reading the packet
        version, type_ID = int(packet[cursor[0]:cursor[0] + 3], 2), int(packet[cursor[0] + 3:cursor[0] + 6], 2) # packet info
        cursor[0] += 6

        if type_ID == 4: # the packet is contains a literal value
            length, value = read_value(packet[cursor[0]:]) # get its value and length of the sub packet
            cursor[0] += length

            tree[id] = [type_ID, value] # tree insertion : only the value for this type of packet

            return parent

        else: # the packet is an operator
            tree[id] = [type_ID, set()] # tree insertion : set of its children

            if packet[cursor[0]] == '0': # the packet contains a sub packet
                cursor[0] += 1

                sub_packet_length = int(packet[cursor[0]:cursor[0] + 15], 2) # length of the sub packet
                cursor[0] += 15
                #print(f"length {sub_packet_length}")

                next_cursor_position = cursor[0] + sub_packet_length

                while cursor[0] < next_cursor_position:
                    read_packet(packet[:next_cursor_position], cursor, tree, id) 

                return parent
            
            else: # the packet contains several sub packets
                cursor[0] += 1

                sub_packet_number = int(packet[cursor[0]:cursor[0] + 11], 2)
                cursor[0] += 11
                #print(f"number {sub_packet_number}")

                for _ in range(sub_packet_number):
                    read_packet(packet, cursor, tree, id)
                
                return parent

    else:
        cursor[0] = len(packet)

        return None
                

def decode_packet(packet):
    cursor = [0] # reading position of the packet

    # packets structure
    tree = {}
    parent = None

    while cursor[0] < len(packet):
        parent = read_packet(packet, cursor, tree, parent)

    return tree

def get_packet_value(tree, current_sub_packet=0):
    type_ID = tree[current_sub_packet][0]
    value = tree[current_sub_packet][1]

    #print(type_ID, value)

    if isinstance(value, int): # Literal value
        return value
    else:
        next_values = [get_packet_value(tree, next_sub_packet) for next_sub_packet in value]

        if type_ID == 0: # Sum
            return sum(next_values)
        
        elif type_ID == 1: # Product
            return prod(next_values)
        
        elif type_ID == 2: # Min
            return min(next_values)
        
        elif type_ID == 3: # Max
            return max(next_values)
        
        elif type_ID == 5: # Greater than
            return int(next_values[0] > next_values[1])

        elif type_ID == 6: # Less than
            return int(next_values[0] < next_values[1])
        
        elif type_ID == 7: # Equal to
            return int(next_values[0] == next_values[1])



# Code


packet = hex_to_bin(input_data[0])

tree = decode_packet(packet)

print('')
print(tree)

pakcet_value = get_packet_value(tree)
print(f"Packet value: {pakcet_value}")

assert get_packet_value(tree) == 539051801941 