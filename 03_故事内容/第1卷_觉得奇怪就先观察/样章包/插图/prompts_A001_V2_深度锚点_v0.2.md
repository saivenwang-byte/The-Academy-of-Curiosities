# A001 V2 · Depth Anchor · SC Prompts · v0.2

> **Status**: **ACTIVE** · 2026-06-07  
> **Brief**: [`07_设计原档/04_样章视觉/A001_V2_深度锚点包_6帧_画师开工单_V0.2.md`](../../../../07_设计原档/04_样章视觉/A001_V2_深度锚点包_6帧_画师开工单_V0.2.md)  
> **Supersedes**: `prompts_A001_深度锚点_v2_正篇画风.md`（侧廊/翘边 · ARCHIVED reference）  
> **Output**: `depth_anchor/V-S01-V2-A1_广播响起.png` … `V-S01-V2-TAIL_修复与尾钩.png`

---

## Global Style Block (prefix all prompts)

```
[Style] Japanese children's mystery bridge book, warm transparent watercolor,
clear ink line, age 10-12 readable, Nagoya elementary school spring late April,
NOT chibi, NOT mature anime, NOT 3D render, NOT horror,
indoor shoes uwabaki on classroom floor, observation club NOT detective agency
[IP] 学堂奇事録 · 学校おもしろ観察クラブ · Campus Ripple V2 A001 broadcast case
[Mechanism] loudspeaker playing voice while boy at podium lips NOT synced — NOT poster curl
```

---

## DA1 · V-S01-V2-A1 · Broadcast · Lips Not Synced

**Positive**
```
[Style block] half-page interior illustration, combined-grade classroom Nagoya spring morning,
public open-day rehearsal week, ceiling PA speaker active with subtle sound-wave or LED indicator,
boy Ito Akira age 10-11 in orange utility vest and white T-shirt standing at teacher podium,
mouth closed or just opening NOT matching broadcast timing, students in uwabaki turning to point,
girl Keimi with silver glasses holding interview notebook blocking accusation gesture,
stocky boy Shiro in green vest checking equipment cart panel near door,
transfer boy Riku Shun looking at PLAY monitor screen NOT at Akira's face,
mobile media equipment cart visible at corridor door, projection screen text mood about school open day,
afternoon slanted light through windows, sink area 流し at classroom rear, cold gray + broadcast orange accent,
fair-play clue: lip sync mismatch readable without text arrows
```

**Negative**
```
side corridor poster, curled poster edge, AC vent wind diagram, horror mob trial,
Chinese classroom, Yamamoto Risa named, detective magnifying glass, sneakers on floor,
night scene, villain spotlight on Mizuno
```

**Output**: `depth_anchor/V-S01-V2-A1_广播响起.png`

---

## DA2 · V-S01-V2-A2 · Observation Club Intervenes

**Positive**
```
[Style block] quarter to half-page, same combined classroom continuity as DA1,
girl Keimi arm gesture stopping classmates from labeling culprit, calm firm expression,
boy Shiro crouching at broadcast log tablet or equipment cart control panel humorous energy,
boy Akira pale quiet NOT confessing pose, boy Riku Shun standing aside taking notes not joining mob,
background ceiling speaker and podium readable, transparent display film sample bag on Shiro's green bag seed for next case,
uwabaki, spring light, whisper bubbles optional empty for Japanese typesetting
```

**Negative**
```
poster curl, corridor chase, violence, Akira kneeling apology, horror, Chinese school
```

**Output**: `depth_anchor/V-S01-V2-A2_观察社介入.png`

---

## DA3 · V-S01-V2-A3 · File Timestamp · FC-2

**Positive**
```
[Style block] quarter-page illustration, close on school tablet or PC monitor held by Riku Shun,
file name rehearsal_0328.wav or similar, timestamp three weeks earlier than today clearly readable,
finger or pencil pointing at date NOT at Akira's face, Keimi's grid notebook margin labeled heard-not-confirmed,
Akira partial profile background soft blur admitting similar words once, classroom clock or chalk note open-day countdown optional,
uwabaki at frame bottom, fair-play old recording clue
```

**Negative**
```
poster, mud prints, chalk circle, answer text overlay, horror UI, Chinese interface
```

**Output**: `depth_anchor/V-S01-V2-A3_文件时间.png`

---

## DA4 · V-S01-V2-A4 · Waveform Hard Cut · FC-3

**Positive**
```
[Style block] quarter-page, two children Shiro and Keimi studying audio waveform on tablet,
visible hard cut discontinuity before phrase segment about should-not-participate,
compressed audio format hint subtle, Shiro round glasses reflection, Keimi numbered grid notes,
classroom blurred background classmates still arguing silhouettes, mechanism diagram clarity for age 10-12,
warm watercolor NOT dense textbook, broadcast orange accent on waveform peak
```

**Negative**
```
wind arrows poster, rubber eraser crumbs, physics equations, horror waveform demon, dark palette
```

**Output**: `depth_anchor/V-S01-V2-A4_波形硬切.png`

---

## DA5 · V-S01-V2-A5 · Misidentification Peak · SC-07

**Positive**
```
[Style block] quarter-page emotional beat, multiple classmates gesturing everyone heard him,
boy Akira white-faced hand half-raised wanting to deny, girl Keimi physically blocking between Akira and class,
girl Mizuno Maho at back row head down NOT villain lighting silent bearing,
Riku Shun still oriented toward equipment side recording, podium speaker and monitor at least two of three visible,
uwabaki, spring classroom, wrong responsibility social peak NOT mechanism reveal yet, no blood no horror
```

**Negative**
```
poster side corridor, bully gang, Akira evil grin, Mizuno thief pose, night, Chinese uniforms
```

**Output**: `depth_anchor/V-S01-V2-A5_误指峰值.png`

---

## DA6 · V-S01-V2-TAIL · Repair + Tail Hook · A002 Seed

**Positive**
```
[Style block] quarter-page tail illustration optional split panel,
upper inset restored full rehearsal sentence context pencil Japanese placeholder latecomers rehearsal wording,
lower main frame equipment cart checklist clipboard next stop 5-2 classroom blackboard display film test record,
boy Shiro speech bubble space blackboard also has something strange, open-day spring light,
Kei diary corner optional tiny inset second truth mood NOT club member,
fair-play FC-4 truncated vs full sentence contrast without spoiler lecture text
```

**Negative**
```
curled poster empty wall column tail only, horror, QR code, lesson summary, Chinese text
```

**Output**: `depth_anchor/V-S01-V2-TAIL_修复与尾钩.png`

---

## Continuity Notes

| Item | DA1–DA6 |
|------|---------|
| Classroom layout | Same combined room · rear sink · door to corridor |
| Equipment cart | Same cart design DA1/2/6 |
| Character heights | L0 lineup · 光 146 · 珣 142 · 慧美 · 志郎 145 |
| Month | Late April Nagoya · cherry petal optional sparse |
| Shoes | uwabaki indoor only |

---

## Auditor Checklist (academy-visual-auditor)

- [ ] No poster curl / side corridor as primary frame
- [ ] FC-1 visible DA1 · FC-2 DA3 · FC-3 DA4 · FC-4 DA6
- [ ] Equipment cart in ≥2 frames
- [ ] Mizuno NOT villain lighting
- [ ] 5年 cross-class correct

---

Last updated: 2026-06-07 · V0.2 broadcast-first prompts
