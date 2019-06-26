# coding = utf-8


import pandas as pd

ratings_filename = "D:\\PycharmProjects\\CCIR\\StaticData\\ml-100k\\u.data"
all_ratings = pd.read_csv(ratings_filename, delimiter="\t", header=None, names=["UserID", "MovieID", "Rating", "Datetime"])

# 解析时间戳
all_ratings["Datetime"] = pd.to_datetime(all_ratings['Datetime'], unit='s')

all_ratings["Favorable"] = all_ratings["Rating"] > 3
ratings = all_ratings[all_ratings['UserID'].isin(range(200))]
favorable_ratings = ratings[ratings["Favorable"]]

num_favorable_by_movie = ratings[["MovieID", "Favorable"]].groupby("MovieID").sum()
print(num_favorable_by_movie.sort_values("Favorable", ascending=False)[:5])

# 打印前5条
# print(all_ratings[10:15])
