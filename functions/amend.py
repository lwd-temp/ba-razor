import json
import yaml
from itertools import groupby
from operator import itemgetter
from pathlib import Path
from typing import List
from colorama import Fore

from utils import save_yaml

from model import FavorScenario, MomotalkOutput, MomotalkContent


def amend_momotalk(source_path: str | Path, amend_path: str | Path, output_path: str | Path):
    source_path = Path(source_path) if isinstance(source_path, str) else source_path
    amend_path = Path(amend_path) if isinstance(amend_path, str) else amend_path
    output_path = Path(output_path) if isinstance(output_path, str) else amend_path

    source_path.mkdir(parents=True, exist_ok=True)
    amend_path.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)

    for each_source_file in source_path.glob("*.yml"):
        # get source file path
        each_amend_file = amend_path / each_source_file.name
        # get amend file path
        if not each_amend_file.exists() or each_amend_file.is_dir():
            continue
        # get output file path
        output_file = output_path / each_source_file.name

        print(f"{Fore.GREEN}Amending [{each_amend_file}] -> [{each_amend_file}] dump to [{output_file}]{Fore.RESET}")

        with open(each_source_file, "r", encoding="utf8") as f:
            source_data = MomotalkOutput(**yaml.load(f, Loader=yaml.CLoader))
        with open(each_amend_file, "r", encoding="utf8") as f:
            amend_data = MomotalkOutput(**yaml.load(f, Loader=yaml.CLoader))

        assert source_data.CharacterId == amend_data.CharacterId

        def __amend_title(a: FavorScenario, b: FavorScenario):
            a.TextJp = b.TextJp if b.TextJp else ""
            a.TextCn = b.TextCn if b.TextCn else ""
            a.TextKr = b.TextKr if b.TextKr else ""
            a.TextEn = b.TextEn if b.TextEn else ""
            a.TextTh = b.TextTh if b.TextTh else ""
            a.TextTw = b.TextTw if b.TextTw else ""

        def __amend_content(a: MomotalkContent, b: MomotalkContent):
            a.MessageKR = b.MessageKR if b.MessageKR else ""
            a.MessageJP = b.MessageJP if b.MessageJP else ""
            a.MessageCN = b.MessageCN if b.MessageCN else ""
            a.MessageEN = b.MessageEN if b.MessageEN else ""
            a.MessageTH = b.MessageTH if b.MessageTH else ""
            a.MessageTW = b.MessageTW if b.MessageTW else ""

        # amend title
        for each_source_momotalk_content in source_data.title:
            for each_amend_momotalk_content in amend_data.title:
                if each_source_momotalk_content.GroupId == each_amend_momotalk_content.GroupId:
                    __amend_title(each_source_momotalk_content, each_amend_momotalk_content)
                    break

        # amend content
        for each_source_momotalk_content in source_data.content:
            for each_amend_momotalk_content in amend_data.content:
                if each_source_momotalk_content.Id == each_amend_momotalk_content.Id:
                    __amend_content(each_source_momotalk_content, each_amend_momotalk_content)
                    break

        save_yaml(source_data, output_file)
