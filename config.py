# -*- coding: utf-8 -*-
"""PassageGenerator 全局配置。

所有可调参数集中于此，便于维护。环境变量优先于默认值。
"""
import os
from pathlib import Path

# ---------------- 路径配置 ----------------
BASE_DIR = Path(__file__).resolve().parent
# 调研结果输出目录（存放 时间戳+hot20 / 时间戳+类别标签 的 json）
RESEARCH_DIR = BASE_DIR / "output" / "research"
# 生成小说输出目录
NOVEL_DIR = BASE_DIR / "output" / "novels"
# 各类库文件目录（事件库 / 主角库 / 配角库 / 地点库 / 时间库）
LIBRARY_DIR = BASE_DIR / "output" / "libraries"

for _d in (RESEARCH_DIR, NOVEL_DIR, LIBRARY_DIR):
    _d.mkdir(parents=True, exist_ok=True)


# ---------------- 本地 .env 加载 ----------------
# 从项目根目录的 .env 文件读取配置（key 等敏感信息不进代码库）。
# 已存在的环境变量优先（不被 .env 覆盖）。Python 3.5+ 兼容，零依赖。
def _load_env(env_path):
    p = str(env_path)
    if not os.path.isfile(p):
        return
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            k, _, v = line.partition("=")
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k and k not in os.environ:
                os.environ[k] = v


_load_env(BASE_DIR / ".env")


# ---------------- LLM 配置 ----------------
# 采用 OpenAI 兼容接口，标准库 urllib 调用，零第三方依赖，兼容 Python 3.5+。
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.85"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "8192"))
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "120"))

# 多平台配置（按优先级：GLM > Kimi > DeepSeek）。
# 只需配置其中一家的 Key 即可使用；某家调用失败会自动切换到下一家，
# 全部失败才回退 mock 模式。各平台 Key 分别读取独立环境变量。
LLM_PROVIDERS = [
    {
        "name": "GLM",                                   # 首选：智谱 GLM
        "base_url": os.getenv("GLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4"),
        "model": os.getenv("GLM_MODEL", "glm-4-plus"),
        "api_key": os.getenv("GLM_API_KEY", os.getenv("LLM_API_KEY", "")),
    },
    {
        "name": "Kimi",                                  # 第二顺位：月之暗面 Kimi
        "base_url": os.getenv("KIMI_BASE_URL", "https://api.moonshot.cn/v1"),
        "model": os.getenv("KIMI_MODEL", "moonshot-v1-32k"),
        "api_key": os.getenv("KIMI_API_KEY", ""),
    },
    {
        "name": "DeepSeek",                              # 第三顺位：DeepSeek
        "base_url": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
        "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        "api_key": os.getenv("DEEPSEEK_API_KEY", ""),
    },
]

# 是否启用 mock 模式：无任何平台 Key 时自动 mock；LLM_MOCK=1 强制 mock。
_any_key = any(p.get("api_key") for p in LLM_PROVIDERS)
LLM_MOCK = os.getenv("LLM_MOCK", "").lower() in ("1", "true", "yes") or (not _any_key)

# ---------------- 生成规则（来自 rules） ----------------
# 章节字数范围
CHAPTER_MIN_WORDS = 2200
CHAPTER_MAX_WORDS = 3200
# 小说名称/简介字数限制
NOVEL_NAME_MAX = 10
NOVEL_BRIEF_MAX = 100
# 章节结合上下文窗口（前1章 + 后1章）
CHAPTER_CONTEXT_BEFORE = 1
CHAPTER_CONTEXT_AFTER = 1

# ---------------- 调研配置 ----------------
RESEARCH_TOP_ALL = 20      # 按时间查询的最热数量
RESEARCH_TOP_BY_TAG = 2    # 按类别标签查询的最热数量

# ---------------- 平台配置 ----------------
# 支持的小说平台：每个平台拥有独立的库目录、调研文件、小说文件，互不混淆。
# code 用于目录/文件名前缀；name 用于提示词展示；rank_name 用于榜单调研提示。
NOVEL_PLATFORMS = {
    "qidian": {"name": "起点", "rank_name": "起点畅销榜"},
    "fanqie": {"name": "番茄", "rank_name": "番茄小说榜单"},
    "feilu": {"name": "飞卢", "rank_name": "飞卢小说天榜"},
}
DEFAULT_PLATFORM = "qidian"


def platform_lib_dir(platform):
    """返回指定平台的库目录（output/libraries/{platform_code}）。

    起点平台向后兼容：若 qidian 子目录不存在但根目录已有库文件，
    则复用根目录（保留现有数据），避免数据迁移。
    """
    code = platform if platform in NOVEL_PLATFORMS else DEFAULT_PLATFORM
    sub = LIBRARY_DIR / code
    if code == DEFAULT_PLATFORM and not sub.exists():
        # 起点向后兼容：根目录有库文件则复用根目录
        if (LIBRARY_DIR / "character_library.json").exists():
            return LIBRARY_DIR
    return sub


def platform_display_name(platform):
    """返回平台展示名（如 起点/番茄/飞卢）。"""
    info = NOVEL_PLATFORMS.get(platform)
    return info["name"] if info else str(platform)


def platform_rank_name(platform):
    """返回平台榜单名（如 起点畅销榜/番茄小说榜单/飞卢小说天榜）。"""
    info = NOVEL_PLATFORMS.get(platform)
    return info["rank_name"] if info else str(platform)
