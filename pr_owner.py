import json
import os.path
import shutil

_pr_res = []
# print(os.path.isdir('./know_something'))
# if os.path.isdir('./know_something'):
#     f_list = os.listdir('./know_something')
#     print(f_list)

_pr_owner_dict = {

}

if os.path.isdir('./script/pr_res'):
    f_list = os.listdir('./script/pr_res')
    for f_name in f_list:
        with open('./script/pr_res/' + f_name, 'r', encoding='utf-8') as f_in:
            f_dict = json.load(f_in)  # list [dict...]
            size = len(f_dict)
            i = 0
            while i < size:
                user = f_dict[i]['user']
                if user['login'] in _pr_owner_dict:
                    _pr_owner_dict[user['login']].append(
                        {
                            'name': user['name'],
                            'prNumber': f_dict[i]['number'],
                            'url': f_dict[i]['url'],
                            'state': f_dict[i]['state'],
                            'created_at': f_dict[i]['created_at'],
                            'closed_at': f_dict[i]['closed_at'],
                        }
                    )
                else:
                    _pr_owner_dict[user['login']] = [
                        {
                            'name': user['name'],
                            'prNumber': f_dict[i]['number'],
                            'url': f_dict[i]['url'],
                            'state': f_dict[i]['state'],
                            'created_at': f_dict[i]['created_at'],
                            'closed_at': f_dict[i]['closed_at'],
                        }
                    ]
                i += 1

if os.path.isdir('./script/pr_owner'):
    shutil.rmtree('./script/pr_owner')

if ~os.path.isdir('./script/pr_owner'):
    os.mkdir('./script/pr_owner')

for k in _pr_owner_dict.keys():
    # print(json.dumps(_pr_owner_dict[k], ensure_ascii=False, indent=2))
    with open('./script/pr_owner/user_' + ('%05d' % len(_pr_owner_dict[k])) + '_' + k + '.json', 'w+',
              encoding='utf-8') as f:
        f.write(json.dumps(_pr_owner_dict[k], ensure_ascii=False, indent=2))
