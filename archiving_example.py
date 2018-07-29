from ossie.utils import redhawk, sb
from ossie.properties import simple_property
from ossie.properties import simpleseq_property
import time
dom=redhawk.attach()

# turn off the GPP's management (for this example, load management is not needed and my VM is pretty light)
for dev in dom.devices:
  if 'GPP' in dev.name:
    dev.thresholds.ignore = True

dom.createApplication('sample_write')
dom.createApplication('archiver')
for app in dom.apps:
  if 'sample_write' in app.name:
    sample_write = app
  if 'archiver' in app.name:
    archiver = app

# set the achiver's file ageoff to 60 seconds; the default is 600 and I don't want to fill up my VM's harddrive
for comp in archiver:
  if 'control_write' in comp.name:
    comp.ageoff = 60.0

# connect my data generator (in this example, complex 100ksps centered at 1MHz
sample_write.connect(archiver, usesPortName='signal_out', providesPortName='signal_in')

sample_write.start()

archiver.start()

# make sure that old stale files from previous runs are deleted by the archiver
time.sleep(1)

# check to make sure that the achiver has created at least 2 files to draw from
print '... waiting for files to be created'
files=dom.fileMgr.list('/data/')
while len(files) < 2:
  time.sleep(0.5)
  files=dom.fileMgr.list('/data/')

now = time.time()

for comp in archiver:
  if 'control' in comp.name:
    control = comp
    break

# these two classes I lifted from the generated component for packing/unpacking messages. I didn't want to deal with dictionaries
class CutResponse(object):
    request_id = simple_property(id_="cut_response::request_id",name="request_id",type_="string")
    file_location = simple_property(id_="cut_response::file_location",name="file_location",type_="string")

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

class FileIO(object):
    file_operation = simple_property(id_="file_io_message::file_operation",name="file_operation",type_="string")
    stream_id = simple_property(id_="file_io_message::stream_id",name="stream_id",type_="string")
    filename = simple_property(id_="file_io_message::filename",name="filename",type_="string")

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

# when the cut that I request is complete, this callback will receive the message
def responseCallback(id_, message_response):
  print 'Got this response:', id_, message_response
  fp=dom.fileMgr.open(message_response.file_location, True)
  data = fp.read(fp.sizeOf())
  fp.close()
  dom.fileMgr.remove(message_response.file_location)
  print '========= got data of length:', len(data)

# request a cut from 15 seconds ago. Make the cut 3 seconds long. The cut is center at 1.01MHz and is 50 kHz wide
request = {'cut_request::time_begin':now-15, 'cut_request::time_end':now-12, 'cut_request::freq_begin':985000, 'cut_request::freq_end':1035000, 'cut_request::request_id':'hello'}
print '... sending request for a cut:', request
src = sb.MessageSource('cut_request')
src.connect(control, providesPortName='request')
snk=sb.MessageSink('cut_response',CutResponse, responseCallback)
control.connect(snk, usesPortName='response')
sb.start()
src.sendMessage(request)

time.sleep(2)

archiver.releaseObject()
sample_write.releaseObject()

