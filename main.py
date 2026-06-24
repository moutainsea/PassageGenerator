# -*- coding: utf-8 -*-
"""PassageGenerator 命令行入口。

用法示例：
  # 1. 仅调研当前最热 top20
  python main.py research

  # 2. 按类别标签调研 top2
  python main.py research --tag 玄幻

  # 3. 生成一部小说（默认 mock 模式可跑通流程）
  python main.py generate --category 玄幻 --tags 玄幻,升级 --chapters 5

  # 4. 指定类别标签调研并生成
  python main.py generate --category 玄幻 --tags 玄幻,升级 --chapters 8 --research-tag 玄幻

  # 5. 查看历史调研文件
  python main.py history

  # 6. 生成番茄小说榜单热点分类小说
  python main.py generate --platform fanqie --category 都市 --tags 都市,系统 --chapters 20

  # 7. 续写飞卢小说（加载飞卢独立库与小说）
  python main.py continue 飞卢书名 5 --platform feilu

  # 8. 一键生成番茄前20章 + 飞卢前20章（互不重复）
  python main.py generate-all --chapters 20

环境变量：
  LLM_API_KEY   LLM 密钥（未设置则自动 mock）
  LLM_BASE_URL  LLM 服务地址
  LLM_MODEL     模型名
  LLM_MOCK=1    强制 mock 模式
"""
import argparse
import sys

from core.generator import NovelGenerator, GenerationConfig
from core.researcher import Researcher


def _split_tags(s):
    return [t.strip() for t in s.split(",") if t.strip()]


def cmd_research(args):
    researcher = Researcher()
    if args.platform:
        result = researcher.research_platform_hot(
            args.platform, top=args.top, category=args.tag, expand=args.expand
        )
        from config import platform_display_name, platform_rank_name
        print("[调研] 平台[" + platform_display_name(args.platform) + "/" + platform_rank_name(args.platform) +
              "] top" + str(len(result.items)) +
              (", 已扩充大纲" if args.expand else "") + "，已保存。")
    elif args.tag:
        result = researcher.research_by_tag(args.tag)
        print("[调研] 按标签[" + args.tag + "]获取 top" + str(len(result.items)) + " 部，已保存。")
    else:
        result = researcher.research_hot_top(top=args.top, expand=args.expand)
        print("[调研] 按时间获取最热 top" + str(len(result.items)) + " 部" +
              (", 已扩充大纲" if args.expand else "") + "，已保存。")
    for i, it in enumerate(result.items, 1):
        print("  " + str(i) + ". 《" + it.name + "》 [" + it.category + "] 热度:" + str(it.heat))
    return 0


def cmd_generate(args):
    tags = _split_tags(args.tags)
    cfg = GenerationConfig(
        category=args.category,
        tags=tags,
        chapter_count=args.chapters,
        do_research=not args.no_research,
        research_tag=args.research_tag,
        reference=args.reference or "",
        auto_fix=not args.no_fix,
        platform=args.platform,
        research_category=args.research_category,
        name=args.name,
    )
    gen = NovelGenerator(platform=cfg.platform)
    print("[生成] 开始生成小说：平台=" + cfg.platform + " 分类=" + cfg.category + " 章节数=" + str(cfg.chapter_count) + " 调研=" + str(cfg.do_research))
    novel, report = gen.generate(cfg)
    print("\n[完成] 小说《" + novel.name + "》已生成（平台=" + cfg.platform + "）")
    print("  分类：" + novel.category + "  标签：" + str(novel.tags))
    print("  简介：" + novel.brief)
    print("  章节数：" + str(len(novel.chapters)))
    for ch in novel.chapters:
        words = len("".join(ch.content.split()))
        print("    第" + str(ch.index) + "章《" + ch.title + "》 " + str(words) + "字")
    print("\n[检查] 通过=" + str(report.passed) + "  问题数=" + str(len(report.issues)))
    for iss in report.issues:
        print("  - " + iss)
    if report.advice:
        print("  [建议] " + report.advice)
    return 0 if report.passed else 1


def cmd_generate_all(args):
    """生成番茄小说榜单热点分类前20章 + 飞卢小说天榜前20章，两者不可重复。"""
    from core.generator import NovelGenerator, GenerationConfig
    from core.cross_platform_check import CrossPlatformChecker

    chapters = args.chapters
    print("=" * 60)
    print("[generate-all] 番茄小说榜单热点分类前" + str(chapters) + "章 + 飞卢小说天榜前" + str(chapters) + "章")
    print("  要求：两者互不重复（书名/章节标题/正文）")
    print("=" * 60)

    checker = CrossPlatformChecker()
    # 第一步：生成番茄
    print("\n>>> 第一步：生成番茄小说榜单热点分类")
    fanqie_cfg = GenerationConfig(
        category=args.fanqie_category or "都市",
        tags=_split_tags(args.fanqie_tags or "都市,系统"),
        chapter_count=chapters,
        do_research=True,
        auto_fix=not args.no_fix,
        platform="fanqie",
        research_category=args.fanqie_category,
    )
    fanqie_gen = NovelGenerator(platform="fanqie")
    fanqie_novel, fanqie_report = fanqie_gen.generate(fanqie_cfg)
    print("[番茄完成] 《" + fanqie_novel.name + "》 " + str(len(fanqie_novel.chapters)) + "章")

    # 第二步：生成飞卢，注入番茄避雷参考避免重复
    print("\n>>> 第二步：生成飞卢小说天榜（注入番茄避雷参考，确保不重复）")
    avoid_ref = checker.build_avoid_reference("fanqie")
    feilu_cfg = GenerationConfig(
        category=args.feilu_category or "玄幻",
        tags=_split_tags(args.feilu_tags or "玄幻,升级"),
        chapter_count=chapters,
        do_research=True,
        auto_fix=not args.no_fix,
        platform="feilu",
        research_category=args.feilu_category,
        reference=avoid_ref,
    )
    feilu_gen = NovelGenerator(platform="feilu")
    feilu_novel, feilu_report = feilu_gen.generate(feilu_cfg)
    print("[飞卢完成] 《" + feilu_novel.name + "》 " + str(len(feilu_novel.chapters)) + "章")

    # 第三步：跨平台去重检查
    print("\n>>> 第三步：跨平台去重检查（番茄 vs 飞卢）")
    cross_report = checker.check("fanqie", "feilu")
    if cross_report.passed:
        print("[去重检查] 通过：番茄与飞卢作品无重复")
    else:
        print("[去重检查] 发现 " + str(len(cross_report.conflicts)) + " 处重复：")
        for c in cross_report.conflicts:
            print("  - [" + c["type"] + "] " + c["detail"])
    print("\n" + "=" * 60)
    print("[全部完成]")
    print("  番茄: 《" + fanqie_novel.name + "》 " + str(len(fanqie_novel.chapters)) + "章  检查通过=" + str(fanqie_report.passed))
    print("  飞卢: 《" + feilu_novel.name + "》 " + str(len(feilu_novel.chapters)) + "章  检查通过=" + str(feilu_report.passed))
    print("  跨平台去重: " + ("通过" if cross_report.passed else "未通过"))
    print("=" * 60)
    return 0 if (fanqie_report.passed and feilu_report.passed and cross_report.passed) else 1


def cmd_history(args):
    researcher = Researcher()
    files = researcher.list_history()
    if not files:
        print("[历史] 暂无调研文件")
        return 0
    print("[历史] 调研文件列表：")
    for p in files:
        print("  " + p.name)
    return 0


def cmd_status(args):
    from core.llm_client import get_llm
    llm = get_llm()
    st = llm.status()
    print("[LLM 状态]")
    print("  mock 模式: " + str(st["mock"]))
    print("  可用平台(按优先级): " + (", ".join(st["available"]) if st["available"] else "无"))
    if st["preferred"]:
        print("  当前使用: " + st["preferred"])
    print("\n配置说明：设置任一平台 Key 即启用真实模型（GLM > Kimi > DeepSeek），失败自动转移。")
    print("  GLM:      $env:GLM_API_KEY=\"...\"")
    print("  Kimi:     $env:KIMI_API_KEY=\"...\"")
    print("  DeepSeek: $env:DEEPSEEK_API_KEY=\"...\"")
    return 0


def cmd_continue(args):
    from core.continuator import NovelContinuator
    c = NovelContinuator(platform=args.platform)
    novel, report = c.continue_novel(args.name, args.chapters)
    print("\n[续写完成] 《" + novel.name + "》（平台=" + args.platform + "）总章节数=" + str(len(novel.chapters)))
    print("  检查通过=" + str(report.passed) + "  问题=" + str(len(report.issues)))
    for iss in report.issues[:20]:
        print("  - " + iss)
    return 0 if report.passed else 1


def cmd_emotion_curve(args):
    """分析小说情绪曲线并输出报告。"""
    from core.emotion_curve import EmotionCurveGenerator
    gen = EmotionCurveGenerator()
    print("[情绪曲线] 加载小说: " + args.novel +
          ("（平台=" + args.platform + "）" if args.platform else ""))
    curve = gen.analyze_novel_file(args.novel, platform=args.platform)
    print("\n" + curve.to_text_report())
    gen.save_curve(curve, args.novel)
    return 0


def build_parser():
    p = argparse.ArgumentParser(
        prog="PassageGenerator",
        description="网络小说生成器：调研最热网文 -> 生成大纲与章节 -> 检查反思",
    )
    sub = p.add_subparsers(dest="command")

    # emotion-curve
    pec = sub.add_parser("emotion-curve", help="分析小说情绪曲线")
    pec.add_argument("novel", help="小说名称（如 八零厨神）")
    pec.add_argument("--platform", default=None,
                     choices=["qidian", "fanqie", "feilu"], help="小说平台")
    pec.set_defaults(func=cmd_emotion_curve)

    # research
    pr = sub.add_parser("research", help="调研最热网文（默认只取 top 2，可选扩充大纲）")
    pr.add_argument("--tag", default=None, help="按类别标签调研 top2；不指定则按时间取 top2")
    pr.add_argument("--platform", default=None, choices=["qidian", "fanqie", "feilu"],
                    help="按平台榜单调研（起点/番茄/飞卢）")
    pr.add_argument("--top", type=int, default=None,
                    help="取前N部（默认2，避免调研过宽导致后续生成写岔劈）")
    pr.add_argument("--expand", action="store_true",
                    help="基于 top 2 扩充每部作品的超详细大纲")
    pr.set_defaults(func=cmd_research)

    # generate
    pg = sub.add_parser("generate", help="生成小说")
    pg.add_argument("--category", default="玄幻", help="小说分类")
    pg.add_argument("--tags", default="玄幻,升级", help="类别标签，逗号分隔")
    pg.add_argument("--chapters", type=int, default=10, help="章节数")
    pg.add_argument("--no-research", action="store_true", help="跳过调研")
    pg.add_argument("--research-tag", default=None, help="使用指定类别标签调研(top2)")
    pg.add_argument("--reference", default="", help="参考信息文本")
    pg.add_argument("--no-fix", action="store_true", help="关闭自动修正")
    pg.add_argument("--platform", default="qidian",
                    choices=["qidian", "fanqie", "feilu"], help="小说平台（起点/番茄/飞卢）")
    pg.add_argument("--research-category", default=None, help="平台榜单调研的热点分类（如 都市/玄幻）")
    pg.add_argument("--name", default=None, help="指定小说名称（覆盖 LLM 自动生成）")
    pg.set_defaults(func=cmd_generate)

    # generate-all: 番茄前20章 + 飞卢前20章，互不重复
    pga = sub.add_parser("generate-all", help="生成番茄榜单前20章 + 飞卢天榜前20章（互不重复）")
    pga.add_argument("--chapters", type=int, default=20, help="每个平台章节数（默认20）")
    pga.add_argument("--fanqie-category", default=None, help="番茄调研热点分类（默认都市）")
    pga.add_argument("--fanqie-tags", default=None, help="番茄小说标签（默认 都市,系统）")
    pga.add_argument("--feilu-category", default=None, help="飞卢调研热点分类（默认玄幻）")
    pga.add_argument("--feilu-tags", default=None, help="飞卢小说标签（默认 玄幻,升级）")
    pga.add_argument("--no-fix", action="store_true", help="关闭自动修正")
    pga.set_defaults(func=cmd_generate_all)

    # history
    ph = sub.add_parser("history", help="查看历史调研文件")
    ph.set_defaults(func=cmd_history)

    # status
    ps = sub.add_parser("status", help="查看 LLM 平台配置与可用状态")
    ps.set_defaults(func=cmd_status)

    # continue
    pc = sub.add_parser("continue", help="续写已有小说")
    pc.add_argument("name", help="小说名称（如 外卖员的觉醒）")
    pc.add_argument("chapters", type=int, help="续写章节数")
    pc.add_argument("--platform", default="qidian",
                    choices=["qidian", "fanqie", "feilu"], help="小说平台（起点/番茄/飞卢）")
    pc.set_defaults(func=cmd_continue)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not getattr(args, "func", None):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
