#!/usr/bin/env python
#
# AUTO-GENERATED CODE.  DO NOT MODIFY!
#
# Source: control_writes.spd.xml
from ossie.cf import CF
from ossie.cf import CF__POA
from ossie.utils import uuid

from ossie.component import Component
from ossie.threadedcomponent import *
from ossie.properties import simple_property
from ossie.properties import simpleseq_property
from ossie.properties import struct_property

import Queue, copy, time, threading
from ossie.resource import usesport, providesport
from ossie.events import MessageConsumerPort
from ossie.events import MessageSupplierPort

class enums:
    # Enumerated values for file_io_message
    class file_io_message:
        # Enumerated values for file_io_message::file_operation
        class file_operation:
            OPEN = "OPEN"
            CLOSE = "CLOSE"

class control_writes_base(CF__POA.Resource, Component, ThreadedComponent):
        # These values can be altered in the __init__ of your derived class

        PAUSE = 0.0125 # The amount of time to sleep if process return NOOP
        TIMEOUT = 5.0 # The amount of time to wait for the process thread to die when stop() is called
        DEFAULT_QUEUE_SIZE = 100 # The number of BulkIO packets that can be in the queue before pushPacket will block

        def __init__(self, identifier, execparams):
            loggerName = (execparams['NAME_BINDING'].replace('/', '.')).rsplit("_", 1)[0]
            Component.__init__(self, identifier, execparams, loggerName=loggerName)
            ThreadedComponent.__init__(self)

            # self.auto_start is deprecated and is only kept for API compatibility
            # with 1.7.X and 1.8.0 components.  This variable may be removed
            # in future releases
            self.auto_start = False
            # Instantiate the default implementations for all ports on this component
            self.port_request = MessageConsumerPort(thread_sleep=0.1, parent = self)
            self.port_file_io_status = MessageConsumerPort(thread_sleep=0.1, parent = self)
            self.port_response = MessageSupplierPort()

        def start(self):
            Component.start(self)
            ThreadedComponent.startThread(self, pause=self.PAUSE)

        def stop(self):
            Component.stop(self)
            if not ThreadedComponent.stopThread(self, self.TIMEOUT):
                raise CF.Resource.StopError(CF.CF_NOTSET, "Processing thread did not die")

        def releaseObject(self):
            try:
                self.stop()
            except Exception:
                self._log.exception("Error stopping")
            Component.releaseObject(self)

        ######################################################################
        # PORTS
        # 
        # DO NOT ADD NEW PORTS HERE.  You can add ports in your derived class, in the SCD xml file, 
        # or via the IDE.

        port_request = providesport(name="request",
                                    repid="IDL:ExtendedEvent/MessageEvent:1.0",
                                    type_="control")

        port_file_io_status = providesport(name="file_io_status",
                                           repid="IDL:ExtendedEvent/MessageEvent:1.0",
                                           type_="control")

        port_response = usesport(name="response",
                                 repid="IDL:ExtendedEvent/MessageEvent:1.0",
                                 type_="control")

        ######################################################################
        # PROPERTIES
        # 
        # DO NOT ADD NEW PROPERTIES HERE.  You can add properties in your derived class, in the PRF xml file
        # or by using the IDE.
        ageoff = simple_property(id_="ageoff",
                                 type_="float",
                                 defvalue=600.0,
                                 mode="readwrite",
                                 action="external",
                                 kinds=("property",),
                                 description="""seconds""")


        class CutRequest(object):
            time_begin = simple_property(
                                         id_="cut_request::time_begin",
                                         
                                         name="time_begin",
                                         type_="double")
        
            time_end = simple_property(
                                       id_="cut_request::time_end",
                                       
                                       name="time_end",
                                       type_="double")
        
            freq_begin = simple_property(
                                         id_="cut_request::freq_begin",
                                         
                                         name="freq_begin",
                                         type_="double")
        
            freq_end = simple_property(
                                       id_="cut_request::freq_end",
                                       
                                       name="freq_end",
                                       type_="double")
        
            request_id = simple_property(
                                         id_="cut_request::request_id",
                                         
                                         name="request_id",
                                         type_="string")
        
            def __init__(self, **kw):
                """Construct an initialized instance of this struct definition"""
                for classattr in type(self).__dict__.itervalues():
                    if isinstance(classattr, (simple_property, simpleseq_property)):
                        classattr.initialize(self)
                for k,v in kw.items():
                    setattr(self,k,v)
        
            def __str__(self):
                """Return a string representation of this structure"""
                d = {}
                d["time_begin"] = self.time_begin
                d["time_end"] = self.time_end
                d["freq_begin"] = self.freq_begin
                d["freq_end"] = self.freq_end
                d["request_id"] = self.request_id
                return str(d)
        
            @classmethod
            def getId(cls):
                return "cut_request"
        
            @classmethod
            def isStruct(cls):
                return True
        
            def getMembers(self):
                return [("time_begin",self.time_begin),("time_end",self.time_end),("freq_begin",self.freq_begin),("freq_end",self.freq_end),("request_id",self.request_id)]

        cut_request = struct_property(id_="cut_request",
                                      structdef=CutRequest,
                                      configurationkind=("message",),
                                      mode="readwrite")


        class CutResponse(object):
            request_id = simple_property(
                                         id_="cut_response::request_id",
                                         
                                         name="request_id",
                                         type_="string")
        
            file_location = simple_property(
                                            id_="cut_response::file_location",
                                            
                                            name="file_location",
                                            type_="string")
        
            def __init__(self, **kw):
                """Construct an initialized instance of this struct definition"""
                for classattr in type(self).__dict__.itervalues():
                    if isinstance(classattr, (simple_property, simpleseq_property)):
                        classattr.initialize(self)
                for k,v in kw.items():
                    setattr(self,k,v)
        
            def __str__(self):
                """Return a string representation of this structure"""
                d = {}
                d["request_id"] = self.request_id
                d["file_location"] = self.file_location
                return str(d)
        
            @classmethod
            def getId(cls):
                return "cut_response"
        
            @classmethod
            def isStruct(cls):
                return True
        
            def getMembers(self):
                return [("request_id",self.request_id),("file_location",self.file_location)]

        cut_response = struct_property(id_="cut_response",
                                       structdef=CutResponse,
                                       configurationkind=("message",),
                                       mode="readwrite")


        class FileIoMessage(object):
            file_operation = simple_property(
                                             id_="file_io_message::file_operation",
                                             
                                             name="file_operation",
                                             type_="string",
                                             defvalue="OPEN"
                                             )
        
            stream_id = simple_property(
                                        id_="file_io_message::stream_id",
                                        
                                        name="stream_id",
                                        type_="string")
        
            filename = simple_property(
                                       id_="file_io_message::filename",
                                       
                                       name="filename",
                                       type_="string")
        
            def __init__(self, **kw):
                """Construct an initialized instance of this struct definition"""
                for classattr in type(self).__dict__.itervalues():
                    if isinstance(classattr, (simple_property, simpleseq_property)):
                        classattr.initialize(self)
                for k,v in kw.items():
                    setattr(self,k,v)
        
            def __str__(self):
                """Return a string representation of this structure"""
                d = {}
                d["file_operation"] = self.file_operation
                d["stream_id"] = self.stream_id
                d["filename"] = self.filename
                return str(d)
        
            @classmethod
            def getId(cls):
                return "file_io_message"
        
            @classmethod
            def isStruct(cls):
                return True
        
            def getMembers(self):
                return [("file_operation",self.file_operation),("stream_id",self.stream_id),("filename",self.filename)]

        file_io_message = struct_property(id_="file_io_message",
                                          structdef=FileIoMessage,
                                          configurationkind=("message",),
                                          mode="readwrite",
                                          description="""The structure representing a file IO message.""")




