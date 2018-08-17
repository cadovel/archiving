#!/usr/bin/env python
#
#
# AUTO-GENERATED
#
# Source: control_writes.spd.xml
from ossie.resource import start_component
import logging
from ossie.cf import CF
from omniORB import any
import os, time

from control_writes_base import *
from pycparser.c_ast import Compound

class control_writes_i(control_writes_base):
    """<DESCRIPTION GOES HERE>"""
    def constructor(self):
        """
        This is called by the framework immediately after your component registers with the system.
        
        In general, you should add customization here and not in the __init__ constructor.  If you have 
        a custom port implementation you can override the specific implementation here with a statement
        similar to the following:
          self.some_port = MyPortImplementation()

        """
        # TODO add customization here.
        self.app = self.getApplication().getRef()
        self.comps = self.app._get_registeredComponents()
        
        self.addPropertyChangeListener('ageoff', self.callback_ageoff)
        self.port_request.registerMessage("cut_request", control_writes_i.CutRequest, self.callback_cut_request)
        self.port_file_io_status.registerMessage("file_io_message", control_writes_i.FileIoMessage, self.callback_file_io_message)
        self.requests = {}
        self.request_count = 0
        self.basedir = os.getenv('SDRROOT')+'/dom/data'
        #self.addPropertyChangeListener('cut_request', self.callback_cut_request)

        for comp in  self.comps:
            if 'FileWriter_1' in comp.identifier:
                self.FileWriter_1 = comp
            if 'FileWriter_2' in comp.identifier:
                self.FileWriter_2 = comp
            if 'FileReader_1' in comp.identifier:
                self.FileReader_1 = comp
            if 'FileWriter_3' in comp.identifier:
                self.FileWriter_3 = comp
            if 'Tune' in comp.identifier:
                self.TFD = comp
            if 'splitter' in comp.identifier:
                self.splitter = comp
                        
    def start(self):
        enabled_false = CF.DataType(id='recording_enabled', value=any.to_any(False))
        self.FileWriter_1.componentObject.configure([enabled_false])
        self.FileWriter_2.componentObject.configure([enabled_false])
        self.FileReader_1
        self.FileWriter_3.componentObject.configure([enabled_false])
        self.TFD

        self.recoding_length = 10
        self.recoding_offset = 2
        self.one_start = time.time()
        self.one_end = self.one_start + self.recoding_length
        self.two_start = self.one_start + self.recoding_length - self.recoding_offset
        self.two_end = self.two_start + self.recoding_length

        control_writes_base.start(self)
        
    def process(self):
        """
        Basic functionality:
        
            The process method should process a single "chunk" of data and then return. This method
            will be called from the processing thread again, and again, and again until it returns
            FINISH or stop() is called on the component.  If no work is performed, then return NOOP.
            
        StreamSRI:
            To create a StreamSRI object, use the following code (this generates a normalized SRI that does not flush the queue when full):
                sri = bulkio.sri.create("my_stream_id")

        PrecisionUTCTime:
            To create a PrecisionUTCTime object, use the following code:
                tstamp = bulkio.timestamp.now() 
  
        Ports:

            Each port instance is accessed through members of the following form: self.port_<PORT NAME>
            
            Data is obtained in the process function through the getPacket call (BULKIO only) on a
            provides port member instance. The optional argument is a timeout value, in seconds.
            A zero value is non-blocking, while a negative value is blocking. Constants have been
            defined for these values, bulkio.const.BLOCKING and bulkio.const.NON_BLOCKING. If no
            timeout is given, it defaults to non-blocking.
            
            The return value is a named tuple with the following fields:
                - dataBuffer
                - T
                - EOS
                - streamID
                - SRI
                - sriChanged
                - inputQueueFlushed
            If no data is available due to a timeout, all fields are None.

            To send data, call the appropriate function in the port directly. In the case of BULKIO,
            convenience functions have been added in the port classes that aid in output.
            
            Interactions with non-BULKIO ports are left up to the component developer's discretion.
            
        Messages:
    
            To receive a message, you need (1) an input port of type MessageEvent, (2) a message prototype described
            as a structure property of kind message, (3) a callback to service the message, and (4) to register the callback
            with the input port.
        
            Assuming a property of type message is declared called "my_msg", an input port called "msg_input" is declared of
            type MessageEvent, create the following code:
        
            def msg_callback(self, msg_id, msg_value):
                print msg_id, msg_value
        
            Register the message callback onto the input port with the following form:
            self.port_input.registerMessage("my_msg", control_writes_i.MyMsg, self.msg_callback)
        
            To send a message, you need to (1) create a message structure, and (2) send the message over the port.
        
            Assuming a property of type message is declared called "my_msg", an output port called "msg_output" is declared of
            type MessageEvent, create the following code:
        
            msg_out = control_writes_i.MyMsg()
            this.port_msg_output.sendMessage(msg_out)

    Accessing the Device Manager and Domain Manager:
    
        Both the Device Manager hosting this Device and the Domain Manager hosting
        the Device Manager are available to the Device.
        
        To access the Domain Manager:
            dommgr = self.getDomainManager().getRef();
        To access the Device Manager:
            devmgr = self.getDeviceManager().getRef();
        Properties:
        
            Properties are accessed directly as member variables. If the property name is baudRate,
            then accessing it (for reading or writing) is achieved in the following way: self.baudRate.

            To implement a change callback notification for a property, create a callback function with the following form:

            def mycallback(self, id, old_value, new_value):
                pass

            where id is the property id, old_value is the previous value, and new_value is the updated value.
            
            The callback is then registered on the component as:
            self.addPropertyChangeListener('baudRate', self.mycallback)
            
            
        Example:
        
            # This example assumes that the component has two ports:
            #   - A provides (input) port of type bulkio.InShortPort called dataShort_in
            #   - A uses (output) port of type bulkio.OutFloatPort called dataFloat_out
            # The mapping between the port and the class if found in the component
            # base class.
            # This example also makes use of the following Properties:
            #   - A float value called amplitude
            #   - A boolean called increaseAmplitude
            
            packet = self.port_dataShort_in.getPacket()
            
            if packet.dataBuffer is None:
                return NOOP
                
            outData = range(len(packet.dataBuffer))
            for i in range(len(packet.dataBuffer)):
                if self.increaseAmplitude:
                    outData[i] = float(packet.dataBuffer[i]) * self.amplitude
                else:
                    outData[i] = float(packet.dataBuffer[i])
                
            # NOTE: You must make at least one valid pushSRI call
            if packet.sriChanged:
                self.port_dataFloat_out.pushSRI(packet.SRI);

            self.port_dataFloat_out.pushPacket(outData, packet.T, packet.EOS, packet.streamID)
            return NORMAL
            
        """

        # TODO fill in your code here
        self._log.debug("process() example log message")
        is_enabled = CF.DataType(id='recording_enabled', value=any.to_any(None))
        enabled_false = CF.DataType(id='recording_enabled', value=any.to_any(False))
        enabled_true = CF.DataType(id='recording_enabled', value=any.to_any(True))
        fw_1_recording = self.FileWriter_1.componentObject.query([is_enabled])[0].value._v
        fw_2_recording = self.FileWriter_2.componentObject.query([is_enabled])[0].value._v
        fw_3_recording = self.FileWriter_3.componentObject.query([is_enabled])[0].value._v
        now = time.time()
       
        if now > self.one_start and now < self.one_end:
            if not fw_1_recording:
                self.FileWriter_1.componentObject.configure([enabled_true])
        if now > self.two_start and now < self.two_end:
            if not fw_2_recording:
                self.FileWriter_2.componentObject.configure([enabled_true])
        if now > self.one_end:
            if fw_1_recording:
                self.FileWriter_1.componentObject.configure([enabled_false])
            self.one_start = self.two_start  + self.recoding_length - self.recoding_offset
            self.one_end = self.one_start  + self.recoding_length
        if now > self.two_end:
            if fw_2_recording:
                self.FileWriter_2.componentObject.configure([enabled_false])
            self.two_start = self.one_start  + self.recoding_length - self.recoding_offset
            self.two_end = self.two_start  + self.recoding_length
                
        filelist = os.listdir(self.basedir)
        for _file in filelist:
            fields = _file.split('.')
            if len(fields) < 6:
                continue
            try:
                format = fields[-1]
                samplerate = fields[-2]
                complexity = fields[-3]
                filetime_in_seconds = self.string_to_seconds(fields[-5], fields[-4])
                now_in_seconds = self.gm_to_seconds(time.gmtime(time.time()))
                if filetime_in_seconds + self.ageoff < now_in_seconds:
                    os.remove(self.basedir+'/'+_file)
            except:
                continue
            
        return NOOP

    def string_to_seconds(self, hoursminutesseconds, partialseconds):
        hours = int(hoursminutesseconds[:2])
        minutes = int(hoursminutesseconds[2:4])
        seconds = float(hoursminutesseconds[4:]+'.'+partialseconds)
        return seconds+minutes*60+hours*60*60

    def gm_to_seconds(self, rightnow):
        return rightnow.tm_hour*60*60+rightnow.tm_min*60+rightnow.tm_sec
        
    def callback_ageoff(self, prop_id, old_value, new_value):
        pass

    def callback_file_io_message(self, msg_id, new_value):
        if "CLOSE" in new_value.file_operation:
            filename = str(new_value.filename)
            filename = filename.split('/')[-1]
            if self.requests.has_key(filename):
                msg_out = control_writes_i.CutResponse()
                msg_out.request_id = self.requests[filename]
                msg_out.file_location = new_value.filename
                self.port_response.sendMessage(msg_out)
                enabled_false = CF.DataType(id='recording_enabled', value=any.to_any(False))
                self.FileWriter_3.componentObject.configure([enabled_false])
        
    def callback_cut_request(self, msg_id, new_value):
        splitter_props = self.splitter.componentObject.query([])
        for prop in splitter_props:
            if prop.id == 'bandwidth':
                bandwidth = prop.value._v
            if prop.id == 'center_freq':
                center_freq = prop.value._v
        if new_value.freq_begin == None or new_value.freq_end == None or new_value.time_begin == None or new_value.time_end == None:
            return
        
        if center_freq - bandwidth/2 < new_value.freq_begin or center_freq + bandwidth/2 > new_value.freq_end:
            print 'bad frequency range:',center_freq - bandwidth/2, center_freq + bandwidth/2, 'vs', new_value.freq_begin, new_value.freq_end
        request_id = new_value.request_id
        timestring = time.asctime(time.gmtime(new_value.time_begin)).split(' ')
        month = timestring[1]
        if timestring[2] == '':
            day = '0'+timestring[3]
        else:
            day = timestring[2]
        year = timestring[-1]
        begin_seconds = self.gm_to_seconds(time.gmtime(new_value.time_begin))
        begin_compounddate = day+month+year

        timestring = time.asctime(time.gmtime(new_value.time_end)).split(' ')
        month = timestring[1]
        if timestring[2] == '':
            day = '0'+timestring[3]
        else:
            day = timestring[2]
        year = timestring[-1]
        end_seconds = self.gm_to_seconds(time.gmtime(new_value.time_end))
        end_compounddate = day+month+year
        filelist = os.listdir(self.basedir)
        for _file in filelist:
            fields = _file.split('.')
            if len(fields) < 6:
                continue
            try:
                format = fields[-1]
                if format == "inProgress":
                    continue
                samplerate = float(fields[-2])
                filesize = os.stat(self.basedir+'/'+_file).st_size
                complexity = fields[-3]
                filetime_in_seconds = self.string_to_seconds(fields[-5], fields[-4])
                compounddate = fields[-6]
                if compounddate != begin_compounddate:
                    continue
                if compounddate != end_compounddate:
                    continue
                if begin_seconds < filetime_in_seconds:
                    continue
                if end_seconds > filetime_in_seconds + (filesize/(samplerate*4)):
                    continue
                self.TFD.DesiredOutputRate = new_value.freq_end - new_value.freq_begin
                self.TFD.FilterBW = new_value.freq_end - new_value.freq_begin
                new_center_freq = (new_value.freq_end + new_value.freq_begin)/2.0
                self.TFD.TuningIF = new_center_freq - center_freq
                
                self.request_count += 1
                newfilename = "datafile_"+str(self.request_count)
                self.requests[newfilename] = request_id
                uri = CF.DataType(id='destination_uri', value=any.to_any('sca:///data/'+newfilename))
                enabled_true = CF.DataType(id='recording_enabled', value=any.to_any(True))
                self.FileWriter_3.componentObject.configure([uri, enabled_true])
                source_uri = CF.DataType(id='source_uri', value=any.to_any('sca:///data/'+_file))
                sample_rate = CF.DataType(id='sample_rate', value=any.to_any(str(samplerate)))
                file_format = CF.DataType(id='file_format', value=any.to_any("COMPLEX_FLOAT"))
                xdelta = CF.DataType(id='xdelta', value=any.to_any(1/samplerate))
                sri = CF.DataType(id='default_sri', value=any.to_any([xdelta]))
                center_frequency = CF.DataType(id='center_frequency', value=any.to_any(str(center_freq)))
            
                start = begin_seconds - filetime_in_seconds
                end = end_seconds - filetime_in_seconds
                print 'start: ',start,' end: ',end, ' difference: ',end-start
                enable_time_filtering = CF.DataType(id='enable_time_filtering', value=any.to_any(True))
                start_time = CF.DataType(id='start_time', value=any.to_any(start))
                stop_time = CF.DataType(id='stop_time', value=any.to_any(end))
                adv_props = CF.DataType(id='advanced_properties', value=any.to_any([enable_time_filtering, start_time, stop_time]))
                self.FileReader_1.componentObject.configure([adv_props, source_uri, sri, center_frequency, sample_rate, file_format])
                
                playback_state = CF.DataType(id='playback_state', value=any.to_any('PLAY'))
                self.FileReader_1.componentObject.configure([playback_state])
                break
                
            except:
                continue

  
if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    logging.debug("Starting Component")
    start_component(control_writes_i)

