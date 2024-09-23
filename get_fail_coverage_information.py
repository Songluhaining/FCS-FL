import logging
import os

from util.FileManager import list_dir, join_path, get_outer_dir
import xml.etree.ElementTree as ET

def get_spectrum_failed_coverage_inf(spectrum_fail_coverage_file, nums, variant):
    if os.path.isfile(spectrum_fail_coverage_file):
        data = {}
        #data[variant] = []
        try:
            tree = ET.parse(spectrum_fail_coverage_file)
            root = tree.getroot()
            project = root.find("project")

            for package in project:
                for file in package:
                    for line in file:
                        if line.get("num") in nums:
                            id = line.get('featureClass') + "." + line.get('featureLineNum')
                            if id not in data and int(line.get('count')) != 0:
                                #data[variant].append(id)
                                ninteractions = {}
                                ninteractions["num_interactions"] = [int(line.get('count')), nums.get(line.get("num"))]
                                data[id] = ninteractions
        except Exception as e:
            print(e)
            logging.info("Exception when parsing %s", spectrum_fail_coverage_file, e)
        return data


def get_spectrum_failed_coverage_inf_new(spectrum_fail_coverage_file, out_exed, out_not_exed):
    if os.path.isfile(spectrum_fail_coverage_file):
        data = {}
        exed_data = set()
        not_exed_data = set()
        #data[variant] = []
        try:
            tree = ET.parse(spectrum_fail_coverage_file)
            root = tree.getroot()
            project = root.find("project")

            for package in project:
                for file in package:
                    file_name = file.get("path")
                    file_name = file_name.split("/")
                    if len(file_name) > 1:
                        file_name = file_name[-1]
                    else:
                        file_name = file_name[0]
                    for line in file:
                        if line.get("num") in out_exed[file_name]:
                            id = line.get('featureClass') + "." + line.get('featureLineNum')
                            exed_data.add(id)
                        elif line.get("num") in out_not_exed[file_name]:
                            id = line.get('featureClass') + "." + line.get('featureLineNum')
                            not_exed_data.add(id)
        except Exception as e:
            print(e)
            logging.info("Exception when parsing %s", spectrum_fail_coverage_file, e)
        return exed_data, not_exed_data

def get_each_failed_test_coverage_inf(failed_coverage_path, funs, production_name, product_with_roles):
    current_coverage_file_list = list_dir(failed_coverage_path)  # each coverage file
    funs_tem = {}
    productFuns = product_with_roles[production_name]
    for sfun in funs:
        if sfun[0] in productFuns:
            for tem in productFuns[sfun[0]]:
                if tem not in funs_tem:
                    funs_tem[tem] = sfun[1]
                    # funs_tem.append([tem, sfun[1]])
        else:
            funs_tem[sfun[0]] = sfun[1]
            # funs_tem.append([sfun[0], sfun[1]])
    out = {}
    for cf in current_coverage_file_list:
        # #read coverage file
        coverage_file = join_path(failed_coverage_path, cf)

        # read
        try:
            tree = ET.parse(coverage_file)
            root = tree.getroot()
            project = root.find("project")
            # package = project.find("package")
            #lines = files.find("line")
            #for package in project:
            #if mutated_project_name == "_MultipleBugs_.NOB_1.ID_2":
            # for key1, value1 in files.attrib.items():
                #print("tem:", tem)

                #print("current:", key1, value1)
                #print("methods_tem", methods_tem)
            start = False
            grade = -1
            for package in project:
                for file in package:
                    for line in file:
                        if line.tag == "line":
                            if line.attrib.get("signature") != None:
                                hn = line.attrib.get("signature").split('(')
                                # if mutated_project_name == "_MultipleBugs_.NOB_1.ID_78":
                                #     if hn[0] == "test":
                                #         print("this is funs:", hn[0])
                                if len(hn) > 0 and hn[0] in funs_tem:
                                    # print(hn[0], type(line.attrib), line.attrib.get("count"),
                                    #       type(line.attrib.get("count")))
                                    start = True
                                    grade = funs_tem[hn[0]]
                                    # out.append(hn[0])
                                else:
                                    start = False
                                    grade = -1

                            if start:
                                # if line.attrib.get("truecount") != None:
                                #     if line.attrib.get("truecount") != "0":
                                num = line.attrib.get("num")
                                if num not in out and grade != -1:
                                    # grade += 0.001
                                    out[num] = grade
                                # elif line.attrib.get("count") != "0":
                                #     num = line.attrib.get("num")
                                #     if num not in out and grade != -1:
                                #         # grade += 0.001
                                #         out[num] = grade
        except:
            logging.info("Exception when parsing %s", coverage_file)
    spectrum_fail_coverage_file = join_path(get_outer_dir(failed_coverage_path), "spectrum_failed_coverage.xml")
    data = get_spectrum_failed_coverage_inf(spectrum_fail_coverage_file, out, production_name)
    return data

def get_gouzao_fun_name(failed_coverage_path):
    failed_production_path = join_path(failed_coverage_path, "src")

def get_unit_test_imformation():
    pass
