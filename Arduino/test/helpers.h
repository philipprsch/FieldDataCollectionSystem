#include "LoggingDevice.h"
#pragma once
int splitString(String data, char delimiter, String *outputArray, int maxItems) {
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

