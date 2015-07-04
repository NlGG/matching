# coding: UTF-8

import numpy as np

def deferred_acceptance(p_prefs, r_prefs, caps=None):
    p_prefs_ar = np.array(p_prefs, dtype=int)
    r_prefs_ar = np.array(r_prefs, dtype=int)
    pnum = len(p_prefs_ar)
    rnum = len(r_prefs_ar)

    if caps == None:
        orcaps = None
        caps = np.ones(rnum, dtype = int)
    else:
        orcaps = caps

    unmatched = [i for i in range(pnum)]
    unmatched_num_p = rnum
    unmatched_num_r = pnum
    down = [0 for i in range(pnum)]
    total_cap = sum(caps)
    prop_matched = np.zeros(pnum, dtype=int) + unmatched_num_p
    resp_matched = np.zeros(total_cap, dtype=int) + unmatched_num_r
    indptr = np.empty(rnum+1, dtype=int)
    indptr[0] = 0
    np.cumsum(caps, out=indptr[1:])
    vacancies = caps
    vacancy_pbest =1

    while len(unmatched) > 0:
        for i in unmatched:
            pbest = p_prefs_ar[i][down[i]] # 現在申し込んだ相手

            if pbest == unmatched_num_p: # unmatchedを志望した場合
                prop_matched[i] = unmatched_num_p
                unmatched.remove(i)

            else:
                rank_i = np.where(r_prefs_ar[pbest] == i)[0][0]
                rank_of_rej = np.where(r_prefs_ar[pbest] == unmatched_num_r)[0][0]
                vacancy_pbest = vacancies[pbest]

                if rank_i < rank_of_rej: # 大学に「こんなやついらない」と思われてない場合
                    if vacancy_pbest != 0: # 空きがある
                        resp_matched[indptr[pbest] + vacancy_pbest - 1] = i
                        prop_matched[i] = pbest
                        unmatched.remove(i)
                        vacancies[pbest] = vacancies[pbest] - 1
                        down[i] += 1

                    else: # 空きがない
                        cap_pbest = len(resp_matched[indptr[pbest]:indptr[pbest+1]])
                        ranks = np.zeros(cap_pbest, dtype=int)
                        # 今受け入れてる人たちが、選好ランキングでいくつかを計算
                        for j, k in enumerate(resp_matched[indptr[pbest]:indptr[pbest+1]]):
                            rank_k = np.where(r_prefs_ar[pbest] == k)[0][0]
                            ranks[j] = rank_k

                        #rank_i = np.where(r_prefs_ar[pbest] == i)[0][0]
                        ranks_sort = ranks.argsort()

                        # 今持ってる人の中で最悪の人より、応募者iのがよい場合
                        if rank_i < ranks[ranks_sort[-1]]:
                            replaced_place = ranks_sort[-1]
                            replaced_name = resp_matched[indptr[pbest]:indptr[pbest+1]][replaced_place]
                            #np.insert(resp_matched, indptr[pbest] + np.where((ranks[rank_i-1] <= rank_i) & (ranks[rank_i+1] > ranks_i ))[0][0], i)
                            resp_matched[indptr[pbest] + replaced_place] = i
                            prop_matched[i] = pbest
                            prop_matched[replaced_name] = unmatched_num_p
                            down[i] += 1
                            unmatched.remove(i)
                            unmatched.append(replaced_name)

                        else: # iさんは今いる誰よりも好きじゃない場合
                            down[i] += 1

                else: # 大学側に「こんなやついらない」と思われてた場合
                    down[i] += 1

    # resp_unmatchedを名前順に直す
    for i in range(rnum):
        resp_matched[indptr[i]:indptr[i+1]].sort()

    if orcaps == None:
        return prop_matched, resp_matched

    else:
        return prop_matched, resp_matched, indptr
