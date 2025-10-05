# This Python file uses the following encoding: utf-8
# @author runhey
# github https://github.com/runhey
from datetime import timedelta
from pydantic import BaseModel, Field
from sympy.categories.baseclasses import Class
from enum import Enum
from tasks.Component.GeneralBattle.config_general_battle import GeneralBattleConfig
from tasks.Component.SwitchSoul.switch_soul_config import SwitchSoulConfig

from tasks.Component.config_scheduler import Scheduler
from tasks.Component.config_base import ConfigBase


class Monster(str, Enum):
    M_TTGG = "跳跳哥哥"
    M_JT = "椒图"
    M_GN = "骨女"
    M_EG = "饿鬼"
    M_EKN = "二口女"
    M_HFZ = "海坊主"
    M_XSW = "小松丸"
    M_GSH = "鬼使黑"
    M_RHF = "日和坊"


class MonsterSealConfig(BaseModel):
   monster_current: Monster = Field(default=Monster.M_GSH, description='target')
   target :int = Field(default=10, description='count')


class MonsterSeal(ConfigBase):
    scheduler: Scheduler = Field(default_factory=Scheduler)
    monster_config: MonsterSealConfig = Field(default_factory=MonsterSealConfig)
    general_battle_config: GeneralBattleConfig = Field(default_factory=GeneralBattleConfig)
    switch_soul: SwitchSoulConfig = Field(default_factory=SwitchSoulConfig)