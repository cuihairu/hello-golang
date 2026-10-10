import { defineConfig } from 'vitepress'
import sidebar from './sidebar.json'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  lang: 'zh-CN',
  title: 'Hello Golang',
  description: 'Go 语言知识体系——从语法入门到并发编程、设计模式、算法与工程实践',
  base: '/hello-golang/',
  cleanUrls: true,
  lastUpdated: true,

  head: [
    // 品牌资产空位：favicon.svg 到位后启用
    // ['link', { rel: 'icon', type: 'image/svg+xml', href: '/hello-golang/favicon.svg' }]
  ],

  // mdbook 遗留的目录文件保留在仓库作映射底稿，不作为页面构建
  srcExclude: ['**/SUMMARY.md'],

  ignoreDeadLinks: true,

  themeConfig: {
    // 品牌资产空位：logo.svg 到位后启用
    // logo: '/logo.svg',
    siteTitle: 'Hello Golang',

    nav: [
      { text: '首页', link: '/' },
      { text: '入门', link: '/start/Starter' },
      { text: '数据类型', link: '/type/CompositeType' },
      { text: '并发编程', link: '/concurrency/Concurrency' },
      { text: '设计模式', link: '/dp/DesignPatterns' },
      { text: '数据库', link: '/db/Readme' },
      { text: 'Gin 框架', link: '/gin/Gin' }
    ],

    // 由 mdbook SUMMARY.md 结构映射而来（scripts: parse_summary.py），
    // 50 个顶层分组
    sidebar: sidebar as never,

    socialLinks: [
      { icon: 'github', link: 'https://github.com/cuihairu/hello-golang' }
    ],

    footer: {
      message: 'Hello Golang',
      copyright: '© 2025 cuihairu'
    },

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

    outline: {
      label: '页面导航',
      level: [2, 3]
    },

    docFooter: {
      prev: '上一篇',
      next: '下一篇'
    },

    lastUpdated: {
      text: '最后更新'
    },

    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '菜单',
    darkModeSwitchLabel: '外观',
    lightModeSwitchTitle: '切换到浅色模式',
    darkModeSwitchTitle: '切换到深色模式'
  },

  markdown: {
    lineNumbers: false
  }
})
