def get_weibo_profile(username,homepage_url):
    '''
    功能 : 根据用户名 和 用户主页地址 返回用户基本信息

    flag : 0 表示成功获取到用户基本信息
           1 表示该用户不存在 或 url不存在
    img_url : 用户头像
    lcoation : 用户位置
    profile : 用户简介
    '''
    flag = img_url = location = profile = ''
    return flag,img_url,location,profile

def get_weibo_state(username):
    '''
    功能 ： 根据用户名 返回 爬取到的该用户的动态（动态内容、发布时间等）


    :param username:
    :return:
    '''
    pass