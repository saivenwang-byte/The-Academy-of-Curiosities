#!/usr/bin/env python3
"""Bootstrap Unit1 V3.6 shot maps, illustration binding, and artist prompts."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "单元1_第一单元_五案"
BODY_V36 = UNIT / "正文" / "V3.6"
ILL_V2 = UNIT / "插图" / "绑定正文_V2.0"
ILL_V36 = UNIT / "插图" / "绑定正文_V3.6"
SHOT_ROOT = BODY_V36 / "04_分镜插画"
MIG = ROOT / "V2迁移"

GLOBAL_STYLE = """Modern Japanese bridge-book illustration ages 10-12,
clear light-manga ink line warm brown outline #2A1810 NOT pure black,
soft painterly coloring restrained watercolor paper texture NOT flat vector,
6-7 head pre-teen proportions NOT chibi NOT shonen hero,
warm golden April morning cinematic side light Nagoya public elementary school,
gentle fair-play mystery observation club NOT detective agency,
uwabaki indoor shoes on floor, IP 学堂奇事録 Campus Ripple V2"""

GLOBAL_NEGATIVE = """chibi SD, horror mob trial, supernatural glow, Chinese classroom layout,
detective magnifying glass pose, 3D render, fluorescent neon,
English or Chinese text rendered in image, watermark,
school uniform blazer sailor suit, sneakers on classroom floor,
generic anime child, villain spotlight"""

# source filename suffix in V2 folder -> canonical bound name
IMAGE_MAP: dict[str, list[tuple[str, str]]] = {
    "A001": [
        ("DA1", "V-S01-V2-A1_广播响起_G1draft_c06.png"),
        ("DA2", "V-S01-A2_误导搜查_G1draft.png"),
        ("DA3", "V-S01-V2-A3_文件时间_G1draft_PH.png"),
        ("DA4", "V-S01-V2-A4_波形硬切_G1draft_PH.png"),
        ("DA5", "V-S01-A2_误导搜查_G1draft_c01.png"),
        ("TAIL", "V-S01-TAIL_壁报空栏_G1draft.png"),
        ("DB1", "V-S01-B1_风侧机制图_G1draft.png"),
    ],
    "A002": [
        ("DA1", "V-S02-V2-A1_黑板对不起_G1draft_c06.png"),
        ("DA2", "SAMPLE_A002_DA1_修正_V0.3.png"),
        ("DA3", "V-S02-V2-A3_膜边反光_G1draft_PH.png"),
        ("DA4", "V-S02-V2-A4_对照实验_G1draft_PH.png"),
        ("DA5", "V-S02-V2-A1_黑板对不起_G1draft_c08.png"),
        ("TAIL", "V-S02-TAIL_无署名窄条.png"),
        ("DB1", "V-S02-V2-A4_对照实验_G1draft_c02.png"),
    ],
    "A003": [
        ("DA1", "V-S03-V2-DEMO_空海报位_G1draft_c08.png"),
        ("DA2", "V-S03-V2-A2_正式照无海报_G1draft_PH.png"),
        ("DA3", "V-S03-V2-DEMO_空海报位_G1draft_c06.png"),
        ("DA4", "V-S03-V2-A4_远标题连线_G1draft_PH.png"),
        ("DA5", "V-S03-V2-DEMO_空海报位_G1draft_c04.png"),
        ("TAIL", "V-S03-TAIL_投稿背面路线.png"),
        ("DB1", "V-S03-V2-A4_远标题连线_G1draft_c05.png"),
    ],
    "A004": [
        ("DA1", "V-S04-V2-A1_抽屉失物_G1draft_c08.png"),
        ("DA2", "V-S04-V2-A1_抽屉失物_G1draft_c04.png"),
        ("DA3", "V-S04-V2-A3_倾斜水泡_G1draft_PH.png"),
        ("DA4", "V-S04-V2-A4_振动复现_G1draft_PH.png"),
        ("DA5", "V-S04-V2-A1_抽屉失物_G1draft_c06.png"),
        ("TAIL", "V-S04-TAIL_中谷远景.png"),
        ("DB1", "V-S04-V2-A4_振动复现_G1draft_c02.png"),
    ],
    "A005": [
        ("DA1", "V-S05-V2-A1_仅水野无影_G1draft_c08.png"),
        ("DA2", "V-S05-V2-A1_仅水野无影_G1draft_c06.png"),
        ("DA3", "V-S05-V2-A3_metadata三帧_G1draft_PH.png"),
        ("DA4", "V-S05-V2-A1_仅水野无影_G1draft_c04.png"),
        ("DA5", "V-S05-V2-A1_仅水野无影_G1draft_c07.png"),
        ("DA6", "V-S05-V2-A6_重拍有影_G1draft_PH.png"),
        ("TAIL", "V-S05-TAIL_瑆日记扶正书.png"),
        ("DB1", "V-S05-V2-A3_metadata三帧_G1draft_c02.png"),
    ],
}

CASE_META = {
    "A001": {
        "num": "01",
        "title_cn": "全班都听见了他的声音",
        "title_jp": "クラス全員が、彼の声を聞いた",
        "jp_file": "案01_全班都听见了他的声音_HybridVoice_V3.6_日本語.txt",
        "v2_map": "03_案01_分镜头与插页地图_V2.0.md",
        "p0_extra": [],
    },
    "A002": {
        "num": "02",
        "title_cn": "没有人写过的道歉",
        "title_jp": "誰も書いていない「ごめんなさい」",
        "jp_file": "案02_没有人写过的道歉_HybridVoice_V3.6_日本語.txt",
        "v2_map": "03_案02_分镜头与插页地图_V2.0.md",
        "p0_extra": [],
    },
    "A003": {
        "num": "03",
        "title_cn": "每个人都记得的海报",
        "title_jp": "みんなが覚えているポスター",
        "jp_file": "案03_每个人都记得的海报_HybridVoice_V3.6_日本語.txt",
        "v2_map": "03_案03_分镜头与插页地图_V2.0.md",
        "p0_extra": [],
    },
    "A004": {
        "num": "04",
        "title_cn": "只出现在她抽屉里的失物",
        "title_jp": "彼女の引き出しにだけあった失物",
        "jp_file": "案04_只出现在她抽屉里的失物_HybridVoice_V3.6_日本語.txt",
        "v2_map": "03_案04_分镜头与插页地图_V2.0.md",
        "p0_extra": [],
    },
    "A005": {
        "num": "05",
        "title_cn": "午休后消失的影子",
        "title_jp": "昼休みのあと、消えた影",
        "jp_file": "案05_午休后消失的影子_HybridVoice_V3.6_日本語.txt",
        "v2_map": "03_案05_分镜头与插页地图_V2.0.md",
        "p0_extra": ["DA6"],
    },
}

# P0 shot §11 + JP anchor (from V3.6 日本語)
P0_SHOTS: dict[str, list[dict]] = {
    "A001": [
        {
            "id": "DA1",
            "sc": "SC-02",
            "func": "S+L",
            "shot": "MS",
            "camera": "合班教室·东向平视·三分构图",
            "center": "天井放送スピーカーが鳴っている",
            "second": "教壇の光·唇がまだ動いていない·PLAY屏",
            "anchor": "合同教室で、光は教壇に立ち、口はまだ開いている……息しか出ない。それなのに天井の放送スピーカーは明るく、はっきりしていた。",
            "props": "上履き·四月光·器材車·発声禁止届",
        },
        {
            "id": "DA2",
            "sc": "SC-03",
            "func": "C+E",
            "shot": "MS",
            "camera": "同轴·略低",
            "center": "慧美が「人を裁く言葉は書かない」",
            "second": "志郎が配線ログ·光は青白い",
            "anchor": "「観察クラブは、へんなところを書く。人を裁く言葉は書かない。」",
            "props": "銀枠メガネ·四欄本·展示膜样品袋",
        },
        {
            "id": "DA3",
            "sc": "SC-05",
            "func": "L+C",
            "shot": "MCU",
            "camera": "珣POV·框中框（屏）",
            "center": "0328·三周前のリハーサル録音",
            "second": "慧美「聞いた話」欄·未確認",
            "anchor": "見ていたのは教壇横の放送卓の画面……小さな文字が点滅している。再生・三周前のリハーサル録音",
            "props": "タブレット·鉛筆·四欄本",
        },
        {
            "id": "DA4",
            "sc": "SC-06",
            "func": "L+P",
            "shot": "CU",
            "camera": "平板CU·志郎/慧美双视",
            "center": "波形の硬切・断点",
            "second": "議論の剪影·社交の時計",
            "anchor": "波形が途中で切れている。誰かが、再生を途中で止めた痕跡。",
            "props": "丸枠メガネ·方格本·平板",
        },
        {
            "id": "DA5",
            "sc": "SC-07",
            "func": "C+E",
            "shot": "MS",
            "camera": "略俯·教室全景圧縮",
            "center": "全班「聞こえた」手势",
            "second": "光脸白·慧美横拦·水野后排",
            "anchor": "誰かが小声で言った。「でも、あなたの声だよ。」",
            "props": "教坛+喇叭+屏其二",
        },
        {
            "id": "TAIL",
            "sc": "SC-08–09",
            "func": "H+P",
            "shot": "¼–半",
            "camera": "分格·侧门清单",
            "center": "器材車下一站·黒板",
            "second": "FC-4完整句 vs 半句",
            "anchor": "次は黒板。展示膜のテストが、まだ終わっていない。",
            "props": "清单·膜卷·A002种子",
        },
        {
            "id": "DB1",
            "sc": "—",
            "func": "P",
            "shot": "信息图",
            "camera": "SUM三格横排",
            "center": "误播/跳播/截断",
            "second": "日文简图·无答案句",
            "anchor": "放送の声は、光が今日一言も話せない。口の動きと、合わない。",
            "props": "B轨机制SUM",
        },
    ],
    "A002": [
        {
            "id": "DA1",
            "sc": "SC-02",
            "func": "S+L",
            "shot": "MS–CU",
            "camera": "教室·黒板平视·三分",
            "center": "黒板「ごめんなさい。」",
            "second": "志郎扫除服·非写字pose",
            "anchor": "黒板に、チョークの字がはっきり：　ごめんなさい。",
            "props": "緑板·粉笔白·上履き",
        },
        {
            "id": "DA2",
            "sc": "SC-03",
            "func": "L+C",
            "shot": "MS",
            "camera": "折叠桌·略俯",
            "center": "慧美四欄格",
            "second": "FC-2握笔角速写",
            "anchor": "確認済みに書く：字が現れた・朝自習前・黒板中央。",
            "props": "銀枠メガネ·方格本",
        },
        {
            "id": "DA3",
            "sc": "SC-05",
            "func": "L+C",
            "shot": "MCU",
            "camera": "板槽POV·斜光",
            "center": "FC-1膜边反光细线",
            "second": "清洁液瓶·FC-3时序",
            "anchor": "雑巾が溝を擦ったが、透明な細い端は剥がれていない。水が入った。",
            "props": "透明膜边·窗缝光",
        },
        {
            "id": "DA4",
            "sc": "SC-07",
            "func": "L+P",
            "shot": "MS",
            "camera": "备课本对照·双格",
            "center": "湿擦→清洁液→旧痕再显",
            "second": "FC-4样品袋标签",
            "anchor": "朝自習のベルが鳴る十分前、字がまた戻った。まだあの三文字。",
            "props": "裁纸刀·清洁液·登记本",
        },
        {
            "id": "DA5",
            "sc": "SC-06",
            "func": "C+E",
            "shot": "MS",
            "camera": "略俯·板前压缩",
            "center": "志郎被推至板前",
            "second": "全班审判词满",
            "anchor": "「志郎が書いたでしょ？」誰かが続ける。「昨日、黒板で膜いじってた！」",
            "props": "黒板+膜边其二",
        },
        {
            "id": "TAIL",
            "sc": "SC-08–09",
            "func": "H+P",
            "shot": "¼–半",
            "camera": "分格·登记+壁报",
            "center": "repair登记句",
            "second": "壁报口述分叉→A003",
            "anchor": "「貼り終わっていない。」慧美が言う。",
            "props": "登録表·空欄壁报",
        },
        {
            "id": "DB1",
            "sc": "—",
            "func": "P",
            "shot": "信息图",
            "camera": "SUM三格",
            "center": "膜残留/清洁再现/未登记",
            "second": "日文简图",
            "anchor": "字は消される。板面はまた緑一色。——それから、字がまた戻った。",
            "props": "B轨",
        },
    ],
    "A003": [
        {
            "id": "DA1",
            "sc": "SC-01",
            "func": "S+L",
            "shot": "MS",
            "camera": "壁报平视·四栏",
            "center": "空海报位·三人口述分叉",
            "second": "FC-1版式口述",
            "anchor": "側廊の壁報欄に、磁石四つ。長方形の空白。ポスターはない。",
            "props": "四栏·钉印·上履き",
        },
        {
            "id": "DA2",
            "sc": "SC-03",
            "func": "L+C",
            "shot": "MS",
            "camera": "折叠桌·略俯",
            "center": "慧美四欄格",
            "second": "FC-2正式照无海报",
            "anchor": "「正式写真にはない。」志郎が言う。「ぼけたんじゃない。ない。」",
            "props": "銀枠メガネ·活动照平板",
        },
        {
            "id": "DA3",
            "sc": "SC-06",
            "func": "L+C",
            "shot": "MCU",
            "camera": "夹页POV·框中框",
            "center": "FC-3尺寸不符草稿",
            "second": "三版本并排",
            "anchor": "三枚の紙を並べる：A 赤地半欄・B 左上太字タイトル・C 中央黒字……枠線すら重ならない。",
            "props": "草稿夹·红铅笔",
        },
        {
            "id": "DA4",
            "sc": "SC-04",
            "func": "L+P",
            "shot": "MS",
            "camera": "侧廊远摄·占位连线",
            "center": "FC-4远标题可读",
            "second": "钉印·占位视觉",
            "anchor": "学校案内板に「私たちの目の学校」と書いてあり、口述のタイトルとは二文字だけ違う。",
            "props": "壁报远距·走廊光",
        },
        {
            "id": "DA5",
            "sc": "SC-07",
            "func": "C+E",
            "shot": "MS",
            "camera": "略俯·壁报前压缩",
            "center": "慧美资格悬停",
            "second": "wrong峰值·珣拦",
            "anchor": "「観察クラブが原稿を消したでしょ？」誰かが半歩だけどく……",
            "props": "四栏其三满",
        },
        {
            "id": "TAIL",
            "sc": "SC-08–09",
            "func": "H+P",
            "shot": "¼–半",
            "camera": "分格·三标识+失物柜",
            "center": "repair三标识",
            "second": "抽屉嗒声→A004",
            "anchor": "失物柜の最下段、半開きの引き出しから、小さな音がした。",
            "props": "三标识格·失物柜远景",
        },
        {
            "id": "DB1",
            "sc": "—",
            "func": "P",
            "shot": "信息图",
            "camera": "SUM三格",
            "center": "口述≠同一张/无实体/碎片拼",
            "second": "日文简图",
            "anchor": "慧美が止まる。ポスターを覚えていることは否定しない。別のことを否定する：「……貼り終わっていない。」",
            "props": "B轨",
        },
    ],
    "A004": [
        {
            "id": "DA1",
            "sc": "SC-02",
            "func": "S+L",
            "shot": "MS–CU",
            "camera": "失物柜·平视略俯",
            "center": "半开抽屉·失物堆",
            "second": "水野无钥匙站侧",
            "anchor": "失物柜の引き出しが、鍵もなく、半開きになっている。",
            "props": "封条·清单·上履き",
        },
        {
            "id": "DA2",
            "sc": "SC-03",
            "func": "L+C",
            "shot": "MS",
            "camera": "折叠桌·教室边",
            "center": "慧美四欄格",
            "second": "FC-1无撬锁特写",
            "anchor": "確認済み：引き出し半開・鍵なし・施錠記録と矛盾なし。",
            "props": "銀枠メガネ·锁舌完好",
        },
        {
            "id": "DA3",
            "sc": "SC-05",
            "func": "L+C",
            "shot": "MCU",
            "camera": "柜顶POV·水平仪",
            "center": "FC-2倾斜水泡",
            "second": "FC-3时刻表重合",
            "anchor": "水平器の泡が、わずかに片側へ寄っている。",
            "props": "水平仪·振动日志",
        },
        {
            "id": "DA4",
            "sc": "SC-05",
            "func": "L+P",
            "shot": "MS",
            "camera": "走廊·器材车过",
            "center": "车过柜震复现",
            "second": "最下抽屉先有物",
            "anchor": "機材ワゴンが通過した瞬間、失物柜が小さく震えた。",
            "props": "器材车·减速垫种子",
        },
        {
            "id": "DA5",
            "sc": "SC-06",
            "func": "C+E",
            "shot": "MS",
            "camera": "略俯·走廊压缩",
            "center": "偷窃词满·水野缩肩",
            "second": "珣本子·非villain",
            "anchor": "「水野が盗んだんでしょ？」廊下に、そういう声が広がった。",
            "props": "失物清单·封条",
        },
        {
            "id": "TAIL",
            "sc": "SC-08–09",
            "func": "H+P",
            "shot": "¼–半",
            "camera": "分格·还卡+合照",
            "center": "repair还卡",
            "second": "合照五人·无影种子",
            "anchor": "カードは返した。再生はしない。——明日、集合写真のリハーサルがある。",
            "props": "录音卡·预拍屏",
        },
        {
            "id": "DB1",
            "sc": "—",
            "func": "P",
            "shot": "信息图",
            "camera": "SUM三格",
            "center": "倾斜/振动/滑入",
            "second": "日文简图",
            "anchor": "引き出しにあったのは、盗んだ証拠じゃない。振動で滑り込んだ失物だった。",
            "props": "B轨",
        },
    ],
    "A005": [
        {
            "id": "DA1",
            "sc": "SC-01",
            "func": "S+L",
            "shot": "MS",
            "camera": "投屏·体育馆平视",
            "center": "五人合照·仅水野脚边空",
            "second": "车/灯杆有影",
            "anchor": "水野だけ、足元に影がない。機材ワゴンの影はある。灯柱の影もある。",
            "props": "预展屏·上履き·器材车",
        },
        {
            "id": "DA2",
            "sc": "SC-03",
            "func": "C+E",
            "shot": "MS",
            "camera": "同轴·略低",
            "center": "慧美拦审判",
            "second": "FC-1全景icon",
            "anchor": "「先に、どう撮ったかを見る。」慧美が言う。",
            "props": "20分倒计时·四栏本",
        },
        {
            "id": "DA3",
            "sc": "SC-05",
            "func": "L+C",
            "shot": "MCU",
            "camera": "平板POV·框中框",
            "center": "FC-2分段曝光三帧",
            "second": "水野侧让帧高亮",
            "anchor": "十四秒分の写真が、一枚に stitched されている。",
            "props": "平板·时间戳",
        },
        {
            "id": "DA4",
            "sc": "SC-04",
            "func": "L",
            "shot": "MS",
            "camera": "静电实验角",
            "center": "静电对照失败",
            "second": "换查拍摄",
            "anchor": "静電は、影の欠けを説明できない。",
            "props": "气球·地面光",
        },
        {
            "id": "DA5",
            "sc": "SC-06",
            "func": "C+E",
            "shot": "MS",
            "camera": "略俯·人群压缩",
            "center": "五案串成破坏链",
            "second": "wrong峰值",
            "anchor": "五つの事件が、観察クラブの仕業みたいに繋がった。",
            "props": "五案链白板",
        },
        {
            "id": "DA6",
            "sc": "SC-08",
            "func": "L+P",
            "shot": "MS",
            "camera": "重拍区·单次快门",
            "center": "FC-4五影全在",
            "second": "水野影回来",
            "anchor": "シャッター一回。五つの影が、全部地面に戻った。",
            "props": "相机·五人队列",
        },
        {
            "id": "TAIL",
            "sc": "SC-09–10",
            "func": "H+P",
            "shot": "跨页",
            "camera": "壁报四栏+入社",
            "center": "五栏章程·珣签名",
            "second": "水野名写回·单元收",
            "anchor": "陸珣は、観察クラブの申請書に名前を書いた。",
            "props": "四栏·申请表",
        },
        {
            "id": "DB1",
            "sc": "—",
            "func": "P",
            "shot": "信息图",
            "camera": "SUM三格",
            "center": "全景/拼接/单人错位",
            "second": "日文简图",
            "anchor": "影が消えたのは、呪いじゃない。撮り方の問題だった。",
            "props": "B轨",
        },
    ],
}


def update_v36_body_meta() -> None:
    note = BODY_V36 / "00_版本说明.md"
    note.write_text(
        """# 第一单元正文 · V3.6 · **CURRENT（JP 轨 · 试读里程碑）**

> 2026-06-09

## 版本摘要

- **CN**：同 V3.1（`01_中文/`）
- **JP**：V3.5 基线 + V3.6 版本号锁定（illustration + 试读 PDF 里程碑）
- **分镜插画**：`04_分镜插画/A00X/`
- **插图绑定**：[`插图/绑定正文_V3.6/`](../插图/绑定正文_V3.6/)
- **试读 PDF**：[`薄样张_试读/Unit1_V3.6_五案试读/PDF/`](../../薄样张_试读/Unit1_V3.6_五案试读/PDF/)

## 流水线位置

V3.5 KIDS-SIMPLIFY → **V3.6 SHOT+ILLUST+TRIAL-PDF** → PRODUCT-GATE 精修
""",
        encoding="utf-8",
    )
    for sub in ("01_中文", "02_日本語"):
        d = BODY_V36 / sub
        if not d.exists():
            continue
        for f in d.glob("*.txt"):
            text = f.read_text(encoding="utf-8")
            text = text.replace("V3.5", "V3.6")
            f.write_text(text, encoding="utf-8")


def resolve_src(case: str, fname: str) -> Path | None:
    src_dir = ILL_V2 / case
    p = src_dir / fname
    if p.exists():
        return p
    stem = Path(fname).stem
    for alt in src_dir.glob(f"{stem}*"):
        if alt.suffix.lower() == ".png":
            return alt
    # fuzzy: match prefix before _G1draft
    prefix = stem.split("_G1draft")[0]
    cands = sorted(src_dir.glob(f"{prefix}*.png"), key=lambda x: ("PH" not in x.name, x.name))
    return cands[0] if cands else None


def copy_illustrations() -> dict[str, int]:
    counts: dict[str, int] = {}
    for case, entries in IMAGE_MAP.items():
        out_dir = ILL_V36 / case
        out_dir.mkdir(parents=True, exist_ok=True)
        lines: list[str] = [
            f"# {case} · 插图清单 · V3.6\n",
            f"> 绑定正文 V3.6 · G1DRAFT 试读用 · PRODUCT-GATE 前不得标 PRODUCT\n\n",
            "| Shot | 文件 | 来源 | 状态 |\n",
            "|------|------|------|:----:|\n",
        ]
        n = 0
        for shot_id, fname in entries:
            src = resolve_src(case, fname)
            if src is None:
                lines.append(f"| {shot_id} | `{fname}` | ⬜ MISSING | — |\n")
                continue
            dest_name = f"{case}_{shot_id}_{src.name}"
            dest = out_dir / dest_name
            shutil.copy2(src, dest)
            status = "G1DRAFT" if "G1draft" in src.name or "SAMPLE" in src.name else "G1DRAFT"
            if "_v1.0" in src.name:
                status = "PRODUCT"
            lines.append(f"| {shot_id} | `{dest_name}` | `{src.name}` | {status} |\n")
            n += 1
        (out_dir / "00_插图清单_V3.6.md").write_text("".join(lines), encoding="utf-8")
        counts[case] = n
    return counts


def write_prompt(shot: dict, case: str, meta: dict) -> str:
    sid = shot["id"]
    return f"""# {case} · {sid} · Prompt · V3.6

> **Status**: G1DRAFT_PRODUCTION · 试读 PDF 用  
> **Shot Map**: [`03_分镜头_插页地图_V3.6_JP.md`](../03_分镜头_插页地图_V3.6_JP.md)  
> **正文锚**: [`../../02_日本語/{meta['jp_file']}`](../../02_日本語/{meta['jp_file']})

## §11 分镜规划书

| 字段 | 值 |
|------|-----|
| 镜头编号 | **{sid}** |
| 所属 | Vol1 · {case} · {shot['sc']} |
| 原文范围 | V3.6 JP · 见 Shot Map JP 锚点句 |
| 镜头功能 | **{shot['func']}** |
| 强制级 | **P0** |
| 景别 | **{shot['shot']}** |
| 机位 | {shot['camera']} |
| 视觉中心 | {shot['center']} |
| 第二信息 | {shot['second']} |
| 服道化 | {shot['props']} |
| JP 锚点句 | {shot['anchor']} |

## Global STYLE

```
{GLOBAL_STYLE}
```

## Global NEGATIVE

```
{GLOBAL_NEGATIVE}
```

## 合成 Prompt

```
[STYLE] {shot['shot']} {shot['camera']},
VISUAL CENTER: {shot['center']},
SECOND READ: {shot['second']},
characters and props per 14_v2 L0 and Vol1画风Sheet,
fair-play clue readable without text arrows, Nagoya elementary April uwabaki,
scene context: {shot['anchor'][:80]}...
[NEGATIVE]
```
"""


def write_shot_map(case: str) -> Path:
    meta = CASE_META[case]
    shots = P0_SHOTS[case]
    jp_rel = f"../../02_日本語/{meta['jp_file']}"
    v2_ref = f"../../../../样章包/{meta['v2_map']}"
    out_dir = SHOT_ROOT / case
    out_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir = out_dir / "prompts"
    prompts_dir.mkdir(exist_ok=True)

    rows = []
    for s in shots:
        rows.append(
            f"| **{s['id']}** | {s['sc']} | {s['func']} | **P0** | {s['shot']} | {s['camera']} | "
            f"{s['center']} | {s['second']} | `{case}_{s['id']}_*` | "
            f"[`prompts/{s['id']}.md`](./prompts/{s['id']}.md) | "
            f"「{s['anchor']}」 | {s['props']} |"
        )
        (prompts_dir / f"{s['id']}.md").write_text(write_prompt(s, case, meta), encoding="utf-8")

    content = f"""# 案{meta['num']} · {meta['title_cn']} · 分镜头与插页地图 · V3.6 · JP 锚定

> **Status**: **SHOT_MAP_V3.6_JP** · 2026-06-09 · 试读 PDF 批次  
> **V2 基线**: [`{meta['v2_map']}`]({v2_ref})  
> **正文锚（JP 定稿）**: [`{meta['jp_file']}`]({jp_rel})  
> **CN 参照**: [`../../01_中文/案{meta['num']}_{meta['title_cn']}_HybridVoice_V3.6.txt`](../../01_中文/案{meta['num']}_{meta['title_cn']}_HybridVoice_V3.6.txt)  
> **插图绑定**: [`../../../插图/绑定正文_V3.6/{case}/`](../../../插图/绑定正文_V3.6/{case}/)  
> **流程**: [`88_单元1_V3.6_分镜插画试读PDF工作流_V0.1.md`](../../../../V2迁移/88_单元1_V3.6_分镜插画试读PDF工作流_V0.1.md)

---

## 元数据

| 项 | 值 |
|----|-----|
| 案 ID | **{case}** |
| 标题（中） | {meta['title_cn']} |
| 标题（日） | {meta['title_jp']} |
| 正文版本 | **V3.6 JP** |
| P0 深度锚点 | **{len(shots)}** 帧 |

---

## Shot Map · P0 全表（§11 + JP 原文锚点句）

| Shot | SC | 功能 | P | 景别 | 机位/构图 | 视觉中心 | 第二信息 | PNG ID | Prompt | **JP 原文锚点句** | 服道化 |
|------|-----|------|---|------|-----------|----------|----------|--------|--------|-------------------|--------|
{chr(10).join(rows)}

---

## 门禁

| 项 | 状态 |
|----|:----:|
| V3.6 JP 正文 | ✅ |
| Shot Map JP 锚定 | ✅ 本文件 |
| 画师开工单 | ✅ [`00_画师开工单_V3.6.md`](./00_画师开工单_V3.6.md) |
| Prompt §11 | ✅ `prompts/` |
| G1DRAFT PNG | 🟡 绑定正文_V3.6 |
| E06-S / PRODUCT | ⬜ 试读后 |

| 版本 | 2026-06-09 · V3.6 · JP-anchored trial batch |
"""
    path = out_dir / "03_分镜头_插页地图_V3.6_JP.md"
    path.write_text(content, encoding="utf-8")
    return path


def write_work_order(case: str) -> None:
    meta = CASE_META[case]
    shots = P0_SHOTS[case]
    out_dir = SHOT_ROOT / case
    out_dir.mkdir(parents=True, exist_ok=True)
    checklist = "\n".join(
        f"- [ ] **{s['id']}** — {s['center']} · prompt: `prompts/{s['id']}.md`"
        for s in shots
    )
    ill_lines = "\n".join(
        f"- [ ] {sid} → `{fname}`"
        for sid, fname in IMAGE_MAP.get(case, [])
    )
    text = f"""# {case} · 画师开工单 · V3.6

> **交付目标**: 试读 PDF（G1DRAFT 可）· PRODUCT-GATE 前精修  
> **Shot Map**: [`03_分镜头_插页地图_V3.6_JP.md`](./03_分镜头_插页地图_V3.6_JP.md)  
> **正文**: V3.6 JP · {meta['title_jp']}

## P0 交付清单

{checklist}

## 插图绑定（V3.6 · 当前 G1 优选）

{ill_lines}

## 验收

1. §11 字段与 Shot Map 一致  
2. 上履き · 四月光 · L0 外装  
3. FC 公平可见 · 无答案箭头  
4. 文件名写入 `../../../插图/绑定正文_V3.6/{case}/00_插图清单_V3.6.md`

## 诚实边界

试读 PDF 使用 **G1DRAFT** 探索稿；E06-S + visual-auditor PASS 后才可标 **PRODUCT**。
"""
    (out_dir / "00_画师开工单_V3.6.md").write_text(text, encoding="utf-8")


def write_master_workflow() -> Path:
    path = MIG / "88_单元1_V3.6_分镜插画试读PDF工作流_V0.1.md"
    path.write_text(
        """# 单元1 · V3.6 · 分镜插画试读 PDF 工作流 · V0.1

> 2026-06-09 · A001–A005 五案试读批次

## Phase 链

```
JP V3.6 定稿（02_日本語/）
  → Shot Map JP 锚定（正文/V3.6/04_分镜插画/A00X/）
  → 画师开工单 + prompts/
  → G1 探索 / 精修（绑定正文_V3.6/）
  → build_unit1_trial_pdf.py
  → 薄样张_试读/Unit1_V3.6_五案试读/PDF/
```

## 角色

| 角色 | 担当 | 产出 |
|------|------|------|
| 导演/编剧 | Agent + Shot Map V2 基线 | `03_分镜头_插页地图_V3.6_JP.md` |
| 美工 | 人类或 GenerateImage | `绑定正文_V3.6/A00X/*.png` |
| 排版 | `tools/build_unit1_trial_pdf.py` | A5 纵排试读 PDF |

## 文件夹 taxonomy

| 路径 | 用途 |
|------|------|
| `正文/V3.6/01_中文/` | CN 参照（同 V3.1） |
| `正文/V3.6/02_日本語/` | **JP 试读正文 SSOT** |
| `正文/V3.6/04_分镜插画/A00X/` | Shot Map · 开工单 · prompts |
| `插图/绑定正文_V3.6/A00X/` | P0 成图 + `00_插图清单_V3.6.md` |
| `薄样张_试读/Unit1_V3.6_五案试读/PDF/` | 读者向试读 PDF |

## 诚实边界

- 当前试读 PDF 使用 **G1DRAFT** 探索稿（`_G1draft_PH.png` / `_c0X.png` 优选）
- **未过 E06-S + visual-auditor → 不得标 PRODUCT**
- PRODUCT-GATE 后替换 `绑定正文_V3.6` 并重跑 PDF

## 命令

```bash
python tools/setup_unit1_v36_pipeline.py
python tools/build_unit1_trial_pdf.py
```

## 参照

- [`academy-illustration-pipeline`](../../../.cursor/skills/academy-illustration-pipeline/SKILL.md)
- 样章包 `03_案0X_分镜头与插页地图_V2.0.md`（叙事/FC 基线）
""",
        encoding="utf-8",
    )
    return path


def main() -> None:
    update_v36_body_meta()
    wf = write_master_workflow()
    ill_counts = copy_illustrations()
    shot_paths = []
    for case in CASE_META:
        shot_paths.append(write_shot_map(case))
        write_work_order(case)
    print("Workflow:", wf)
    print("Shot maps:", len(shot_paths))
    print("Illustrations per case:", ill_counts)


if __name__ == "__main__":
    main()
