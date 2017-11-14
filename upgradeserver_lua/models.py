#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author: limanman
# emails: xmdevops@vip.qq.com


from __future__ import unicode_literals
from django.db import models
from django.utils import timezone


AREA_CHOICE = [
    ('亚洲区域', (
        ('Asia', 'Asia'),
        ('Asia_Afghanistan', 'Asia_Afghanistan'),
        ('Asia_Aomen', 'Asia_Aomen'),
        ('Asia_Azerbaijan', 'Asia_Azerbaijan'),
        ('Asia_Bahrein', 'Asia_Bahrein'),
        ('Asia_Bangladesh', 'Asia_Bangladesh'),
        ('Asia_Bhutan', 'Asia_Bhutan'),
        ('Asia_Brunei', 'Asia_Brunei'),
        ('Asia_China', 'Asia_China'),
        ('Asia_China_AnHui', 'Asia_China_AnHui'),
        ('Asia_China_BeiJing', 'Asia_China_BeiJing'),
        ('Asia_China_ChongQing', 'Asia_China_ChongQing'),
        ('Asia_China_FuJian', 'Asia_China_FuJian'),
        ('Asia_China_GanSu', 'Asia_China_GanSu'),
        ('Asia_China_GuangDong', 'Asia_China_GuangDong'),
        ('Asia_China_GuangXi', 'Asia_China_GuangXi'),
        ('Asia_China_GuiZhou', 'Asia_China_GuiZhou'),
        ('Asia_China_HaiNan', 'Asia_China_HaiNan'),
        ('Asia_China_HeBei', 'Asia_China_HeBei'),
        ('Asia_China_HeNan', 'Asia_China_HeNan'),
        ('Asia_China_HeiLongJiang', 'Asia_China_HeiLongJiang'),
        ('Asia_China_HuBei', 'Asia_China_HuBei'),
        ('Asia_China_HuNan', 'Asia_China_HuNan'),
        ('Asia_China_JiLin', 'Asia_China_JiLin'),
        ('Asia_China_JiangSu', 'Asia_China_JiangSu'),
        ('Asia_China_JiangXi', 'Asia_China_JiangXi'),
        ('Asia_China_LiaoNing', 'Asia_China_LiaoNing'),
        ('Asia_China_NeiNengGu', 'Asia_China_NeiNengGu'),
        ('Asia_China_NingXia', 'Asia_China_NingXia'),
        ('Asia_China_QingHai', 'Asia_China_QingHai'),
        ('Asia_China_ShanDong', 'Asia_China_ShanDong'),
        ('Asia_China_ShanXi', 'Asia_China_ShanXi'),
        ('Asia_China_ShanXi2', 'Asia_China_ShanXi2'),
        ('Asia_China_ShangHai', 'Asia_China_ShangHai'),
        ('Asia_China_SiChuan', 'Asia_China_SiChuan'),
        ('Asia_China_TianJin', 'Asia_China_TianJin'),
        ('Asia_China_XiZang', 'Asia_China_XiZang'),
        ('Asia_China_XinJiang', 'Asia_China_XinJiang'),
        ('Asia_China_YunNan', 'Asia_China_YunNan'),
        ('Asia_China_ZheJiang', 'Asia_China_ZheJiang'),
        ('Asia_ChristmasIsland', 'Asia_ChristmasIsland'),
        ('Asia_Hongkong', 'Asia_Hongkong'),
        ('Asia_India', 'Asia_India'),
        ('Asia_Indonesia', 'Asia_Indonesia'),
        ('Asia_Iran', 'Asia_Iran'),
        ('Asia_Iraq', 'Asia_Iraq'),
        ('Asia_Israel', 'Asia_Israel'),
        ('Asia_Japan', 'Asia_Japan'),
        ('Asia_Jordan', 'Asia_Jordan'),
        ('Asia_Kampuchea', 'Asia_Kampuchea'),
        ('Asia_Kazakhstan', 'Asia_Kazakhstan'),
        ('Asia_Korea', 'Asia_Korea'),
        ('Asia_Kuwait', 'Asia_Kuwait'),
        ('Asia_Lanka', 'Asia_Lanka'),
        ('Asia_Laos', 'Asia_Laos'),
        ('Asia_Lebanon', 'Asia_Lebanon'),
        ('Asia_Malaysia', 'Asia_Malaysia'),
        ('Asia_Maldives', 'Asia_Maldives'),
        ('Asia_Mongolia', 'Asia_Mongolia'),
        ('Asia_Myanmar', 'Asia_Myanmar'),
        ('Asia_Nepal', 'Asia_Nepal'),
        ('Asia_NorthKorea', 'Asia_NorthKorea'),
        ('Asia_Oman', 'Asia_Oman'),
        ('Asia_Pakistan', 'Asia_Pakistan'),
        ('Asia_Palau', 'Asia_Palau'),
        ('Asia_Philippines', 'Asia_Philippines'),
        ('Asia_Qatar', 'Asia_Qatar'),
        ('Asia_Saudi', 'Asia_Saudi'),
        ('Asia_Singapore', 'Asia_Singapore'),
        ('Asia_Syria', 'Asia_Syria'),
        ('Asia_Taiwan', 'Asia_Taiwan'),
        ('Asia_Tajikistan', 'Asia_Tajikistan'),
        ('Asia_Thailand', 'Asia_Thailand'),
        ('Asia_TimorLeste', 'Asia_TimorLeste'),
        ('Asia_TimorLeste', 'Asia_TimorLeste'),
        ('Asia_Turkmenistan', 'Asia_Turkmenistan'),
        ('Asia_UnitedArabEmirates', 'Asia_UnitedArabEmirates'),
        ('Asia_Uzbekistan', 'Asia_Uzbekistan'),
        ('Asia_Vietnam', 'Asia_Vietnam'),
        ('Asia_Yemen', 'Asia_Yemen'))
    ),
    ('欧洲区域', (
        ('Europe', 'Europe'),
        ('Europe_Ahvenanmaa', 'Europe_Ahvenanmaa'),
        ('Europe_Albania', 'Europe_Albania'),
        ('Europe_Andorra', 'Europe_Andorra'),
        ('Europe_Armenia', 'Europe_Armenia'),
        ('Europe_Austria', 'Europe_Austria'),
        ('Europe_Belarus', 'Europe_Belarus'),
        ('Europe_Belgium', 'Europe_Belgium'),
        ('Europe_BosniaAndHerzegovina', 'Europe_BosniaAndHerzegovina'),
        ('Europe_Britain', 'Europe_Britain'),
        ('Europe_Britain', 'Europe_Britain'),
        ('Europe_Bulgaria', 'Europe_Bulgaria'),
        ('Europe_Croatia', 'Europe_Croatia'),
        ('Europe_Curaao', 'Europe_Curaao'),
        ('Europe_Cyprus', 'Europe_Cyprus'),
        ('Europe_CzechRepublic', 'Europe_CzechRepublic'),
        ('Europe_CzechRepublic', 'Europe_CzechRepublic'),
        ('Europe_Denmark', 'Europe_Denmark'),
        ('Europe_Estonia', 'Europe_Estonia'),
        ('Europe_EuropeanUnion', 'Europe_EuropeanUnion'),
        ('Europe_FaroeIslands', 'Europe_FaroeIslands'),
        ('Europe_Finland', 'Europe_Finland'),
        ('Europe_France', 'Europe_France'),
        ('Europe_Germany', 'Europe_Germany'),
        ('Europe_Gibraltar', 'Europe_Gibraltar'),
        ('Europe_Greece', 'Europe_Greece'),
        ('Europe_Greenland', 'Europe_Greenland'),
        ('Europe_Guernsey', 'Europe_Guernsey'),
        ('Europe_Hungary', 'Europe_Hungary'),
        ('Europe_Iceland', 'Europe_Iceland'),
        ('Europe_Ireland', 'Europe_Ireland'),
        ('Europe_IsleOfMan', 'Europe_IsleOfMan'),
        ('Europe_Italy', 'Europe_Italy'),
        ('Europe_Jersey', 'Europe_Jersey'),
        ('Europe_Latvia', 'Europe_Latvia'),
        ('Europe_Liechtenstein', 'Europe_Liechtenstein'),
        ('Europe_Lithuania', 'Europe_Lithuania'),
        ('Europe_Luxembourg', 'Europe_Luxembourg'),
        ('Europe_Macedonia', 'Europe_Macedonia'),
        ('Europe_Malta', 'Europe_Malta'),
        ('Europe_Micronesia', 'Europe_Micronesia'),
        ('Europe_Moldova', 'Europe_Moldova'),
        ('Europe_Monaco', 'Europe_Monaco'),
        ('Europe_NetherlandAntilles', 'Europe_NetherlandAntilles'),
        ('Europe_Netherlands', 'Europe_Netherlands'),
        ('Europe_Norway', 'Europe_Norway'),
        ('Europe_Palestine', 'Europe_Palestine'),
        ('Europe_Poland', 'Europe_Poland'),
        ('Europe_Portugal', 'Europe_Portugal'),
        ('Europe_Romania', 'Europe_Romania'),
        ('Europe_Russia', 'Europe_Russia'),
        ('Europe_SanMarino', 'Europe_SanMarino'),
        ('Europe_Serbia', 'Europe_Serbia'),
        ('Europe_Slovakia', 'Europe_Slovakia'),
        ('Europe_Slovenia', 'Europe_Slovenia'),
        ('Europe_SolomonIslands', 'Europe_SolomonIslands'),
        ('Europe_Spain', 'Europe_Spain'),
        ('Europe_Svalbard', 'Europe_Svalbard'),
        ('Europe_Sweden', 'Europe_Sweden'),
        ('Europe_Switzerland', 'Europe_Switzerland'),
        ('Europe_Turkey', 'Europe_Turkey'),
        ('Europe_Tuvalu', 'Europe_Tuvalu'),
        ('Europe_Ukraine', 'Europe_Ukraine'),
        ('Europe_Vatican', 'Europe_Vatican'),
        ('Europe_Yugoslavia', 'Europe_Yugoslavia'))
    ),
    ('美洲区域', (
        ('America', 'America'),
        ('America_America', 'America_America'),
        ('America_AmericanSamoa', 'America_AmericanSamoa'),
        ('America_Anguilla', 'America_Anguilla'),
        ('America_AntiguaBarbuda', 'America_AntiguaBarbuda'),
        ('America_Argentina', 'America_Argentina'),
        ('America_Aruba', 'America_Aruba'),
        ('America_AscensionIslands', 'America_AscensionIslands'),
        ('America_Bahamas', 'America_Bahamas'),
        ('America_Barbados', 'America_Barbados'),
        ('America_Bermuda', 'America_Bermuda'),
        ('America_Bolivia', 'America_Bolivia'),
        ('America_Brazil', 'America_Brazil'),
        ('America_Canada', 'America_Canada'),
        ('America_CaymanIslands', 'America_CaymanIslands'),
        ('America_Chile', 'America_Chile'),
        ('America_CocosIslands', 'America_CocosIslands'),
        ('America_Colombia', 'America_Colombia'),
        ('America_Congo', 'America_Congo'),
        ('America_CostaRica', 'America_CostaRica'),
        ('America_Cuba', 'America_Cuba'),
        ('America_Dominica', 'America_Dominica'),
        ('America_DominicanRepublic', 'America_DominicanRepublic'),
        ('America_Ecuador', 'America_Ecuador'),
        ('America_FrenchGuiana', 'America_FrenchGuiana'),
        ('America_Georgia', 'America_Georgia'),
        ('America_Grenada', 'America_Grenada'),
        ('America_Guadeloupe', 'America_Guadeloupe'),
        ('America_Guam', 'America_Guam'),
        ('America_Guatemala', 'America_Guatemala'),
        ('America_Guyana', 'America_Guyana'),
        ('America_Hayti', 'America_Hayti'),
        ('America_Honduras', 'America_Honduras'),
        ('America_Jamaica', 'America_Jamaica'),
        ('America_MalvieIslands', 'America_MalvieIslands'),
        ('America_MarianaIslands', 'America_MarianaIslands'),
        ('America_Martinique', 'America_Martinique'),
        ('America_Mexico', 'America_Mexico'),
        ('America_MontserratIsland', 'America_MontserratIsland'),
        ('America_Nicaragua', 'America_Nicaragua'),
        ('America_Panama', 'America_Panama'),
        ('America_Paraguay', 'America_Paraguay'),
        ('America_Peru', 'America_Peru'),
        ('America_PitcairnIsland', 'America_PitcairnIsland'),
        ('America_PuertoRico', 'America_PuertoRico'),
        ('America_SaintKittsAndNevis', 'America_SaintKittsAndNevis'),
        ('America_SaintLucia', 'America_SaintLucia'),
        ('America_SaintPierreAndMiquelon', 'America_SaintPierreAndMiquelon'),
        ('America_SaintVincent', 'America_SaintVincent'),
        ('America_Salvador', 'America_Salvador'),
        ('America_SouthGeorgiaAndTheSouthIsland', 'America_SouthGeorgiaAndTheSouthIsland'),
        ('America_Surinam', 'America_Surinam'),
        ('America_TrinidadAndTobago', 'America_TrinidadAndTobago'),
        ('America_TurksAndCaicosIslands', 'America_TurksAndCaicosIslands'),
        ('America_USMinorOutlyingIslands', 'America_USMinorOutlyingIslands'),
        ('America_Uruguay', 'America_Uruguay'),
        ('America_Venezuela', 'America_Venezuela'),
        ('America_VirginIslands', 'America_VirginIslands'),
        ('America_VirginIslands', 'America_VirginIslands'),
        ('America_Zaire', 'America_Zaire'))
    ),
    ('非洲区域', (
        ('Africa', 'Africa'),
        ('Africa_Algeria', 'Africa_Algeria'),
        ('Africa_Angola', 'Africa_Angola'),
        ('Africa_Benin', 'Africa_Benin'),
        ('Africa_Botswana', 'Africa_Botswana'),
        ('Africa_BouvetIsland', 'Africa_BouvetIsland'),
        ('Africa_BritishIndianOceanTerritory', 'Africa_BritishIndianOceanTerritory'),
        ('Africa_BurkinaFaso', 'Africa_BurkinaFaso'),
        ('Africa_Burundi', 'Africa_Burundi'),
        ('Africa_Cameroon', 'Africa_Cameroon'),
        ('Africa_CapeVerde', 'Africa_CapeVerde'),
        ('Africa_CaymanIslands', 'Africa_CaymanIslands'),
        ('Africa_CentralAfricanRepublic', 'Africa_CentralAfricanRepublic'),
        ('Africa_Comoros', 'Africa_Comoros'),
        ('Africa_Djibouti', 'Africa_Djibouti'),
        ('Africa_Egypt', 'Africa_Egypt'),
        ('Africa_EquatorialGuinea', 'Africa_EquatorialGuinea'),
        ('Africa_Eritrea', 'Africa_Eritrea'),
        ('Africa_Ethiopia', 'Africa_Ethiopia'),
        ('Africa_Gabon', 'Africa_Gabon'),
        ('Africa_Gambia', 'Africa_Gambia'),
        ('Africa_Ghana', 'Africa_Ghana'),
        ('Africa_Guinea', 'Africa_Guinea'),
        ('Africa_GuineaBissau', 'Africa_GuineaBissau'),
        ('Africa_Kenya', 'Africa_Kenya'),
        ('Africa_Kyrgyzstan', 'Africa_Kyrgyzstan'),
        ('Africa_Lesotho', 'Africa_Lesotho'),
        ('Africa_Liberia', 'Africa_Liberia'),
        ('Africa_Libya', 'Africa_Libya'),
        ('Africa_Madagascar', 'Africa_Madagascar'),
        ('Africa_Malawi', 'Africa_Malawi'),
        ('Africa_Mali', 'Africa_Mali'),
        ('Africa_Mauritania', 'Africa_Mauritania'),
        ('Africa_Mauritius', 'Africa_Mauritius'),
        ('Africa_Mayotte', 'Africa_Mayotte'),
        ('Africa_Morocco', 'Africa_Morocco'),
        ('Africa_Mozambique', 'Africa_Mozambique'),
        ('Africa_Namibia', 'Africa_Namibia'),
        ('Africa_Niger', 'Africa_Niger'),
        ('Africa_Nigeria', 'Africa_Nigeria'),
        ('Africa_Reunion', 'Africa_Reunion'),
        ('Africa_Rwanda', 'Africa_Rwanda'),
        ('Africa_SaintHelena', 'Africa_SaintHelena'),
        ('Africa_SaoTomePrincipe', 'Africa_SaoTomePrincipe'),
        ('Africa_Senegal', 'Africa_Senegal'),
        ('Africa_Seychelles', 'Africa_Seychelles'),
        ('Africa_SierraLeone', 'Africa_SierraLeone'),
        ('Africa_Somali', 'Africa_Somali'),
        ('Africa_SouthAfrica', 'Africa_SouthAfrica'),
        ('Africa_Sudan', 'Africa_Sudan'),
        ('Africa_Swaziland', 'Africa_Swaziland'),
        ('Africa_Tanzania', 'Africa_Tanzania'),
        ('Africa_Togo', 'Africa_Togo'),
        ('Africa_Tunisia', 'Africa_Tunisia'),
        ('Africa_Uganda', 'Africa_Uganda'),
        ('Africa_WesternSahara', 'Africa_WesternSahara'),
        ('Africa_Zambia', 'Africa_Zambia'),
        ('Africa_Zimbabwe', 'Africa_Zimbabwe'))
    ),
    ('大洋洲区', (
        ('Oceania', 'Oceania'),
        ('Oceania_Australia', 'Oceania_Australia'),
        ('Oceania_CookIs', 'Oceania_CookIs'),
        ('Oceania_Fiji', 'Oceania_Fiji'),
        ('Oceania_FrenchPolynesia', 'Oceania_FrenchPolynesia'),
        ('Oceania_FrenchSouthernTerritories', 'Oceania_FrenchSouthernTerritories'),
        ('Oceania_HeardIslandsMcDonaldIslands', 'Oceania_HeardIslandsMcDonaldIslands'),
        ('Oceania_IndependentStateOfSamoa', 'Oceania_IndependentStateOfSamoa'),
        ('Oceania_Kiribati', 'Oceania_Kiribati'),
        ('Oceania_MarshallIslands', 'Oceania_MarshallIslands'),
        ('Oceania_Nauru', 'Oceania_Nauru'),
        ('Oceania_NewCaledonia', 'Oceania_NewCaledonia'),
        ('Oceania_NewZealand', 'Oceania_NewZealand'),
        ('Oceania_Niue', 'Oceania_Niue'),
        ('Oceania_NorfolkIsland', 'Oceania_NorfolkIsland'),
        ('Oceania_PapuaNewCuinea', 'Oceania_PapuaNewCuinea'),
        ('Oceania_Tokelau', 'Oceania_Tokelau'),
        ('Oceania_Tonga', 'Oceania_Tonga'),
        ('Oceania_Vanuatu', 'Oceania_Vanuatu'),
        ('Oceania_WallisEtFutuna', 'Oceania_WallisEtFutuna'))
    )
]


class Control(object):
    def is_expired(self):
        time = timezone.now()
        if self.start_time is None and self.end_time is None:
            return u'否'
        elif self.end_time is None and self.start_time and time > self.start_time:
            return u'否'
        elif self.start_time is None and self.end_time and time < self.end_time:
            return u'否'
        elif self.start_time and time > self.start_time and self.end_time and time < self.end_time:
            return u'否'
        else:
            return u'是'

    is_expired.short_description = u'是否过期'


class AreaControl(models.Model, Control):
    area = models.CharField(u'设备区域', max_length=100, choices=AREA_CHOICE, unique=False)
    devid = models.CharField(u'固件序列号', max_length=100, unique=False)
    start_time = models.DateTimeField(u'开始时间', default=None, null=True, blank=True)
    end_time = models.DateTimeField(u'结束时间', default=None, null=True, blank=True)
    notes = models.TextField(u'附加信息', default='', blank=True)

    def __str__(self):
        return '<AreaControl {0}>'.format(self.area)


class UuidControl(models.Model, Control):
    uuid = models.CharField(u'设备序列号', max_length=100, unique=True)
    devid = models.CharField(u'固件序列号', max_length=100, unique=False)
    start_time = models.DateTimeField(u'开始时间', default=None, null=True, blank=True)
    end_time = models.DateTimeField(u'结束时间', default=None, null=True, blank=True)
    notes = models.TextField(u'附加信息', default='', blank=True)


class DateControl(models.Model, Control):
    devid = models.CharField(u'固件序列号', max_length=100, unique=False)
    start_time = models.DateTimeField(u'开始时间', default=None, null=True, blank=True)
    end_time = models.DateTimeField(u'结束时间', default=None, null=True, blank=True)
    start_date = models.DateField(u'开始日期', default=None, null=True, blank=True)
    end_date = models.DateField(u'结束日期', default=None, null=True, blank=True)
    notes = models.TextField(u'附加信息', default='', blank=True)


class UpgradeLog(models.Model):
    uuid = models.CharField(u'设备序列号', max_length=100, unique=False)
    devid = models.CharField(u'固件序列号', max_length=100, unique=False)
    area = models.CharField(u'设备区域', max_length=100, unique=False)
    upgrade_time = models.DateTimeField(u'升级时间', default=timezone.now, blank=True)


class Firmware(models.Model):
    name = models.FileField(u'上传文件', unique=True)
    date = models.DateTimeField(u'上传时间', default=timezone.now, blank=True)
    is_important = models.BooleanField(u'重要版本', default=False, blank=True)
    is_generated = models.BooleanField(u'是否生成', default=False, blank=True)

    notes = models.TextField(u'附加信息', blank=True)

    def __str__(self):
        return '<Firmware {0}>'.format(self.name)


