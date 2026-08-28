import type { IoMode, Language } from './types.ts'

export interface DraftKey {
  slug: string
  language: Language
  ioMode: IoMode
}

export interface DraftSnapshot extends DraftKey {
  code: string
  revision: number
}

export interface FlushOptions {
  maxAttempts?: number
  timeoutMs?: number
}

export type FlushResult =
  | { status: 'clean' }
  | { status: 'saved'; snapshot: DraftSnapshot }
  | { status: 'failed'; snapshot: DraftSnapshot; error: unknown }
  | { status: 'timeout'; snapshot: DraftSnapshot }

interface DraftEntry {
  key: DraftKey
  code: string
  revision: number
  savedRevision: number
}

const DEFAULT_MAX_ATTEMPTS = 2
const DEFAULT_TIMEOUT_MS = 1500

function keyId(key: DraftKey): string {
  return `${key.slug}\u0000${key.language}\u0000${key.ioMode}`
}

class FlushTimeoutError extends Error {}

async function withinDeadline<T>(operation: Promise<T>, timeoutMs: number): Promise<T> {
  let timer: ReturnType<typeof setTimeout> | null = null
  try {
    return await Promise.race([
      operation,
      new Promise<never>((_resolve, reject) => {
        timer = setTimeout(() => reject(new FlushTimeoutError('draft flush timed out')), timeoutMs)
      }),
    ])
  } finally {
    if (timer) clearTimeout(timer)
  }
}

/**
 * Tracks unsaved revisions per draft slot. A failed transition keeps its old
 * slot dirty, so a later flush can retry it without writing into the new slot.
 */
export class DraftSaveQueue {
  private entries = new Map<string, DraftEntry>()
  private saveTails = new Map<string, Promise<void>>()
  private pendingSaves = new Map<string, Promise<void>>()

  recordLoaded(key: DraftKey, serverCode: string): { code: string; dirty: boolean } {
    const id = keyId(key)
    const existing = this.entries.get(id)
    if (existing && existing.revision !== existing.savedRevision) {
      return { code: existing.code, dirty: true }
    }
    const revision = existing?.revision ?? 0
    this.entries.set(id, {
      key: { ...key },
      code: serverCode,
      revision,
      savedRevision: revision,
    })
    return { code: serverCode, dirty: false }
  }

  edit(key: DraftKey, code: string): void {
    const id = keyId(key)
    const existing = this.entries.get(id)
    this.entries.set(id, {
      key: { ...key },
      code,
      revision: (existing?.revision ?? 0) + 1,
      savedRevision: existing?.savedRevision ?? 0,
    })
  }

  isDirty(key: DraftKey): boolean {
    const entry = this.entries.get(keyId(key))
    return Boolean(entry && entry.revision !== entry.savedRevision)
  }

  snapshot(key: DraftKey): DraftSnapshot | null {
    const entry = this.entries.get(keyId(key))
    if (!entry || entry.revision === entry.savedRevision) return null
    return {
      ...entry.key,
      code: entry.code,
      revision: entry.revision,
    }
  }

  dirtyKeys(): DraftKey[] {
    return [...this.entries.values()]
      .filter((entry) => entry.revision !== entry.savedRevision)
      .map((entry) => ({ ...entry.key }))
  }

  private saveSerially(
    snapshot: DraftSnapshot,
    save: (snapshot: DraftSnapshot) => Promise<void>,
  ): Promise<void> {
    const id = keyId(snapshot)
    const pendingId = `${id}\u0000${snapshot.revision}`
    const existing = this.pendingSaves.get(pendingId)
    if (existing) return existing

    const previous = this.saveTails.get(id) ?? Promise.resolve()
    const operation = previous.catch(() => undefined).then(() => save(snapshot))
    this.pendingSaves.set(pendingId, operation)
    this.saveTails.set(id, operation)
    const cleanup = () => {
      if (this.pendingSaves.get(pendingId) === operation) {
        this.pendingSaves.delete(pendingId)
      }
      if (this.saveTails.get(id) === operation) {
        this.saveTails.delete(id)
      }
    }
    void operation.then(cleanup, cleanup)
    return operation
  }

  async flush(
    key: DraftKey,
    save: (snapshot: DraftSnapshot) => Promise<void>,
    options: FlushOptions = {},
  ): Promise<FlushResult> {
    const snapshot = this.snapshot(key)
    if (!snapshot) return { status: 'clean' }

    const maxAttempts = Math.max(1, Math.trunc(options.maxAttempts ?? DEFAULT_MAX_ATTEMPTS))
    const timeoutMs = Math.max(1, Math.trunc(options.timeoutMs ?? DEFAULT_TIMEOUT_MS))
    const deadline = Date.now() + timeoutMs
    let lastError: unknown = new Error('draft flush failed')

    for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
      const remaining = deadline - Date.now()
      if (remaining <= 0) return { status: 'timeout', snapshot }
      try {
        await withinDeadline(this.saveSerially(snapshot, save), remaining)
        const current = this.entries.get(keyId(key))
        if (current) {
          current.savedRevision = Math.max(current.savedRevision, snapshot.revision)
        }
        return { status: 'saved', snapshot }
      } catch (error) {
        if (error instanceof FlushTimeoutError) {
          return { status: 'timeout', snapshot }
        }
        lastError = error
      }
    }
    return { status: 'failed', snapshot, error: lastError }
  }

  async flushAll(
    save: (snapshot: DraftSnapshot) => Promise<void>,
    options: FlushOptions = {},
  ): Promise<FlushResult[]> {
    return Promise.all(this.dirtyKeys().map((key) => this.flush(key, save, options)))
  }
}

export interface GenerationGate {
  next(): number
  invalidate(): void
  isCurrent(generation: number): boolean
}

export function createGenerationGate(): GenerationGate {
  let current = 0
  return {
    next() {
      current += 1
      return current
    },
    invalidate() {
      current += 1
    },
    isCurrent(generation: number) {
      return generation === current
    },
  }
}
