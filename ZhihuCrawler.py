# Create in 2019-05-29
# Project: Store data from Zhihu in Mysql Database
# Author: SHIELD_QIQI
from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedCaptchaException
from Database import MysqlQI
import jieba
import jieba.analyse
import re
from collections import Counter
import wordcloud

client = ZhihuClient()
# 直接用首次登陆的token文件登陆我的知乎
client.load_token('token.pkl')

# 在数据库中添加删除表为存储数据做准备
mysql = MysqlQI()

# # 删除数据库(urldata)中的所有的表
# tableNum = mysql.cur.execute("SELECT concat('DROP TABLE IF EXISTS ', table_name, ';') ""FROM information_schema.tables WHERE table_schema = 'urldata';")
# print("-------------------------------------\n数据库中原有"+str(tableNum)+"个表")
# print("正在删除.....")
# for i in range(0,tableNum):
#     mysql.cur.execute("SELECT concat('DROP TABLE IF EXISTS ', table_name, ';') ""FROM information_schema.tables WHERE table_schema = 'urldata';")
#     mysql.cur.execute(mysql.cur.fetchone()[0])
#
# tableNum = mysql.cur.execute("SELECT concat('DROP TABLE IF EXISTS ', table_name, ';') ""FROM information_schema.tables WHERE table_schema = 'urldata';")
# if tableNum == 0:
#     print("该数据库下所有表删除完毕\n---------------------------------------")
# else:
#     print("删除失败")
#
# 在数据库(urldata)中新建表
try:
    mysql.cur.execute("create table answer(answer_id int(4),author_name varchar(40),author_healine varchar(40),agree_num int(4),comment_num int(4),thanks_count int(4), url varchar(100))")
    mysql.cur.execute("create table comments(currentanswer_id int(4),commentID int(4), commentpersonName varchar(40), words varchar(300))")
    # 爬取知乎热榜第一的所有回答//5G发放牌照
    question = client.question(328058110)
    for answer in question.answers:
        try:
            mysql.cur.execute("insert into answer values(%d,'%s','%s',%d,%d,%d,'%s')"
                              % (answer.id, answer.author.name, answer.author.headline ,answer.voteup_count, answer.comment_count,answer.thanks_count,answer._build_url()))
        except BaseException:
            print("a answer is nelected")
    question = client.question(328058110)
    for answer in question.answers:
        print(answer.pure_data)
    # 爬取知乎热榜所有评论
    question = client.question(328058110)
    for answer in question.answers:
        for comment in answer.comments:
            if len(comment.content)<300:
                try:
                    pureComment =""
                    Word = re.findall(r'[\u4e00-\u9fa5]', comment.content)
                    for i in range (0,len(Word)):
                        pureComment+=Word[i]
                    mysql.cur.execute("insert into comments values(%d,%d,'%s','%s')"%(answer.id,comment.id,comment.author.name,pureComment))
                except BaseException:
                    print("a comment is nelected")
except BaseException:
    print("数据库中已经存在该表")

#-----------------------------------------------评论词云---------------------------------------------#
comment_num = mysql.cur.execute("select * from comments")
Wordlist = []
wordstring = ""
for i in range(0,comment_num):
    Wordlist += mysql.cur.fetchone()[3]
# Wordlist = re.findall(r'[\u4e00-\u9fa5]',Word)
for i in Wordlist:
    wordstring+=i
# jieba分词
words = list(jieba.cut(wordstring,cut_all=False))
cnt = Counter()
string_final = ""
# 删除无意义的词汇
for string in words:
    if len(string)!=1 and string !="但是" and string !="没有" and string !="不是" and string !="就是" \
            and string !="真的" and string !="如果" and string !="这个" and string !="怎么" and string !="应该" \
            and string != "因为" and string !="那么" and string !="一定" and string !="而且" and string !="一个" \
            and string != "所以" and string !="还有" and string !="可能" and string !="他们" and string !="我们" \
            and string != "你们" and string !="这样" and string !="现在" and string !="只是" and string !="还是" \
            and string != "觉得" and string != "这种" and string != "不会" and string != "那个" and string != "其实" \
            and string != "这些" and string != "然后" and string != "甚至" and string != "只是" and string != "不要" \
            and string != "什么" and string != "可以" and string != "这种" and string != "只是" and string != "还是" \
            and string != "自己" and string != "知道" and string != "不能" and string != "别人" and string != "那些" \
            and string != "只要" and string != "毕竟" and string != "不过" and string != "可是" and string != "就算" \
            and string != "只有" and string != "当然" and string != "之前" and string != "虽然" and string != "以后" \
            and string != "不到" and string != "只能" and string != "或者" and string != "难道" and string != "最后" \
            and string != "而已" and string != "已经" and string != "每个" and string != "基本" and string != "几个" \
            and string != "一样" and string != "需要" and string != "时候" and string != "看到" and string != "这么" \
            and string != "出来" and string != "的话" and string != "一些" and string != "感觉" and string != "事情" \
            and string != "以为" and string != "比较" and string != "比如" and string != "认为" and string != "大家" \
            and string != "确实" and string != "一点" and string != "一下" and string != "是因为" and string != "任何":
        string_final+=string
        cnt[string] += 1
stringForComment = list(jieba.cut(string_final,cut_all=False))
# cnt.most_common()
# 生成词云
words_ls = jieba.cut(string_final, cut_all=False)
words_split = " ".join(words_ls)
wc = wordcloud.WordCloud(font_path="fronts/lanting.TTF",width=1000,height=700,background_color="white")
my_wordcloud = wc.generate(words_split)
wc.to_file("image/wordcloud.png")

#-----------------------------------------------回答headline词云---------------------------------------------#
answer_num = mysql.cur.execute("select * from answer")
Wordlist = []
wordstring = ""
for i in range(0,answer_num):
    Wordlist += mysql.cur.fetchone()[2]
# Wordlist = re.findall(r'[\u4e00-\u9fa5]',Word)
for i in Wordlist:
    wordstring+=i
# jieba分词
words = list(jieba.cut(wordstring,cut_all=False))
cnt = Counter()
string_final = ""
# 删除无意义的词汇
for string in words:
    if len(string)!=1 and string !="None":
        string_final+=string
        cnt[string] += 1
stringForAuthor = list(jieba.cut(string_final,cut_all=False))
# cnt.most_common()
# 生成词云
words_ls = jieba.cut(string_final, cut_all=False)
words_split = " ".join(words_ls)
wc = wordcloud.WordCloud(font_path="fronts/lanting.TTF",width=1000,height=700,background_color="white")
my_wordcloud = wc.generate(words_split)
wc.to_file("image/authorcloud.png")
# client = ZhihuClient()
# user = '+8617863110617'
# pwd = '8256688925cba'
# try:
#     client.login(user, pwd)
#     print(u"登陆成功!")
# except NeedCaptchaException: # 处理要验证码的情况
#     # 保存验证码并提示输入，重新登录
#     with open('a.gif', 'wb') as f:
#         f.write(client.get_captcha())
#     captcha = input('please input captcha:')
#     client.login(user, pwd, captcha)
#
# client.save_token('token.pkl') # 保存token
#有了token之后，下次登录就可以直接加载token文件了
# 爬取知乎热榜第一的所有回答//南昌红谷滩事件
# question = client.question(326429999)
# for answer in question.answers:
#     mysql.cur.execute("insert into answer values(%d,'%s',%d,%d)"
#                       %(answer.id,answer.author.name,answer.voteup_count,answer.comment_count))
# 获取我的知乎基础信息
# me = client.me()
# print('name', me.name)
# print('headline', me.headline)
# print('description', me.description)
# print('following topic count', me.following_topic_count)
# print('following people count', me.following_count)
# print('followers count', me.follower_count)
# print('voteup count', me.voteup_count)
# print('get thanks count', me.thanked_count)
# print('answered question', me.answer_count)
# print('question asked', me.question_count)
# print('collection count', me.collection_count)
# print('article count', me.articles_count)
# print('following column count', me.following_column_count)
#
# print('----------')
# for _, answer in zip(range(5), me.answers.order_by('votenum')):
#     print(answer.question.title, answer.voteup_count)
# print('----------')
# 获取知乎某用户数据///贱贱
# jianjian = client.people("splitter")
# print('name', jianjian.name)
# print('headline', jianjian.headline)
# print('description', jianjian.description)
# print('following topic count', jianjian.following_topic_count)
# print('following people count', jianjian.following_count)
# print('followers count', jianjian.follower_count)
# print('voteup count', jianjian.voteup_count)
# print('get thanks count', jianjian.thanked_count)
# print('answered question', jianjian.answer_count)
# print('question asked', jianjian.question_count)
# print('collection count', jianjian.collection_count)
# print('article count', jianjian.articles_count)
# print('following column count', jianjian.following_column_count)
#
# print('----------')
# for _, answer in zip(range(5), jianjian.answers.order_by('votenum')):
#     print(answer.question.title, answer.voteup_count)
# print('----------')

# ******************************************************* END OF FILE ******************************************************* #