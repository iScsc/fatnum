#include "hdinfo.hpp"

void getCacheInfo() {
    std::map<int, std::string> cacheInfo;
    
    // Read cache information for each level
    for (int i = 0; i <= 3; ++i) {
        std::string path = "/sys/devices/system/cpu/cpu0/cache/index" + std::to_string(i) + "/size";
        std::ifstream cache(path);
        
        if (cache) {
            std::string size;
            std::getline(cache, size);
            cacheInfo[i] = size;
            cache.close();
        }
    }
    
    // Display cache information
    for (const auto& [level, size] : cacheInfo) {
        std::cout << "L" << level << " Cache Size: " << size << std::endl;
    }
}
