import json
import os
import shutil
import sys
import urllib.request

_gitee_base_api_uri = 'https://gitee.com/api/v5/'
_req_method_get = 'GET'

_gitee_org_repos = ['' for _ in range(1024 * 100)]
_gitee_org_repos_size = 0
_gitee_token = ''
_org_name = ''


def do_req_collect_repo():
    headers = {
        'Content-type': 'application-json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    }
    page_no = 1
    global _org_name, _gitee_token
    query = '?access_token=' + _gitee_token + '&page=' + str(page_no) + '&per_page=50'
    req = urllib.request.Request(url=_gitee_base_api_uri + 'orgs/' + _org_name + '/repos' + query, headers=headers,
                                 method='GET')
    res = ''
    repo = None
    repo_size = 0
    global _gitee_org_repos, _gitee_org_repos_size
    flag = True
    while flag:
        with urllib.request.urlopen(req) as netio:
            res = netio.read().decode('utf-8')  # str
            repo = json.loads(res)  # list [dict...]
            repo_size = len(repo)
            for i in range(repo_size):
                _gitee_org_repos[_gitee_org_repos_size] = repo[i]['url']
                _gitee_org_repos_size = _gitee_org_repos_size + 1
            flag = res != '[]'
            print('正在写收集仓，每次请求收集 50 个，当前仓库数: ' + str(_gitee_org_repos_size))
            page_no = page_no + 1
            query = '?access_token=' + _gitee_token + '&page=' + str(page_no) + '&per_page=50'
            req = urllib.request.Request(url=_gitee_base_api_uri + 'orgs/' + _org_name + '/repos' + query,
                                         headers=headers,
                                         method='GET')


def do_req_collect_pr(path):
    headers = {
        'Content-type': 'application-json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    }
    page_no = 1
    query = '?access_token=' + _gitee_token + '&page=' + str(page_no) + '&per_page=50'
    req = urllib.request.Request(url=path + '/pulls' + query, headers=headers, method='GET')
    flag = True
    while flag:
        with urllib.request.urlopen(req) as netio:
            res = netio.read().decode('utf-8')  # str
            flag = res != '[]'
            if flag:
                with open('./pr_res/' + path[31:].split('/')[1] + '_' + str(page_no) + '.json', 'w+',
                          encoding='utf-8') as f:
                    f.write(res)
                print('正在写 pr json 文件...')
            page_no = page_no + 1
            query = '?access_token=' + _gitee_token + '&page=' + str(page_no) + '&per_page=50'
            req = urllib.request.Request(url=path + '/pulls' + query, headers=headers, method='GET')
    print('仓库: ' + path[31:] + ' pr json 文件写入完成')


if __name__ == '__main__':
    args_len = len(sys.argv)

    if args_len != 3:
        sys.exit('请输入正确的参数: python pr_owner_gather.py 组织名称 GiteeToken')

    _org_name = sys.argv[1]
    if len(_org_name) == 0:
        sys.exit('请输入正确的组织名称')
    print('组织名称: ' + _org_name)
    _gitee_token = sys.argv[2]
    if len(_gitee_token) == 0:
        sys.exit('请输入正确的 Gitee Token')
    print('Gitee Token: ' + _gitee_token)

    do_req_collect_repo()
    if os.path.isdir('./pr_res'):
        shutil.rmtree('./pr_res')
    os.mkdir('./pr_res')

    for k in _gitee_org_repos:
        if k:
            do_req_collect_pr(k)
        else:
            break
