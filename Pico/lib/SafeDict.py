
class IndexOutOfRange(Exception):
    """Raised when attempting to access an out-of-bounds index in a list."""
    pass

class InvalidAccess(Exception):
    """Raised when trying to access beyond the structure of the JSON data."""
    pass


class SafeDict:
    def __init__(self, dict):
        self.data = dict
    
    def get(self, *keys, fb=None): #fb is Fallback
        value = self.data
        for key in keys:
            if isinstance(value, dict):
                if key not in value:
                    return fb  # Return the specified fallback if the key is not found
                value = value[key]
            elif isinstance(value, list):
                if not isinstance(key, int) or key < 0 or key >= len(value):
                    raise IndexOutOfRange("Index out of range for SafeDict list.")
                value = value[key]
            else:
                raise InvalidAccess("Cannot access further into a non-dict/non-list value.")
        return value
    
    
