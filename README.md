# PassageGenerator 网文生成器

基于 autonomous workflow 的网络小说生成器，支持起点、番茄、飞卢等多平台，采用分线叙事结构，具备完整的调研、生成、检查、续写流程。

## 核心功能

### 一、调研当前最热的网文小说
- **按时间查询**：获取最热 top 20 小说（名称/简介/分类/章节名称/详细大纲），存为 `{时间戳}_hot20.json`
- **按类别标签查询**：获取最热 top 2 小说（超详细大纲），存为 `{时间戳}_{标签}.json`
- **按平台榜单调研**：支持起点畅销榜、番茄小说榜单、飞卢小说天榜，各平台调研产物独立存储

### 二、根据信息生成小说
- **小说结构**：名称(≤10字)、简介(≤100字)、分类、大纲、章节内容
- **分线叙事结构**（最高优先级）：
  - 每部小说定义 2 条以上分线（如事业线、生活线）
  - 分线交替推进，避免读者疲惫
  - 切换处自然衔接，不得生硬跳转
- **事件线大纲**：大事件 → 中事件 → 小事件
  - 小事件 = 事件影响 + 事件背景 + 主角人数(≥1) + 配角人数(0-3) + 人物形象 + 人物行为 + 所处时间 + 所在地表状态表
  - 小事件的转移 = 状态表的转移
- **独立事件库文件**，并派生维护：
  - 主角人物形象库、配角人物形象库（可复用，场景如 故地重逢/碰巧遇到/共同目标）
  - 地点库、时间库（可复用）
- **章节内容**：每个章节扩写一个小事件；书写时结合前 1 章与后 1 章的标题/大纲/内容；每章 2200-3200 字

### 三、检查小说内容、大纲、章节名称
- 章节内容/大纲/章节名称与小说总体大纲对应节点是否匹配
- 人物/时间/地点与各库对应节点是否匹配、合理
- 章节内容与章节名称是否重复（n-gram 相似度）
- 分线交替是否合理：切换处是否衔接自然、章节归属是否与 subplots 定义一致
- 反思：错漏/不通顺/太AI风格（结合前后章节），并支持自动修正

### 四、续写已有小说
- 加载已有小说 JSON 文件
- 分析现有情绪曲线，参考前文节奏
- 遵循分线交替规律续写
- 自动扩展大纲和库文件

### 五、情绪曲线分析
- 分段分析小说情绪走向
- 生成情绪曲线报告（JSON + TXT）
- 检测情绪异常段落，提供修正建议

### 六、跨平台去重检查
- 番茄与飞卢作品互不重复（书名/章节标题/正文）
- 一键生成双平台小说，自动去重验证

## 目录结构

```
PassageGenerator/
├── architechture.txt            # 架构说明（最高参考）
├── requirements.txt             # 实际零依赖（说明用）
├── config.py                    # 全局配置（路径/LLM/.env加载/生成规则/平台）
├── main.py                      # CLI 入口（research/generate/continue/generate-all/history/status/emotion-curve）
├── .env                         # 本地密钥配置（gitignore，勿提交）
├── .gitignore
├── models/                      # 数据模型
│   ├── character.py             # 人物（主角/配角，含技能/道具/称号）
│   ├── event.py                 # 事件线（大/中/小事件+状态表）
│   ├── location.py              # 地点库
│   ├── timeline.py              # 时间库
│   └── novel.py                 # 小说/章节/大纲/Subplot分线模型
├── storage/                     # 库管理与持久化
│   ├── libraries.py             # 主角/配角/地点/时间库（JSON，按平台隔离）
│   └── research_store.py        # 调研结果存储
├── core/                        # 核心生成逻辑
│   ├── llm_client.py            # LLM 客户端（多平台故障转移+mock）
│   ├── researcher.py            # 调研模块
│   ├── outline_builder.py       # 大纲构建（事件线+分线+回填各库+标题清洗）
│   ├── chapter_writer.py        # 章节写作（结合前后章节+分线上下文）
│   ├── checker.py               # 检查与反思（含分线一致性检查）
│   ├── continuator.py           # 续写模块（加载已有小说+分线+情绪曲线参考+扩展大纲）
│   ├── emotion_curve.py         # 情绪曲线生成器（分段情绪分析+曲线合并+检测修正建议）
│   ├── character_consistency.py # 角色一致性检测
│   ├── cross_platform_check.py  # 跨平台去重检查
│   └── generator.py             # 生成器主流程
└── output/                      # 运行时生成（gitignore）
    ├── research/                # 调研 json
    ├── novels/                  # 生成的小说（json + txt）
    │   └── emotion_curves/      # 情绪曲线报告
    └── libraries/               # 各库 json（按平台隔离）
        ├── qidian/             # 起点平台库（向后兼容根目录）
        ├── fanqie/             # 番茄平台库
        └── feilu/               # 飞卢平台库
```

## 安装

本项目使用 Python 标准库（`urllib`/`json`/`argparse` 等）调用 LLM，**零第三方依赖**，兼容 Python 3.5+，无需 `pip install`。

```bash
# 克隆项目
git clone <repository_url>
cd PassageGenerator

# 无需安装依赖，直接使用
python main.py --help
```

## 配置 LLM

采用 OpenAI 兼容接口，支持**多平台故障转移**：GLM（首选）→ Kimi（第二）→ DeepSeek（第三）→ mock（兜底）。某平台调用失败自动切换下一家，全部失败才回退 mock。

### 方式一：`.env` 文件（推荐，key 不进代码库）

项目根目录已内置 `.env`（已被 `.gitignore` 忽略），填入任一平台 Key 即可：

```ini
# DeepSeek
DEEPSEEK_API_KEY=sk-xxxx
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

# 智谱 GLM（首选，如需启用）
# GLM_API_KEY=...
# GLM_MODEL=glm-4-plus

# 月之暗面 Kimi（第二顺位，如需启用）
# KIMI_API_KEY=...
# KIMI_MODEL=moonshot-v1-32k
```

### 方式二：环境变量（PowerShell）

```powershell
$env:DEEPSEEK_API_KEY="sk-xxxx"   # 或 GLM_API_KEY / KIMI_API_KEY
```

### 查看当前启用状态

```bash
python main.py status
```

### 强制 mock 模式（无需 Key，输出占位内容用于联调）

```bash
# PowerShell
$env:LLM_MOCK="1"
```

## 使用指南

### 1. 调研功能

#### 1.1 调研当前最热 top 20

```bash
python main.py research
```

生成文件：`output/research/{时间戳}_hot20.json`

#### 1.2 按标签调研 top 2

```bash
python main.py research --tag 玄幻
```

生成文件：`output/research/{时间戳}_玄幻.json`

#### 1.3 按平台榜单调研

```bash
# 调研番茄小说榜单热点分类
python main.py research --platform fanqie --top 5 --expand

# 调研飞卢小说天榜
python main.py research --platform feilu --top 3

# 调研起点畅销榜
python main.py research --platform qidian --top 10
```

参数说明：
- `--platform`：平台选择（qidian/fanqie/feilu）
- `--top`：取前N部（默认2，避免调研过宽导致后续生成写岔劈）
- `--expand`：基于 top 2 扩充每部作品的超详细大纲

#### 1.4 查看历史调研文件

```bash
python main.py history
```

### 2. 生成小说

#### 2.1 基础生成（mock 模式可直接运行）

```bash
python main.py generate --category 玄幻 --tags 玄幻,升级 --chapters 5
```

#### 2.2 指定平台生成

```bash
# 生成番茄小说
python main.py generate --platform fanqie --category 都市 --tags 都市,系统 --chapters 20

# 生成飞卢小说
python main.py generate --platform feilu --category 玄幻 --tags 玄幻,升级 --chapters 15

# 生成起点小说（默认）
python main.py generate --category 都市 --tags 都市,重生 --chapters 10
```

#### 2.3 带标签调研后生成

```bash
python main.py generate --category 玄幻 --tags 玄幻,升级 --chapters 8 --research-tag 玄幻
```

#### 2.4 指定平台榜单分类调研并生成

```bash
# 番茄都市热点分类
python main.py generate --platform fanqie --category 都市 --tags 都市,系统 --chapters 20 --research-category 都市

# 飞卢玄幻热点分类
python main.py generate --platform feilu --category 玄幻 --tags 玄幻,升级 --chapters 20 --research-category 玄幻
```

#### 2.5 指定小说名称

```bash
python main.py generate --name "我的小说名" --category 都市 --tags 都市,系统 --chapters 10
```

#### 2.6 跳过调研直接生成

```bash
python main.py generate --category 玄幻 --tags 玄幻,升级 --chapters 5 --no-research
```

#### 2.7 关闭自动修正

```bash
python main.py generate --category 玄幻 --tags 玄幻,升级 --chapters 5 --no-fix
```

### 3. 续写小说

#### 3.1 续写起点小说

```bash
python main.py continue 外卖员的觉醒 10
```

#### 3.2 续写番茄小说

```bash
python main.py continue 我的番茄小说 5 --platform fanqie
```

#### 3.3 续写飞卢小说

```bash
python main.py continue 八零厨神 5 --platform feilu
```

参数说明：
- `name`：小说名称（对应 output/novels/ 下的 JSON 文件名）
- `chapters`：续写章节数
- `--platform`：小说平台（默认 qidian）

### 4. 情绪曲线分析

```bash
# 分析起点小说
python main.py emotion-curve 外卖员的觉醒

# 分析番茄小说
python main.py emotion-curve 我的番茄小说 --platform fanqie

# 分析飞卢小说
python main.py emotion-curve 八零厨神 --platform feilu
```

生成文件：
- `output/novels/emotion_curves/{小说名}_emotion_curve.json`
- `output/novels/emotion_curves/{小说名}_emotion_curve.txt`

### 5. 跨平台一键生成

一键生成番茄前20章 + 飞卢前20章（互不重复）：

```bash
python main.py generate-all --chapters 20
```

自定义参数：

```bash
python main.py generate-all \
  --chapters 20 \
  --fanqie-category 都市 \
  --fanqie-tags 都市,系统 \
  --feilu-category 玄幻 \
  --feilu-tags 玄幻,升级
```

流程说明：
1. 第一步：生成番茄小说榜单热点分类
2. 第二步：生成飞卢小说天榜（注入番茄避雷参考，确保不重复）
3. 第三步：跨平台去重检查（番茄 vs 飞卢）

### 6. 查看状态

```bash
python main.py status
```

显示：
- mock 模式状态
- 可用平台列表（按优先级）
- 当前使用的平台
- 配置说明

## 生成规则说明

### 最高级优先规则——分线叙事制

1. **分线定义**：每部小说须在 outline.subplots 中定义 2 条以上分线
   - 每条分线包含：id、name、description、chapter_indices（所属章节）、stages（阶段划分）
   
2. **交替推进**：一个分线完成一个小阶段叙述后，切换到另一个分线叙述，避免读者疲惫

3. **自然衔接**：分线之间的切换必须保证衔接自然、前后情节合理通顺
   - 切换处须有过渡铺垫：或以时间推移衔接、或以因果联系衔接、或以人物心理衔接
   - 不得生硬跳转

4. **章节归属**：
   - 章节标题须体现当前章节所属分线的主题特征
   - 章节内容须聚焦当前分线的核心事件，同时可适当提及另一分线的进展作为呼应，但不得喧宾夺主

5. **续写规则**：续写时须先确定续写章节的分线归属，遵循交替规律，并在切换处做好衔接

### 最高级优先规则

1. 该项目的架构组成文件为本文件夹下的 architecture.txt，此文件详细讲述了该项目的架构组成、功能组成，其为最高可信且使用的参考资料
2. 在思考分析后生成的内容，进行反思，查看是否有错漏地方，若有则进行修改，若无则进行下一步
3. 生成的内容进行检查，查看是否有不合理、不通顺、太AI风格，若有则进行修改，若无则进行下一步
4. 生成的内容需要结合前面和后面章节（前面1章，后面1章）的内容，进行检查，若有不合理的地方，则进行修改，若无则进行下一步

### 次高级优先规则

1. 生成的内容需要符合网络小说相关的格式，包括标题、章节、段落、内容等
2. 生成的内容需要符合给出的事件描述+人物形象+所在时间+所处地点
3. 注意生成的内容不要与参考的内容太相似，否则会导致生成内容的质量下降
4. 每个章节的内容要在 2200-3200 字之间

### 普通规则

1. 句子语义通顺
2. 词语使用恰当
3. 段落结构合理
4. 章节内容完整

## 输出文件说明

### 小说文件

- `output/novels/{小说名}.json`：完整结构化数据（含事件线大纲、分线定义与各库引用）
- `output/novels/{小说名}.txt`：可读正文
- `output/novels/{平台前缀}_{小说名}.json/txt`：平台隔离的小说文件（如 feilu_八零厨神.json）

### 调研文件

- `output/research/{时间戳}_hot20.json`：按时间查询的最热 top 20
- `output/research/{时间戳}_{标签}.json`：按标签查询的最热 top 2
- `output/research/{时间戳}_{平台}_{分类}.json`：按平台榜单调研的结果

### 库文件

- `output/libraries/character_library.json`：主角人物形象库（起点平台向后兼容）
- `output/libraries/location_library.json`：地点库
- `output/libraries/timeline_library.json`：时间库
- `output/libraries/{平台}/`：各平台独立库目录（fanqie/feilu/qidian）

### 情绪曲线文件

- `output/novels/emotion_curves/{小说名}_emotion_curve.json`：结构化情绪数据
- `output/novels/emotion_curves/{小说名}_emotion_curve.txt`：可读情绪报告

## 平台隔离说明

本项目支持起点、番茄、飞卢三个平台，各平台拥有独立的：

1. **库目录**：`output/libraries/{platform}/`
   - 起点平台向后兼容：若 qidian 子目录不存在但根目录已有库文件，则复用根目录
   
2. **调研文件**：`output/research/{时间戳}_{platform}_{分类}.json`

3. **小说文件**：`output/novels/{platform}_{小说名}.json/txt`

4. **生成流程**：各平台独立生成，互不干扰

## 分线叙事示例

以《八零厨神》为例：

```json
{
  "subplots": [
    {
      "id": "career_line",
      "name": "餐饮事业线",
      "description": "主人公从小人物成长为厨神，在餐饮事业取得高成就",
      "chapter_indices": [1, 3, 5, 7, 9, 11, 13, 15, 17, 19],
      "stages": [
        {"name": "摆摊创业", "chapters": [1, 3], "summary": "主人公开始摆摊卖早点"},
        {"name": "规范化经营", "chapters": [5, 7], "summary": "开设正规餐馆"},
        {"name": "工坊扩建", "chapters": [9, 11, 13], "summary": "扩大经营规模"},
        {"name": "成名厨神", "chapters": [15, 17, 19], "summary": "成为知名大厨"}
      ]
    },
    {
      "id": "life_line",
      "name": "四合院生活线",
      "description": "主人公在四合院的生活，与邻居、亲人、朋友、情感的生活线",
      "chapter_indices": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
      "stages": [
        {"name": "立足院落", "chapters": [2, 4], "summary": "在四合院站稳脚跟"},
        {"name": "亲情纽带", "chapters": [6, 8], "summary": "与家人建立深厚感情"},
        {"name": "邻里斗争", "chapters": [10, 12, 14], "summary": "处理邻里矛盾"},
        {"name": "情感收束", "chapters": [16, 18, 20], "summary": "情感线圆满收束"}
      ]
    }
  ]
}
```

## 常见问题

### Q1: 如何选择平台？

- **起点（qidian）**：默认平台，适合传统网文风格
- **番茄（fanqie）**：适合快节奏、爽文风格
- **飞卢（feilu）**：适合脑洞大、节奏快的风格

### Q2: 生成速度慢怎么办？

- 使用 `--no-research` 跳过调研步骤
- 使用 `--no-fix` 关闭自动修正
- 减少章节数量

### Q3: 如何提高生成质量？

- 先调研热门作品：`python main.py research --platform fanqie --expand`
- 使用调研结果生成：`python main.py generate --research-category 都市`
- 确保配置了有效的 LLM API Key

### Q4: 续写时如何保持风格一致？

续写模块会自动：
- 加载已有小说的大纲和分线定义
- 分析情绪曲线，参考前文节奏
- 遵循分线交替规律
- 扩展大纲和库文件

### Q5: 如何查看生成进度？

生成过程中会实时输出：
- 当前生成的章节标题
- 每章字数统计
- 检查结果（通过/问题数）

### Q6: 跨平台去重如何工作？

`generate-all` 命令会：
1. 先生成番茄小说
2. 将番茄内容作为"避雷参考"注入飞卢生成流程
3. 最后进行跨平台去重检查（书名/章节标题/正文）

## 开发说明

### 核心模块

- **llm_client.py**：LLM 调用封装，支持多平台故障转移
- **researcher.py**：调研模块，支持多平台榜单调研
- **outline_builder.py**：大纲构建，包含分线设计和事件线生成
- **chapter_writer.py**：章节写作，结合前后章节和分线上下文
- **checker.py**：检查与反思，包含分线一致性检查
- **continuator.py**：续写模块，支持情绪曲线参考
- **emotion_curve.py**：情绪曲线分析器

### 扩展平台

在 `config.py` 的 `NOVEL_PLATFORMS` 中添加新平台配置：

```python
NOVEL_PLATFORMS = {
    "qidian": {"name": "起点", "rank_name": "起点畅销榜"},
    "fanqie": {"name": "番茄", "rank_name": "番茄小说榜单"},
    "feilu": {"name": "飞卢", "rank_name": "飞卢小说天榜"},
    # 添加新平台
    "new_platform": {"name": "新平台", "rank_name": "新平台榜单"},
}
```

## 许可证

本项目仅供学习和研究使用，请勿用于商业用途。

## 贡献

欢迎提交 Issue 和 Pull Request！