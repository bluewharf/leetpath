/** 悬浮窗 / 抽屉共用：粘贴文字与截图。 */

export type AiContentPart =
  | { type: 'text'; text: string }
  | { type: 'image_url'; image_url: { url: string } }

const MAX_IMAGES = 4
const MAX_EDGE = 1280
const JPEG_QUALITY = 0.82

export function insertAtCursor(
  el: HTMLTextAreaElement | null,
  current: string,
  insert: string,
): { next: string; caret: number } {
  const start = el?.selectionStart ?? current.length
  const end = el?.selectionEnd ?? start
  return {
    next: current.slice(0, start) + insert + current.slice(end),
    caret: start + insert.length,
  }
}

async function drawToJpeg(source: CanvasImageSource, width: number, height: number): Promise<string> {
  const scale = Math.min(1, MAX_EDGE / Math.max(width, height))
  const w = Math.max(1, Math.round(width * scale))
  const h = Math.max(1, Math.round(height * scale))
  const canvas = document.createElement('canvas')
  canvas.width = w
  canvas.height = h
  const ctx = canvas.getContext('2d')
  if (!ctx) throw new Error('无法处理图片')
  ctx.drawImage(source, 0, 0, w, h)
  return canvas.toDataURL('image/jpeg', JPEG_QUALITY)
}

export async function compressImageFile(file: File): Promise<string> {
  try {
    const bitmap = await createImageBitmap(file)
    const url = await drawToJpeg(bitmap, bitmap.width, bitmap.height)
    bitmap.close()
    return url
  } catch {
    const objectUrl = URL.createObjectURL(file)
    try {
      const img = await new Promise<HTMLImageElement>((resolve, reject) => {
        const el = new Image()
        el.onload = () => resolve(el)
        el.onerror = () => reject(new Error('图片读取失败'))
        el.src = objectUrl
      })
      return await drawToJpeg(img, img.naturalWidth || img.width, img.naturalHeight || img.height)
    } finally {
      URL.revokeObjectURL(objectUrl)
    }
  }
}

function collectImageFiles(dt: DataTransfer): File[] {
  const seen = new Set<File>()
  const out: File[] = []
  const add = (file: File | null) => {
    if (!file || !file.type.startsWith('image/') || seen.has(file)) return
    seen.add(file)
    out.push(file)
  }
  if (dt.items) {
    for (const item of Array.from(dt.items)) {
      if (item.kind === 'file' && item.type.startsWith('image/')) add(item.getAsFile())
    }
  }
  if (dt.files) {
    for (const file of Array.from(dt.files)) add(file)
  }
  return out
}

export async function readClipboard(dt: DataTransfer | null): Promise<{ text: string; images: string[] }> {
  if (!dt) return { text: '', images: [] }
  const text = dt.getData('text/plain') || ''
  const files = collectImageFiles(dt).slice(0, MAX_IMAGES)
  const images: string[] = []
  for (const file of files) {
    images.push(await compressImageFile(file))
  }
  return { text, images }
}

export async function compressPickedFiles(fileList: FileList | File[] | null): Promise<string[]> {
  if (!fileList) return []
  const files = Array.from(fileList)
    .filter((f) => f.type.startsWith('image/'))
    .slice(0, MAX_IMAGES)
  const images: string[] = []
  for (const file of files) images.push(await compressImageFile(file))
  return images
}

export function toApiContent(text: string, images: string[]): string | AiContentPart[] {
  const trimmed = text.trim()
  if (!images.length) return trimmed
  const parts: AiContentPart[] = images.map((url) => ({ type: 'image_url', image_url: { url } }))
  if (trimmed) parts.push({ type: 'text', text: trimmed })
  return parts
}

export function messageText(content: string | AiContentPart[]): string {
  if (typeof content === 'string') return content
  return content
    .filter((p): p is { type: 'text'; text: string } => p.type === 'text')
    .map((p) => p.text)
    .join('\n')
}
