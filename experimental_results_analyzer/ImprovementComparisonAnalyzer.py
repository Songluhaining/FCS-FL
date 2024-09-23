from ranking.Keywords import *
from ranking.Spectrum_Expression import JACCARD, SORENSEN_DICE, TARANTULA, OCHIAI, OP2, BARINEL, DSTAR, ROGERS_TANIMOTO, \
    AMPLE, \
    SIMPLE_MATCHING, RUSSELL_RAO, COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2, WONG1, SOKAL, DICE, HUMANN, OVERLAP, ZOLTAR, \
    WONG3, WONG2, M1, ROGOT2, EUCLID, HAMMING, FLEISS, ANDERBERG, KULCZYNSKI1, KULCZYNSKI2, HARMONIC_MEAN, GOODMAN

from xlsxwriter import Workbook

comparison_list = [VARCOP_WIN_RANK, VARCOP_WIN_EXAM, VARCOP_DISABLE_BPC_WIN_RANK, VARCOP_DISABLE_BPC_WIN_EXAM,
                   SBFL_WIN_VARCOP_RANK, SBFL_WIN_VARCOP_EXAM, SBFL_WIN_VARCOP_DISABLED_BPC_RANK,
                   SBFL_WIN_VARCOP_DISABLED_BPC_EXAM]

comparison_metrics = [
    [VARCOP_RANK, SBFL_RANK], [VARCOP_TC_RANK, SBFL_TC_RANK], [VARCOP_RANK, SBFL_TC_RANK],
    [VARCOP_RANK, VARCOP_TC_RANK], [VARCOP_DISABLE_BPC_RANK, SBFL_TC_RANK], [VARCOP_DISABLE_BPC_RANK, SBFL_RANK]
]

SBFL_METRIC_COL = 0
VARCOP_VS_SBFL_RANK_COL = 1
VARCOP_VS_SBFL_EXAM_COL = 2

SPECTRUM_EXPRESSIONS_LIST = [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR,
                             RUSSELL_RAO, SIMPLE_MATCHING, ROGERS_TANIMOTO, AMPLE, JACCARD,
                             COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2,
                             WONG1, SOKAL, SORENSEN_DICE, DICE, HUMANN, WONG2, ZOLTAR,
                             EUCLID, ROGOT2, HAMMING, FLEISS, ANDERBERG,
                             GOODMAN, HARMONIC_MEAN, KULCZYNSKI2]


def init_comparison_data():
    data = {}
    for i in range(0, len(comparison_metrics)):
        metric = comparison_metrics[i][0] + "_vs_" + comparison_metrics[i][1]
        if metric not in data:
            data[metric] = 0
    return data


def comparison(data, average_value_list, spectrum_expression):
    data[spectrum_expression] = {}
    for metrics in comparison_metrics:
        if metrics[0] in average_value_list and metrics[1] in average_value_list:
            tmp = varcop_win(average_value_list[metrics[0]], average_value_list[metrics[1]])
            metric_tmp = metrics[0] + "_vs_" + metrics[1]
            data[spectrum_expression][metric_tmp] = tmp

            if tmp > 0:
                data[metric_tmp] += 1

    return data


def varcop_win(varcop, sbfl):
    return (sbfl - varcop) / sbfl
