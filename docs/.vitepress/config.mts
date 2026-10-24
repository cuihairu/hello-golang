import { defineConfig } from 'vitepress'
import { enSidebar, pageExists, zhSidebar, type NavList } from './i18n.mts'
import sidebar from './sidebar.json'

// https://vitepress.dev/reference/site-config
//
// Bilingual layout via VitePress locales: English lives at the docs root,
// Simplified Chinese under /zh/. sidebar.json stays the single source of the
// navigation structure; i18n.mts derives each locale's sidebar from it.

// [en label, zh label, root-relative page path]
const NAV: [string, string, string][] = [
  ['Home', '首页', '/'],
  ['Getting Started', '项目记录', '/start/Starter'],
  ['Data Types', '数据类型', '/type/CompositeType'],
  ['Concurrency', '并发编程', '/concurrency/Concurrency'],
  ['Design Patterns', '设计模式', '/dp/DesignPatterns'],
  ['Databases', '数据库', '/db/Readme'],
  ['Gin', 'Gin 框架', '/gin/Gin']
]

// Fail the build when a nav entry has no page behind it in either locale.
for (const [, , link] of NAV) {
  for (const locale of ['', 'zh'] as const) {
    if (!pageExists(link, locale)) {
      throw new Error(`nav link ${link} has no page in locale "${locale || 'root'}"`)
    }
  }
}

const enNav: NavList = NAV.map(([en, , link]) => ({ text: en, link }))
const zhNav: NavList = NAV.map(([, zh, link]) => ({
  text: zh,
  link: link === '/' ? '/zh/' : '/zh' + link
}))

export default defineConfig({
  lang: 'en-US',
  title: 'Hello Golang',
  description:
    'A game developer taking notes on Go: the practices, the trade-offs and the pitfalls.',
  base: '/hello-golang/',
  cleanUrls: true,
  lastUpdated: true,

  head: [
    // 品牌资产空位：favicon.svg 到位后启用
    // ['link', { rel: 'icon', type: 'image/svg+xml', href: '/hello-golang/favicon.svg' }]
  ],

  // mdbook 遗留的目录文件保留在仓库作映射底稿，不作为页面构建
  srcExclude: ['**/SUMMARY.md'],

  ignoreDeadLinks: false,

  locales: {
    root: {
      label: 'English',
      lang: 'en-US',
      themeConfig: {
        nav: enNav,
        sidebar: enSidebar(sidebar),
        search: { provider: 'local' },
        outline: { label: 'On this page', level: [2, 3] },
        docFooter: { prev: 'Previous', next: 'Next' },
        lastUpdated: { text: 'Last updated' },
        returnToTopLabel: 'Back to top',
        sidebarMenuLabel: 'Menu',
        darkModeSwitchLabel: 'Appearance',
        lightModeSwitchTitle: 'Switch to light theme',
        darkModeSwitchTitle: 'Switch to dark theme'
      }
    },
    zh: {
      label: '简体中文',
      lang: 'zh-CN',
      link: '/zh/',
      themeConfig: {
        nav: zhNav,
        sidebar: zhSidebar(sidebar),
        search: {
          provider: 'local',
          options: {
            translations: {
              button: { buttonText: '搜索文档', buttonAriaLabel: '搜索' },
              modal: {
                noResultsText: '没有找到结果',
                resetButtonTitle: '清除查询条件',
                footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' }
              }
            }
          }
        },
        outline: { label: '页面导航', level: [2, 3] },
        docFooter: { prev: '上一篇', next: '下一篇' },
        lastUpdated: { text: '最后更新' },
        returnToTopLabel: '回到顶部',
        sidebarMenuLabel: '菜单',
        darkModeSwitchLabel: '外观',
        lightModeSwitchTitle: '切换到浅色模式',
        darkModeSwitchTitle: '切换到深色模式'
      }
    }
  },

  themeConfig: {
    // 品牌资产空位：logo.svg 到位后启用
    // logo: '/logo.svg',
    siteTitle: 'Hello Golang',

    socialLinks: [
      { icon: 'github', link: 'https://github.com/cuihairu/hello-golang' }
    ],

    footer: {
      message: 'Hello Golang',
      copyright: '© 2025 cuihairu'
    }
  },

  markdown: {
    lineNumbers: false
  }
})
