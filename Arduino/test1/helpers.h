#include "LoggingDevice.h"
#pragma once

//outputArray was String *outputArray, changed for testing
int splitString(String data, char delimiter, String outputArray[], int maxItems) {
  int start = 0;
  int end;
  int itemCount = 0;

  while ((end = data.indexOf(delimiter, start)) >= 0) {
    if (itemCount < maxItems) {
      outputArray[itemCount++] = data.substring(start, end);
      start = end + 1;
    } else {
      break;
    }
  }

  // Add the last element if there’s any remaining data
  if (start < data.length() && itemCount < maxItems) {
    outputArray[itemCount++] = data.substring(start);
  }

  return itemCount; // Return the number of items
}

void splitStringTwo(const String &input, char delimiter, String &part1, String &part2) {
    int delimiterIndex = input.indexOf(delimiter);

    if (delimiterIndex != -1) {
        // If delimiter is found, split at the delimiter
        part1 = input.substring(0, delimiterIndex);
        part2 = input.substring(delimiterIndex + 1);
    } else {
        // If delimiter is not found, store the entire string in part1, leave part2 empty
        part1 = input;
        part2 = "";
    }
}

extern int __heap_start, *__brkval;
int freeMemory() {
    int v;
    return (int)&v - (__brkval == 0 ? (int)&__heap_start : (int)__brkval);
}

