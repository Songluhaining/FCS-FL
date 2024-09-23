import os

import pandas

from util.FileManager import join_path, EXPERIMENT_RESULT_FOLDER
from experimental_results_analyzer.ImprovementComparisonAnalyzer import comparison, init_comparison_data
from ranking.Keywords import *
from ranking.RankingManager import VARCOP_RANK, VARCOP_SPACE, VARCOP_DISABLE_BPC_RANK, SBFL_RANK, SPACE
from ranking.Spectrum_Expression import JACCARD, SORENSEN_DICE, TARANTULA, OCHIAI, OP2, BARINEL, DSTAR, ROGERS_TANIMOTO, \
    AMPLE, \
    SIMPLE_MATCHING, RUSSELL_RAO, COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2, WONG1, SOKAL, DICE, HUMANN, ZOLTAR, \
    WONG2, ROGOT2, EUCLID, HAMMING, FLEISS, ANDERBERG, KULCZYNSKI2, HARMONIC_MEAN, GOODMAN

from xlsxwriter import Workbook

default_data_column = [VARCOP_RANK, VARCOP_EXAM, VARCOP_SPACE, VARCOP_TC_RANK, VARCOP_TC_EXAM, SBFL_TC_RANK,
                       SBFL_TC_EXAM,
                       FB_TC_RANK, FB_TC_EXAM, TC_SPACE, VARCOP_DISABLE_BPC_RANK, VARCOP_DISABLE_BPC_EXAM,
                       SBFL_RANK, SBFL_EXAM, FB_RANK, FB_EXAM, SPACE]
default_rank_column = [VARCOP_RANK, VARCOP_TC_RANK, SBFL_TC_RANK, FB_TC_RANK, VARCOP_DISABLE_BPC_RANK, SBFL_RANK,
                       FB_RANK]
SBFL_METRIC_COL = 0
NUM_CASES_COL = 1
NUM_BUGS_COL = 2
VARCOP_RANK_COL = 3
VARCOP_EXAM_COL = 4
VARCOP_SPACE_COL = 5
VARCOP_DISABLE_BPC_RANK_COL = 6
VARCOP_DISABLE_BPC_EXAM_COL = 7
SBFL_RANK_COL = 8
SBFL_EXAM_COL = 9
FB_RANK_COL = 10
FB_EXAM_COL = 11
SPACE_COL = 12

SPECTRUM_EXPRESSIONS_LIST = [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR,
                             RUSSELL_RAO, SIMPLE_MATCHING, ROGERS_TANIMOTO, AMPLE, JACCARD,
                             COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2,
                             WONG1, SOKAL, SORENSEN_DICE, DICE, HUMANN, WONG2, ZOLTAR,
                             EUCLID, ROGOT2, HAMMING, FLEISS, ANDERBERG,
                             GOODMAN, HARMONIC_MEAN, KULCZYNSKI2]


# SPECTRUM_EXPRESSIONS_LIST = [TARANTULA]

def write_all_bugs_to_a_file(all_bugs_file_dir, experimental_dirs):
    writer = pandas.ExcelWriter(all_bugs_file_dir, engine='openpyxl')

    row = 0
    num_of_file = 0
    for file in experimental_dirs:

        file_path = os.path.join(EXPERIMENT_RESULT_FOLDER, file)
        if os.path.exists(file_path):
            excel_data_df = pandas.read_excel(file_path, sheet_name=None)
            num_of_file += 1
            if num_of_file > 1:
                for spectrum_expression_type in SPECTRUM_EXPRESSIONS_LIST:
                    excel_data_df[spectrum_expression_type].to_excel(writer, sheet_name=spectrum_expression_type,
                                                                     startrow=row,
                                                                     index=False, header=False)
                row += len(excel_data_df[TARANTULA])
            else:
                for spectrum_expression_type in SPECTRUM_EXPRESSIONS_LIST:
                    excel_data_df[spectrum_expression_type].to_excel(writer, sheet_name=spectrum_expression_type,
                                                                     startrow=row,
                                                                     index=False)
                row += len(excel_data_df[TARANTULA]) + 1

    writer.save()


def summary_hitx(hitx_file_dir, all_bugs_file_dir, hitn):
    wb = Workbook(hitx_file_dir)
    sheet = wb.add_worksheet("sheet1")
    excel_data_df = pandas.read_excel(all_bugs_file_dir, sheet_name=None)

    row = 0
    for hit_index in range(1, hitn + 1):
        sheet.write(row, hit_index * 3 - 2, HIT + str(hit_index))

    row += 1
    sheet.write(row, 0, SBFL_METRIC)
    for hit_index in range(1, hitn + 1):
        col = hit_index * 3 - 2
        sheet.write(row, col, HIT_VARCOP)

        col += 1
        sheet.write(row, col, HIT_TC_SBFL)
        col += 1
        sheet.write(row, col, HIT_SBFL)
    row += 1

    for spectrum_expression_type in SPECTRUM_EXPRESSIONS_LIST:
        sheet.write(row, 0, spectrum_expression_type)

        col = 0;
        for hit in range(1, hitn + 1):
            col += 1
            sheet.write(row, col, count_hit_x(excel_data_df[spectrum_expression_type][VARCOP_RANK], hit))
            col += 1
            if SBFL_TC_RANK in excel_data_df[TARANTULA]:
                sheet.write(row, col,
                            count_hit_x(excel_data_df[spectrum_expression_type][SBFL_TC_RANK], hit))
            col += 1
            sheet.write(row, col,
                        count_hit_x(excel_data_df[spectrum_expression_type][SBFL_RANK], hit))

        row += 1

    wb.close()


def count_hit_x(value_list, x):
    count = 0
    for value in value_list:
        if type(value) != str and value != -1 and value <= x:
            count += 1
    return count


def summary_result(all_bugs_file, summary_file):
    summary_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                 summary_file)
    wb = Workbook(summary_file_dir)
    sheet = wb.add_worksheet("sheet1")
    excel_data_df = pandas.read_excel(all_bugs_file, sheet_name=None)
    row = 0
    header_column = []
    for item in default_data_column:
        if item in excel_data_df[TARANTULA]:
            header_column.append(item)
    write_header_in_sumary_file(row, sheet, header_column)
    row += 1
    comparison_data = calculate_average_in_a_file(excel_data_df, row, sheet, header_column)

    wb.close()
    return comparison_data


def write_header_in_sumary_file(row, sheet, header_column):
    sheet.write(row, SBFL_METRIC_COL, SBFL_METRIC)
    sheet.write(row, NUM_CASES_COL, NUM_CASES)
    sheet.write(row, NUM_BUGS_COL, NUM_BUGS)
    col = NUM_BUGS_COL + 1
    for item in header_column:
        sheet.write(row, col, item)
        col += 1


def num_of_element(data_list):
    element_count = 0
    for r in data_list:
        if not pandas.isnull(r):
            element_count += 1
    return element_count


def calculate_average_in_a_file(excel_data_df, row, sheet, header_column):
    comparison_data = init_comparison_data()

    for spectrum_expression_type in SPECTRUM_EXPRESSIONS_LIST:
        num_of_cases = num_of_element(excel_data_df[spectrum_expression_type][BUG_ID])
        sheet.write(row, NUM_CASES_COL, num_of_cases)

        num_of_bugs = num_of_element(excel_data_df[spectrum_expression_type][BUGGY_STM])
        sheet.write(row, NUM_BUGS_COL, num_of_bugs)

        sheet.write(row, SBFL_METRIC_COL, spectrum_expression_type)

        average_value_list = average_best_rank_exam(excel_data_df, spectrum_expression_type, header_column)
        # average_value_list = percentage_of_cases_found_bugs(experimental_file_dir, spectrum_expression_type, 3)
        col = NUM_BUGS_COL + 1
        for metric in header_column:
            sheet.write(row, col, average_value_list[metric])
            col += 1
        row += 1

        comparison_data = comparison(comparison_data, average_value_list, spectrum_expression_type)

    return comparison_data


def summary_pbl(all_bugs_file, summary_file, num_of_examed_stms):
    summary_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                 summary_file)
    wb = Workbook(summary_file_dir)
    sheets = []
    num_sheet = 0
    excel_data_df = pandas.read_excel(all_bugs_file, sheet_name=None)
    rank_column = []
    for item in default_rank_column:
        if item in excel_data_df[TARANTULA]:
            rank_column.append(item)

    for spectrum_expression_type in [TARANTULA, OP2, OCHIAI, BARINEL, DSTAR]:
        sheets.append(wb.add_worksheet(spectrum_expression_type))
        sheet = sheets[num_sheet]
        num_sheet += 1
        row = 0
        col = 0
        sheet.write(row, col, "NUM OF EXAMED STMS")
        col += 1
        for item in rank_column:
            sheet.write(row, col, item)
            col += 1
        row += 1
        for num_stm in range(1, num_of_examed_stms + 1):
            col = 0
            sheet.write(row, col, num_stm)
            col = +1
            average_value_list = percentage_of_bugs_found_per_case(excel_data_df, rank_column, spectrum_expression_type,
                                                                   num_stm)
            for metric in rank_column:
                sheet.write(row, col, average_value_list[metric])
                col += 1
            row += 1

    wb.close()


def summary_percentage_of_cases_found_bugs(all_bugs_file, summary_file, num_of_examed_stms):
    summary_file_dir = join_path(EXPERIMENT_RESULT_FOLDER,
                                 summary_file)
    wb = Workbook(summary_file_dir)
    sheets = []
    num_sheet = 0
    excel_data_df = pandas.read_excel(all_bugs_file, sheet_name=None)
    rank_column = []
    for item in default_rank_column:
        if item in excel_data_df[TARANTULA]:
            rank_column.append(item)

    for spectrum_expression_type in [TARANTULA, OP2, OCHIAI, BARINEL, DSTAR]:
        sheets.append(wb.add_worksheet(spectrum_expression_type))
        sheet = sheets[num_sheet]
        num_sheet += 1
        row = 0
        col = 0
        sheet.write(row, col, "NUM OF EXAMED STMS")
        col += 1
        for item in rank_column:
            sheet.write(row, col, item)
            col += 1
        row += 1
        for num_stm in range(1, num_of_examed_stms + 1):
            col = 0
            sheet.write(row, col, num_stm)
            col = +1
            average_value_list = percentage_of_cases_found_bugs(excel_data_df, rank_column, spectrum_expression_type,
                                                                num_stm)

            for metric in rank_column:
                sheet.write(row, col, average_value_list[metric])
                col += 1
            row += 1

    wb.close()


MAX = 100000
MIN = -100000


def percentage_of_bugs_found_per_case(excel_data_df, rank_column, sbfl_metric, num_examined_stm):
    index = 0
    percentage_list = {}
    for metric in rank_column:
        percentage_list[metric] = []
    while index < len(excel_data_df[sbfl_metric][BUG_ID]):
        data, index = get_values_of_a_case(excel_data_df, sbfl_metric, index, rank_column)
        for metric in rank_column:
            temp = 0
            for item in data[metric]:
                if item <= num_examined_stm:
                    temp += 1
            percentage_list[metric].append(temp / len(data[metric]))

    average_percentage_list = {}
    for metric in rank_column:
        average_percentage_list[metric] = calculate_average(percentage_list[metric])
    return average_percentage_list


def percentage_of_cases_found_bugs(excel_data_df, rank_column, sbfl_metric, num_examined_stm):
    index = 0
    percentage_list = {}
    for metric in rank_column:
        percentage_list[metric] = 0
    while index < len(excel_data_df[sbfl_metric][BUG_ID]):
        data, index = get_values_of_a_case(excel_data_df, sbfl_metric, index, rank_column)
        for metric in rank_column:
            for item in data[metric]:
                if item <= num_examined_stm:
                    percentage_list[metric] += 1
                    break

    average_percentage_list = {}
    num_of_cases = num_of_element(excel_data_df[sbfl_metric][BUG_ID])
    for metric in rank_column:
        average_percentage_list[metric] = percentage_list[metric] / num_of_cases
    return average_percentage_list


def calculate_average(data):
    sum = 0
    for item in data:
        sum += item
    return sum / len(data)


def average_best_rank_exam(excel_data_df, sbfl_metric, header_column):
    best_value_list = get_best_rank_exam(excel_data_df, sbfl_metric, header_column)
    average_value_list = {}
    for metric in header_column:
        average_value_list[metric] = calculate_average(best_value_list[metric])
    return average_value_list


def average_worst_rank_exam(excel_data_df, sbfl_metric, header_column):
    best_value_list = get_worst_rank_exam(excel_data_df, sbfl_metric)
    average_value_list = {}
    for metric in header_column:
        average_value_list[metric] = calculate_average(best_value_list[metric])
    return average_value_list


def get_best_rank_exam(excel_data_df, sbfl_metric, header_column):
    index = 0
    best_value_list = {}
    for metric in header_column:
        best_value_list[metric] = []

    while index < len(excel_data_df[sbfl_metric][BUG_ID]):
        data, index = get_values_of_a_case(excel_data_df, sbfl_metric, index, header_column)
        for metric in header_column:
            best_value_list[metric].append(min(data[metric]))
    return best_value_list


def get_worst_rank_exam(excel_data_df, sbfl_metric, header_column):
    index = 0
    best_value_list = {}
    for metric in header_column:
        best_value_list[metric] = []

    while index < len(excel_data_df[sbfl_metric][BUG_ID]):
        data, index = get_values_of_a_case(excel_data_df, sbfl_metric, index, header_column)
        for metric in header_column:
            best_value_list[metric].append(max(data[metric]))
    return best_value_list


def get_values_of_a_case(excel_data_df, sbfl_metric, index, column_list):
    list_of_values = {}
    for metric in column_list:
        list_of_values[metric] = []
        list_of_values[metric].append(excel_data_df[sbfl_metric][metric][index])
    index += 1
    while index < len(excel_data_df[sbfl_metric][BUG_ID]) and pandas.isnull(excel_data_df[sbfl_metric][BUG_ID][index]):
        for metric in column_list:
            list_of_values[metric].append(excel_data_df[sbfl_metric][metric][index])
        index += 1
    return list_of_values, index
