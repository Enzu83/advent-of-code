// Advent of Code 2022

#include <limits.h>
#include <stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void solve(FILE *input) {
    int calories = 0;
    int max_calories[3];

    char *line = NULL;
    size_t length = 0;
    ssize_t read;
    while ((read = getline(&line, &length, input)) != -1) {
        // reset calories count to 0 when the serie of calories ends
        if (strcmp(line, "\n") == 0) {
            // shift values when a new maximum is gotten
            if (max_calories[0] < calories) {
                max_calories[2] = max_calories[1];
                max_calories[1] = max_calories[0];
                max_calories[0] = calories;
            } else if (max_calories[1] < calories) {
                max_calories[2] = max_calories[1];
                max_calories[1] = calories;
            } else if (max_calories[2] < calories) {
                max_calories[2] = calories;
            }
            // reset the calories counter
            calories = 0;
        } else {
            // increase the calories counter
            calories += atoi(line);
        }
    }

    printf("Part one: %d\n", max_calories[0]);
    printf("Part two: %d\n", max_calories[0] + max_calories[1] + max_calories[2]);
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
