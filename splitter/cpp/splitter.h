#ifndef SPLITTER_I_IMPL_H
#define SPLITTER_I_IMPL_H

#include "splitter_base.h"

class splitter_i : public splitter_base
{
    ENABLE_LOGGING
    public:
        splitter_i(const char *uuid, const char *label);
        ~splitter_i();

        void constructor();

        int serviceFunction();
};

#endif // SPLITTER_I_IMPL_H
