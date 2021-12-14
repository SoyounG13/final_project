import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

lost = pd.read_csv("data\\서울특별시 대중교통 분실물 습득물 정보.csv")
rainfall = pd.read_csv("data\\STCS_강수일수_MNH_20211212013612.csv")

lost = lost.iloc[218954:, :]
rainfall = rainfall.iloc[762:, :]

real_date_rainfall = []
for k, j in enumerate(rainfall["연도"]):
    i = k + 762
    if rainfall["날짜"][i] < 1000:
        if rainfall['날짜'][i] % 100 < 10:
            real_date_rainfall.append(f"{j}-0{rainfall['날짜'][i] // 100}-0{rainfall['날짜'][i] % 100}")
        else:
            real_date_rainfall.append(f"{j}-0{rainfall['날짜'][i] // 100}-{rainfall['날짜'][i] % 100}")
    else:
        if rainfall['날짜'][i] % 100 < 10:
            real_date_rainfall.append(f"{j}-{rainfall['날짜'][i] // 100}-0{rainfall['날짜'][i] % 100}")
        else:
            real_date_rainfall.append(f"{j}-{rainfall['날짜'][i] // 100}-{rainfall['날짜'][i] % 100}")

rainfall["진짜날짜"] = real_date_rainfall
real_date = []

for K, i in enumerate(lost["유실물상세내용"]):
    K += 218954
    try:
        if i[0:2] == '저희' and not i[3].isdigit():
            if i[3:7] == '택시번호':
                count = 19
            else:
                count = 2

            while True:
                if i[count].isdigit():
                    break
                else:
                    count += 1

            if f"{i[count:count + 4]}-{i[count + 6:count + 8]}-{i[count + 10:count + 12]}" in real_date_rainfall:
                real_date.append(f"{i[count:count + 4]}-{i[count + 6:count + 8]}-{i[count + 10:count + 12]}")
        else:
            if lost["등록일자"][K] in real_date_rainfall:
                real_date.append(lost["등록일자"][K])

    except:
        if lost["등록일자"][K] in real_date_rainfall:
            real_date.append(lost["등록일자"][K])

x = pd.Series(real_date)
new_data = x.value_counts(sort=False)

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

ax = plt.gca()
plt.plot(list(new_data.sort_index().index.values), list(new_data.values))
rainfall.plot(kind='line', x='진짜날짜', y='관측값', ax=ax)
plt.title('강수량과 분실물 수')
plt.show()

x = np.arange(11)
plt.bar(x, lost["분실물종류"].value_counts().values)
plt.xticks(x, lost["분실물종류"].value_counts().index.values)
plt.show()

x = np.arange(20)
plt.bar(x, lost["수령자치구"].value_counts().values)
plt.xticks(x, lost["수령자치구"].value_counts().index.values)
plt.show()
