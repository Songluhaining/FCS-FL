import logging
import os
import time
import pandas as pd

from get_fail_coverage_information import get_spectrum_failed_coverage_inf_new
from util.FileManager import list_dir, join_path, get_outer_dir
import xml.etree.ElementTree as ET


def start(production_path, nodes):
    oberData = []

    # production_path = join_path(variants_list_path, variant)
    failed_coverage_path = production_path + "/" + "coverage/failed"
    passed_coverage_path = production_path + "/" + "coverage/passed"
    if os.path.exists(failed_coverage_path):
        failed_coverage_path = join_path(production_path, "coverage/failed")
        current_coverage_file_list = list_dir(failed_coverage_path)  # each coverage file
        spectrum_fail_coverage_file = join_path(get_outer_dir(failed_coverage_path), "spectrum_failed_coverage.xml")

        for cf in current_coverage_file_list:
            out_exed = {}
            out_not_exed = {}
            # #read coverage file
            coverage_file = join_path(failed_coverage_path, cf)
            # if os.path.isfile(coverage_file):
            #     data[variant] = []

            # read
            try:
                tree = ET.parse(coverage_file)
                root = tree.getroot()

                project = root.find("project")

                start = False
                for package in project:
                    for file in package:
                        file_name = file.get("name")
                        if file_name != None:
                            out_exed[file_name] = set()
                            out_not_exed[file_name] = set()
                            for line in file:
                                if line.tag == "line":
                                    if line.attrib.get("truecount") != None:
                                        num = line.attrib.get("num")
                                        if line.attrib.get("truecount") == "0":
                                            if num in out_exed[file_name]:
                                                out_exed[file_name].remove(num)
                                            out_not_exed[file_name].add(num)
                                        else:
                                            if num in out_not_exed[file_name]:
                                                out_not_exed[file_name].remove(num)
                                            out_exed[file_name].add(num)
                                    elif line.attrib.get("num") != None:
                                        num = line.attrib.get("num")
                                        if line.attrib.get("count") == "0":
                                            out_not_exed[file_name].add(num)
                                        else:
                                            out_exed[file_name].add(num)
            except:
                logging.info("Exception when parsing %s", coverage_file, exc_info=True)



            exed_data, not_exed_data = get_spectrum_failed_coverage_inf_new(spectrum_fail_coverage_file, out_exed, out_not_exed)


            temp = []
            for node in nodes:
                if node == "Results":
                    temp.append(0)
                    continue
                if node in exed_data:
                    temp.append(1)
                else:
                    temp.append(0)

            oberData.append(temp)

    if os.path.exists(passed_coverage_path):
        passed_coverage_path = join_path(production_path, "coverage/passed")

        current_coverage_file_list = list_dir(passed_coverage_path)  # each coverage file
        spectrum_pass_coverage_file = join_path(get_outer_dir(passed_coverage_path), "spectrum_passed_coverage.xml")
        for cf in current_coverage_file_list:
            # if cf.split('.')[1] == "Transaction_ESTest":
            out_exed = {}
            out_not_exed = {}
            # #read coverage file
            coverage_file = join_path(passed_coverage_path, cf)
            # if os.path.isfile(coverage_file):
            #     data[variant] = []

            # read
            try:
                tree = ET.parse(coverage_file)
                root = tree.getroot()
                project = root.find("project")

                start = False
                for package in project:
                    for file in package:
                        file_name = file.get("name")
                        if file_name != None:
                            out_exed[file_name] = set()
                            out_not_exed[file_name] = set()
                            for line in file:
                                if line.tag == "line":
                                    if line.attrib.get("truecount") != None:
                                        num = line.attrib.get("num")
                                        if line.attrib.get("truecount") == "0":
                                            if num in out_exed[file_name]:
                                                out_exed[file_name].remove(num)
                                            out_not_exed[file_name].add(num)
                                        else:
                                            if num in out_not_exed[file_name]:
                                                out_not_exed[file_name].remove(num)
                                            out_exed[file_name].add(num)
                                    elif line.attrib.get("num") != None:
                                        num = line.attrib.get("num")
                                        if line.attrib.get("count") == "0":
                                            out_not_exed[file_name].add(num)
                                        else:
                                            out_exed[file_name].add(num)
            except:
                logging.info("Exception when parsing %s", coverage_file)

            exed_data, not_exed_data = get_spectrum_failed_coverage_inf_new(spectrum_pass_coverage_file, out_exed,
                                                                            out_not_exed)

            temp = []
            for node in nodes:
                if node == "Results":
                    temp.append(1)
                    continue
                if node in exed_data:
                    temp.append(1)
                else:
                    temp.append(0)

            oberData.append(temp)
    return oberData


# nodePath = "/home/whn/codes/Static_Slicing-master/Static_Slicing-master/output/nodes.txt"

def gererateObDataFromSB(buggy_system_path, failed_graph_nodes, failed_graph_oberData):
    buggy_system_path = join_path(buggy_system_path, "variants")
    # buggy_system_path = "/home/whn/Desktop/BankAccountTP/4wise-BankAccountTP-1BUG-Full/_MultipleBugs_.NOB_1.ID_160/variants"
    list_failed_graph = list_dir(failed_graph_nodes)
    for nodeName in list_failed_graph:
        #if nodeName.split('.')[0] == "model_m_ca4_0002":
        nodePath = failed_graph_nodes + "/" + nodeName
        # slicenodeFileName = nodeName.replace("nodes", "sliceNodes")
        product_path = join_path(buggy_system_path, nodeName.split('.')[0])
        # print("product_path", product_path)
        nodes = []
        with open(nodePath, 'r') as f:
            content = f.read()
            nodes = content.split(",")

        df = pd.DataFrame(columns=nodes)

        oberData = start(product_path, nodes)
        for i in range(len(oberData)):
            df.loc[i] = oberData[i]

        df.to_csv(failed_graph_oberData + '/' + nodeName.split('.')[0] + ".csv")
        time.sleep(1)