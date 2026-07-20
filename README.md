# Zotero Analytical Workflow Skills

把 Zotero 文献库、Codex/Agent skill 和 Obsidian 文献笔记连接起来的一组可复用技能包。

本项目参考并延展了 [cheneternity/Zotero-Analytical-Workflow-Skills](https://github.com/cheneternity/Zotero-Analytical-Workflow-Skills)：参考项目提供了清晰的 Zotero 论文精读 skill 分层，本仓库在此基础上补充了批量队列、断点续跑、只读安全门禁、evidence schema、二次精读升级和旧笔记迁移审计工具。

## 包含内容

```text
skills/
  zotero-data-fetcher/
    SKILL.md
    scripts/zotero_fetch.py
  zotero-analytical-writer/
    SKILL.md
  zotero-collection-manager/
    SKILL.md
    scripts/
      zotero_collection_queue.py
      batch_import_collection.py
      deep_read_collection.py
      deep_read_all_imported.py
      import_unimported_report.py
      evidence_migration_planner.py
      evidence_migration_executor.py
      safety_io.py
templates/
  论文精读模板.md
```

## 三个核心 Skill

`zotero-data-fetcher` 用于按 Zotero Item Key 或标题提取元数据、批注、全文缓存和公开学术元数据。它默认优先读取本机 Zotero 服务，再回退到本地 SQLite；本步骤只负责取数，不翻译、不扩写。

`zotero-analytical-writer` 用于把原始语料重构为中文 Obsidian 精读笔记。它强调 frontmatter 提炼、证据等级、引用资格、公式乱码防护和正文噪音过滤。

`zotero-collection-manager` 用于批量处理 Zotero 分类，支持队列生成、断点续跑、初录入、二次精读升级、旧笔记 evidence schema 只读规划和小样本迁移执行。

## 安全设计

所有可能改写文件的脚本默认都是只读计划模式。真实写入必须显式传入 `--write`；覆盖已有 Markdown 还必须显式传入 `--overwrite`；旧笔记 evidence 迁移写入还需要 sample-only 门禁和 `--allow-vault-write`。

公开仓库不包含认证凭据、私有 Zotero 数据库、Obsidian vault、PDF、个人路径或处理日志。示例中的 `<note_root>`、`<vault_root>`、`<zotero_data_dir>`、`<workflow_root>` 都需要替换成你自己的本地路径。

## 快速使用

把 `skills/` 下的三个目录复制到你的 Codex skills 目录，把 `templates/论文精读模板.md` 放到对应模板目录。也可以把整个仓库作为 skill bundle 参考，让代理按 `SKILL.md` 中的脚本说明执行。

生成 Zotero 分类待处理队列：

```bash
python skills/zotero-collection-manager/scripts/zotero_collection_queue.py --collection "<分类名称>" --recursive --note-root "<note_root>"
```

批量初录入 dry-run：

```bash
python skills/zotero-collection-manager/scripts/batch_import_collection.py --collection "<分类名称>" --recursive --note-root "<note_root>"
```

确认无误后真实写入：

```bash
python skills/zotero-collection-manager/scripts/batch_import_collection.py --collection "<分类名称>" --recursive --note-root "<note_root>" --write
```

二次精读 dry-run：

```bash
python skills/zotero-collection-manager/scripts/deep_read_collection.py --collection "<分类名称>" --recursive --note-root "<note_root>"
```

旧笔记 evidence schema 只读审计：

```bash
python skills/zotero-collection-manager/scripts/evidence_migration_planner.py --note-root "<note_root>" --skip-zotero-check
```

## 项目简介

一句话版：一组面向 Zotero + Obsidian + Codex 的文献精读与批量录入 skills，支持只读队列、断点续跑、证据等级和安全写入门禁。

适合在知乎 Vibe-Coding 项目页填写的说明：

> 这是一个把个人 Zotero 文献库转换为结构化 Obsidian 文献笔记的 Codex skills 工作流。它将文献处理拆成取数、写作和批量调度三个 agent skill：先从本机 Zotero 服务或 SQLite 抽取元数据、批注和全文缓存，再按模板生成中文精读笔记，最后用队列脚本支持分类批处理、断点续跑、二次精读和 evidence schema 审计。公开版已移除个人路径、私有 vault、认证凭据和本地处理日志，所有写入脚本默认 dry-run，真实写入需要显式授权参数。

## Upstream attribution and mixed licensing

本项目改编并扩展了 [cheneternity/Zotero-Analytical-Workflow-Skills](https://github.com/cheneternity/Zotero-Analytical-Workflow-Skills)，上游作者为 Eternity Chen（GitHub [`cheneternity`](https://github.com/cheneternity)）。

五个固定上游文件版本及其下游对应文件由 [`UPSTREAM_PERMISSION_FINAL.md`](UPSTREAM_PERMISSION_FINAL.md) 管辖。这五个完整的下游对应文件，包括 `README.md`、三个 `SKILL.md` 文件和 `templates/论文精读模板.md`，采用单独许可，不属于本仓库下游 MIT License 的许可范围。只有仓库所有者有权以 MIT 许可发布的独立下游原创内容，才可能适用 MIT License。

有关来源、固定版本、文件映射和许可边界，请同时查阅：

- [`UPSTREAM_PERMISSION_FINAL.md`](UPSTREAM_PERMISSION_FINAL.md)
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)
- [`LICENSE_SCOPE.md`](LICENSE_SCOPE.md)
- [`ACKNOWLEDGEMENTS.md`](ACKNOWLEDGEMENTS.md)
- [`FILE_MAPPING_AND_HASH_MANIFEST.md`](FILE_MAPPING_AND_HASH_MANIFEST.md)

公开访问本仓库并不意味着这些单独许可的上游衍生材料被许可为 MIT。

## 许可证

本仓库采用混合许可。根目录 `LICENSE` 中的 MIT License 仅适用于仓库所有者有权以 MIT 许可发布的独立下游原创内容；完整边界见 [`LICENSE_SCOPE.md`](LICENSE_SCOPE.md)。
