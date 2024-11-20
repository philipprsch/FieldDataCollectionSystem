#include "LoggingDevice.h"
#pragma once


int splitCharArrayIntoMultiple(const char* input, char** outputArray, int maxParts, char delimiter) {
    int partIndex = 0;
    const char* currentPosition = input;
    char* token = nullptr;

    // Use strtok to tokenize the input string based on the delimiter
    while ((token = strtok_r((char*)currentPosition, &delimiter, (char**)&currentPosition)) != nullptr && partIndex < maxParts) { //Added (char**)
        strcpy(outputArray[partIndex], token); // Copy the token to the output array
        partIndex++;
    }

    // If there are fewer parts than maxParts, clear the remaining output buffers
    for (int i = partIndex; i < maxParts; i++) {
        outputArray[i][0] = '\0'; // Clear remaining buffers
    }
    return partIndex; // Return the number of parts found
}

//#include <cstring> // For strlen and strcpy

void splitCharArrayIntoTwo(const char* input, char* part1, char* part2, char delimiter) {
    int delimiterIndex = -1;

    // Find the position of the delimiter in the input
    for (int i = 0; i < strlen(input); i++) {
        if (input[i] == delimiter) {
            delimiterIndex = i;
            break;
        }
    }

    // If delimiter is found, split the array into two parts
    if (delimiterIndex != -1) {
        // Copy the first part into part1
        strncpy(part1, input, delimiterIndex);
        part1[delimiterIndex] = '\0'; // Null-terminate part1

        // Copy the second part into part2
        strcpy(part2, &input[delimiterIndex + 1]); // Skip the delimiter
    } else {
        // If delimiter is not found, copy the whole input into part1
        strcpy(part1, input);
        part2[0] = '\0'; // Clear part2 if delimiter is not found
    }
}

extern int __heap_start, *__brkval;
int freeMemory() {
    int v;
    return (int)&v - (__brkval == 0 ? (int)&__heap_start : (int)__brkval);
}

