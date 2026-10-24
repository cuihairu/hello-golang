// Locale helpers for the docs site.
//
// The navigation structure lives in one place (sidebar.json, zh labels,
// root-relative links, written for the mdbook legacy layout). From it we derive:
//   - the zh sidebar: same structure, every link prefixed with /zh
//   - the en sidebar: only the pages that already exist at the docs root,
//     labelled with the English page title
//
// English pages are added one batch at a time, so the en sidebar has to grow
// with the tree instead of listing links that do not exist yet.

import { existsSync, readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import enGroupLabels from './sidebar.en-labels.ts'

export interface NavItem {
  text: string
  link?: string
  collapsed?: boolean
  items?: NavItem[]
}

export type NavList = NavItem[]

const docsRoot = join(dirname(fileURLToPath(import.meta.url)), '..')

function pageFile(link: string, locale = ''): string {
  return join(docsRoot, locale, link.replace(/^\//, '') + '.md')
}

/** Whether the page behind `link` exists in the given locale (root by default). */
export function pageExists(link: string, locale = ''): boolean {
  const file = link === '/' ? join(docsRoot, locale, 'index.md') : pageFile(link, locale)
  return existsSync(file)
}

/** First `# ` heading of a page, if it has one. */
function headingOf(link: string, locale = ''): string | undefined {
  const file = pageFile(link, locale)
  if (!existsSync(file)) return undefined
  const line = readFileSync(file, 'utf8').split('\n').find((l) => /^#\s+/.test(l))
  const text = line?.replace(/^#\s+/, '').trim()
  return text || undefined
}

/** "ReleaseNotes" -> "Release Notes"; used where a page carries no heading. */
export function prettyName(link: string): string {
  const base = link.split('/').pop() ?? ''
  return base
    .replace(/\.md$/, '')
    .replace(/[_-]+/g, ' ')
    .replace(/([a-z0-9])([A-Z])/g, '$1 $2')
    .replace(/(^|\s)([a-z])/g, (_m, pre: string, ch: string) => pre + ch.toUpperCase())
    .trim()
}

/** English label for a root-locale page: its own heading, else the file name. */
function enLabel(link: string): string {
  return headingOf(link) ?? prettyName(link)
}

/** zh locale: keep the written labels, prefix every link with /zh. */
export function zhSidebar(structure: NavList): NavList {
  return structure.map((item) => {
    const next: NavItem = { text: item.text, collapsed: item.collapsed }
    if (item.link) next.link = '/zh' + item.link
    if (item.items?.length) next.items = zhSidebar(item.items)
    return next
  })
}

/** en locale: keep a node only while its page exists (or a child's does). */
export function enSidebar(structure: NavList): NavList {
  const out: NavList = []
  for (const item of structure) {
    const node = enNode(item)
    if (node) out.push(node)
  }
  return out
}

function enNode(item: NavItem): NavItem | undefined {
  const node: NavItem = { text: item.text, collapsed: item.collapsed }
  let hasItems = false
  if (item.items?.length) {
    const items: NavList = []
    for (const child of item.items) {
      const childNode = enNode(child)
      if (childNode) {
        items.push(childNode)
        hasItems = true
      }
    }
    if (items.length) node.items = items
  }
  if (item.link && pageExists(item.link)) {
    node.link = item.link
    node.text = enLabel(item.link)
  } else if (hasItems) {
    node.text = enGroupLabels[item.text] ?? prettyName(item.link ?? '') ?? item.text
  } else {
    return undefined
  }
  return node
}
