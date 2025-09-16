// Advent of Code 2022

#include <stdio.h>
#include <stdlib.h>

void solve(FILE *input) {
    char *line = NULL;
    size_t length = 0;
    ssize_t read;
    while ((read = getline(&line, &length, input)) != -1) {
        /* write solution here */
    }
}

int main(int argc, char *argv[]) {
    // open the input file
    FILE *input = fopen("input.txt", "r");
    if (!input) {
        printf("Input file not found.\n");
        return -1;
    }

    // print the solution
    solve(input);
    
    fclose(input);

    return 0;
}
