# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

from re import compile


class REGEXES:
    """
    Regexes Class

    Included Regexes:

        arab: Arabic Language
        chinese: Chinese Language
        japanese: Japanese Language (Includes Hiragana, Kanji and Katakana)
        sinhala: Sinhala Language
        tamil: Tamil Language
        cyrillic: Cyrillic Language
    """

    arab = compile('[\u0627-\u064a]')
    chinese = compile('[\u4e00-\u9fff]')
    japanese = compile('[(\u30A0-\u30FF|\u3040-\u309Fー|\u4E00-\u9FFF)]')
    sinhala = compile('[\u0D80-\u0DFF]')
    tamil = compile('[\u0B02-\u0DFF]')
    cyrillic = compile('[\u0400-\u04FF]')