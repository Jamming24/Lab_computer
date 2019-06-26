# encoding:utf-8
# n表示总用户数
n = int(input())
# m表示关注对
m = int(input())
# 输入关系对
f = input()
focus = f.split(" ")
focus_pair = []
for i in range(0, m):
    focus_pair.append([int(focus[i*2]), int(focus[i*2+1])])
user_focus_content = dict()
for item in focus_pair:
    focus_user = item[1]
    user = item[0]
    if focus_user in user_focus_content.keys():
        content = user_focus_content[focus_user]
        content.append(user)
    else:
        content = [user]
        user_focus_content[focus_user] = content
user_focus_count = dict()
users = user_focus_content.keys()
for user in users:
    user_count = len(user_focus_content[user])
    user_content = user_focus_content[user]
    for u in user_content:
        if user in user_focus_content[u]:
            user_count = user_count + len(user_focus_content[u]) - 1
        else:
            user_count += len(user_focus_content[u])
    user_focus_count[user] = user_count
count = 0
for us in users:
    if user_focus_count[us] == n-1:
        count += 1
print(count)
