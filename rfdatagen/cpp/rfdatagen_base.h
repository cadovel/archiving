#ifndef RFDATAGEN_BASE_IMPL_BASE_H
#define RFDATAGEN_BASE_IMPL_BASE_H

#include <boost/thread.hpp>
#include <ossie/Component.h>
#include <ossie/ThreadedComponent.h>

#include <bulkio/bulkio.h>

class rfdatagen_base : public Component, protected ThreadedComponent
{
    public:
        rfdatagen_base(const char *uuid, const char *label);
        ~rfdatagen_base();

        void start() throw (CF::Resource::StartError, CORBA::SystemException);

        void stop() throw (CF::Resource::StopError, CORBA::SystemException);

        void releaseObject() throw (CF::LifeCycle::ReleaseError, CORBA::SystemException);

        void loadProperties();

    protected:
        // Member variables exposed as properties
        /// Property: sample_rate
        double sample_rate;
        /// Property: center_frequency
        double center_frequency;
        /// Property: complex_data
        bool complex_data;

        // Ports
        /// Port: dataFloat
        bulkio::OutFloatPort *dataFloat;

    private:
};
#endif // RFDATAGEN_BASE_IMPL_BASE_H
