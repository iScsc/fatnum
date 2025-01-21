#include <fstream>
#include <iostream>
#include <map>
#include <string>

void getCacheInfo()
{
    std::map<int, std::string> cacheInfo;

    // Read cache information for each level
    for(int i = 0; i <= 3; ++i) {
        std::string path = "/sys/devices/system/cpu/cpu0/cache/index"
                           + std::to_string(i) + "/size";
        std::ifstream cache(path);

        if(cache) {
            std::string size;
            std::getline(cache, size);
            cacheInfo[i] = size;
            cache.close();
        }
    }

    // Display cache information
    for(const auto& [level, size]: cacheInfo) {
        std::cout << "L" << level << " Cache Size: " << size << std::endl;
    }
}

void getMemoryInfo()
{
    std::ifstream meminfo("/proc/meminfo");
    if(!meminfo) {
        std::cerr << "Error opening /proc/meminfo" << std::endl;
        return;
    }

    std::string line;
    while(std::getline(meminfo, line)) { std::cout << line << std::endl; }

    meminfo.close();
}

int main()
{
    std::cout << "Cache Information:" << std::endl;
    getCacheInfo();
    std::cout << "\nMemory Information:" << std::endl;
    getMemoryInfo();
    return 0;
}