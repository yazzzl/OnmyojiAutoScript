# This Python file uses the following encoding: utf-8
# @author runhey
# github https://github.com/runhey
from datetime import timedelta, datetime
from pydantic import BaseModel, Field
from sympy.categories.baseclasses import Class
from enum import Enum
from tasks.Component.GeneralBattle.config_general_battle import GeneralBattleConfig
from tasks.Component.SwitchSoul.switch_soul_config import SwitchSoulConfig

from tasks.Component.config_scheduler import Scheduler
from tasks.Component.config_base import ConfigBase




# L_NAME = RuleList(folder="./tasks/DemonSeal/res", direction="vertical", mode="ocr", roi_back=(391,182,198,389), size=(94, 64), array=["跳跳哥哥", "椒图", "骨女", "饿鬼", "二口女", "海坊主", "鬼使黑", "小松丸", "日和坊"])

class Demon(str, Enum):
    M_TTGG = "ttgg"
    M_JT = "jt"
    M_GN = "gn"
    M_EG = "eg"
    M_EKN = "ekn"
    M_HFZ = "hfz"
    M_XSW = "xsw"
    M_GSH = "gsh"
    M_RHF = "rhf"



class DemonSealConfig(BaseModel):
   demon_current: Demon = Field(default=Demon.M_GSH, description='target')
   last_run: datetime = Field(default=datetime.now(), description='last_run',deprecated = True)
   target :int = Field(default=10, description='target')
   today_count :int = Field(default=0, description='today_count')




class DemonSeal(ConfigBase):
    scheduler: Scheduler = Field(default_factory=Scheduler)
    demon_config: DemonSealConfig = Field(default_factory=DemonSealConfig)
    general_battle_config: GeneralBattleConfig = Field(default_factory=GeneralBattleConfig)
    switch_soul: SwitchSoulConfig = Field(default_factory=SwitchSoulConfig)