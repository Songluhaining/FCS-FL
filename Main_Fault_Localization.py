import json
import os

import numpy as np
import pandas as pd
#import dowhy
from dowhy import CausalModel
import subprocess

from sklearn import preprocessing
from tables.path import join_path

from ConductDAG import conductDAG, computePred, computePred_copy, computePred_copy1
from dsEvfusion import softmax

from generateObData import gererateObDataFromSB
from methods.mutual_information import su_calculation
from ranking.RankingManager import get_set_of_stms_withScore, get_executed_stms_of_the_system, product_based_assessment, \
    local_ranking_a_suspicious_list, global_ranking_a_suspicious_list, get_set_of_stms, locate_multiple_bugs, \
    search_rank_worst_case_by_layer
from ranking.VarBugManager import is_var_bug_by_config
from spc import SPCsManager
from suspicious_statements_manager.SuspiciousStatementManager import get_multiple_buggy_statements, read_coverage_file, \
    get_suspicious_statement_varcop
from util.FileManager import list_dir, join_path, get_outer_dir
from ranking.Spectrum_Expression import JACCARD, SORENSEN_DICE, TARANTULA, OCHIAI, OP2, BARINEL, DSTAR, ROGERS_TANIMOTO, \
    AMPLE, \
    SIMPLE_MATCHING, RUSSELL_RAO, COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2, WONG1, SOKAL, DICE, HUMANN, ZOLTAR, \
    WONG2, ROGOT2, EUCLID, HAMMING, FLEISS, ANDERBERG, KULCZYNSKI2, HARMONIC_MEAN, GOODMAN



#def quicksort(arr)

def mahalanobis_distance(x, y, cov):
    x = np.array(x).reshape(-1, 1)
    y = np.array(y).reshape(-1, 1)

    diff = x - y
    distance = np.sqrt(np.dot(np.dot(diff.T, np.linalg.inv(cov)), diff))
    return distance[0, 0]


def manhattan_distance(x, y):
    # new_x = np.array(x)
    # new_y = np.array(y)
    return np.sum(np.abs(x - y))

def delete_files_in_folder(folder_path):
    for filename in list_dir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


def get_stms_withScore(dict_of_stm_per_variant):
    stm_set = {}
    for variant in dict_of_stm_per_variant:
        for stm in dict_of_stm_per_variant[variant]:
            if stm not in stm_set:
                stm_set[stm] = dict_of_stm_per_variant[variant][stm]["num_interactions"][1]
            else:
                if dict_of_stm_per_variant[variant][stm]["num_interactions"][1] > stm_set[stm]:
                    stm_set[stm] = dict_of_stm_per_variant[variant][stm]["num_interactions"][1]
    return stm_set

def start_statements_ranking(buggy_systems_folder, failed_graph_nodes, failed_graph_edges, failed_graph_slicenodes, failed_graph_oberData):

    mutated_projects = list_dir(buggy_systems_folder)
    n = 0
    sum = 0
    i = 0
    product_with_roles = {}
    isFirst = True
    Hit1 = 0

    sbfl_metrics = [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR]

    juhe_type = ["SAvg", "JAvg", "Max", "Min", "Mid"]
    output = {}
    for metric in sbfl_metrics:
        output[metric] = pd.DataFrame(columns=["mutated_project_name", "RANK", "EXAM"])



    for mutated_project_name in mutated_projects:
        if i > 0:
            isFirst = False

        mutated_project_dir = join_path(buggy_systems_folder, mutated_project_name)

        if system_name == "ZipMe":
            is_a_var_bug = is_var_bug_by_config(mutated_project_dir, ["Base", "Compress"])
        else:
            is_a_var_bug = is_var_bug_by_config(mutated_project_dir, ["Base"])

        if not is_a_var_bug:
            continue
        SPCsManager.find_SPCs(mutated_project_dir, filtering_coverage_rate=0.1)
        buggy_statements = get_multiple_buggy_statements(mutated_project_name, mutated_project_dir)  #读取mutant.log文件得到异常语句

        delete_files_in_folder(failed_graph_nodes)
        delete_files_in_folder(failed_graph_edges)
        delete_files_in_folder(failed_graph_slicenodes)
        delete_files_in_folder(failed_graph_oberData)

        subprocess.run(['java', '-jar', 'Static_Slicing-master.jar',
                        mutated_project_dir, tem_saved_path]) #join_path(mutated_project_dir, 'spc_10.log')

        suspicious_stms_list = get_suspicious_statement_varcop(mutated_project_dir,0.1)

        # print("suspicious_stms_list", suspicious_stms_list)

        global all_buggy_positions
        all_buggy_positions = {}

        all_stms_of_the_system, all_stms_in_failing_products = get_executed_stms_of_the_system(
            mutated_project_dir, "", 0.1)


        variant_level_suspiciousness = product_based_assessment(mutated_project_dir, all_stms_of_the_system,
                                                                sbfl_metrics, "")

        local_suspiciousness_of_all_the_system = local_ranking_a_suspicious_list(mutated_project_dir,
                                                                                 all_stms_in_failing_products,
                                                                                 sbfl_metrics,
                                                                                 "")  # 能够得到每个语句的可疑分数

        full_ranked_list = {}
        _A = {}
        _B = {}

        suspicious_value_by_varcop = {}
        # varcop_isolated_set = {}
        varcop_isolated_set = get_set_of_stms(suspicious_stms_list)
        if len(varcop_isolated_set) == 0:
            continue
        for metric in sbfl_metrics:
            suspicious_value_by_varcop_metric = {}
            full_ranked_list[metric], _A[metric], _B[metric]  = global_ranking_a_suspicious_list(all_stms_of_the_system,
                                                                all_stms_in_failing_products,
                                                                all_stms_in_failing_products,
                                                                local_suspiciousness_of_all_the_system[metric],
                                                                variant_level_suspiciousness[metric],
                                                                metric,
                                                                "AGGREGATION_ARITHMETIC_MEAN",
                                                                "ENABLE_NORMALIZATION", 0.5)
            if is_a_var_bug:


                varcop_isolated_ranked_list, ranked_list_changed_key, ranked_list_changed_value = global_ranking_a_suspicious_list(all_stms_of_the_system,
                                                                               all_stms_in_failing_products,
                                                                               suspicious_stms_list,
                                                                               local_suspiciousness_of_all_the_system[metric],
                                                                               variant_level_suspiciousness[metric],
                                                                               metric,
                                                                               "AGGREGATION_ARITHMETIC_MEAN",
                                                                               "ENABLE_NORMALIZATION", 0.5)
                for l in range(len(ranked_list_changed_key)):
                    suspicious_value_by_varcop_metric[ranked_list_changed_key[l]] = ranked_list_changed_value[l]
                suspicious_value_by_varcop[metric] = suspicious_value_by_varcop_metric




                RankBySBFL_with_RANK_and_EXAM = locate_multiple_bugs(buggy_statements, varcop_isolated_set,
                                                                                varcop_isolated_ranked_list,
                                                                                full_ranked_list[metric])
            else:
                for l in range(len(_A)):
                    suspicious_value_by_varcop[_A[l]] = _B[l]
                stms_in_f_products_set = get_set_of_stms(all_stms_in_failing_products)
                RankBySBFL_with_RANK_and_EXAM = locate_multiple_bugs(buggy_statements,
                                     stms_in_f_products_set,
                                     full_ranked_list,
                                     full_ranked_list)

        all_stms = len(get_set_of_stms(all_stms_of_the_system))
        gererateObDataFromSB(mutated_project_dir, failed_graph_nodes, failed_graph_oberData)

        list_failed_data = list_dir(failed_graph_nodes)
        results_MAX = {}
        results_MIN = {}
        results_SAVG = {}
        results_JAVG = {}
        results_MED = {}
        failed_product_size = len(list_failed_data)
        for failed_data in list_failed_data:
            productName = failed_data.split('.')[0]
            data_path = join_path(failed_graph_oberData, productName + ".csv")
            data = pd.read_csv(data_path, index_col=0)
            nodePath = failed_graph_slicenodes + productName + ".txt"
            nodes = list(suspicious_stms_list[productName].keys())

            for node in nodes:
                try:
                    if node != "Results":
                        graph, selected_nodes = computePred(node, productName)
                        model = CausalModel(data=data, treatment=node, outcome='Results', graph=graph) #, graph=graphPath  graph
                        identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)
                        estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression") #propensity_score_weighting  linear_regression
                        if node in results_MAX:
                            #max
                            if abs(estimate.value) > results_MAX[node]:
                                results_MAX[node] = abs(estimate.value)
                            #min
                            if abs(estimate.value) < results_MIN[node]:
                                results_MIN[node] = abs(estimate.value)
                            # SAVG
                            results_SAVG[node] += (abs(estimate.value) / failed_product_size)
                            # JAVG
                            results_JAVG[node] *= (abs(estimate.value) ** (1 / failed_product_size))
                            # results[node] = results[node] + abs(estimate.value)
                        else:
                            results_MAX[node] = abs(estimate.value)
                            results_MIN[node] = abs(estimate.value)
                            results_SAVG[node] = (abs(estimate.value) / failed_product_size)
                            results_JAVG[node] = (abs(estimate.value) ** (1 / failed_product_size))
                            results_MED[node] = []
                        results_MED[node].append(abs(estimate.value))

                    #print(node, estimate.value)
                except:
                    results_MAX[node] = 0
                    results_MIN[node] = 0
                    results_SAVG[node] = 0
                    results_JAVG[node] = 0
                    results_MED[node] = 0


        for node in results_MED:
            results_MED[node] = np.median(results_MED[node])

        value_results_MAX = list(results_MAX.values())
        value_results_MIN = list(results_MIN.values())
        value_results_SAVG = list(results_SAVG.values())
        value_results_JAVG = list(results_JAVG.values())
        value_results_MED = list(results_MED.values())

        # ex4
        if len(value_results_MAX) > 0:

            value_results_MAX = softmax(value_results_MAX)
            value_results_MIN = softmax(value_results_MIN)
            value_results_SAVG = softmax(value_results_SAVG)
            value_results_JAVG = softmax(value_results_JAVG)
            value_results_MED = softmax(value_results_MED)


        key_results = list(results_MAX.keys())
        for tem in range(len(key_results)):
            results_MAX[key_results[tem]] = value_results_MAX[tem]
            results_MIN[key_results[tem]] = value_results_MIN[tem]
            results_SAVG[key_results[tem]] = value_results_SAVG[tem]
            results_JAVG[key_results[tem]] = value_results_JAVG[tem]
            results_MED[key_results[tem]] = value_results_MED[tem]

        sstatements_by_sicling = set(list(results_MAX.keys()))
        sstatements = sstatements_by_sicling#.intersection(sstatements_by_FCFLA)
        new_results = {}
        new_results_ci = {}
        tem_row = i
        alpha_w = 0.2
        for metric in sbfl_metrics:
            aw_tem = 0.1

            combined = []

            for sstatement in sstatements:
                new_results[sstatement] = aw_tem * results_MAX[sstatement] + (1 - aw_tem) * \
                                                 suspicious_value_by_varcop[OP2][sstatement]
                combined.append((sstatement, new_results[sstatement]))

            sorted_results = sorted(combined, key=lambda x: x[1], reverse=True)
            index_i = 0

            if is_a_var_bug:
                counter = 0
                for no2, buggy_statement in enumerate(buggy_statements):

                    isNotSearched = True
                    for index, (key, value) in enumerate(sorted_results):
                        # sstatement = sstatements[index]
                        if key == buggy_statement:
                            while index < len(sorted_results) - 1:
                                if sorted_results[index][1] == sorted_results[index + 1][1]: #and sorted_results[index][2] == sorted_results[index + 1][2]:
                                    index += 1
                                else:
                                    break
                            # print("index: ", index+1, buggy_statement)
                            if index == 0:
                                Hit1 += 1
                            isNotSearched = False

                            sum += (index+1)

                            output[metric].loc[i] = [mutated_project_name, index+1, ((index+1) / all_stms) * 100]
                            counter += 1
                            if metric == TARANTULA:
                                i += 1
                            break
            else:
                for buggy_statement in buggy_statements:
                    sum += (RankBySBFL_with_RANK_and_EXAM[buggy_statement]["RANK"])
            n += 1
    return output

if __name__ == '__main__':
    current_working_path = os.getcwd()
    tem_saved_path = join_path(current_working_path, "tem_output")
    if not os.path.isdir(tem_saved_path):
        os.mkdir(tem_saved_path)

    failed_graph_nodes = join_path(tem_saved_path, "node")
    failed_graph_edges = join_path(tem_saved_path, "edge")
    failed_graph_slicenodes = join_path(tem_saved_path, "sliceNode")
    failed_graph_oberData = join_path(tem_saved_path, "oberData")

    if not os.path.exists(failed_graph_nodes):
        os.makedirs(failed_graph_nodes)
    if not os.path.exists(failed_graph_edges):
        os.makedirs(failed_graph_edges)
    if not os.path.exists(failed_graph_slicenodes):
        os.makedirs(failed_graph_slicenodes)
    if not os.path.exists(failed_graph_oberData):
        os.makedirs(failed_graph_oberData)

    system_name = "ExamDB"
    buggy_systems_folder = "/home/whn/Desktop/ExamDB/4wise-ExamDB-1BUG-Full"

    #statement-leavel localization
    output = start_statements_ranking(buggy_systems_folder, failed_graph_nodes, failed_graph_edges, failed_graph_slicenodes, failed_graph_oberData)

    with pd.ExcelWriter("./experimental_results/expriment1/rank_1BUG_results"  + "-" + system_name + ".xlsx") as writer:
        for metric, df in output.items():
            df.to_excel(writer, sheet_name=str(metric))
