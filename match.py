# coding: UTF-8

male = {}
male2 = []
for i in range(5):
    list = []
    for j in range(5):
        print "男性No",i+1,"が",j+1,"番目に好きな女性は"
        pref = input()
        list.append(int(pref))
    male.update({i+1: list})
    male2 = male.items()
    print "男性No", i+1,"の選好入力終わり"
mpref = []
for i in range(len(male2)):
    mpref.append(male2[i][1])
mpref

female = {}
female2 = []
for i in range(5):
    list = []
    for j in range(5):
        print "女性No",i+1,"が",j+1,"番目に好きな男性は"
        pref = input()
        list.append(int(pref))
    female.update({i+1: list})
    female2 = female.items()
    print "No", i+1,"の選好入力終わり"
fpref = []
for i in range(len(female2)):
    fpref.append(female2[i][1])
fpref

mnum = len(mpref)
fnum = len(fpref)
single = []
married = {}
have = []
down = 0

for i in range(fnum):
    have.append(0)

for i in range(mnum):
    single.append(i)

while len(single) > 0:

    for i in single:

        mbest = mpref[i][down] - 1

        if i+1 in fpref[mbest]:
            if have[mbest] == 0:
                single.remove(i)
                have[mbest] = i + 1
            else:
                if down <= len(mpref):
                    if fpref[mbest].index(i+1) > fpref[mbest].index(have[mbest]):
                        single.remove(i)
                        single.append(have[mbest]-1)
                        have[mbest] = i + 1
                    else:
                        down += 1
                else:
                    single.remove(i)
                    married.update({i+1: 0})

        elif down < len(mpref)-1:
            down += 1
        else:
            single.remove(i)
            married.update({i+1: 0})


for i in have:
    if i != 0:
        married.update({i:have.index(i)+1})
    else:
        married.update({0:have.index(i)+1})

married = married.items()
for (i, j) in married:
    print "男性No.%sは女性No.%sと結ばれました。" % (i, j)
