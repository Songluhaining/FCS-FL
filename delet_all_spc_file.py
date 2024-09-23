import os

from ranking.RankingManager import get_set_of_stms
from suspicious_statements_manager.SuspiciousStatementManager import get_suspicious_statement_varcop
from util.FileManager import join_path, list_dir


def delete_spc_file(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for dirs_s in dirs:
            parent_path = os.path.join(root, dirs_s)
            for root_ss, dirs_ss, files_ss in os.walk(parent_path):
                for file in files_ss:
                    if file == "spc_10.log": #slicing_10.log   spc_10
                        file_path = os.path.join(root_ss, file)
                        os.remove(file_path)
                        #print(file_path)


def get_isSelect_mut(folder_path):
    list_files = list_dir(folder_path)
    for file_name in list_files:
        parent_path = join_path(folder_path, file_name)
        suspicious_stms_list = get_suspicious_statement_varcop(parent_path, 0.1)
        varcop_isolated_set = get_set_of_stms(suspicious_stms_list)
        if len(varcop_isolated_set) == 0:
            print(file_name)
        # print(len(varcop_isolated_set))

folder_path = "/home/whn/Desktop/ExamDB/4wise-ExamDB-1BUG-Full"

delete_spc_file(folder_path)