#ifndef SPLITTER_BASE_IMPL_BASE_H
#define SPLITTER_BASE_IMPL_BASE_H

#include <boost/thread.hpp>
#include <ossie/Component.h>
#include <ossie/ThreadedComponent.h>

#include <bulkio/bulkio.h>

class splitter_base : public Component, protected ThreadedComponent
{
    public:
        splitter_base(const char *uuid, const char *label);
        ~splitter_base();

        void start() throw (CF::Resource::StartError, CORBA::SystemException);

        void stop() throw (CF::Resource::StopError, CORBA::SystemException);

        void releaseObject() throw (CF::LifeCycle::ReleaseError, CORBA::SystemException);

        void loadProperties();

    protected:
        // Member variables exposed as properties
        /// Property: center_freq
        double center_freq;
        /// Property: bandwidth
        double bandwidth;

        // Ports
        /// Port: dataFloat
        bulkio::InFloatPort *dataFloat;
        /// Port: dataFloat_1
        bulkio::OutFloatPort *dataFloat_1;
        /// Port: dataFloat_2
        bulkio::OutFloatPort *dataFloat_2;

    private:
};
#endif // SPLITTER_BASE_IMPL_BASE_H
