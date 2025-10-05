# This Python file uses the following encoding: utf-8
# @author runhey
# github https://github.com/runhey
from time import sleep

import re
from datetime import timedelta, datetime, time
from cached_property import cached_property
from module.atom.click import RuleClick
from module.atom.long_click import RuleLongClick
from module.atom.ocr import RuleOcr

from tasks.GameUi.game_ui import GameUi
from tasks.GameUi.page import page_main, page_team
from tasks.Component.GeneralBattle.general_battle import GeneralBattle
from tasks.Component.GeneralBattle.config_general_battle import GeneralBattleConfig
from tasks.Component.GeneralRoom.general_room import GeneralRoom
from tasks.Component.GeneralInvite.general_invite import GeneralInvite
from tasks.MonsterSeal.assets import MonsterSealAssets
from tasks.Component.GeneralBuff.config_buff import BuffClass

from module.exception import TaskEnd
from module.logger import logger
from module.base.timer import Timer
from tasks.MonsterSeal.config import Monster
from typing import Union


class ScriptTask(GameUi, GeneralBattle, GeneralRoom, GeneralInvite, MonsterSealAssets):

    def run(self) -> None:

        con = self.config.monster_seal
        monster = con.monster_config
        logger.info(con)

        current = {}
        match monster.monster_current:
            case Monster.M_TTGG:
                current ={"i":self.I_TTGG, "o":self.O_TTGG,'n':'跳跳哥哥'}
            case Monster.M_JT:
                current ={"i":self.I_JT, "o":self.O_JT,'n':'椒图'}
            case Monster.M_GN:
                current ={"i":self.I_GN, "o":self.O_GN,'n':'骨女'}
            case Monster.M_EG:
                current ={"i":self.I_EG, "o":self.O_EG,'n':'饿鬼'}
            case Monster.M_EKN:
                current ={"i":self.I_EKN, "o":self.O_EKN,'n':'二口女'}
            case Monster.M_HFZ:
                current ={"i":self.I_HFZ, "o":self.O_HFZ,'n':'海坊主'}
            case Monster.M_XSW:
                current ={"i":self.I_XSW, "o":self.O_XSW,'n':'小松丸'}
            case Monster.M_GSH:
                current ={"i":self.I_GSH, "o":self.O_GSH,'n':'鬼使黑'}
            case Monster.M_RHF:
                current ={"i":self.I_RHF, "o":self.O_RHF,'n':'日和坊'}


        self.ui_get_current_page()
        # 进入组队页面
        self.ui_goto(page_team)
        # 进入组队后 有可能已经选了妖怪封印  要判断妖怪列表是否存在
        logger.info(current)
        while 1:
            self.screenshot()
            # 选过之后不需要二次再选
            if self.appear(current.get("i")):
                logger.info("检测到在鬼使黑里")
                break
            # 检测是否在妖气封印里面
            if self.appear(self.I_YQFY):
                logger.info(["检测到在妖气封印里面",])
                while 1:
                    self.screenshot()
                    if self.check_monster(current.get("n"),current):
                        break
                break
            # 什么都没进
            if self.check_zones("妖气封印") and self.check_monster(current.get("n"),current) :
                logger.info("选择妖气封印，并选择妖怪")
                break


        count = 0

        while 1:
            self.screenshot()
            if self.appear(self.I_WAIT) :
                break
            if self.appear_then_click(self.I_GR_AUTO_MATCH, interval=1.5):
                logger.info('点击自动匹配')
                count += 1
                continue
            if count > 4:
                logger.info('匹配超时')
                break

        # # 匹配个8分钟，要是八分钟还没人拿没啥了
        # logger.info('Waiting for match')
        click_timer = Timer(240)

        check_timer = Timer(480)
        click_timer.start()
        check_timer.start()
        self.device.stuck_record_add('BATTLE_STATUS_S')
        while 1:
            self.screenshot()
            # 如果被秒开进入战斗, 被秒开不支持开启buff

            if self.check_then_accept():
                continue

            # 如果没有自动匹配 且也页面在主页 则跳出 等下次执行
            if  not self.appear(self.I_WAIT) and self.ui_get_current_page() and self.ui_current == page_main:

                logger.info(self.ui_current)
                break

            if self.check_take_over_battle(False, config=self.battle_config):
                logger.info('开始战斗')
            # 如果进入房间
            elif self.is_in_room():
                self.device.stuck_record_clear()
                if self.wait_battle(wait_time=time(minute=1)):
                    self.run_general_battle(config=self.battle_config)
                    # 打完后返回庭院，记得关闭buff

                else:
                    break
            # 如果时间到了
            if click_timer and click_timer.reached():
                logger.warning('It has waited for 240s , but the battle has not started.')
                logger.warning('It will be waited for 240s and try again.')
                self.screenshot()
                self.ocr_appear_click(self.I_WAIT)
                click_timer = None
                self.device.stuck_record_clear()
                self.device.stuck_record_add('BATTLE_STATUS_S')
                continue

            if check_timer.reached():
                logger.warning('MonsterSeal match timeout')
                while 1:
                    self.screenshot()
                    if not self.appear(self.I_M_CHECK):
                        break
                    if self.appear_then_click(self.I_UI_CONFIRM, interval=1):
                        continue
                    if self.appear_then_click(self.I_UI_CONFIRM_SAMLL, interval=1):
                        continue
                    if self.appear_then_click(self.I_M_CHECK, interval=1):
                        continue
                logger.info('MonsterSeal match timeout, exit')
                break
            # 如果还在匹配中
            if self.appear(self.I_WAIT):
                continue

        # 退出结束
        self.set_next_run(task='MonsterSeal', success=True, finish=False)
        raise TaskEnd('MonsterSeal')



    @cached_property
    def battle_config(self) -> GeneralBattleConfig:
        conf = GeneralBattleConfig()
        return conf

    def check_monster(self, name: str,current: dict) -> bool:
        """
        确认妖气的名字，并选中
        :param name:
        :param current:
        :return:
        """
        last_group_text = ''
        while 1:
            self.screenshot()
            compare1 = self.O_CHECK_LIST.detect_and_ocr(self.device.image)
            now_group_text = str([result.ocr_text for result in compare1])
            if now_group_text == last_group_text:
                break
            self.swipe(self.S_UP, 1)
            sleep(2.5)
            last_group_text = now_group_text

        while 1:
            self.screenshot()
            # 获取的列表
            results = self.O_CHECK_LIST.detect_and_ocr(self.device.image)
            logger.info(results)
            text1 = [result.ocr_text for result in results]
            # 判断当前有无目标
            result = set(text1).intersection({name})
            # 有则跳出检测
            if result and len(result) > 0:
                break
            self.swipe(self.S_DOWN)
            sleep(1.5)

        logger.info(f'开始找名字 {name}')

        self.O_CHECK_LIST.keyword = name
        monster = ["跳跳哥哥", "椒图", "骨女", "饿鬼", "二口女", "海坊主", "鬼使黑", "小松丸", "日和坊",'俄鬼']
        while 1:
            self.screenshot()
            name = current.get('o').ocr(self.device.image)
            if  name in monster:
                current.get('o').keyword = name
            pos =  self.ocr_appear_click(current.get('o'))
            if pos:
                break
            logger.info(f' 结果 {pos}')


        return True


if __name__ == '__main__':
    from module.config.config import Config
    from module.device.device import Device
    c = Config('oas1')
    d = Device(c)
    t = ScriptTask(c, d)
    t.screenshot()

    t.run()


