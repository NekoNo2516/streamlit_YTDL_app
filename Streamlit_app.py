#导入streamlit制作网页
import streamlit as st
#导入pytube来爬取油管视频信息
import pytube
from pytube import extract, request, YouTube
import pytube.exceptions as exceptions
#导入图片处理相关的库
from PIL import Image
from skimage import io
#导入时间处理相关的库
import datetime as dt
from datetime import time
#导入EasyGui模块来调用文件夹窗口
import easygui as g
#其他用到的库
import ffmpeg
import sys
import os



#通过不同复选框筛选下载选项
def options_filter(a,b,c,d):
    row1, row2, row3, row4, row5 = st.beta_columns((1,1,1,1,1))

    with row1:
        st.write(a)
        
    with row2:
        st.write(b)
        
    with row3:
        st.write(c)
        
    with row4:
        st.write(StrofSize(my_video.streams.get_by_itag(d).filesize))#显示各文件大小
        
    with row5:
        #设置下载按钮#给每个文件的按钮一个唯一的键以区分
        if st.button("Download",key=a+b+c+str(d),help="Click here to download"):

            #通过easygui的diropenbox函数打开文件资源管理器#让用户选择下载地址
            my_path = g.diropenbox('open file', 'C:/User/Administrator/Desktop/__pycache__')
            my_video.streams.get_by_itag(d).download(my_path)

            #优先下载官方字幕#备用自动生成字幕
            if  get_caption_by_language_name(my_video,'English')!=None and language == 'English':
                caption=get_caption_by_language_name(my_video,'English')
            elif get_caption_by_language_name(my_video,'English (auto-generated)')!=None and language == 'English':
                caption=get_caption_by_language_name(my_video,'English (auto-generated)')
            elif get_caption_by_language_name(my_video,'Japanese')!=None and language == 'Japanese':
                caption=get_caption_by_language_name(my_video,'Japanese')
            elif get_caption_by_language_name(my_video,'Japanese (auto-generated)')!=None and language == 'Japanese':
                caption=get_caption_by_language_name(my_video,'Japanese (auto-generated)')
            elif get_caption_by_language_name(my_video,'Chinese')!=None and language == 'Chinese':
                caption=get_caption_by_language_name(my_video,'Chinese')
            elif get_caption_by_language_name(my_video,'Chinese (auto-generated)')!=None and language == 'Chinese':
                caption=get_caption_by_language_name(my_video,'Chinese (auto-generated)')

            content = caption.generate_srt_captions()
            makefile(my_path,content,language)
            

#过滤字幕选项
def get_caption_by_language_name(yt, lang_name):
	for caption in yt.caption_tracks:
		if caption.name == lang_name:
			return caption
		    

#创建srt格式字幕文件并输入文本内容
def makefile(path,content,language):
    if os.path.exists(path):
        if os.path.isdir(path):
            os.chdir(path)
            title='Subtitle['+language+'].srt'
            f = open(title,'w+')
            f.write(content)
            f.seek(0)
            read = f.readline()
            f.close()
            print(read)
        else:
            print('please input the dir name')
    else:
        print('the path is not exists')


#转换文件大小单位的函数
def StrofSize(size):
    def strofsize(integer, remainder, level):
        if integer >= 1024:
            remainder = integer % 1024
            integer //= 1024
            level += 1
            return strofsize(integer, remainder, level)
        else:
            return integer, remainder, level
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    integer, remainder, level = strofsize(size, 0, 0)
    if level+1 > len(units):
        level = -1
    return ('{}.{:>03d} {}'.format(integer, remainder, units[level]))


#配置网页的默认设置
st.set_page_config(page_title=None, page_icon=None, layout='wide', initial_sidebar_state='auto')

#默认打开侧边框
row12, row22, row32 = st.sidebar.beta_columns((3,1,6))

with row12:
    st.text('')
    st.button("Subtitle\nLanguage")
    
with row22:
    st.text('')
    
with row32:
    language = st.select_slider(
         "",
         options=['English', 'Japanese', 'Chinese'])

#在界面首页放一张图片以增加美观
image1=Image.open("C:/Users/David Wu/Pictures/Screenshots/屏幕截图(1).png")
st.image(image1, use_column_width=True)

#设置标题与副标题
st.header("Save"+" YouTube "+"Videos")
st.write('''*\000———Use Python to download YouTube videos*!''')
st.text("\n\n")

#让用户输入视频的URL#并列交互插件使输入文本工具和按钮并排
row1_1, row1_2 = st.beta_columns((6,1))

with row1_1:
    url=row1_1.text_input("ENTER the URL here 👇🏻", value='')    

with row1_2:
    st.header("")
    st.button('SEARCH',help="Click here to search")

if url!="":    
    #对用户输入进行反馈
    st.write("")
    st.write("🌟GOT The Video INFO‼ Check it out!")
    st.write("")
    #用url获取视频信息
    my_video=YouTube(url)
    
    #显示视频标题
    st.write('''🎞︎''',my_video.title)

    row2_1, row2_2 = st.beta_columns((14,15))
    
    with row2_1:
        #封面预览:将视频封面图用skimage通过URL读取并展示在网页界面上
        image2 = io.imread(my_video.thumbnail_url)
        st.image(image2, width=420)
        
    with row2_2:
        #显示视频的作者和时长
        st.header("")
        st.write("Author—",my_video.author)
        st.write("Length*(of time)*—",
            dt.timedelta(seconds=my_video.length))

        #提供复选框让用户筛选下载选项#默认情况下给出的下载选项是720p的mp4视频
        options = st.multiselect(
            "",
            ['Only Audio', 'Only Video','A/V','2160p','1440p','1080p', '720p','360p'],
            ['720p', 'Only Audio'])

    #在侧边显示视频发布日期和播放量
    st.sidebar.title("**【_More Informations_】**")
    st.sidebar.write("🔸PublishDate—",my_video.publish_date)
    st.sidebar.write("🔸Views—",my_video.views,"times")
     
    #显示视频封面的URL以便下载
    st.sidebar.markdown("🔸Thumbnail_URL: ")
    st.sidebar.markdown(my_video.thumbnail_url)

    #用复选框显示视频的关键词#默认显示前四个关键词
    if len(my_video.keywords)>=4:
        st.sidebar.multiselect(
            "🔸Keywords:",
            my_video.keywords,
            [my_video.keywords[0],my_video.keywords[1],my_video.keywords[2],my_video.keywords[3]],
            key=1111)
    #如果关键词很少则全部输出#如果没有关键词提示无关键词
    elif len(my_video.keywords)>0:
        st.sidebar.multiselect(
            "🔸Keywords:",
            my_video.keywords,
            my_video.keywords,
            key=1112)
    else:
        st.sidebar.write("🔸Keywords:") 
        st.text("SORRY~~This video has NO keywords.")
        

    #用代码框的形式输出视频简介以减少简介面积避免喧宾夺主
    st.sidebar.write("🔸Description:")
    st.sidebar.code(my_video.description,language=None)

    ###################下载界面####################
    
    row1, row2, row3, row4, row5 = st.beta_columns((1,1,1,1,1))#显示各列信息名

    with row1:
        st.code("Format")
    with row2:
        st.code("Resolution")
    with row3:
        st.code("Audio Info")
    with row4:
        st.code("File Size")
    with row5:
        st.code("DownloadLink")

    #针对复选框不同的标签过滤下载选项
    ###'Onlu Audio'标签会给出一个纯音频的文件#默认为160kbps#备用70kbps
    if 'Only Audio' in options and my_video.streams.get_by_itag(251)!=None:
        options_filter("WEBM","No","160kbps",251)
    if 'Only Audio' in options and my_video.streams.get_by_itag(251)==None:
        options_filter("WEBM","No","70kbps",250)

    ###'2160p'标签仅有纯视频选项#油管将高分辨率视频全部拆分为音视频两个文件#提供MP4和WEBM两种格式
    if '2160p' in options and 'A/V' not in options and my_video.streams.get_by_itag(313)!=None :
        options_filter("WEBM",'2160p','No',313)
    if '2160p' in options and 'A/V' not in options and my_video.streams.get_by_itag(401)!=None :
        options_filter("MP4",'2160p','No',401)

    ###'1440p'选项同'2160p'
    if '1440p' in options and 'A/V' not in options and my_video.streams.get_by_itag(271)!=None :
        options_filter("WEBM",'1440p','No',271)
    if '1440p' in options and 'A/V' not in options and my_video.streams.get_by_itag(400)!=None :
        options_filter("MP4",'1440p','No',400)

    ##'1080p'选项同'2160p'
    if '1080p' in options and 'A/V' not in options and my_video.streams.get_by_itag(248)!=None :
        options_filter("WEBM",'1080p','No',248)
    if '1080p' in options and 'A/V' not in options and my_video.streams.get_by_itag(137)!=None :
        options_filter("MP4",'1080p','No',137)

    ##'720p'及以下的油管视频有音视频为一个文件#此处提供纯视频和音视频选项
    if '720p' in options and 'A/V' not in options and my_video.streams.get_by_itag(247)!=None :
        options_filter("WEBM",'720p','No',247)
    if '720p' in options and 'A/V' not in options and my_video.streams.get_by_itag(136)!=None :
        options_filter("MP4",'720p','No',136)
    if '720p' in options and 'Only Video' not in options and my_video.streams.get_by_itag(22)!=None :
        options_filter("MP4",'720p','Yes',22)

    ##'360p'仅给出音视频选项
    if '360p' in options and 'Only Video' not in options and my_video.streams.get_by_itag(18)!=None :
        options_filter("MP4","360p","Yes",18)
  

else:
    #使用python代码文本格式输出爬虫限制信息
    code1='''#Caution: Downloading some of music videos and copyrighted content is restricted.'''
    st.text(code1)

