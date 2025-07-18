# Custom input
input_data = """1
2
3
2024"""
input_data = input_data.split('\n')


# Input from file
input_data = open("input.txt").read().split('\n')
input_data.pop()


# Formatting

secret_numbers = list(map(int, input_data))


# Functions

def computeNextSecret(secret):
    # 1st step
    secret = (secret ^ (secret * 64)) % 16777216

    # 2nd step
    secret = (secret ^ (secret // 32)) % 16777216

    # 3rd step
    secret = (secret ^ (secret * 2048)) % 16777216

    return secret

def getSequencePrices(secret, steps):
    sequence_prices = {}
    sequence = []

    for _ in range(steps):
        new_secret = computeNextSecret(secret)

        # build the sequence
        if len(sequence) < 4:
            sequence.append(new_secret % 10 - secret % 10)
        else:
            sequence = sequence[1:] + [new_secret % 10 - secret % 10]

        # update the prices if necessary
        if len(sequence) == 4 and tuple(sequence) not in sequence_prices:
            sequence_prices[tuple(sequence)] = new_secret % 10
            
        secret = new_secret
    
    return sequence_prices

def findBestSequence(secrets, steps):
    all_sequence_prices = {secret: getSequencePrices(secret, steps) for secret in secrets}
    prices = {}

    # iterate over all sequence prices for each secret number
    for sequence_prices in all_sequence_prices.values():
        
        # add each prices to the total
        for sequence, price in sequence_prices.items():
            if sequence not in prices:
                prices[sequence] = price
            else:
                prices[sequence] += price

    return max(prices.items(), key= lambda x: x[1])


# Code

print(findBestSequence(secret_numbers, 2000))
