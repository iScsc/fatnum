class Bigint:
    # 32-bit word = 8 hex digits
    DEFAULT_CHUNK_SIZE = 8  # in hex digits
    MUL_THRESHOLD = 50   # switch to FFT-based multiplication
    
    @staticmethod
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
    
    @staticmethod
    def calculate_chunk_size(value_length: int) -> int:
        """Calculate optimal hex chunk size based on input length"""
        # Approximate number of hex digits needed
        hex_length = value_length * 4 // 10  # rough decimal to hex ratio
        if hex_length <= Bigint.DEFAULT_CHUNK_SIZE:
            return Bigint.DEFAULT_CHUNK_SIZE
        
        # Target reasonable number of chunks
        chunk_size = max(
            Bigint.DEFAULT_CHUNK_SIZE,
            min(hex_length // 1000, 16)
        )
        # Round to power of 2
        return 1 << (chunk_size - 1).bit_length()

    @staticmethod
    def compute_digits(a: 'Bigint') -> int:
        """Compute number of decimal digits in a Bigint"""
        return sum(len(chunk) * 4 for chunk in a.chunks)

    def __init__(self, value: str, chunksize: int = None):
        self.sign = 1 if value[0] != '-' else -1
        value = value.lstrip('-') # remove sign
        if chunksize is None:
            chunksize = self.calculate_chunk_size(len(value))
        self.chunksize = chunksize
        # Store as hex chunks
        self.chunks = self.to_hex_chunks(value, chunksize)

    def __str__(self):
        # Convert back to decimal for display
        hex_str = ''.join(self.chunks)
        value = str(int(hex_str, 16))
        return f'-{value}' if self.sign < 0 else value
    
    def __repr__(self):
        return f'Bigint(sign={self.sign}, chunks={self.chunks}, chunksize={self.chunksize})'
    
    def negate(self):
        self.sign *= -1
    
    def __eq__(self, other):
        if self.sign != other.sign or len(self.chunks) != len(other.chunks):
            return False
        return self.chunks == other.chunks
    
    def __ne__(self, other):
        return not self == other
    
    def __lt__(self, other):
        if self.sign != other.sign:
            return self.sign < other.sign
        if len(self.chunks) != len(other.chunks):
            return len(self.chunks) < len(other.chunks)
        return self.chunks < other.chunks
    
    def __le__(self, other):
        return self < other or self == other
    
    def __gt__(self, other):
        return not self <= other
    
    def __ge__(self, other):
        return not self < other

    def __abs__(self):
        """Return absolute value"""
        result = Bigint('0', self.chunksize)
        result.chunks = self.chunks.copy()
        result.sign = 1
        return result
    
    def __neg__(self):
        result = Bigint('0', self.chunksize)
        result.chunks = self.chunks.copy()
        result.sign = -self.sign
        return result
    
    # Implement addition, subtraction, multiplication, division

    @staticmethod
    def add(a: 'Bigint', b: 'Bigint') -> 'Bigint':
        """Add two positive Bigint objects"""
        if a.chunksize != b.chunksize:
            raise ValueError("Chunk sizes must match")
        
        # Pad shorter number
        max_len = max(len(a.chunks), len(b.chunks))
        chunks1 = ['0' * a.chunksize] * (max_len - len(a.chunks)) + a.chunks
        chunks2 = ['0' * b.chunksize] * (max_len - len(b.chunks)) + b.chunks
        
        result = []
        carry = 0
        
        # Process right to left
        for c1, c2 in zip(reversed(chunks1), reversed(chunks2)):
            chunk_sum = int(c1, 16) + int(c2, 16) + carry
            carry = chunk_sum >> (4 * a.chunksize)
            chunk_value = chunk_sum & ((1 << (4 * a.chunksize)) - 1)
            result.insert(0, f'{chunk_value:0{a.chunksize}x}')
        
        if carry:
            result.insert(0, f'{carry:0{a.chunksize}x}')
        
        result_bigint = Bigint('0', a.chunksize)
        result_bigint.chunks = result
        return result_bigint

    @staticmethod
    def subtract(a: 'Bigint', b: 'Bigint') -> 'Bigint':
        """Subtract two positive Bigint objects"""
        if a.chunksize != b.chunksize:
            raise ValueError("Chunk sizes must match")
        
        # Ensure a >= b
        if a < b:
            raise ValueError("First number must be greater than or equal to second")
        
        max_len = max(len(a.chunks), len(b.chunks))
        chunks1 = ['0' * a.chunksize] * (max_len - len(a.chunks)) + a.chunks
        chunks2 = ['0' * b.chunksize] * (max_len - len(b.chunks)) + b.chunks
        
        result = []
        borrow = 0
        
        # Process right to left
        for c1, c2 in zip(reversed(chunks1), reversed(chunks2)):
            chunk1 = int(c1, 16)
            chunk2 = int(c2, 16) + borrow
            
            if chunk1 < chunk2:
                chunk1 += (1 << (4 * a.chunksize))
                borrow = 1
            else:
                borrow = 0
                
            chunk_diff = chunk1 - chunk2
            result.insert(0, f'{chunk_diff:0{a.chunksize}x}')
        
        # Remove leading zeros
        while len(result) > 1 and result[0] == '0' * a.chunksize:
            result.pop(0)
        
        result_bigint = Bigint('0', a.chunksize)
        result_bigint.chunks = result
        return result_bigint

    def __add__(self, other):
        """Add two BigInt numbers handling signs"""
        if not isinstance(other, Bigint):
            raise TypeError("Unsupported operand type")

        if self.sign == other.sign:
            # Same signs: add absolute values and keep sign
            result = Bigint.add(abs(self), abs(other))
            result.sign = self.sign
            return result
        else:
            # Different signs: subtract absolute values
            a, b = abs(self), abs(other)
            if a >= b:
                # |self| >= |other|
                result = Bigint.subtract(a, b) 
                result.sign = self.sign
            else:
                # |self| < |other| 
                result = Bigint.subtract(b, a)
                result.sign = other.sign
            return result

    def __sub__(self, other):
        """Subtract two BigInt numbers handling signs"""
        if not isinstance(other, Bigint):
            raise TypeError("Unsupported operand type")

        if self.sign == other.sign:
            # Same signs
            if abs(self) >= abs(other):
                # |self| >= |other|
                result = Bigint.subtract(self, other)
                result.sign = self.sign
            else:
                # |self| < |other|
                result = Bigint.subtract(other, self)
                result.sign = -self.sign
        else:
            # Different signs: add absolute values
            result = Bigint.add(self, other)
        # TODO Implement addition and subtraction for cases where one operand is a non-Bigint integer
        return result

    @staticmethod
    def karatsuba(a: 'Bigint', b: 'Bigint') -> 'Bigint':
        """Karatsuba multiplication for Bigint objects"""
        # Base case
        if len(a.chunks) <= 2 or len(b.chunks) <= 2:
            # Convert chunks to integers safely
            a_val = int(''.join(a.chunks), 16)
            b_val = int(''.join(b.chunks), 16)
            product = a_val * b_val
            
            # Convert back to Bigint maintaining chunk size
            result = Bigint(str(product), a.chunksize)
            result.sign = a.sign * b.sign
            return result

        # Make numbers same length
        n = max(len(a.chunks), len(b.chunks))
        if n % 2:  # Ensure even length
            n += 1
        n2 = n // 2

        # Split numbers
        def split_number(num, n, n2):
            padded = ['0' * num.chunksize] * (n - len(num.chunks)) + num.chunks
            high = Bigint('0', num.chunksize)
            high.chunks = padded[:n2]
            low = Bigint('0', num.chunksize)
            low.chunks = padded[n2:]
            return high, low

        a_high, a_low = split_number(a, n, n2)
        b_high, b_low = split_number(b, n, n2)

        # Recursive steps
        z0 = Bigint.karatsuba(a_low, b_low)  # low * low
        z2 = Bigint.karatsuba(a_high, b_high)  # high * high

        # (a_high + a_low) * (b_high + b_low) - z2 - z0
        sum1 = a_high + a_low
        sum2 = b_high + b_low
        z1 = Bigint.karatsuba(sum1, sum2) - z2 - z0

        # Combine results: z2 * BASE^(2*n2) + z1 * BASE^n2 + z0
        result = z2
        for _ in range(2 * n2):
            result = Bigint.left_shift_by_base(result)
        
        temp = z1
        for _ in range(n2):
            temp = Bigint.left_shift_by_base(temp)
        
        result = result + temp + z0
        result.sign = a.sign * b.sign
        
        # Remove leading zeros
        while len(result.chunks) > 1 and result.chunks[0] == '0' * result.chunksize:
            result.chunks.pop(0)
            
        return result

    @staticmethod 
    def left_shift_by_base(a: 'Bigint', amount: int = 1) -> 'Bigint':
        """Shift left by multiplying by BASE (effectively adding a '0' chunk)"""
        if amount <= 0:
            return a
        result = Bigint('0', a.chunksize)
        result.chunks = a.chunks + ['0' * a.chunksize] * amount
        result.sign = a.sign
        return result

    @staticmethod
    def schonhage_strassen(a: 'Bigint', b: 'Bigint') -> 'Bigint':
        """
        Implement Schönhage-Strassen multiplication algorithm for large integers
        """
        return Bigint.karatsuba(a, b)

    def __mul__(self, other):
        """Multiply two BigInt numbers"""
        if not isinstance(other, Bigint):
            raise TypeError("Unsupported operand type")
        
        if len(self.chunks) < Bigint.MUL_THRESHOLD or len(other.chunks) < Bigint.MUL_THRESHOLD:
            # Use Toom-Cook or Karatsuba for small numbers
            return Bigint.karatsuba(self, other)
        else:
            # Use FFT-based multiplication for large numbers
            return Bigint.schonhage_strassen(self, other)
    
if __name__ == "__main__":
    # Test Schönhage-Strassen multiplication on big numbers with 50 digits
    a = Bigint('1234' * 20)
    b = Bigint('5678' * 20)
    value_a = int(str(a))
    value_b = int(str(b))
    result_karatsuba = a * b
    value_result = int(str(result_karatsuba))
    print(f"Karatsuba: {value_a} * {value_b} = {value_result}")
    print(f"Expected: {value_a * value_b}")
    assert value_result == value_a * value_b