import random

def generate_random_number(length: int, to_text: bool) -> str|None:
    result = ""
    for i in range(length):
        result += str(random.randint(0, 9))
    if to_text:
        with open("data.txt", "w") as file:
            file.write(result)
    else:
        return result
    
generate_random_number(1000, True)

# Test different chunk separation functions

# Reference
def to_hex_chunks(decimal_str: str, chunk_size: int) -> list:
        """Convert decimal string to hex chunks"""
        # Convert to single hex string first
        hex_str = hex(int(decimal_str))[2:]  # remove '0x' prefix
        # Pad to multiple of chunk_size
        pad_len = (-len(hex_str)) % chunk_size
        hex_str = '0' * pad_len + hex_str
        # Split into chunks
        return [hex_str[i:i + chunk_size] 
                for i in range(0, len(hex_str), chunk_size)]

def to_base_chunks(decimal_str: str, chunk_size: int, base: int) -> list:
    """Convert decimal string to chunks in the specified base"""
    # Convert decimal string to integer
    decimal_value = int(decimal_str)
    
    # Convert integer to string in the specified base
    if base == 10:
        base_str = str(decimal_value)
    else:
        base_str = ''
        while decimal_value > 0:
            base_str = str(decimal_value % base) + base_str
            decimal_value //= base
    
    # Pad to multiple of chunk_size
    pad_len = (-len(base_str)) % chunk_size
    base_str = '0' * pad_len + base_str
    
    # Split into chunks
    return [base_str[i:i + chunk_size] 
            for i in range(0, len(base_str), chunk_size)]

# Example usage
print(to_base_chunks("12345678901234567890", 8, 16))  # Hexadecimal
print(to_base_chunks("12345678901234567890", 4, 2))   # Binary
print(to_base_chunks("12345678901234567890", 4, 10))  # Decimal