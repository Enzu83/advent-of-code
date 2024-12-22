# Custom input
input_data = """1
10
100
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

def sumSecretsAfterSteps(secrets, steps):
    for _ in range(steps):
        for i, secret in enumerate(secrets):
            secrets[i] = computeNextSecret(secret)
    
    return sum(secrets)


# Code

print(sumSecretsAfterSteps(secret_numbers, 2000))
