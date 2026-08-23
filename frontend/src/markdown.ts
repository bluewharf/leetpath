import DOMPurify from 'dompurify'
import { marked } from 'marked'
import markedKatex from 'marked-katex-extension'

marked.use(
  markedKatex({
    throwOnError: false,
    output: 'htmlAndMathml',
  }),
)

export function renderMarkdown(source: string): string {
  if (!source) return ''
  const rawHtml = marked.parse(source, { async: false }) as string
  return DOMPurify.sanitize(rawHtml, {
    ADD_TAGS: [
      'math',
      'semantics',
      'mrow',
      'mi',
      'mo',
      'mn',
      'msup',
      'msub',
      'msubsup',
      'mfrac',
      'mover',
      'munder',
      'munderover',
      'mtable',
      'mtr',
      'mtd',
      'annotation',
      'span',
      'svg',
      'path',
      'line',
    ],
    ADD_ATTR: [
      'xmlns',
      'display',
      'aria-hidden',
      'viewBox',
      'd',
      'fill',
      'stroke',
      'class',
      'style',
      'target',
      'rel',
    ],
  })
}
