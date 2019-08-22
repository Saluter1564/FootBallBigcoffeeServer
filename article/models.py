
# Create your models here.
from django.db import models
import datetime
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Category(models.Model):
    title = models.CharField(max_length=20,verbose_name='名称',help_text="大类")

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']
        verbose_name = '新闻类别'
        verbose_name_plural = verbose_name

class Item(models.Model):
    title = models.CharField(max_length=20, verbose_name='名称',help_text="名称")
    created_date = models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间',help_text="创建时间")
    completed = models.BooleanField(default=False, verbose_name='是否完成',help_text="是否完成")
    categorys = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='items',help_text="大类")

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']
        verbose_name = '新闻子栏目'
        verbose_name_plural = verbose_name

class Tag(models.Model):
    name=models.CharField(max_length=50,verbose_name=u'名称',help_text="名称")
    slug=models.SlugField(max_length=50,verbose_name=u'描述')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题',help_text="名称")
    slug = models.SlugField(unique_for_year='publish_date', verbose_name='描述')
    #author = models.CharField(max_length=100, verbose_name='作者', help_text="作者")
    author = models.ForeignKey(User,related_name='author', on_delete=models.CASCADE,verbose_name='作者',help_text="作者")
    # content = models.TextField(verbose_name='内容')
    content = UEditorField(u'内容', height=400, width=600, default='', imagePath="upload/",
                           toolbars='mini', filePath='upload/', blank=True)
    status = models.CharField(max_length=2, verbose_name='状态',help_text="状态")
    tags = models.ManyToManyField(Tag,related_name='tags', blank=True,help_text="标签")
    publish_date = models.DateTimeField(default=datetime.datetime.now(), verbose_name='发布日期',help_text="发布日期")
    expiration_date = models.DateTimeField(blank=True, null=True, verbose_name='有效日期',help_text="有效日期")
    is_active = models.BooleanField(default=True, blank=True, verbose_name='是否热门',help_text="是否热门")
    item = models.ForeignKey(Item,related_name='item',on_delete=models.CASCADE, verbose_name='类别名称',help_text="类别名称")
    pic = models.ImageField(upload_to='uploads', verbose_name='图片',help_text="图片")
    praise_num = models.IntegerField(default=0, verbose_name='点赞',help_text="点赞")
    read_num  = models.IntegerField(default=0, verbose_name='浏览数',help_text="浏览数")
    fav_num  = models.IntegerField(default=0, verbose_name='收藏数',help_text="收藏数")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '新闻文章'
        verbose_name_plural = verbose_name

class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题',help_text="标题")
    pic = models.ImageField(upload_to='uploads', verbose_name='广告图',help_text="广告图")
    adurl = models.URLField(verbose_name='地址',help_text="地址")
    adlocation = models.CharField(max_length=2, verbose_name='位置',help_text="位置")  # a1,a2,a3,b1,b2,b3....
    status = models.CharField(max_length=1, default=1, verbose_name='状态',help_text="状态")

class UserFav(models.Model):
    """
    用户收藏
    """
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, verbose_name="用户")
    articles = models.ForeignKey(Article, related_name='articles', on_delete=models.CASCADE, verbose_name="文章",
                                 help_text="文章id")
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        unique_together = ("user", "articles")

    def __str__(self):
        return self.user.username
class MatchList(models.Model):
    """
    比赛列表
    """
    aicaiAwayId=models.IntegerField(blank=True,null=True, verbose_name='爱彩客队ID',help_text="爱彩客队ID")
    aicaiHomeId=models.IntegerField( blank=True,null=True,verbose_name='爱彩主队ID',help_text="爱彩主队ID")
    aicaiLeagueId=models.IntegerField( blank=True,null=True,verbose_name='爱彩联赛ID',help_text="爱彩联赛ID")
    awayId=models.IntegerField( verbose_name='客队ID',help_text="客队ID")
    awayLogo=models.CharField( max_length=500,verbose_name='客队LOGO地址',help_text="客队LOGO地址")
    awayName=models.CharField( max_length=50,verbose_name='客队名称',help_text="客队名称")
    awayRank=models.CharField( max_length=50,verbose_name='客队排名',help_text="客队排名")
    bigsmall=models.CharField( max_length=50,verbose_name='大小球盘口',help_text="大小球盘口")
    card=models.CharField( max_length=50,verbose_name='红黄牌',help_text="红黄牌")
    corner=models.CharField( blank=True,null=True,max_length=50,verbose_name='角球',help_text="角球")
    elapsedTime=models.CharField( max_length=50,verbose_name='比赛进行时间',help_text="比赛进行时间")
    homeId=models.IntegerField( verbose_name='主队ID',help_text="主队ID")
    homeLogo=models.CharField( max_length=500,verbose_name='主队LOGO地址',help_text="主队LOGO地址")
    homeName=models.CharField( max_length=50,verbose_name='主队名称',help_text="主队名称")
    homeRank=models.CharField( max_length=50,verbose_name='主队排名',help_text="主队排名")
    isCartoon=models.BooleanField( default=False,verbose_name='是否有动画直播',help_text="是否有动画直播")
    isVideo=models.BooleanField( default=False,verbose_name='是否有视频直播',help_text="是否有视频直播")
    leagueColor =models.CharField( max_length=50,verbose_name='联赛颜色',help_text="联赛颜色")
    leagueId=models.IntegerField( verbose_name='联赛ID',help_text="联赛ID")
    leagueName  =models.CharField( max_length=50,verbose_name='联赛名称',help_text="联赛名称")
    leagueType  =models.IntegerField( verbose_name='联赛类型',help_text="联赛类型")
    matchDate =models.DateTimeField( blank=True,max_length=50,verbose_name='比赛开始日期',help_text="比赛开始日期")
    matchId=models.IntegerField( primary_key=True,verbose_name='比赛ID',help_text="比赛ID")
    matchTime   =models.CharField( max_length=50,verbose_name='比赛开始时间',help_text="比赛开始时间")
    middle=models.BooleanField( default=False,verbose_name='是否中立场地',help_text="是否中立场地")
    oddsAsia=models.CharField( max_length=50,verbose_name='亚盘赔率',help_text="亚盘赔率")
    oddsEurope =models.CharField( max_length=50,verbose_name='欧盘赔率',help_text="欧盘赔率")
    qtMatchId=models.IntegerField( verbose_name='qt比赛ID',help_text="qt比赛ID")
    score =models.CharField( max_length=50,verbose_name='比分数据',help_text="比分数据")
    status=models.IntegerField( verbose_name='比赛进行状态',help_text="比赛进行状态")


class LeagueMatchVo(models.Model):
    """
    比赛信息列表
    """
    awayRank=models.CharField( max_length=50,verbose_name='客队排名',help_text="客队排名")
    awayTeamId=models.IntegerField( verbose_name='客队ID',help_text="客队ID")
    awayTeamLogo=models.CharField(max_length=50, verbose_name='客队LOGO',help_text="客队LOGO")
    awayTeamName=models.CharField( max_length=50,verbose_name='客队名称',help_text="客队名称")
    elapsedTime=models.CharField(max_length=50,verbose_name='比赛进行时间',help_text="比赛进行时间")
    existGroupMatch=models.IntegerField( verbose_name='??',help_text="??")
    homeRank=models.CharField( max_length=50,verbose_name='主队排名',help_text="主队排名")
    homeTeamId=models.IntegerField( verbose_name='主队ID',help_text="主队ID")
    homeTeamLogo=models.CharField(max_length=50,verbose_name='主队LOGO',help_text="主队LOGO")
    homeTeamName=models.CharField( max_length=50,verbose_name='主队名称',help_text="主队名称")
    leagueId=models.IntegerField( verbose_name='联赛ID',help_text="联赛ID")
    leagueMatchId=models.IntegerField( primary_key=True,verbose_name='比赛ID',help_text="比赛ID")
    leagueName=models.CharField( max_length=50,verbose_name='联赛名称',help_text="联赛名称")
    leagueSeasonId=models.IntegerField( verbose_name='联赛季节ID',help_text="联赛季节ID")
    leagueStageId=models.IntegerField( verbose_name='联赛阶段ID',help_text="联赛阶段ID")
    leagueType=models.IntegerField( verbose_name='联赛类型',help_text="联赛类型")
    matchStatus=models.IntegerField( verbose_name='比赛状态',help_text="比赛状态")
    matchTime=models.CharField( max_length=50,verbose_name='比赛开始时间',help_text="比赛开始时间")
    middle=models.BooleanField( verbose_name='是否中立场',help_text="是否中立场")
    qtMatchId=models.IntegerField(blank=True,null=True, verbose_name='???',help_text="???")
    score=models.CharField( blank=True,null=True,max_length=50,verbose_name='比分',help_text="比分")
    seasonFlag=models.IntegerField( blank=True,null=True,verbose_name='联赛季节旗帜',help_text="联赛季节旗帜")

class TeamBoutExploits(models.Model):
    """
    历史交战记录
    """
    amidithion=models.CharField( verbose_name='赛果',help_text="赛果",max_length=50)
    asiaHanciap=models.CharField( verbose_name='亚盘盘口',help_text="亚盘盘口",max_length=50)
    asiaResult=models.CharField( verbose_name='亚盘结果',help_text="亚盘结果",max_length=50)
    awayName=models.CharField( verbose_name='客队名称',help_text="客队名称",max_length=50)
    awayTeamId=models.IntegerField( verbose_name='客队ID',help_text="客队ID")
    awayTeamLogo=models.CharField( verbose_name='客队LOGO',help_text="客队LOGO",max_length=50)
    bigSamllResult=models.CharField( verbose_name='大小球结果',help_text="大小球结果",max_length=50)
    bigSmallHanciap=models.CharField( verbose_name='大小球盘口',help_text="大小球盘口",max_length=50)
    fullResult=models.CharField( verbose_name='全场比分结果',help_text="全场比分结果",max_length=50)
    halfResult=models.CharField( verbose_name='半场比分结果',help_text="半场比分结果",max_length=50)
    homeName=models.CharField( verbose_name='主队名称',help_text="主队名称",max_length=50)
    homeTeamId=models.IntegerField( verbose_name='主队ID',help_text="主队ID")
    homeTeamLogo=models.CharField( verbose_name='主队LOGO',help_text="主队LOGO",max_length=50)
    leagueId=models.IntegerField( verbose_name='联赛ID',help_text="联赛ID")
    leagueName=models.CharField( verbose_name='联赛名称',help_text="联赛名称",max_length=50)
    matchId=models.IntegerField( verbose_name='比赛ID',help_text="比赛ID",primary_key=True)
    matchTime=models.CharField( verbose_name='比赛日期',help_text="比赛日期",max_length=50)
    middle=models.BooleanField( verbose_name='是否中立场',help_text="是否中立场",default=False)
    qiutanMatchId=models.IntegerField( verbose_name='球探网比赛ID',help_text="球探网比赛ID")

class MatchStanding(models.Model):
    attackToScoreRate=models.FloatField( verbose_name='进球转化率',help_text="赛果",max_length=200)
    averageLost=models.FloatField( verbose_name='？？',help_text="？？",max_length=200)
    averageScore=models.FloatField( verbose_name='？？',help_text="？？",max_length=200)
    beCornerKick=models.FloatField( verbose_name='被罚角球',help_text="被罚角球",max_length=200)
    beFreeKick=models.FloatField( verbose_name='被罚任意球',help_text="被罚任意球",max_length=200)
    beShootOn=models.FloatField( verbose_name='被射正',help_text="被射正",max_length=200)
    beShooted=models.FloatField( verbose_name='被射门',help_text="被射门",max_length=200)
    control=models.FloatField( verbose_name='控球比例',help_text="控球比例",max_length=200)
    cornerKick=models.FloatField( verbose_name='角球',help_text="角球",max_length=200)
    dangerousAttack=models.FloatField( verbose_name='危险进攻次数',help_text="危险进攻次数",max_length=200)
    freeKick=models.FloatField( verbose_name='任意球次数',help_text="任意球次数",max_length=200)
    halfControlRate=models.FloatField( verbose_name='半场控球比例',help_text="半场控球比例",max_length=200)
    lostScoreRate=models.FloatField( verbose_name='失分比例',help_text="失分比例",max_length=200)
    shoot=models.FloatField( verbose_name='射门次数',help_text="射门次数",max_length=200)
    shootOn=models.FloatField( verbose_name='射正次数',help_text="射正次数",max_length=200)
    leagueMatchId=models.IntegerField( verbose_name='比赛ID',help_text="比赛ID",primary_key=True)
    homeId = models.IntegerField(verbose_name='主队ID', help_text="主队ID",blank=True,null=True)
    homeLogo = models.CharField(max_length=250, verbose_name='主队LOGO地址', help_text="主队LOGO地址",blank=True,null=True)
    homeName = models.CharField(max_length=50, verbose_name='主队名称', help_text="主队名称",blank=True,null=True)
    awayId = models.IntegerField(verbose_name='客队ID', help_text="客队ID",blank=True,null=True)
    awayLogo = models.CharField(max_length=250, verbose_name='客队LOGO地址', help_text="客队LOGO地址",blank=True,null=True)
    awayName = models.CharField(max_length=50, verbose_name='客队名称', help_text="客队名称",blank=True,null=True)


# class LeagueMatchVO(models.Model):
#     awayTeamId = models.IntegerField(verbose_name='客队ID', help_text="客队ID")
#     awayTeamLogo = models.CharField(verbose_name='客队LOGO', help_text="客队LOGO", max_length=50)
#     awayTeamName=models.CharField( verbose_name='客队名称',help_text="客队名称",max_length=50)
#     homeTeamId = models.IntegerField(verbose_name='主队ID', help_text="主队ID")
#     homeTeamLogo = models.CharField(verbose_name='主队LOGO', help_text="主队LOGO", max_length=50)
#     homeTeamName = models.CharField(verbose_name='主队名称', help_text="主队名称", max_length=50)
#     leagueId = models.IntegerField(verbose_name='联赛ID', help_text="联赛ID")
#     leagueName = models.CharField(verbose_name='联赛名称', help_text="联赛名称", max_length=50)
#     leagueMatchId=models.IntegerField(verbose_name='联赛比赛ID', help_text="联赛比赛ID")
#     matchStatus=models.IntegerField(verbose_name='比赛进行状态', help_text="比赛进行状态")
#     matchTime = models.CharField(verbose_name='比赛日期', help_text="比赛日期", max_length=50)
#     middle = models.BooleanField(verbose_name='是否中立场', help_text="是否中立场", default=False)
#     qtMatchId=models.IntegerField( verbose_name='球探网比赛ID',help_text="球探网比赛ID")
#     seasonFlag=models.IntegerField( blank=True,null=True,verbose_name='联赛季节旗帜',help_text="联赛季节旗帜")



# class jcobMember(models.Model):
#     """
#     竞彩推荐用户数据
#     """
#     user=models.ForeignKey(User,related_name='user',on_delete=models.CASCADE,verbose_name="用户")
#     formatNickName=models.CharField(max_length=40, verbose_name='格式化昵称',help_text="格式化昵称")
#     icon=models.ImageField(upload_to='uploads', verbose_name='头像',help_text="头像")
#     nickName=models.CharField(max_length=40, verbose_name='昵称',help_text="昵称")
#
#     def __str__(self):
#         return self.user.id,self.formatNickName,self.icon,self.nickName
#     class Meta:
#         verbose_name = '竞彩用户数据'
#         verbose_name_plural = verbose_name
#
# class leagueScore(models.Model):
#     """
#     竞彩用户联赛推荐数据
#     """
#     userId=models.ForeignKey(User,related_name='user',on_delete=models.CASCADE,verbose_name="用户")
#     d15OpenCount=models.IntegerField(default=0, verbose_name='近15日推荐数量',help_text="近15日推荐数量")
#     d15PlanCount = models.IntegerField(default=0, verbose_name='近15日推荐数量', help_text="近15日推荐数量")
#     d15ProfitRatio=models.FloatField(default=0,max_length=19,verbose_name='近15日盈利率', help_text="近15日盈利率")
#     d15ReturnRatio = models.FloatField(default=0, max_length=19, verbose_name='近15日返还率', help_text="近15日返还率")
#     d15WinCount=models.IntegerField(default=0, verbose_name='近15日胜场数', help_text="近15日胜场数")
#     d15WinRatio=models.FloatField(default=0, max_length=19, verbose_name='近15日胜率', help_text="近15日胜率")
#     d30OpenCount = models.IntegerField(default=0, verbose_name='近30日推荐数量', help_text="近30日推荐数量")
#     d30PlanCount = models.IntegerField(default=0, verbose_name='近30日推荐数量', help_text="近30日推荐数量")
#     d30ProfitRatio = models.FloatField(default=0, max_length=19, verbose_name='近30日盈利率', help_text="近30日盈利率")
#     d30ReturnRatio = models.FloatField(default=0, max_length=19, verbose_name='近30日返还率', help_text="近30日返还率")
#     d30WinCount = models.IntegerField(default=0, verbose_name='近30日胜场数', help_text="近30日胜场数")
#     d30WinRatio = models.FloatField(default=0, max_length=19, verbose_name='近30日胜率', help_text="近30日胜率")
#     d7OpenCount = models.IntegerField(default=0, verbose_name='近7日推荐数量', help_text="近7日推荐数量")
#     d7PlanCount = models.IntegerField(default=0, verbose_name='近7日推荐数量', help_text="近7日推荐数量")
#     d7ProfitRatio = models.FloatField(default=0, max_length=19, verbose_name='近7日盈利率', help_text="近7日盈利率")
#     d7ReturnRatio = models.FloatField(default=0, max_length=19, verbose_name='近7日返还率', help_text="近7日返还率")
#     d7WinCount = models.IntegerField(default=0, verbose_name='近7日胜场数', help_text="近7日胜场数")
#     d7WinRatio = models.FloatField(default=0, max_length=19, verbose_name='近7日胜率', help_text="近7日胜率")
#     d90PlanCount=models.IntegerField(default=0, verbose_name='近90日推荐数量', help_text="近90日推荐数量")
#     firstGetPrize=models.IntegerField(default=0, verbose_name='近90日推荐数量', help_text="近90日推荐数量")
#     firstHitAmount=models.FloatField(default=0, max_length=19, verbose_name='近7日胜率', help_text="近7日胜率")
#     gameId=models.IntegerField(default=0, verbose_name='比赛类型', help_text="比赛类型")
#     gameLost=models.IntegerField(default=0, verbose_name='未命中', help_text="未命中")
#     leagueId=models.IntegerField(default=0, verbose_name='联赛ID', help_text="联赛ID")
#     lhcount=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     qiuflag=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     record=models.CharField(max_length=40, verbose_name='记录',help_text="记录")
#     secondGetPrize=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     secondHitAmount=models.FloatField(default=0, max_length=19, verbose_name='？？', help_text="？？")
#     unOpenedCount=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     updateTime=models.DateTimeField(default=datetime.datetime.now, verbose_name=u"添加时间")
#     version=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#
#
# class tjExpertInfo(models.Model):
#     """
#     用户推荐相关数据
#     """
#     userId = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, verbose_name="用户")
#     followReds=models.IntegerField(default=0, verbose_name='带红人数', help_text="带红人数")
#     level=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     lqUnOpenedCount=models.IntegerField(default=0, verbose_name='篮球推荐场次', help_text="篮球推荐场次")
#     qiuFlag=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     zqUnopenedCount=models.IntegerField(default=0, verbose_name='足球推荐场次', help_text="足球推荐场次")
#
# class tjInterpretationSimple(models.Model):
#     contentType=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     createTime=models.DateTimeField( verbose_name='发布日期',help_text="发布日期")
#     displayNoteCount=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     flagBit=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     freeType=models.IntegerField(default=0, verbose_name='免费类型', help_text="免费类型")
#     gameDesc=models.CharField( max_length=40,verbose_name='比赛类型描述',help_text="比赛类型描述")
#     gameEndTime=models.DateTimeField( verbose_name='比赛截止日期',help_text="比赛截止日期")
#     gameId=models.IntegerField(default=0, verbose_name='比赛ID', help_text="比赛ID")
#     gameTypeDesc=models.CharField( max_length=40,verbose_name='比赛类型描述',help_text="比赛类型描述")
#     id=models.IntegerField(default=0, verbose_name='推荐ID', help_text="推荐ID")
#     imgUrl=models.IntegerField(default=0, verbose_name='图片地址', help_text="图片地址")
#     improvStatus=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     issueNo=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     jcobMemberId=models.ForeignKey(User,related_name='user',on_delete=models.CASCADE,verbose_name="用户")
#     lookerCount=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     minRaceMatchTime=models.DateTimeField( verbose_name='？？',help_text="？？")
#     notWinRefund=models.IntegerField(default=0, verbose_name='不中退', help_text="不中退")
#     passType=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     playType=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     price=models.IntegerField(default=0, verbose_name='价格', help_text="价格")
#     publishType=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     raceEndTime=models.DateTimeField( verbose_name='比赛截止时间',help_text="比赛截止时间")
#     raceLeagueList=models.CharField(max_length=40, verbose_name='比赛联赛列表', help_text="比赛联赛列表")
#     raceStatus=models.IntegerField(default=0, verbose_name='比赛状态', help_text="比赛状态")
#     raceStatusDesc=models.CharField(max_length=40, verbose_name='比赛状态描述', help_text="比赛状态描述")
#     raceType=models.IntegerField(default=0, verbose_name='比赛类型', help_text="比赛类型")
#     raceTypeDesc=models.CharField(max_length=40, verbose_name='比赛类型描述', help_text="比赛类型描述")
#     shortDesc=models.CharField(max_length=400, verbose_name='比赛短描述', help_text="比赛短描述")
#     title=models.CharField(max_length=400, verbose_name='标题', help_text="标题")
#     tjInterpretationNo=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     virLookerCount=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     voiceFreeSecond=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     winStatus=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#
# class raceList(models.Model):
#     flagBit=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     formatMatchNo=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     guestTeam=models.CharField(max_length=400, verbose_name='客队', help_text="客队")
#     homeTeam=models.CharField(max_length=400, verbose_name='主队', help_text="主队")
#     isDel=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     isMiddle=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     isOfficial=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     isOwner=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     issueNo=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     matchName=models.CharField(max_length=40, verbose_name='？？', help_text="？？")
#     matchShortName=models.CharField(max_length=40, verbose_name='??', help_text="？？")
#     matchTime=models.DateTimeField(blank=True, null=True, verbose_name='有效日期',help_text="有效日期")
#     planCount=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     raceType=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     saleEndTime=models.DateTimeField(blank=True, null=True, verbose_name='有效日期',help_text="有效日期")
#     status=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     statusStr=models.CharField(max_length=40, verbose_name='??', help_text="??")
#     viewpointCount=models.IntegerField(default=0, verbose_name='？？', help_text="？？")
#     weekName=models.CharField(max_length=40, verbose_name='??', help_text="??")