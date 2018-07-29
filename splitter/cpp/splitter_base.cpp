#include "splitter_base.h"

/*******************************************************************************************

    AUTO-GENERATED CODE. DO NOT MODIFY

    The following class functions are for the base class for the component class. To
    customize any of these functions, do not modify them here. Instead, overload them
    on the child class

******************************************************************************************/

splitter_base::splitter_base(const char *uuid, const char *label) :
    Component(uuid, label),
    ThreadedComponent()
{
    setThreadName(label);

    loadProperties();

    dataFloat = new bulkio::InFloatPort("dataFloat");
    addPort("dataFloat", dataFloat);
    dataFloat_1 = new bulkio::OutFloatPort("dataFloat_1");
    addPort("dataFloat_1", dataFloat_1);
    dataFloat_2 = new bulkio::OutFloatPort("dataFloat_2");
    addPort("dataFloat_2", dataFloat_2);
}

splitter_base::~splitter_base()
{
    dataFloat->_remove_ref();
    dataFloat = 0;
    dataFloat_1->_remove_ref();
    dataFloat_1 = 0;
    dataFloat_2->_remove_ref();
    dataFloat_2 = 0;
}

/*******************************************************************************************
    Framework-level functions
    These functions are generally called by the framework to perform housekeeping.
*******************************************************************************************/
void splitter_base::start() throw (CORBA::SystemException, CF::Resource::StartError)
{
    Component::start();
    ThreadedComponent::startThread();
}

void splitter_base::stop() throw (CORBA::SystemException, CF::Resource::StopError)
{
    Component::stop();
    if (!ThreadedComponent::stopThread()) {
        throw CF::Resource::StopError(CF::CF_NOTSET, "Processing thread did not die");
    }
}

void splitter_base::releaseObject() throw (CORBA::SystemException, CF::LifeCycle::ReleaseError)
{
    // This function clears the component running condition so main shuts down everything
    try {
        stop();
    } catch (CF::Resource::StopError& ex) {
        // TODO - this should probably be logged instead of ignored
    }

    Component::releaseObject();
}

void splitter_base::loadProperties()
{
    addProperty(center_freq,
                -1,
                "center_freq",
                "",
                "readwrite",
                "",
                "external",
                "property");

    addProperty(bandwidth,
                -1,
                "bandwidth",
                "",
                "readwrite",
                "",
                "external",
                "property");

}


