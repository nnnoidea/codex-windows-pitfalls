# Codex Windows 踩坑记录

Codex 在 Windows 上会反复遇到一些小问题：PowerShell 的差异、反斜杠转义、非 ASCII 路径、换行符提示、沙箱审批、Git/SSH 网络绕行等。

`codex-windows-pitfalls` 是一个让 Codex 记住这些经验的 skill。skill 负责告诉 Codex 怎么查、怎么更新；真正重要的坑库是一个独立 Markdown 文件：

```text
.codex-windows-pitfalls.md
```

需要保存和分享的是这个文件。

## 你需要做什么

- 在 Codex 里安装或启用 `codex-windows-pitfalls` skill。
- 把 `.codex-windows-pitfalls.md` 放在 Codex 能找到的工作区里。
- 想让其他工作区或其他人复用经验时，分享 `.codex-windows-pitfalls.md`。
- 偶尔 review 这个文件，删掉私密信息、合并弱条目，或把重要模式整理得更清楚。

正常使用时，你不需要手动运行记录脚本。

## Codex 会做什么

触发 skill 后，Codex 应该：

- 找到 `.codex-windows-pitfalls.md`。
- 从中生成一份启动摘要，最多 20 条，按 `Count` 排序。
- 在执行 Windows shell、文件系统、Git/SSH、编码或沙箱敏感操作前，先读这份摘要。
- 当摘要没有覆盖当前症状时，再搜索完整坑库。
- 把可复用的新坑记录回 `.codex-windows-pitfalls.md`。
- 遇到同类问题时增加 `Count`，而不是创建重复条目。

## 坑库文件

每个条目记录症状、原因、推荐做法、避免做法、来源和 `Count`。

`Count` 用来决定优先级。高频坑会进入启动摘要；低频坑继续留在完整文件里，遇到对应症状时再查。

不要把密钥、凭证、私密原始日志或很长的会话记录写进坑库。

## 分享

想分享经验时，分享 `.codex-windows-pitfalls.md` 就够了。

对方可以直接阅读这个文件。如果对方也安装了这个 skill，Codex 就可以基于它生成摘要，并在之后的工作里继续扩展。

