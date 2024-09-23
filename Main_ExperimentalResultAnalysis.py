import os

from experimental_results_analyzer.ExperimentalResultsAnalyzer import summary_result, summary_hitx, \
    write_all_bugs_to_a_file, summary_percentage_of_cases_found_bugs, summary_pbl
from util.FileManager import join_path, EXPERIMENT_RESULT_FOLDER


def aggreate_results(experimental_dirs, num_of_examed_stms):
    experimental_folder_dir = EXPERIMENT_RESULT_FOLDER
    aggregation_folder_dir = join_path(experimental_folder_dir, "result_aggreation")
    print(aggregation_folder_dir)
    if not os.path.exists(aggregation_folder_dir):
        os.makedirs(aggregation_folder_dir)

    all_bugs_file_dir = join_path(aggregation_folder_dir,
                                  "all_bugs_temp_Varcop_Elavetor2.xlsx")

    write_all_bugs_to_a_file(all_bugs_file_dir, experimental_dirs)

    aggregation_file = join_path(aggregation_folder_dir,
                                 "aggreation_Varcop_Elavetor2.xlsx")
    comparison_data = summary_result(all_bugs_file_dir, aggregation_file)

    hitx_file_dir = join_path(aggregation_folder_dir,
                              "hitx_Varcop_Elavetor2.xlsx")
    summary_hitx(hitx_file_dir, all_bugs_file_dir, num_of_examed_stms)
    pbl_file = join_path(aggregation_folder_dir, "pbl_Varcop_Elavetor.xlsx")
    summary_pbl(all_bugs_file_dir, pbl_file, num_of_examed_stms)
    percentage_case_found_bug_file = join_path(aggregation_folder_dir, "percentage_case_found_bug_file_Varcop_Elavetor2.xlsx")

    summary_percentage_of_cases_found_bugs(all_bugs_file_dir, percentage_case_found_bug_file, num_of_examed_stms)
    os.remove(all_bugs_file_dir)


if __name__ == "__main__":
    # parameter configuration
    experimental_dirs = [
        "w=0.5/Elevator/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/ElevatorVarcop_ranking_1Bug_result.xlsx",
        # "w=0.5/BankAccountTP/ENABLE_NORMALIZATION/AGGREGATION_ARITHMETIC_MEAN/4wise/full/2Bug.xlsx",
    ]
    num_of_examed_stms = 10
    # -----------------------------

    aggreate_results(experimental_dirs, num_of_examed_stms)
