/**
 * @file hdinfo.hpp
 * @brief Header file for the HardwareInfo class and related functions which provide information about the hardware on which the program is running.
 * @author Nicolas Lesquoy
 */

#ifndef HDINFO_H
#define HDINFO_H

#include <iostream>
#include <fstream>
#include <string>
#include <map>

// OpenMP is used to get some hardware information.
// TODO Add relevant compiler flags in the Makefile.
#include <omp.h>

class HardwareInfo {
    public:
        /**
         * @brief Get the cache information for the CPU.
         * @return An array of integers containing the cache information for each level of cache in this order: L1, L2, L3, L0 (if available).
         */
        std::array<int, 4> getCacheInfo();

        /**
         * @brief Get the number of CPU cores and threads.
         * @return An array of integers containing the number of CPU cores and threads in this order: cores, threads.
         */
        std::array<int, 2> getCpuInfo();

        /**
         * @brief Get the content of /proc/meminfo on Linux distributions.
         * @return A string containing the content of /proc/meminfo.
         */
        std::string getMemoryInfo();
    private:
        // Helper functions to directly access the corresponding files.
        std::string readCacheInfo(const std::string& path);
        std::string readCpuInfo(const std::string& path);
        std::string readMemoryInfo(const std::string& path);
};


#endif // HDINFO_H