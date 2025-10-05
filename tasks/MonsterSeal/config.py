# This Python file uses the following encoding: utf-8
# @author runhey
# github https://github.com/runhey
from datetime import timedelta
from pydantic import BaseModel, Field
from sympy.categories.baseclasses import Class
from enum import Enum

from tasks.Component.config_scheduler import Scheduler
from tasks.Component.config_base import ConfigBase


# L_NAME = RuleList(folder="./tasks/MonsterSeal/res", direction="vertical", mode="ocr", roi_back=(391,182,198,389), size=(94, 64), array=["跳跳哥哥", "椒图", "骨女", "饿鬼", "二口女", "海坊主", "鬼使黑", "小松丸", "日和坊"])

class MonsterConfig(str, Enum):
    M_TTGG = "ttgg"
    M_JT = "jt"
    M_GN = "gn"
    M_EH = "eh"
    M_EK = "ek"
    M_HFZ = "hfz"
    M_XSM = "xsm"
    M_GSH = "gsh"
    M_RHF = "rhf"


class MonsterSealConfig(BaseModel):
   monster_current: MonsterConfig = Field(default=MonsterConfig.M_GSH, description='target')
   target :int = Field(default=10, description='目标次数')


class MonsterSeal(ConfigBase):
    scheduler: Scheduler = Field(default_factory=Scheduler)
    monster_config: MonsterSealConfig = Field(default_factory=MonsterSealConfig)
