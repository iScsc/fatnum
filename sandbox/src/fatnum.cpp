#ifndef FATNUM_H
#define FATNUM_H

#include <iostream>
#include <cmath>
#include <vector>
#include <string>
#include <sstream>
#include <limits.h>

using namespace std;

/**
 * Specs for the FatNum class:
 * - FatNum is a class that represents a very large integer and implements basic arithmetic operations.
 * - The class should be able to handle integers of any size by using a datastructure to store hexadicimal chunks stored as strings of the number.
 * - The class should be able to handle negative numbers and provides the following fiels :
 * - A integer to handle the sign of the number : 1 for positive, 0 for negative
 * - A vector of strings to store the hexadicimal chunks of the number
 * - A chunksize integer that defines the size of the chunks associated with a default value of 8
 */

constexpr int DEFAULT_CHUNK_SIZE = 8;

class FatNum {
    private:
        int sign; // 1 for positive, 0 for negative
        vector<string> chunks;
        int chunkSize;
        int length;
    public:
        // Constructors
        FatNum() : sign(1), chunkSize(DEFAULT_CHUNK_SIZE), length(0) {}; // Default constructor
        // TODO: Implement the following methods : fromInt, fromString to be used in the constructors
        FatNum(const string& num); // Constructor with string argument
        FatNum(const int num); // Constructor with int argument -> better approach for relatively small numbers -> use limits.h to get INT_MAX and INT_MIN
        FatNum(const string& num, const int chunkSize); // Constructor with string and chunkSize arguments
        FatNum(const int num, const int chunkSize); // Constructor with int and chunkSize arguments

        // Destructor
        // TODO: to be modified if dynamic memory is used
        ~FatNum() {};

        // Getters
        int getSign() const { return sign; };
        vector<string> getChunks() const { return chunks; };
        int getChunkSize() const { return chunkSize; };
        int getLength() const { return length; };

        // Setters
        void setSign(const int sign) { this->sign = sign; };
        void setChunks(const vector<string>& chunks) { this->chunks = chunks; };
        void setChunkSize(const int chunkSize) { this->chunkSize = chunkSize; };
        void setLength(const int length) { this->length = length; };

        // Methods
        string toString(FatNum n) const;
        // TODO: Modify return type after implementation
        int toInt(FatNum n) const; // Returns the integer value of the FatNum if FatNum is small enough to fit in an int

        // Construction specific methods
        vector<string> toHexChunks(const string& decimalStr, int chunkSize);
};

// By default, we use the default chunk size
// TODO: check how to improve for very very large numbers because memory will be a problem
std::vector<std::string> toHexChunks(const std::string& decimalStr, int chunkSize) {
    // Convert decimal string to integer
    unsigned long long decimalValue = std::stoull(decimalStr);

    // Convert integer to hexadecimal string
    std::stringstream ss;
    ss << std::hex << decimalValue;
    std::string hexStr = ss.str();

    // Pad to multiple of chunkSize
    int padLen = (chunkSize - hexStr.length() % chunkSize) % chunkSize;
    hexStr.insert(0, padLen, '0');

    // Split into chunks
    std::vector<std::string> chunks;
    for (size_t i = 0; i < hexStr.length(); i += chunkSize) {
        chunks.push_back(hexStr.substr(i, chunkSize));
    }

    return chunks;
}

#endif // FATNUM_H