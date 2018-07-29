# archiving
This is a simple archiver for REDHAWK and some sample code to test it out. It stores an incoming Bulk IO data stream and will create tuned cuts from the archived data upon requested

# installing
Run setup.sh

Note that rh.FileReader, rh.FileWriter, and rh.TuneFilterDecimate need to be installed

# testing
Run archiving_example.py

The script archiving_example.py also provides an example of how to use the archiver. Even though the example uses a synthetic data source, this archiver is designed to receive data from an FEI device.

Notes: 
 - The output file format is a BLUEFILE. To change the file format output, remove the default file_format property override for FileWriter_3.
 - As shown in the archiving_example.py script, once the requested cut is generated, it is up to the requester to delete the file that was created.
 