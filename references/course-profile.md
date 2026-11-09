# 课程地图与资料角色

本文件给出课程环境：身份字段、本地资料的角色与匹配方式、资料优先级、2026 三份 Word 模板结构、本学期编号映射、交付命名、公开边界。核对时间 2026-10。

模板换版、教师换人、学期变更后重新核对本文件；不把旧日期、旧编号、旧实验参数当永久常量。

## 身份字段

个人信息只存在于本地 `config/student_profile.yaml`（已被 `.gitignore` 排除）。仓库与文档中一律用占位符，不写真实姓名、学号、邮箱、教师或助教。

| 字段 | 占位符 | 出现位置 |
| --- | --- | --- |
| 姓名（中文） | `Your Name` | 封面 Name (in Chinese) |
| 学号 | `2024XXXXXXXX` | 封面 UESTC ID、页眉 UESTC Student Number、文件名前缀 |
| 邮箱 | `student@example.com` | 页眉 Email |
| 教师 | `Instructor Name` | 封面 Instructor |
| 助教 | `TA Name` | 封面 Teaching Assistant |
| 学院 / 专业 / 班级 | `Glasgow College` / `Your Major` / `2024XXXXXX` | 仅在模板有对应栏时填 |

字段名与取值来源见 `config/student_profile.example.yaml` 与 `config/template_fields.example.yaml`。第一次使用：复制 `config/*.example.yaml` 为同目录 `*.yaml` 再填写。

做与不做：

- 模板没有的字段不加栏。封面无邮箱栏就不在封面加邮箱；页眉有 Email 字段就填。
- 日期用客户端 `Asia/Shanghai` 当前日期。用户指定实验日期时用指定值。仅修订既有报告时保留原实验/报告日期，不自动替换成修订日。
- 中文姓名等身份字段按用户提供原样填写；报告正文用英文。

## 资料角色与匹配方式

本 skill 不用向量库或检索服务：资料靠下面的静态规则加用户运行时提供的本地文件来选。

本地课程资料按角色分类，不按固定绝对路径。下表给角色、典型文件名模式和用途；实际目录名可能不同，按模式匹配。

| 角色 | 典型文件名 / 目录模式 | 用途与选择方式 |
| --- | --- | --- |
| 本学期安排 | `本学期实验安排*.png`；仓库内 `assets/course-schedule-2026.png` | 确认本学期编号、实验全名和先后顺序。「下一个实验」查这张表，不按编号递增猜 |
| 当前教师 Word 模板 | `01-Template for Prelab work-Physical Experiment 2-2026.docx`、`02-Template for short lab report-Physical Experiment 2-2026.docx`、`03-Template for long lab report-Physical Experiment 2-2026.docx`；仓库内 `assets/word-templates/` | 控制封面字段、节标题、分值、评分框、附录。优先于任何资料包里的 2019 旧模板 |
| 教师公式与数据表格 | `Calculations for Lab-*.docx`、`Calculations for Lab *.docx`、`Data tables*.docx` | 本学期的公式结构、符号、计算顺序、表格列与合并关系。复制出来填，不重画 |
| 教师说明 | `报告说明.txt`、`Readme.txt` | 报告类型分配等硬性要求。编码常为 GB18030/GBK，按该编码读取，纯 UTF-8 打开出乱码不代表文件损坏 |
| 教师课件 | `EXP1*.ppt`、`EXP2*.ppt` 等 `EXP<n>` 命名 | 原理图、装置参数、思考题出处。只取对应实验 |
| 教材 | 实验书 PDF（文件名含 `大学物理实验`、`英文版`、`科学出版社` 与 ISBN） | 理论与公式来源。扫描版无文本层时按页渲染阅读，不能据此判定无内容 |
| 学长范例 | 以学号+姓名开头、含 `expNN` 的整学期报告目录 | 核对题目覆盖、结构、计算展开、版面。不复制测量值，不沿用错误公式 |
| 本人报告 | 以「学号 姓名 实验英文全名」开头的 `.docx` / `.pdf` | 当前提交文件。修改前确认版本，避免错改构建目录里的副本 |
| 原始数据 | 手写数据表扫描、`labNData.docx`、补测记录 | 唯一数据来源。扫描不清时只做草稿转写，逐值经用户确认后才计算 |
| 签名照片 | 根目录 `*.jpg` 中的已签数据表 | 已有签名不是所有未来报告的自动签署授权；prelab 不自动沿用签名 |
| 构建与缓存 | 任意 `build/`、`cache/`、制作工作目录 | 中间产物与提交版分开存放；不作为独立提交目录 |

匹配方式：

1. 先用实验英文全名匹配，再用别名，最后才用编号当线索。编号只用于封面和文件名。
2. 当前年份的模板与教师文件优先于历史资料包。
3. 找不到材料时按角色模式在课程目录里找，不在不存在的旧路径上继续假设。
4. 同一材料有多个版本时取更新、更具体的那份，并在汇报里说明用的是哪一版。
5. 教材引用要核对题名页和实际印刷页码，不把 PDF 页序号当书页码。
6. 笔记里保留原始文件名；生成的图、脚本、中间文件用短 ASCII 名，避免空格与中文路径带来的编译问题。
7. 学长报告的结论不是本学期结论：只借结构与展开方式，实验条件、常数、误差水平都要按当次材料重算。

忽略 Office 锁文件 `~$*` 与 `.DS_Store`；它们不是资料。

## 资料优先级

用户当次的明确要求高于下表全部条目；与下面任何一条冲突时按用户要求执行，并把冲突点告诉用户。

其余来源冲突时从上到下取：

| 优先级 | 来源 | 用法 |
| --- | --- | --- |
| 1 | 当次教师 Word 模板 | 决定封面字段、节标题、分值、评分框、附录要求 |
| 2 | 当次教师公式文件与数据表格（`Calculations for Lab-*.docx`、`Data tables*.docx`、`报告说明.txt`） | 决定本学期公式结构、表格列、特殊要求 |
| 3 | 实验卡片 `references/experiments/*.md` | 提供别名、必需数据表、公式清单、常见错误 |
| 4 | 教材 | 理论与公式解释；与教师文件冲突时以教师文件为准 |
| 5 | 学长报告 | 只作结构与版面参照；不覆盖当前模板，不提供数据 |

用户确认过的实测数据是计算输入的唯一来源，不因与理论值或学长结果不符而改动。

## 2026 三份 Word 模板结构

以下是 2026 三份模板的核验快照，制作时仍要打开实际文件核对；模板换版后重新核验。

| 模板 | 封面字段（表格行） | 页眉 | 正文节标题与分值 | 评分框 |
| --- | --- | --- | --- | --- |
| 01 Prelab | Lab Title / Name (in Chinese) / UESTC ID / Instructor / Teaching Assistant / Date / Score | `UESTC Student Number:   Email:   Date:`（正文节） | Answers to Questions (20 points) | 1 |
| 02 Short | 同上 | 无文字字段 | Abstract (About 100 words, 10 points)；Calculations and Results (Calculations, data tables and figures; 15 points)；Conclusions (About 100 words, 5 points)；Answers to Postlab Questions (10 points)；Appendix (Scanned data sheets) | 4 |
| 03 Long | 同上 | 同 Prelab（正文节）；第二节页眉 `Physics Experiment II` | Abstract (About 100 words, 3 points)；Introduction (3 points)；Experimental Procedure (State main steps in order of performance, 3 points)；Results (Data tables and figures, 2 points)；Discussion (More than 150 words, 5 points)；Conclusions (About 50 words, 2 points)；References (1 points)；Answers to Questions (6 points)；Appendix (Calculations, 15 points)；Appendix (Scanned data sheets) | 9 |

结构细节：

- 每份模板 2 节：封面（`different first page`）+ 正文（页码域，从 1 开始）。
- A4；页边距上下 1 inch、左右 1.25 inch。
- 模板内嵌图片 2 张（校徽 + 水印），正文 rFonts 全部为 Times New Roman；长报告模板另有 3 处宋体、1 处 Meiryo 残留。
- 模板本身不含 OMML 公式；公式由制作者以原生 OMML 插入，不贴图片。
- Prelab 与短报告不加 References、不放文内引用编号；长报告保留真实、核验过的 References。
- 分值只出现在模板评分框与节标题里，不另写进正文。

## 本学期编号与报告类型

2026 秋季学期编号（实验全名为主键，编号只用于封面和文件名）：

| 本学期编号 | 实验全名 | 正式报告类型 | 学长对应编号 |
| --- | --- | --- | --- |
| Lab6 | Measuring Laser Wavelength and Index of Refraction of Air by Michelson Interferometer | Long | exp08 |
| Lab7 | Measurement of the Apex Angle of a Prism and the Wavelengths of Mercury Lights Using a Spectrometer | Short | exp12 |
| Lab8 | The Franck-Hertz Experiment | Long | exp09 |
| Lab9 | The Millikan Oil Drop Experiment | Short | exp10 |
| Lab10 | The Photoelectric Effect | Short | exp11 |
| Lab11 | The Potentiometer | Short | exp13 |

- 本学期两个长报告：Michelson 与 Franck-Hertz；其余为短报告（教师说明原文：这学期写两个长报告，其余的短报告）。
- 顺序：Lab6 → Lab7 → Lab9 → Lab8，其后按学号单双号与安排表，查 `assets/course-schedule-2026.png` 决定。
- 每个实验都要交 prelab 和正式报告；正式报告用短报告或长报告模板按上表。
- 2026-10-24 Lab9 教师要求：只测 5 组油滴，每组 3 次电压和时间读数；两张数据表与附录保留 5 组、删除第 6–10 组空白行，平均元电荷取 5 组均值。此要求仅适用该次 Lab9，不外推到其他实验。
- 编号每年变化，学长编号（exp08、exp12 等）只是线索；完整对照见 [实验索引](experiment-index.md)。

## 交付命名

`<学号> <姓名> <实验英文全名>_prelab.docx` / `.pdf`；正式报告用 `_postlab` 或 `_lab_report`。

- 文件名变量与默认模板见 `config/naming.example.yaml`；复制为 `config/naming.yaml` 后按当次要求调整。
- 已有文件后缀不统一时先确认配对关系，不为统一后缀擅自重命名。例如某次预习 Word 无 `_prelab` 而对应 PDF 有，保留原名并说明。
- 同一实验的 `.docx` 与 `.pdf` 必须同版本导出；PDF 不是独立产物。

## 版权与公开边界

公开仓库只放结构化摘要与自写说明，不放课程原始材料：

- 不进公开仓库：教材 PDF、教师课件与计算文件、`Data tables*.docx`、学长报告、本人原始数据与扫描件、含签名的照片、任何含真实身份信息的文件。
- 可以进公开仓库：实验卡片（别名、必需数据表字段、公式名与计算步骤、常见错误）、流程与写作规则、模板结构快照、编号映射。
- 课程方要求撤下时，删除对应文件即可，不影响其余内容。
- 引用教材只写题名、版本与页码，不整段复制原文。
- 课程材料的来源与许可边界另见 `assets/ASSETS.md`。