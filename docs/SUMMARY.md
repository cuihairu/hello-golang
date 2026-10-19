# 导航维护说明

本站侧边栏的权威源是 [`docs/.vitepress/sidebar.json`](.vitepress/sidebar.json)，VitePress 配置直接读取该文件。此文件因 mdbook 历史兼容而保留，不再维护为第二份目录；手工修改本文件不会改变站点导航。

维护规则：新增、移除或调整页面导航时，只修改 `docs/.vitepress/sidebar.json`，并确认目标 Markdown 文件存在。若未来恢复生成脚本，应以 sidebar 为输入生成本文件或直接移除此映射底稿的用途；不得双向手工维护。构建配置通过 `srcExclude` 排除此页。
