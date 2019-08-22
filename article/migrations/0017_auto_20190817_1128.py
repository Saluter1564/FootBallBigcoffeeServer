# Generated by Django 2.0.3 on 2019-08-17 11:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0016_auto_20190817_0959'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamBoutExploits',
            fields=[
                ('amidithion', models.CharField(help_text='赛果', max_length=50, verbose_name='赛果')),
                ('asiaHanciap', models.CharField(help_text='亚盘盘口', max_length=50, verbose_name='亚盘盘口')),
                ('asiaResult', models.CharField(help_text='亚盘结果', max_length=50, verbose_name='亚盘结果')),
                ('awayName', models.CharField(help_text='客队名称', max_length=50, verbose_name='客队名称')),
                ('awayTeamId', models.IntegerField(help_text='客队ID', verbose_name='客队ID')),
                ('awayTeamLogo', models.CharField(help_text='客队LOGO', max_length=50, verbose_name='客队LOGO')),
                ('bigSamllResult', models.CharField(help_text='大小球结果', max_length=50, verbose_name='大小球结果')),
                ('bigSmallHanciap', models.CharField(help_text='大小球盘口', max_length=50, verbose_name='大小球盘口')),
                ('fullResult', models.CharField(help_text='全场比分结果', max_length=50, verbose_name='全场比分结果')),
                ('halfResult', models.CharField(help_text='半场比分结果', max_length=50, verbose_name='半场比分结果')),
                ('homeName', models.CharField(help_text='主队名称', max_length=50, verbose_name='主队名称')),
                ('homeTeamId', models.IntegerField(help_text='主队ID', verbose_name='主队ID')),
                ('homeTeamLogo', models.CharField(help_text='主队LOGO', max_length=50, verbose_name='主队LOGO')),
                ('leagueId', models.IntegerField(help_text='联赛ID', verbose_name='联赛ID')),
                ('leagueName', models.CharField(help_text='联赛名称', max_length=50, verbose_name='联赛名称')),
                ('matchId', models.IntegerField(help_text='比赛ID', primary_key=True, serialize=False, verbose_name='比赛ID')),
                ('matchTime', models.CharField(help_text='比赛日期', max_length=50, verbose_name='比赛日期')),
                ('middle', models.BooleanField(default=False, help_text='是否中立场', verbose_name='是否中立场')),
                ('qiutanMatchId', models.IntegerField(help_text='球探网比赛ID', verbose_name='球探网比赛ID')),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 17, 11, 28, 3, 283413), help_text='发布日期', verbose_name='发布日期'),
        ),
    ]
