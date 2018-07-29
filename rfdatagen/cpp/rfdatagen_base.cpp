#include "rfdatagen_base.h"

/*******************************************************************************************

    AUTO-GENERATED CODE. DO NOT MODIFY

    The following class functions are for the base class for the component class. To
    customize any of these functions, do not modify them here. Instead, overload them
    on the child class

******************************************************************************************/

rfdatagen_base::rfdatagen_base(const char *uuid, const char *label) :
    Component(uuid, label),
    ThreadedComponent()
{
    setThreadName(label);

    loadProperties();

    dataFloat = new bulkio::OutFloatPort("dataFloat");
    addPort("dataFloat", dataFloat);
}

rfdatagen_base::~rfdatagen_base()
{
    dataFloat->_remove_ref();
    dataFloat = 0;
}

/*******************************************************************************************
    Framework-level functions
    These functions are generally called by the framework to perform housekeeping.
*******************************************************************************************/
void rfdatagen_base::start() throw (CORBA::SystemException, CF::Resource::StartError)
{
    Component::start();
    ThreadedComponent::startThread();
}

void rfdatagen_base::stop() throw (CORBA::SystemException, CF::Resource::StopError)
{
    Component::stop();
    if (!ThreadedComponent::stopThread()) {
        throw CF::Resource::StopError(CF::CF_NOTSET, "Processing thread did not die");
    }
}

void rfdatagen_base::releaseObject() throw (CORBA::SystemException, CF::LifeCycle::ReleaseError)
{
    // This function clears the component running condition so main shuts down everything
    try {
        stop();
    } catch (CF::Resource::StopError& ex) {
        // TODO - this should probably be logged instead of ignored
    }

    Component::releaseObject();
}

void rfdatagen_base::loadProperties()
{
    addProperty(sample_rate,
                100000,
                "sample_rate",
                "",
                "readwrite",
                "",
                "external",
                "property");

    addProperty(center_frequency,
                1000000,
                "center_frequency",
                "",
                "readwrite",
                "",
                "external",
                "property");

    addProperty(complex_data,
                false,
                "complex_data",
                "",
                "readwrite",
                "",
                "external",
                "property");

}


