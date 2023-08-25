import os
import pickle
import requests
import http.cookiejar

login_url = 'https://web-api.okjike.com/api/graphql'
phone_number = '131xxx'
area_code = '+86'
cookies_filename = 'cookies.txt'



# ========== 触发短信验证码 ========== #
def triggerSmsCode(session):
    # 构造验证码请求数据
    SmsCodeData = {
        "operationName": "GetSmsCode",
        "query": "mutation GetSmsCode($mobilePhoneNumber: String!, $areaCode: String!) {\n  getSmsCode(action: PHONE_MIX_LOGIN, mobilePhoneNumber: $mobilePhoneNumber, areaCode: $areaCode) {\n    action\n    __typename\n  }\n}\n",
        "variables": {
            "areaCode": area_code,
            "mobilePhoneNumber": phone_number
        }
    }

    # 发送验证码请求
    response = session.post(login_url, json=SmsCodeData)

    if response.status_code == 200:
        # 请求成功
        response_json = response.json()
        # print(response_json)

        # 处理响应结果
        if 'data' in response_json and 'getSmsCode' in response_json['data']:
            action = response_json['data']['getSmsCode']['action']
            print(f'验证码发送成功，动作：{action}')
            return True
        else:
            print('验证码发送失败')
            return False
    else:
        # 请求失败
        print(f'请求失败，状态码：{response.status_code}')
        return False



# ========== 发送验证码登录请求 ========== #
def loginBySms(session, verification_code):
    # 构造验证码登录请求数据
    loginData = {
        "operationName": "MixLoginWithPhone",
        "query": "mutation MixLoginWithPhone($smsCode: String!, $mobilePhoneNumber: String!, $areaCode: String!) {\n  mixLoginWithPhone(smsCode: $smsCode, mobilePhoneNumber: $mobilePhoneNumber, areaCode: $areaCode) {\n    isRegister\n    user {\n      distinctId: id\n      ...TinyUserFragment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment TinyUserFragment on UserInfo {\n  avatarImage {\n    thumbnailUrl\n    smallPicUrl\n    picUrl\n    __typename\n  }\n  isSponsor\n  username\n  screenName\n  briefIntro\n  __typename\n}\n",
        "variables": {
            "areaCode": "+86",
            "mobilePhoneNumber": phone_number,
            "smsCode": verification_code
        }
    }

    # 发送登录请求
    response = session.post(login_url, json=loginData)

    if response.status_code == 200:
        # 登录请求成功
        response_json = response.json()
        # print(response_json)

        # 摘取信息
        user_info = {}
        if 'data' in response_json and 'mixLoginWithPhone' in response_json['data']:
            # 摘出用户信息
            _user_info = response_json['data']['mixLoginWithPhone']['user']
            # 保留感兴趣的部分
            user_info['distinctId'] = _user_info['distinctId']
            user_info['isSponsor'] = _user_info['isSponsor']
            user_info['username'] = _user_info['username']
            user_info['screenName'] = _user_info['screenName']
            print(f'登录成功！用户ID：{user_info["screenName"]}')
            # # for debug
            # for item in user_info:
            #     print(user_info.get(item))
        else:
            print('登录失败')
    else:
        # 登录请求失败
        print(f'登录请求失败，状态码：{response.status_code}')



# ========== 抓取关注列表动态信息 ========== #
def getFollowingUpdates(session):
    # 构造关注列表动态请求数据
    followingData = {
        "operationName": "FetchSelfFeeds",
        "query": "query FetchSelfFeeds($loadMoreKey: JSON) {\n  viewer {\n    followingUpdates(loadMoreKey: $loadMoreKey) {\n      ...BasicFeedItem\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment BasicFeedItem on FeedsConnection {\n  pageInfo {\n    loadMoreKey\n    hasNextPage\n    __typename\n  }\n  nodes {\n    ... on ReadSplitBar {\n      id\n      type\n      text\n      __typename\n    }\n    ... on MessageEssential {\n      ...FeedMessageFragment\n      __typename\n    }\n    ... on UserAction {\n      id\n      type\n      action\n      actionTime\n      ... on UserFollowAction {\n        users {\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          __typename\n        }\n        allTargetUsers {\n          ...TinyUserFragment\n          following\n          statsCount {\n            followedCount\n            __typename\n          }\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          __typename\n        }\n        __typename\n      }\n      ... on UserRespectAction {\n        users {\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          __typename\n        }\n        targetUsers {\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          __typename\n        }\n        content\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment FeedMessageFragment on MessageEssential {\n  ...EssentialFragment\n  ... on OriginalPost {\n    ...LikeableFragment\n    ...CommentableFragment\n    ...RootMessageFragment\n    ...UserPostFragment\n    ...MessageInfoFragment\n    isPrivate\n    pinned {\n      personalUpdate\n      __typename\n    }\n    __typename\n  }\n  ... on Repost {\n    ...LikeableFragment\n    ...CommentableFragment\n    ...UserPostFragment\n    ...RepostFragment\n    isPrivate\n    pinned {\n      personalUpdate\n      __typename\n    }\n    __typename\n  }\n  ... on Question {\n    ...UserPostFragment\n    __typename\n  }\n  ... on OfficialMessage {\n    ...LikeableFragment\n    ...CommentableFragment\n    ...MessageInfoFragment\n    ...RootMessageFragment\n    __typename\n  }\n  __typename\n}\n\nfragment EssentialFragment on MessageEssential {\n  id\n  type\n  content\n  shareCount\n  repostCount\n  createdAt\n  collected\n  pictures {\n    format\n    watermarkPicUrl\n    picUrl\n    thumbnailUrl\n    smallPicUrl\n    width\n    height\n    __typename\n  }\n  urlsInText {\n    url\n    originalUrl\n    title\n    __typename\n  }\n  __typename\n}\n\nfragment LikeableFragment on LikeableMessage {\n  liked\n  likeCount\n  __typename\n}\n\nfragment CommentableFragment on CommentableMessage {\n  commentCount\n  __typename\n}\n\nfragment RootMessageFragment on RootMessage {\n  topic {\n    id\n    content\n    __typename\n  }\n  __typename\n}\n\nfragment UserPostFragment on MessageUserPost {\n  readTrackInfo\n  user {\n    ...TinyUserFragment\n    __typename\n  }\n  __typename\n}\n\nfragment TinyUserFragment on UserInfo {\n  avatarImage {\n    thumbnailUrl\n    smallPicUrl\n    picUrl\n    __typename\n  }\n  isSponsor\n  username\n  screenName\n  briefIntro\n  __typename\n}\n\nfragment MessageInfoFragment on MessageInfo {\n  video {\n    title\n    type\n    image {\n      picUrl\n      __typename\n    }\n    __typename\n  }\n  linkInfo {\n    originalLinkUrl\n    linkUrl\n    title\n    pictureUrl\n    linkIcon\n    audio {\n      title\n      type\n      image {\n        thumbnailUrl\n        picUrl\n        __typename\n      }\n      author\n      __typename\n    }\n    video {\n      title\n      type\n      image {\n        picUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment RepostFragment on Repost {\n  target {\n    ...RepostTargetFragment\n    __typename\n  }\n  targetType\n  __typename\n}\n\nfragment RepostTargetFragment on RepostTarget {\n  ... on OriginalPost {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    topic {\n      id\n      content\n      __typename\n    }\n    user {\n      ...TinyUserFragment\n      __typename\n    }\n    __typename\n  }\n  ... on Repost {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    user {\n      ...TinyUserFragment\n      __typename\n    }\n    __typename\n  }\n  ... on Question {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    user {\n      ...TinyUserFragment\n      __typename\n    }\n    __typename\n  }\n  ... on Answer {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    user {\n      ...TinyUserFragment\n      __typename\n    }\n    __typename\n  }\n  ... on OfficialMessage {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    __typename\n  }\n  ... on DeletedRepostTarget {\n    status\n    __typename\n  }\n  __typename\n}\n",
        "variables": {}
    }

    # 发送获取动态请求
    response = session.post(login_url, json=followingData)

    if response.status_code == 200:
        # 请求成功
        response_json = response.json()
        # print(response_json)
        if response_json['data']['viewer']['followingUpdates']['nodes']:
            nodes = response_json['data']['viewer']['followingUpdates']['nodes']
            # print(nodes)
            for post in nodes:
                if 'user' in post and 'screenName' in post['user']:
                    print(post['user']['screenName'])
                if 'topic' in post and post['topic']:
                    if 'content' in post['topic']:
                        print(post['topic']['content'])
                if 'content' in post:
                    print(post['content'])
                print('\n')

    else:
        # 请求失败
        print(f'获取动态信息请求失败，状态码：{response.status_code}')



# ========== 抓取广场动态 ========== #
def getRecommendUpdates(session):
    # 构造广场动态请求数据
    recommendData = {
        "operationName": "FetchRecommendFeeds",
        "query": "query FetchRecommendFeeds($loadMoreKey: JSON) {\n  viewer {\n    recommendFeeds(trigger: user, loadMoreKey: $loadMoreKey) {\n      ...BasicFeedItem\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment BasicFeedItem on FeedsConnection {\n  pageInfo {\n    loadMoreKey\n    hasNextPage\n    __typename\n  }\n  nodes {\n    ... on ReadSplitBar {\n      id\n      type\n      text\n      __typename\n    }\n    ... on MessageEssential {\n      ...FeedMessageFragment\n      __typename\n    }\n    ... on UserAction {\n      id\n      type\n      action\n      actionTime\n      ... on UserFollowAction {\n        users {\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          __typename\n        }\n        allTargetUsers {\n          ...TinyUserFragment\n          following\n          statsCount {\n            followedCount\n            __typename\n          }\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          __typename\n        }\n        __typename\n      }\n      ... on UserRespectAction {\n        users {\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          __typename\n        }\n        targetUsers {\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          __typename\n        }\n        content\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment FeedMessageFragment on MessageEssential {\n  ...EssentialFragment\n  ... on OriginalPost {\n    ...LikeableFragment\n    ...CommentableFragment\n    ...RootMessageFragment\n    ...UserPostFragment\n    ...MessageInfoFragment\n    isPrivate\n    pinned {\n      personalUpdate\n      __typename\n    }\n    __typename\n  }\n  ... on Repost {\n    ...LikeableFragment\n    ...CommentableFragment\n    ...UserPostFragment\n    ...RepostFragment\n    isPrivate\n    pinned {\n      personalUpdate\n      __typename\n    }\n    __typename\n  }\n  ... on Question {\n    ...UserPostFragment\n    __typename\n  }\n  ... on OfficialMessage {\n    ...LikeableFragment\n    ...CommentableFragment\n    ...MessageInfoFragment\n    ...RootMessageFragment\n    __typename\n  }\n  __typename\n}\n\nfragment EssentialFragment on MessageEssential {\n  id\n  type\n  content\n  shareCount\n  repostCount\n  createdAt\n  collected\n  pictures {\n    format\n    watermarkPicUrl\n    picUrl\n    thumbnailUrl\n    smallPicUrl\n    width\n    height\n    __typename\n  }\n  urlsInText {\n    url\n    originalUrl\n    title\n    __typename\n  }\n  __typename\n}\n\nfragment LikeableFragment on LikeableMessage {\n  liked\n  likeCount\n  __typename\n}\n\nfragment CommentableFragment on CommentableMessage {\n  commentCount\n  __typename\n}\n\nfragment RootMessageFragment on RootMessage {\n  topic {\n    id\n    content\n    __typename\n  }\n  __typename\n}\n\nfragment UserPostFragment on MessageUserPost {\n  readTrackInfo\n  user {\n    ...TinyUserFragment\n    __typename\n  }\n  __typename\n}\n\nfragment TinyUserFragment on UserInfo {\n  avatarImage {\n    thumbnailUrl\n    smallPicUrl\n    picUrl\n    __typename\n  }\n  isSponsor\n  username\n  screenName\n  briefIntro\n  __typename\n}\n\nfragment MessageInfoFragment on MessageInfo {\n  video {\n    title\n    type\n    image {\n      picUrl\n      __typename\n    }\n    __typename\n  }\n  linkInfo {\n    originalLinkUrl\n    linkUrl\n    title\n    pictureUrl\n    linkIcon\n    audio {\n      title\n      type\n      image {\n        thumbnailUrl\n        picUrl\n        __typename\n      }\n      author\n      __typename\n    }\n    video {\n      title\n      type\n      image {\n        picUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment RepostFragment on Repost {\n  target {\n    ...RepostTargetFragment\n    __typename\n  }\n  targetType\n  __typename\n}\n\nfragment RepostTargetFragment on RepostTarget {\n  ... on OriginalPost {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    topic {\n      id\n      content\n      __typename\n    }\n    user {\n      ...TinyUserFragment\n      __typename\n    }\n    __typename\n  }\n  ... on Repost {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    user {\n      ...TinyUserFragment\n      __typename\n    }\n    __typename\n  }\n  ... on Question {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    user {\n      ...TinyUserFragment\n      __typename\n    }\n    __typename\n  }\n  ... on Answer {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    user {\n      ...TinyUserFragment\n      __typename\n    }\n    __typename\n  }\n  ... on OfficialMessage {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    __typename\n  }\n  ... on DeletedRepostTarget {\n    status\n    __typename\n  }\n  __typename\n}\n",
        "variables": {}
    }

    # 发送获取动态请求
    response = session.post(login_url, json=recommendData)

    if response.status_code == 200:
        # 请求成功
        response_json = response.json()
        # print(response_json)
        if response_json['data']['viewer']['recommendFeeds']['nodes']:
            nodes = response_json['data']['viewer']['recommendFeeds']['nodes']
            # print(nodes)
            cnt_of_post = 0
            for post in nodes:
                # 过滤掉带有图片和视频的动态
                if 'pictures' in post and 'video' in post:
                    if post['pictures'] == None and post['video'] == None:
                        # 输出动态信息
                        cnt_of_post = cnt_of_post + 1
                        if 'user' in post and 'screenName' in post['user']:
                            print('user: ' + post['user']['screenName'])
                        if 'topic' in post and post['topic']:
                            if 'content' in post['topic']:
                                print('theme: ' + post['topic']['content'])
                        if 'likeCount' in post and 'commentCount' in post:
                            print('likeCount: ' + str(post['likeCount']) + ', commentCount: ' + str(post['commentCount']) + '\n')
                        if 'content' in post:
                            print(post['content'])
                        print('\n-----------------------------------------------------\n')
            return cnt_of_post
    else:
        # 请求失败
        print(f'获取广场动态信息请求失败，状态码：{response.status_code}')



# ========== 抓取 N 条广场动态 ========== #
def get_N_RecommendUpdates(session, N):
    print('\n-----------------------------------------------------\n')
    cnt_of_post = getRecommendUpdates(session)
    while(cnt_of_post < N):
        cnt_of_cur = getRecommendUpdates(session)
        cnt_of_post = cnt_of_post + cnt_of_cur




# ========== 加载 cookies 登录 ========== #
def loadfromCookies():
    load_cookiejar = http.cookiejar.MozillaCookieJar()
    load_cookiejar.load(cookies_filename, ignore_discard=True, ignore_expires=True)
    load_cookies = requests.utils.dict_from_cookiejar(load_cookiejar)
    cookies = requests.utils.cookiejar_from_dict(load_cookies)
    session = requests.Session()
    session.cookies = cookies
    return session



# ========== 短信验证码登录 ========== #
def login():
    # 创建会话
    session = requests.Session()
    session.cookies = http.cookiejar.MozillaCookieJar(filename=cookies_filename)
    if(triggerSmsCode(session)):
        # 获取用户输入的验证码
        verification_code = input('请输入收到的验证码：')
    else:
        return
    loginBySms(session, verification_code)
    # 保存登录状态到 cookies 中
    session.cookies.save(ignore_discard=True, ignore_expires=True)
    return session


def main():
    # 判断本地是否有可用 cookies
    if os.path.exists(cookies_filename):
        print("读取本地 cookies")
        # 从 cookies 文件中加载会话状态
        session = loadfromCookies()
    else:
        # 重新登录
        print("无本地 cookies，通过短信验证码登录")
        # 通过短信验证码进行验证登录
        session = login()

    # 开始处理业务逻辑
    # getFollowingUpdates(session)
    cmd = ''
    while cmd != 'bye':
        cmd = input('请输入指令:\n')
        if cmd == 'post':
            get_N_RecommendUpdates(session, 20)
        elif cmd == 'hot':
            print('待开发，可根据点赞数or评论数进行过滤')
        elif cmd == 'bye':
            return
        else:
            print('plz retry')
    # get_N_RecommendUpdates(session, 20)
    return



main()




