#include <iostream>
#include "ossie/ossieSupport.h"

#include "rfdatagen.h"
extern "C" {
    Resource_impl* make_component(const std::string& uuid, const std::string& identifier)
    {
        return new rfdatagen_i(uuid.c_str(), identifier.c_str());
    }
}

