
# zzu_auto_jktb
郑州大学每日健康自动填报脚本

12点钟还没起床的同学必备 ：）

![image](https://github.com/Cerber2ol8/zzu_auto_jktb/blob/master/GQPLJJ2D%259X7UW)9YX_%40C%40B.png)

与计划任务一同食用更佳~

代码已更新定时自动运行（前提你得有服务器或者电脑一直不关 ^ ^）

需要自行安装几个必要依赖包

$pip install lxml requests beautifulsoup4

当然你也可以只运行一次，填写好自己的数据和时间后

$python zzu_jktb.py 即可



如果要每天都运行，执行时可以选择后台挂起

$nohup python zzu_jktb.py &

签到什么的都让服务器去做吧~

麻麻再也不用担心中午12点被导员在微信群里艾特了！

代码最后

schedule.every().day.at("08:53").do(main) 

中的时间根据自身情况修改

代码中的表单数据，两个data部分需要根据自身情况修改

    data = {'uid':'学号',    #学号
            'upw':    '登录密码',   #登录密码
            'day6':     'b',    #修改首次填报=a     每日填报=b
            'myvs_1':   '是',    #1体温是否正常     是/否
            'myvs_2':   '否',    #2是否有咳嗽       是/否
            'myvs_3':   '否',    #3否有乏力症状     是/否
            'myvs_4':   '否',    #4是否有鼻塞     是/否
            'myvsw_1':  '否',    #5是否在郑州       是/否
            'myvsp_1':  'xx',       #6现在居住地       如河南省=41
            'myvsp_3':  'xxxx',     #地市             (身份证地区编码)如河南郑州=4101
            'myvsw_2':  'xxxxxxx',    #详细地址         xxxxxxx
            'myvsw_a1': '否',    #7所在小区(村)是否有确诊    是/否
            'myvsw_a2': '否',    #8共同居住人是否有确诊    是/否
            'myvsp_6':  '否',    #9是否刚从外地返回郑州    是/否
            'myvsp_5':  '正常',  #10是否刚从外地返回郑州    正常
            'myvsw_3':  '否',    #11是否有外出       是/否
            'myvsw_5':  '在家学习', #12在家还在校         在家学习/在学校学习
            }
