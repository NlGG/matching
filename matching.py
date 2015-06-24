# coding: UTF-8

def deferred_acceptance(m_prefs, f_prefs):
    mnum = len(m_prefs)
    fnum = len(f_prefs)
    single = [i for i in range(mnum)]
    married = {}
    have = [mnum for i in range(fnum)]
    down = [0 for i in range(mnum)]

    while len(single) > 0:

        for i in single:

            mbest = m_prefs[i][down[i]]

            if mbest != fnum:

                if  np.where(f_prefs[mbest] == i)[0][0] < \
                      np.where(f_prefs[mbest] == have[mbest])[0][0]:
                    single.remove(i)
                    if have[mbest] != mnum:
                        single.append(have[mbest])
                    have[mbest] = i
                else:
                    if down[i] < fnum - 1:
                        down[i] += 1
                    else:
                        single.remove(i)
                        married.update({i: fnum})
            else:
                single.remove(i)
                married.update({i: fnum})

    for i in have:
        if i != mnum:
            married.update({i: have.index(i)})

    married = married.items()

    m_matched_computed = []
    for i in range(mnum):
        m_matched_computed.append(married[i][1])
    f_matched_computed = have

    return m_matched_computed, f_matched_computed
