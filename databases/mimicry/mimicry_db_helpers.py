import csv
import os
import re
from sbpy_utils.core.command_line import my_system,get_local_os

class MimicryDBHelper:


    def __init__(self,mimicry_db_root=None):
        self.read_recording_details()
        self.create_mimicry_subject_uid_lookup_table()
        self.mimicry_db_root=mimicry_db_root
        
    def read_recording_details(self):
        parent_dir = os.path.dirname(os.path.abspath(__file__))   
        recording_details=os.path.join(parent_dir,'RecordingDetails.csv')
    
        records=[]
        with open(recording_details, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for record in reader:
                records.append(record)
    
        self.recording_details=records
        

    def create_mimicry_subject_uid_lookup_table(self):
        mimicry_subject_uid_lookup_table = []
        mimicry_subject_name_lookup_table = []
        for f in self.recording_details:
            tmp = [f['P1 id'] , f['P2 id']]
            tmp2 = [f['P1 name'] , f['P2 name']]
            mimicry_subject_uid_lookup_table.append(tmp)
            mimicry_subject_name_lookup_table.append(tmp2)
        self.mimicry_subject_uid_lookup_table=mimicry_subject_uid_lookup_table
        self.mimicry_subject_name_lookup_table=mimicry_subject_name_lookup_table
        
    def mimicry_get_metadata_from_path(self,video_path):
        
        folder_path=os.path.dirname(video_path);
        folder_name=os.path.basename(folder_path);
        
        
        role = int(video_path[re.finditer('_P[0-9]+_', video_path).next().start()+2])
        session = int(folder_name)
        subject_uid = self.mimicry_subject_uid_lookup_table[session-1][role-1]
        subject_name = self.mimicry_subject_name_lookup_table[session-1][role-1]
        
        return {'session':session,
                'role':role,
                'subject_uid':subject_uid,
                'subject_name':subject_name}


    def mhi_mimicry_get_subj_session_from_name( video_stem, mimicry_db_root=None):
        platform=get_local_os()

        if not self.mimicry_db_root is None:
            mimicry_db_root_final=self.mimicry_db_root

        if not mimicry_db_root is None:
            mimicry_db_root_final=mimicry_db_root
        
        if platform in ['linux','mac'] :
           
            cmd = ['dirname $(find ', mimicry_db_root_final, ' -wholename "*', video_stem, '*" | head -1 ) | tail -c 2'] 
            res = my_system(cmd)
            session = int(res.strip());
            regexp_matcher = re.compile('_P[0-9]*_')
            
            role = int(video_name[regexp_matcher.match(video_name).start()+2])
            subject_uid = self.mimicry_subject_uid_lookup_table[session][role]

            return {'session':session,
                    'role':role,
                    'subject_uid':subject_uid}

        else:
            raise RuntimeError("Must use a Unix-based platform")

