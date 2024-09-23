import random

import numpy as np
from numpy.random import rand
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from methods.mutual_information import su_calculation
from sklearn import metrics

def get_new_SU(df, class_number_train, dim):
    new_su = np.zeros(dim)
    dis_with_features = np.zeros((class_number_train, dim))
    fangcha = np.zeros(dim)
    xx = np.zeros((dim, class_number_train))
    store_class_i = []
    for i in range(class_number_train):
        class_i_df = df[df.iloc[:, -1] == i]
        store_class_i.append(class_i_df)
    total_n = (class_number_train*(class_number_train-1))/2
    for i in range(class_number_train):
        class_i = store_class_i[i]
        for j in range(i+1, class_number_train):
            class_j = store_class_i[j]
            for qq in range(dim):
                arr1 = class_i.iloc[:, qq]
                arr2 = class_j.iloc[:, qq]
                avg1 = arr1.mean()

                avg2 = arr2.mean()

                dis_with_features[i, qq] = avg1

                # print("np.sqrt(avg1 - avg2):", np.abs(avg1 - avg2))
                # print("np.max(arr1):", np.max(arr1))
                # print("np.min(arr1):", np.min(arr1))
                new_su[qq] += (np.abs(avg1 - avg2) / (abs(np.max(arr1) - np.min(arr1)) + abs(np.max(arr2) - np.min(arr2))))
                xx[qq, i] = avg1
                #new_su[qq] += (stats.mannwhitneyu(arr1, arr2)[1] / total_n)
                variance_fj = np.var(arr1)
                fangcha[qq] += (variance_fj / class_number_train)
    for i in range(dim):
        new_su[i] = new_su[i] + fangcha[i]
    print("每个特征的方差平均值为:", new_su)
    return new_su#, xx, dis_with_features


def get_fitness(particle, cluster_k, df, x_train, y_train, x_test, y_test, tot_features, features_counter, best_ind):
    features = []
    # particle = transfer_func(particle).copy()
    # for x in range(len(particle)):
    #     if particle[x] >= 0.5:
    #         features.append(df.columns[x])
    # for lll in range(0, len(particle)):
    #     cluster_lll = particle[lll].copy()

    for jjj in range(0, len(particle)):
        #cluster_counter_j = features_counter[jjj]

        clu_attack = cluster_k[jjj].copy()
        clu_attack_values = list(clu_attack.values()).copy()
        clu_attack_keys = list(clu_attack.keys()).copy()
        if particle[jjj] >= 0.5:
            if particle[jjj] >= len(clu_attack_keys):
                particle[jjj] = len(clu_attack_keys)-1

            #print("sadas:", len(clu_attack_keys), int(particle[jjj]))
            features.append(clu_attack_keys[int(particle[jjj]) - 1])
            #cluster_counter_j[int(particle[jjj])- 1] = cluster_counter_j[int(particle[jjj])- 1] + 1
        else:
            particle[jjj] = 0
        #features_counter[jjj] = cluster_counter_j
    # if (len(features) == 0):
    # return 10000
    if (len(features) == 0):
        # print("no empty", particle)
        # return 10000
        kk = random.randint(1, tot_features)
        k1 = random.randint(0, tot_features - 1)
        for x in range(kk):
            k1 = (k1 + random.randint(0, tot_features - 1)) // tot_features
            particle[k1] = np.random.rand() / 2 + 0.5
            features.append(df.columns[k1])
    new_x_train = x_train[features].copy()
    new_x_test = x_test[features].copy()

    _classifier = KNeighborsClassifier(n_neighbors=5)
    _classifier.fit(new_x_train, y_train)
    predictions = _classifier.predict(new_x_test)
    #acc = accuracy_score(y_true=y_test, y_pred=predictions)
    acc = np.sum(y_test == predictions) / new_x_test.shape[0]
    #error = 1 - acc
    # fitness = acc
    err = 1 - acc
    num_features = len(features)
    d1 = np.sqrt(np.sum(np.square(best_ind - particle)))
    fitness = (0.01 * (num_features / tot_features) + 0.99 * err)
    return fitness, acc, features_counter, particle


def get_fitness_NB(particle, cluster_k, df, x_train, y_train, x_test, y_test, tot_features, features_counter):
    features = []
    # particle = transfer_func(particle).copy()
    # for x in range(len(particle)):
    #     if particle[x] >= 0.5:
    #         features.append(df.columns[x])
    # for lll in range(0, len(particle)):
    #     cluster_lll = particle[lll].copy()

    for jjj in range(0, len(particle)):
        #cluster_counter_j = features_counter[jjj]

        clu_attack = cluster_k[jjj].copy()
        clu_attack_values = list(clu_attack.values()).copy()
        clu_attack_keys = list(clu_attack.keys()).copy()
        if particle[jjj] >= 0.5:
            if particle[jjj] >= len(clu_attack_keys):
                particle[jjj] = len(clu_attack_keys)-1

            #print("sadas:", len(clu_attack_keys), int(particle[jjj]))
            features.append(clu_attack_keys[int(particle[jjj]) - 1])
            #cluster_counter_j[int(particle[jjj])- 1] = cluster_counter_j[int(particle[jjj])- 1] + 1
        else:
            particle[jjj] = 0
        #features_counter[jjj] = cluster_counter_j
    # if (len(features) == 0):
    # return 10000
    if (len(features) == 0):
        # print("no empty", particle)
        # return 10000
        kk = random.randint(1, tot_features)
        k1 = random.randint(0, tot_features - 1)
        for x in range(kk):
            k1 = (k1 + random.randint(0, tot_features - 1)) // tot_features
            particle[k1] = np.random.rand() / 2 + 0.5
            features.append(df.columns[k1])
    new_x_train = x_train[features].copy()
    new_x_test = x_test[features].copy()
    clf = GaussianNB()
    clf.fit(new_x_train, y_train)
    y_predict = clf.predict(new_x_test)
    y_proba = clf.predict_proba(new_x_test)
    acc = metrics.accuracy_score(new_x_test, y_predict) * 100
    err = 1 - acc
    num_features = len(features)
    fitness = 0.01 * (num_features / tot_features) + (1 - 0.01) * err
    return fitness, acc, features_counter, particle

def get_fitness_ini(particle, cluster_k, df, x_train, y_train, x_test, y_test, tot_features, features_counter, x, C_relevance_fCorr, flCorr):
    #print("flCorr的类型为:", type(flCorr))
    features = []
    #ffCorr = np.zeros((len(particle), len(particle)))
    # particle = transfer_func(particle).copy()
    # for x in range(len(particle)):
    #     if particle[x] >= 0.5:
    #         features.append(df.columns[x])
    # for lll in range(0, len(particle)):
    #     cluster_lll = particle[lll].copy()
    qian_n = 0
    for jjj in range(0, len(particle)):
        #cluster_counter_j = features_counter[jjj].copy()
        C_fCorr = C_relevance_fCorr[jjj]
        clu_attack = cluster_k[jjj].copy()
        clu_attack_values = list(clu_attack.values()).copy()
        clu_attack_keys = list(clu_attack.keys()).copy()
        if particle[jjj] >= 0.5:
            if particle[jjj] >= len(clu_attack_keys):
                particle[jjj] = len(clu_attack_keys) - 1
            # print("sadas:", len(clu_attack_keys), int(particle[jjj]))
            features.append(clu_attack_keys[int(particle[jjj])])
            #cluster_counter_j[int(particle[jjj])] = cluster_counter_j[int(particle[jjj])] + 1
            total_C = 0
            st_st1 = su_calculation(x.values[:, clu_attack_keys[int(particle[jjj])]],
                                               x.values[:, clu_attack_keys[0]])

            total_C = flCorr.get(clu_attack_keys[int(particle[jjj])]) / (
                        1 + st_st1)
            #rt1 = flCorr.get(keys_j[b]) / (1 + st_st1)


            # ffCorr[jjj, qqq] = C_relevance_fCorr111
            # total_C += (C_relevance_fCorr111 / len(particle))
                #ffCorr.append(C_relevance_fCorr)
            if total_C > C_fCorr[int(particle[jjj])]:
                C_fCorr[int(particle[jjj])] = total_C
        else:
            particle[jjj] = 0
        C_relevance_fCorr[jjj] = C_fCorr
        #features_counter[jjj] = cluster_counter_j
    if (len(features) == 0):
        # print("no empty", particle)
        # return 10000
        kk = random.randint(1, tot_features)
        k1 = random.randint(0, tot_features - 1)
        for x in range(kk):
            k1 = (k1 + random.randint(0, tot_features - 1)) // tot_features
            particle[k1] = np.random.rand() / 2 + 0.5
            features.append(df.columns[k1])
    new_x_train = x_train[features].copy()
    new_x_test = x_test[features].copy()

    _classifier = KNeighborsClassifier(n_neighbors=5)
    _classifier.fit(new_x_train, y_train)
    predictions = _classifier.predict(new_x_test)
    # acc = accuracy_score(y_true=y_test, y_pred=predictions)
    acc = np.sum(y_test == predictions) / new_x_test.shape[0]
    # error = 1 - acc
    # fitness = acc
    err = 1 - acc
    num_features = len(features)
    fitness = 0.01 * (num_features / tot_features) + (1 - 0.01) * err
    return fitness, acc, features_counter, C_relevance_fCorr

def get_fitness2(selected_feature_index, df, x_train, y_train, x_test, y_test, tot_features):
    features = selected_feature_index.copy()

    # for x in range(len(particle)):
    #     if particle[x] >= 0.5:
    #         features.append(strong_relevance_features_keys[x])
    # if (len(features) == 0):
    # return 10000
    # if (len(features) == 0):
    #     # print("no empty", particle)
    #     # return 10000
    #     kk = random.randint(1, tot_features)
    #     k1 = random.randint(0, tot_features - 1)
    #     for x in range(kk):
    #         k1 = (k1 + random.randint(0, tot_features - 1)) // tot_features
    #         particle[k1] = np.random.rand() / 2 + 0.5
    #         features.append(df.columns[k1])
    new_x_train = x_train[features].copy()
    new_x_test = x_test[features].copy()

    _classifier = KNeighborsClassifier(n_neighbors=5)
    _classifier.fit(new_x_train, y_train)
    predictions = _classifier.predict(new_x_test)
    acc = accuracy_score(y_true=y_test, y_pred=predictions)

    # fitness = acc
    err = 1 - acc
    num_features = len(features)
    fitness = 0.01 * (num_features / tot_features) + (1 - 0.01) * err
    return fitness, acc


def cluster(x, y, dim):
    C_relevance = np.zeros(dim)
    strong_relevance_features = {}
    weak_correlation_features = {}

    #print(y.values)
    for i in range(0, dim):
        #print("x.values[:, 0]", x.values[:, i])
        C_relevance[i] = calculate_C_Relevance(x.values[:, i], y.values)
    print("相关系数为:", C_relevance)
    SU_max = max(C_relevance)
    print("最大相关值为:", SU_max)
    # p0 = getMin(0.1 * SU_max, (C_relevance[math.floor(dim / (math.log(dim)))]))
    p0 = C_relevance[math.floor(dim / (math.log(dim)))]
    print("p0:", p0)
    for i in range(0, dim):
        if (C_relevance[i] >= p0):
            strong_relevance_features[i] = C_relevance[i]
        else:
            weak_correlation_features[i] = C_relevance[i]
    print("强相关性特征数量为:", len(strong_relevance_features.keys()))
    print("弱相关性特征数量为:", len(weak_correlation_features.keys()))
    # second stage
    U0 = sorted(strong_relevance_features.items(), key=lambda kv: kv[1], reverse=True)
    U0 = dict(U0)
    k = 0
    cluster_k = []
    while len(U0) > 1:
        U1 = U0.copy()
        # C_relevance_f1 = list(U1.keys())[0]
        cluster = []
        values_list = list(U1.values()).copy()
        key_list = list(U1.keys()).copy()
        # print("values_list:", values_list)
        # print("key_list", key_list)
        fj = {}
        fj[key_list[0]] = values_list[0]
        cluster.append(key_list[0])
        C_relevance_f1 = values_list[0]  # 第一个的C相关性
        # print("len(U1):", len(U1))
        dt_max = 0
        for i in range(1, len(values_list)):
            C_relevance_fi = values_list[i]
            dt_with_1th = abs(C_relevance_f1 - C_relevance_fi)
            if dt_with_1th > dt_max:
                dt_max = dt_with_1th
        p1 = dt_max * (math.log(len(U0)) / len(U0))
        #p1 = dt_max * 0.2
        for i in range(1, len(key_list)):
            C_relevance_fi = values_list[i]
            dt_with_1th = abs(C_relevance_f1 - C_relevance_fi)
            if dt_with_1th > p1:
                U1.pop(key_list[i])
        values_list2 = list(U1.values()).copy()
        key_list2 = list(U1.keys()).copy()
        print("U1的长度为:", len(U1))
        for j in range(1, len(values_list2)):
            su_f1_with_fj = su_calculation(x.values[:, key_list[0]], x.values[:, key_list2[j]])
            if su_f1_with_fj >= min(C_relevance_f1, values_list2[j]):
                fj[key_list2[j]] = values_list2[j]
                cluster.append(key_list2[j])
        print("***********************")
        print("U0的长度为:", len(U0))
        print("这类特征的数量:", len(fj))
        for q in fj:
            U0.pop(q)
        print("U0的长度为:", len(U0))
        print("***********************")

        cluster_k.append(fj)
        k = k + 1
    U0 = cluster_k[k - 1].copy()

    print("----------------------------")
    print("聚类结果:", cluster_k)
    print("----------------------------")

    # M = len(cluster_k)
    M = k
    print("M为:", M)
    return M, cluster_k

def bounder(x, a, b):
    if x < a:
        x = random.uniform(a, (a+b)/2)
    if x > b:
        x = random.uniform((a+b)/2, b)
    return x


def init_velocity(lb, ub, N, dim):
    V = np.zeros([N, dim], dtype='float')
    Vmax = np.zeros([1, dim], dtype='float')
    Vmin = np.zeros([1, dim], dtype='float')
    # Maximum & minimum velocity
    for d in range(dim):
        Vmax[0, d] = (1 - 0) / 2
        Vmin[0, d] = -Vmax[0, d]

    for i in range(N):
        for d in range(dim):
            V[i, d] = Vmin[0, d] + (Vmax[0, d] - Vmin[0, d]) * rand()

    return V, Vmax, Vmin