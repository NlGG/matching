# coding: UTF-8

def deferred_acceptance(m_prefs, f_prefs):
    mnum = len(m_prefs)
    fnum = len(f_prefs)
    single = []
    married = {}
    have = []
    down = []

    for i in range(mnum):
        down.append(0)

    for i in range(fnum):
        have.append(-1)

    for i in range(mnum):
        single.append(i)

    while len(single) > 0:

        for i in single:

            mbest = m_prefs[i][down[i]]

            if mbest != -1:

                if f_prefs[mbest].index(i) < f_prefs[mbest].index(have[mbest]):
                    single.remove(i)
                    if have[mbest] != -1:
                        single.append(have[mbest])
                    have[mbest] = i
                else:
                    if down[i] < mnum - 1:
                        down[i] += 1
                    else:
                        single.remove(i)
                        married.update({i: -1})
            else:
                single.remove(i)
                married.update({i: -1})

    for i in have:
        if i != -1:
            married.update({i: have.index(i)})

    married = married.items()

    m_matched_computed = []
    for i in range(mnum):
        m_matched_computed.append(married[i][1])
    f_matched_computed = have

    return m_matched_computed, f_matched_computed
