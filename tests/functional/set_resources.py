
import os
import inspect
import shutil

class SetResources():

    def setup(self, app="FDTD"):
        """Set resources setup."""
        caller_frame = inspect.stack()[1]
        caller_filepath = caller_frame.filename
        base_name = os.path.basename(caller_filepath)
        self.file_name, _ = os.path.splitext(base_name)
        self.test_path = os.path.dirname(os.path.abspath(self.file_name))
        self.resource_path = os.path.join(self.test_path, self.file_name)

        if os.path.exists(self.resource_path): 
            os.chdir(self.resource_path)

        extension = { "DEVICE" : "ldev",
                      "FDTD" : "fsp", 
                      "INTERCONNECT" : "icp",
                      "MODE" : "lms" }[ app ]
        self.project_file = "%s.%s" % ( self.file_name, extension )
        self.project_temp_file = "%s_temp.%s" % ( self.file_name, extension )
        self.log_file = "%s_temp_p0.log" % self.file_name
        self.script_file = "%s.lsf" % self.file_name

        self.teardown(change_dir=False)

        if os.path.exists(self.project_file):
            shutil.copyfile(self.project_file, self.project_temp_file) 
       
        return self.project_temp_file, self.file_name, self.resource_path, self.script_file

    def teardown(self, change_dir=True, delete_file=''):
        """Set resources teardown."""
        if os.path.exists(self.project_temp_file):        
            os.remove(self.project_temp_file)
            
        if os.path.exists(self.log_file):        
            os.remove(self.log_file)

        if delete_file and os.path.exists(delete_file):        
            os.remove(delete_file)

        if change_dir and os.path.exists(self.test_path): 
            os.chdir(self.test_path)
