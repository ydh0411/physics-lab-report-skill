# 语言与写作规则

本文件是报告的表达关卡，不是文采建议。报告正文用英文；本文件的判定说明用中文，例句保持英文原文，方便直接对照删改。

流程位置：草稿 → 第一次内容通读 → 第二次表达通读 → 删除与改写 → 导出 DOCX/PDF（关卡定义见 [references/course-workflow.md](course-workflow.md)）。数值取舍与版式见 [references/calculation-layout-qa.md](calculation-layout-qa.md)，模板结构与篇幅见 [references/course-profile.md](course-profile.md)。

规则 id 固定，与 `scripts/lint_writing.py --list-rule` 一一对应：`AI-1`～`AI-8`（去 AI 味）、`DEF-1`～`DEF-6`（去防御性语言）、`OK-1`～`OK-3`（允许保留）。

---

## 1. 总原则

1. 内容完整但不重复。 同一件事只写一次：方法里写清楚做法，结果里只报数，讨论里只解释偏差。
2. 每句话回答四件事之一：测了什么、怎么测、得到什么数、凭什么这么说。答不上来的句子删掉。
3. 直接讲物理过程、测量、结果、解释。 不预告、不回顾、不评价自己写得如何。
4. 术语一致。 全报告一个物理量一个符号、一个器材一个英文词（如统一用 `interferometer`），同义词轮换视为错误（见 `AI-3`）。
5. 用户与课程要求高于通用科研写作默认。 模板要求写定义、写步骤、写思考题，就写；模板没要求的不补背景综述。
6. 表达问题就是评分风险。 评审读不懂你的推导会直接判为不懂实验，而不是「语言问题」。

---

## 2. 去 AI 味（`AI-1`～`AI-8`）

通用判据：这句话删掉或换成数字，报告的信息量是否减少？ 不减少就是 AI 味填充。

### `AI-1` 浮夸形容词与空泛意义

- 判定：形容词/副词替数据说话，删掉后信息量不变。命中词表：`crucial`、`vital`、`plays a key role`、`robust`、`comprehensive`、`remarkable`、`seamless`、`state-of-the-art`、`groundbreaking`、`pivotal`、`very important`、`extremely accurate`。
- 处理：换成数值、条件或对比；换不出就整句删。

```text
bad:  The alignment procedure plays a crucial role in this robust and comprehensive experiment.
good: The mirrors were aligned until a single central fringe remained.
```

### `AI-2` 机械三段式与套话

- 判定：段首/段尾的模板套话与总-分-总腔调：`First of all`、`It is worth noting that`、`It should be noted that`、`All in all`、`To sum up`、`In conclusion`、`needless to say`。
- 处理：删掉套话，直接给现象或结论；结论段第一句就写「测得什么、与参考值差多少」。

```text
bad:  All in all, it is worth noting that the measured wavelength is close to the reference value.
good: The measured wavelength is 632.6 ± 0.4 nm, against a reference value of 632.8 nm.
```

### `AI-3` 同义词轮换

- 判定：同一段落里用多个近义词指同一对象：`apparatus`/`device`/`instrument`/`equipment`；`method`/`procedure`/`approach`；`show`/`demonstrate`/`indicate`；`calculate`/`compute`/`derive`。
- 处理：一个对象只用一个词，全文锁定；新术语先在第 1 节术语层面定下来。

```text
bad:  The apparatus was levelled, the instrument was calibrated, and the equipment was checked.
good: The interferometer was levelled and calibrated before the first reading.
```

### `AI-4` 聊天腔开场

- 判定：以预告或讲解姿态开场：`In this report, we will …`、`This report aims to …`、`Let us consider …`、`As we all know …`、`In the following section, we …`。
- 处理：摘要与正文第一句直接给测量对象、方法、结果量级。

```text
bad:  In this report, we will explore how a Michelson interferometer measures wavelength.
good: The wavelength of a He-Ne laser was measured with a Michelson interferometer.
```

### `AI-5` 无信息承诺

- 判定：承诺后面要讲的内容而不给内容：`will be discussed in detail`、`is presented below`、`as will be shown later`、`more details can be found below`。
- 处理：删承诺；该讲的当场讲，不想讲就不提。

```text
bad:  The alignment procedure will be discussed in detail in the following section.
good: The movable mirror was tilted until the fringe spacing was uniform across the field.
```

### `AI-6` 列表堆砌代替论证

- 判定：同一段落出现 3 个及以上顺序标记（`first`/`second`/`third`、`1)`/`2)`/`3)`），或 `there are three main reasons` 式开头。
- 处理：改写成因果句或测量记录；真正的操作顺序放在 Experimental Procedure 的独立段落里（Long report）。
- 例外：Long report 的 Experimental Procedure 按操作顺序陈述属于允许，lint 在 Procedure 标题下不报此项。

```text
bad:  There are three main reasons for the offset: first the tilt, second the counting, third the drift.
good: A 0.4° tilt of the movable mirror accounts for most of the offset.
```

### `AI-7` 排比、粗体与感叹号滥用

- 判定：正文感叹号、emoji、同一段落 3 处以上粗体强调、`not only … but also` 对仗句。
- 处理：全删；强调靠对比数字（「比第二次测量大 1.8%，超过不确定度」）。

```text
bad:  Crucial: the fringe count decides the result!
good: One miscounted fringe shifts the wavelength by 0.6 nm.
```

### `AI-8` 每段必加过渡语

- 判定：同一段落有 2 句以上以 `Moreover`、`Furthermore`、`Additionally`、`In addition`、`Besides`、`Similarly` 开头。
- 处理：删过渡词，用物理因果连接（`because`、`so`、`which gives`）；段落之间靠内容衔接，不靠连接词。

```text
bad:  Moreover, the fringes were sharp. Furthermore, the count was stable. Additionally, the fit was good.
good: The fringes were sharp and the count stayed stable, so the fit residuals stayed below 2 counts.
```

---

## 3. 去防御性语言（`DEF-1`～`DEF-6`）

防御性语言的作用是保护作者，不是报告实验。读者不需要知道你多谨慎，只需要知道数据多可靠。

### `DEF-1` 模板与流程使用声明

- 判定：`We use the provided template`、`the provided tables`、`according to the template`、`the report follows the required format`。
- 处理：删。版式是否合规由成稿自己证明，正文不声明。

```text
bad:  We use the provided template and the provided data tables in this report.
good: Fringe counts and mirror positions are listed in Table 1.
```

### `DEF-2` 教材章节与处理流程旁白

- 判定：`Data are processed using Sec. 3.9.6`、`according to Chapter 5`、`as described in the lab manual`、`following the textbook procedure`。
- 处理：写公式、代入和结果，不写章节号。Long report 的 References 里正常列教材条目，那是文献，不是流程旁白。

```text
bad:  Data are processed using Sec. 3.9.6 of the textbook.
good: Fringe order N was converted to mirror displacement with d = Nλ/2.
```

### `DEF-3` 重复限定堆叠

- 判定：`might potentially`、`may possibly`、`could plausibly`、`seems to suggest`、`it is possible that … may`、`would appear to`。
- 处理：只留一层限定。结论段允许一个 `may` 或 `suggests`（见 `OK-1`），不允许叠两层。

```text
bad:  The residual offset might potentially suggest that the plate was slightly tilted.
good: The residual 0.4° offset suggests the plate was slightly tilted.
```

### `DEF-4` 自我辩护与免责

- 判定：`To ensure rigor`、`to avoid misunderstanding`、`for completeness`、`for clarity`、`it must be emphasized that`、`not to be confused with`。
- 处理：删。谨慎要体现在数据处理步骤里，不体现在声明里。

```text
bad:  To ensure rigor and avoid misunderstanding, we emphasize that all data were checked twice.
good: Each fringe count was repeated by a second observer, and the two counts differ by at most one.
```

### `DEF-5` 有效数字与不确定度规则的教学式解释

- 判定：解释取位与合成规则：`according to the rules of significant figures`、`the uncertainty is kept to one significant figure`、`by convention the coverage factor is two`、`the last digit is aligned`。
- 处理：取位直接体现在数值里：写 `d = 0.126 ± 0.002 mm`。只有题目明确要求解释规则时才答一次，且放在被问的位置。

```text
bad:  According to the rules of significant figures, the uncertainty is kept to one significant figure.
good: d = 0.126 ± 0.002 mm.
```

### `DEF-6` 假想反驳与自我设问

- 判定：`Some may argue that`、`One might object`、`It could be argued that`、`It may seem counterintuitive`、`contrary to common belief`。
- 处理：删。确有系统偏差时按 `OK-3` 写机制与量级，不写「有人可能会说」。

```text
bad:  Some may argue that fringe counting is subjective, but our data are reliable.
good: Two observers counted independently and differed by at most one count in ten.
```

---

## 4. 正例与反例对照（英文 before → after）

同一段 Michelson 干涉仪短报告，五组改写。每组只改表达，数字与结论不变。

### 4.1 摘要

```text
before: In this report, we will explore the Michelson interferometer. The experiment plays a crucial
        role in understanding wave interference. It is worth noting that the results are very
        important: the wavelength was found to be close to the reference value. All in all, the
        experiment was successful.
after:  The wavelength of a He-Ne laser was measured with a Michelson interferometer. Mirror
        displacement was read to 0.01 mm, and fringe counts were recorded at five positions. A
        least-squares fit gives 632.6 ± 0.4 nm, against a reference value of 632.8 nm.
```

要点：删预告（`AI-4`）、删浮夸（`AI-1`）、删套话（`AI-2`），换成方法、数据、结果。

### 4.2 结果段

```text
before: The apparatus was levelled, the instrument was calibrated, and the equipment was checked.
        Moreover, the fringes were sharp. Furthermore, the count was stable. Additionally, the fit
        was good. There are three main reasons for the offset: first the plate tilt, second the
        counting error, third the room drift. We use the provided data tables.
after:  The interferometer was levelled and the mirrors were aligned until a single central fringe
        remained. Fringe counts at five displacements are listed in Table 1. The fitted slope is
        1.2663, with a residual spread below 2 counts. A 0.4° tilt of the movable mirror accounts
        for the 0.2% deviation of the fitted wavelength.
```

要点：一个器材一个词（`AI-3`）、删过渡填充（`AI-8`）、删列举（`AI-6`）、删模板声明（`DEF-1`）。

### 4.3 讨论段

```text
before: The residual offset might potentially suggest that the plate was slightly tilted. To ensure
        rigor and avoid misunderstanding, we emphasize that all data were checked twice. Some may
        argue that the drift can be neglected, but we can confirm that it stays small.
after:  The residual 0.4° tilt suggests the plate holder was not seated flat. Two observers counted
        fringes independently and differed by at most one count in ten. Excluding the drift run
        changes the mean by less than the quoted uncertainty.
```

要点：限定只留一层（`DEF-3`）、删免责声明（`DEF-4`）、删假想反驳（`DEF-6`）；把「检查过两次」写成可验证的事实。

### 4.4 误差解释

```text
before: According to the rules of significant figures, the uncertainty is kept to one significant
        figure, and by convention the coverage factor is two. The dominant error might possibly come
        from the counting, which potentially affected the result.
after:  Fringe counting dominates the final uncertainty: one count in 240 contributes 0.6 nm, while
        the length reading contributes 0.1 nm. The combined uncertainty is 0.4 nm.
```

要点：删规则教学（`DEF-5`）、删限定堆叠（`DEF-3`）、删浮夸（`AI-1`）；误差按来源与量级写。

### 4.5 结论

```text
before: All in all, the method is robust and the experiment was successful. It should be noted that
        the measured value is very close to the reference value, which proves the theory.
after:  The measured wavelength, 632.6 ± 0.4 nm, agrees with the 632.8 nm reference value to within
        the quoted uncertainty. Fringe counting, not the length reading, limits the precision.
```

要点：结论段第一句就给数值与比较；不推销方法（`AI-1`）、不写「证明了理论」（超出证据边界）。

---

## 5. 两次通读

两次通读改同一份成稿，不另写语言评审报告，也不在两轮之间改数据。顺序固定：先内容，后表达。

### 5.1 第一次：内容通读

逐段回答下列问题，答不上来的整段重写：

- 模板要求的每个问题、每个小标题都答到了吗？有没有答非所问或漏题？
- 这段的职责是单一的（方法/结果/讨论/结论）吗？有没有把结果混进方法、把方法混进讨论？
- 论述链完整吗：为什么做这一步 → 公式 → 代入的数 → 得到的结果 → 与参考值比较。
- 详略符合模板篇幅吗（见第 6 节字数要求）？有没有在低分值内容上铺陈。
- 正文数字与图、表、附录数据表逐项一致吗？一处不一致就回数据源核对。

### 5.2 第二次：表达通读

按第 2、3 节的规则逐句过，逐类扫：

- 过程旁白与预告：删掉「本报告将」「下文将详细讨论」「按模板」（`AI-4`、`AI-5`、`DEF-1`、`DEF-2`）。
- 过度解释：删掉有效数字与不确定度规则的教学式说明（`DEF-5`），只在被问的位置保留一次。
- 重复限定与免责：限定收成一层，删自我辩护（`DEF-3`、`DEF-4`、`DEF-6`）。
- 聊天腔与浮夸：删套话、形容词、感叹号、粗体（`AI-1`、`AI-2`、`AI-7`）。
- 最后跑一遍 lint，确认命中项逐条处理或明确保留：

```bash
python3 scripts/lint_writing.py report.md --json
```

---

## 6. 报告类型差异

同一套规则，三种交付的篇幅与结构要求不同。

- Prelab（预习报告）：按题号逐题作答；不复述题目原文；不写「本报告将回答…」。每题先给结论，再给依据与公式。
- Short report（短报告）：摘要约 100 词，结论约 100 词；不设独立 Experimental Procedure 节，做法写在正文里。
- Long report（长报告）：Discussion 超过 150 词，Conclusion 约 50 词；有独立的 Experimental Procedure 与 References。
- 字数、分值与版式以当前教师 Word 模板为准（模板结构与占位见 [references/course-profile.md](course-profile.md)）；模板与本节冲突时以模板为准。

---

## 7. 允许保留的内容

去 AI 味与去防御性不是清零。下列内容保留，且只写一次、写在相关位置：

- `OK-1` 一层准确限定：`may`、`suggests`、`could indicate` 这类单层限定保留，表示证据强度而非逃避结论。
- `OK-2` 真实假设：影响结论的近似假设必须写，例如忽略浮力、忽略导轨摩擦、认为室温恒定；写在用到它的那一步，并给出影响量级。
- `OK-3` 异常数据、失败与偏差解释：异常值、装调失败、系统性漂移照实写，给机制与量级，不得删掉或改到贴近参考值。
- 证据边界：结论的适用范围（位移点数、单次装调、观测者数量）写一次，通常在结论末句。
- 必要的物理推导：从基本关系推到所用公式的关键步骤保留，不要跳步。
- 题目要求的定义：模板或思考题要求解释的概念，按题目要求写，不额外扩写。

```text
OK-1 示例: The 3% excess may come from the plate thickness tolerance.
OK-2 示例: The buoyancy correction was neglected because it changes the result by 0.02%.
OK-3 示例: The third run drifted by 1.8% and was excluded; the drift followed the room warm-up.
```

---

## 8. 自查清单

导出前逐项勾选，全部为「是」才提交。

- [ ] 每段都在答：测了什么 / 怎么测 / 得到什么数 / 凭什么这么说。
- [ ] 摘要与结论都有具体数值和与参考值的比较，没有「成功」「重要」这类评价。
- [ ] 同一器材、同一物理量全报告用词与符号一致。
- [ ] 正文没有预告、旁白、模板声明与教材章节号。
- [ ] 限定语只有一层，没有自我辩护与假想反驳。
- [ ] 取位直接体现在数值里，没有解释有效数字规则。
- [ ] 正文数字与图、表、附录逐项一致。
- [ ] 异常数据与失败尝试已按 `OK-3` 如实说明，未删除或改动。
- [ ] 真实假设只在相关位置说明一次，并给出影响量级。
- [ ] `python3 scripts/lint_writing.py <file>` 命中项已逐条处理或明确保留。

---

## 附录：lint 用法

```bash
python3 scripts/lint_writing.py report.md                 # 人读输出，命中即退出 1
python3 scripts/lint_writing.py report.docx --json        # 结构化结果，供 CI 判断
python3 scripts/lint_writing.py report.md --max 5         # 允许少量命中（配合人工复核）
python3 scripts/lint_writing.py --list-rule               # 打印全部规则 id 与判定要点
```

- 退出码：`0` 无命中或命中数 ≤ `--max`；`1` 超过阈值；`2` 用法错误；`3` 文件不可读或格式不支持。
- `.md`/`.txt` 纯标准库解析；`.docx` 优先用 python-docx，缺失时退化为解析 `word/document.xml`，仍不可读才退出 `3`。
- 命中是复核提示，不是删除命令：`OK-1`～`OK-3` 覆盖的句子应当保留。机器判断不了语境，最终由作者逐条确认。
- 回归样例：`tests/fixtures/bad-prose.md`（应退出 `1`）与 `tests/fixtures/good-prose.md`（应退出 `0`），CI 用它们防止规则退化。