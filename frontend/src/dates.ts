/** 本地日历日 YYYY-MM-DD，避免 toISOString() 在东八区错一天。 */

export function formatLocalDate(d: Date): string {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

export function todayLocalDate(): string {
  return formatLocalDate(new Date())
}

export function parseLocalDate(iso: string): Date {
  const [y, m, d] = iso.split('-').map(Number)
  return new Date(y || 1970, (m || 1) - 1, d || 1)
}

export function addDays(iso: string, n: number): string {
  const d = parseLocalDate(iso)
  d.setDate(d.getDate() + n)
  return formatLocalDate(d)
}

export function formatZhDate(iso: string): string {
  const [y, m, d] = iso.split('-')
  if (!y || !m || !d) return iso
  return `${Number(y)}年${Number(m)}月${Number(d)}日`
}

export function formatZhMd(iso: string): string {
  const parts = iso.split('-')
  const m = parts[1]
  const d = parts[2]
  if (!m || !d) return iso
  return `${Number(m)}月${Number(d)}日`
}
