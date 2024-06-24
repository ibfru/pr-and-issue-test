import os
import shutil

a = '%05d' % 1
print(type(a))

if os.path.isdir('./script/pr_owner'):
    f_list = os.listdir('./script/pr_owner')
    for f_name in f_list:
        print(f_name)
        # print(f_name.split('_'))

# if os.path.isdir('./script/pr_owner'):
#     shutil.rmtree('./script/pr_owner')
#
# if ~os.path.isdir('./script/pr_owner'):
#     os.mkdir('./script/pr_owner')
#     with open('./script/pr_owner/1.json', 'w+') as f:
#         f.write('11111')
