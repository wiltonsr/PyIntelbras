from datetime import datetime

from .exceptions import IntelbrasAPIException


def parse_response(s: str) -> dict:
    # Helper function to try convert types
    def convert_value(value):
        # Check for null or None values
        if value.lower() in ('null', 'none'):
            return None

        # Try to convert to int
        try:
            return int(value)
        except ValueError:
            pass

        # Try to convert to float
        try:
            return float(value)
        except ValueError:
            pass

        # Try to convert to boolean
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'

        # Try to convert to datetime
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass

        # Return the value as string if no conversion is possible
        return value

    # Initialize the dictionary
    result = {}

    # Split the string into lines, handling various line breaks and spaces
    lines = [line.strip() for line in s.splitlines() if line.strip()]

    try:
        # Process each line
        for line in lines:
            # Ignore entries without '=' sign
            if '=' in line:
                # Split the line at '=' to separate the path from the value
                path, value = line.split('=', 1)
                # Try convert the value to the appropriate type
                value = convert_value(value.strip())
            else:
                path, value = line, None

            # Split the path into parts
            parts = path.split('.')

            # Initialize the current level of the dictionary
            current_level = result

            # Iterate over the parts of the path (except the last one)
            for part in parts[:-1]:
                # Check if the part contains a list index (e.g., Snap[0])
                if '[' in part and ']' in part:
                    # If it's a double index (e.g., TimeSection[0][1]), treat it as a key
                    if part.count('[') > 1:
                        # Use the entire part as the key (e.g., 'TimeSection[0][1]')
                        key = part
                        if key not in current_level:
                            current_level[key] = {}
                        current_level = current_level[key]
                    else:
                        # Handle single index (e.g., Snap[0])
                        key, index = part.split('[')
                        # Remove the ']' and convert to integer
                        index = int(index.rstrip(']'))
                        if key not in current_level:
                            current_level[key] = []
                        # Ensure the list has the required size
                        while len(current_level[key]) <= index:
                            current_level[key].append({})
                        current_level = current_level[key][index]
                else:
                    # Handle regular keys
                    if part not in current_level:
                        current_level[part] = {}
                    current_level = current_level[part]

            # Add the final value
            last_part = parts[-1]
            if '[' in last_part and ']' in last_part:
                # If it's a double index (e.g., TimeSection[0][1]), treat it as a key
                if last_part.count('[') > 1:
                    # Use the entire part as the key (e.g., 'TimeSection[0][1]')
                    key = last_part
                else:
                    # Handle single index (e.g., Snap[0])
                    key, index = last_part.split('[')
                    index = int(index.rstrip(']'))
                    if key not in current_level:
                        current_level[key] = []
                    while len(current_level[key]) <= index:
                        current_level[key].append(None)
                    current_level[key][index] = value
                    continue  # Skip the assignment below
            else:
                key = last_part  # Use the part as the key

            current_level[key] = value
    except Exception as e:
        raise IntelbrasAPIException(f'Parser Response Error: {e}')

    return result
