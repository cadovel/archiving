#ifndef RFDATAGEN_I_IMPL_H
#define RFDATAGEN_I_IMPL_H

#include "rfdatagen_base.h"

class rfdatagen_i : public rfdatagen_base
{
    ENABLE_LOGGING
    public:
        rfdatagen_i(const char *uuid, const char *label);
        ~rfdatagen_i();

        void constructor();

        int serviceFunction();
};

#endif // RFDATAGEN_I_IMPL_H
