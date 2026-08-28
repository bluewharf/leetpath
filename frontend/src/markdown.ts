import DOMPurify from 'dompurify'
import { marked } from 'marked'
import markedKatex from 'marked-katex-extension'

marked.use(
  markedKatex({
    throwOnError: false,
    output: 'htmlAndMathml',
  }),
)

const EXTERNAL_URL = /^(?:https?:)?\/\//i

/** 题面 / 题解 / AI 回复共用的消毒配置：禁 style，禁 SVG，禁外链图片。 */
export const MARKDOWN_PURIFY_CONFIG = {
  USE_PROFILES: { html: true, mathMl: true, svg: false },
  FORBID_TAGS: ['svg', 'iframe', 'object', 'embed', 'form', 'input', 'link', 'meta', 'base', 'style'],
  FORBID_ATTR: ['style', 'srcset', 'srcdoc', 'xlink:href'],
  ADD_ATTR: ['target', 'rel', 'aria-hidden', 'display', 'xmlns', 'encoding'],
  ALLOW_DATA_ATTR: false,
}

// 外链必须带 noopener；外网图片 src 直接剥掉，避免像素追踪。
DOMPurify.addHook('afterSanitizeAttributes', (node) => {
  if (node.tagName === 'A' && node.hasAttribute('href')) {
    node.setAttribute('rel', 'noopener noreferrer')
  }
  if (node.tagName === 'IMG') {
    const src = node.getAttribute('src') || ''
    if (EXTERNAL_URL.test(src)) {
      node.removeAttribute('src')
    }
  }
})

export function filterSolutionMarkdown(markdown: string, lang: 'python3' | 'cpp'): string {
  if (!markdown) return ''
  
  const hasPy = /###\s*Python/i.test(markdown)
  const hasCpp = /###\s*C\+\+/i.test(markdown)
  
  if (!hasPy || !hasCpp) return markdown

  // 提取公共部分（思路与复杂度）
  const parts = markdown.split(/###\s*(Python|C\+\+)/i)
  const basePart = parts[0] || ''

  // 提取 Python 代码段
  const pyMatch = markdown.match(/(###\s*Python[\s\S]*?)(?=(?:###\s*C\+\+)|$)/i)
  // 提取 C++ 代码段
  const cppMatch = markdown.match(/(###\s*C\+\+[\s\S]*?)(?=(?:###\s*Python)|$)/i)

  if (lang === 'python3' && pyMatch) {
    return `${basePart.trim()}\n\n${pyMatch[1].trim()}`
  } else if (lang === 'cpp' && cppMatch) {
    return `${basePart.trim()}\n\n${cppMatch[1].trim()}`
  }

  return markdown
}

export function renderMarkdown(source: string): string {
  if (!source) return ''
  const rawHtml = marked.parse(source, { async: false }) as string
  return String(DOMPurify.sanitize(rawHtml, MARKDOWN_PURIFY_CONFIG))
}
