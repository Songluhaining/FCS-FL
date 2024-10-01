# FCS-FL

Fault localization is one of the most expensive, tedious, and time-consuming activities in software debugging, and it is also an indispensable key step in software maintenance. Due to the variability of faults, fault localization is even more challenging in software product lines. Although significant progress has been made in fault localization for single-system software, research on fault localization for variability in software product lines is relatively insufficient. Meanwhile, existing methods face challenges such as low efficiency and poor root cause localization due to the issues of repeated generation and checking of feature interactions, as well as the propagation of faults between program statements. To address this, this paper proposes an efficient and accurate fault localization method for software product lines, which performs localization at both the feature level and the statement level. At the feature level, based on the observations of inclusion relationships and identical subsets between suspicious feature selection sets, the method identifies suspicious feature interactions more efficiently. At the statement level, a reduced causal model with mediator variables is used, combining causal effects and spectrum effects to achieve more precise fault localization. Four advanced fault localization methods for software product lines were selected, and experiments were conducted on six real-world software product line systems for comparison. The results demonstrate that the proposed method significantly outperforms other mainstream methods in terms of localization efficiency and accuracy.

### Ranking buggy SPL system

In order to rank buggy statements in SPL systems, you can simply configure the appropriate arguments in the file Main_Fault_Localization.py and then execute it.

The meaning of arguments are as following:
1. **system_name**: For example Email, GPL, or ZipMe, etc
2. **buggy_systems_folder**: the path of the folder where you place the buggy versions of the systems, e.g. /home/whn/ExamDB/4wise-ExamDB-1BUG-Full

The ranking result will be written into an excel file and store in the folder experimental_results, which is a folder of this project.

### Data.
1. The full version of data, you can download [here](https://tuanngokien.github.io/splc2021/)
2. In our work, we eliminated all cases of non-feature interaction defects to demonstrate the validity of the method.

