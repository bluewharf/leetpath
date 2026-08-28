import assert from 'node:assert/strict'
import { describe, it } from 'node:test'

import {
  DraftSaveQueue,
  createGenerationGate,
  type DraftKey,
  type DraftSnapshot,
} from './problemDraftSession.ts'

const PYTHON_A: DraftKey = { slug: 'two-sum', language: 'python3', ioMode: 'acm' }
const CPP_A: DraftKey = { slug: 'two-sum', language: 'cpp', ioMode: 'acm' }
const PYTHON_B: DraftKey = { slug: 'three-sum', language: 'python3', ioMode: 'acm' }

describe('DraftSaveQueue', () => {
  it('flushes an immutable snapshot to the old language slot and keeps newer edits dirty', async () => {
    const queue = new DraftSaveQueue()
    queue.recordLoaded(PYTHON_A, 'initial')
    queue.edit(PYTHON_A, 'print("python")')

    let releaseSave!: () => void
    const saveStarted = new Promise<void>((resolve) => {
      releaseSave = resolve
    })
    const saved: DraftSnapshot[] = []
    const flushing = queue.flush(
      PYTHON_A,
      async (snapshot) => {
        saved.push(snapshot)
        await saveStarted
      },
      { maxAttempts: 1, timeoutMs: 200 },
    )

    queue.edit(PYTHON_A, 'print("newer")')
    queue.recordLoaded(CPP_A, '#include <iostream>')
    releaseSave()

    const result = await flushing
    assert.equal(result.status, 'saved')
    assert.deepEqual(saved, [{ ...PYTHON_A, code: 'print("python")', revision: 1 }])
    assert.equal(queue.isDirty(PYTHON_A), true)
    assert.equal(queue.snapshot(PYTHON_A)?.code, 'print("newer")')
    assert.equal(queue.isDirty(CPP_A), false)
  })

  it('stops after the configured retry limit and retains the dirty snapshot', async () => {
    const queue = new DraftSaveQueue()
    queue.edit(PYTHON_A, 'unsaved')
    let attempts = 0

    const result = await queue.flush(
      PYTHON_A,
      async () => {
        attempts += 1
        throw new Error('offline')
      },
      { maxAttempts: 2, timeoutMs: 200 },
    )

    assert.equal(result.status, 'failed')
    assert.equal(attempts, 2)
    assert.equal(queue.isDirty(PYTHON_A), true)
    assert.equal(queue.snapshot(PYTHON_A)?.code, 'unsaved')
  })

  it('times out a stuck save and ignores its late completion', async () => {
    const queue = new DraftSaveQueue()
    queue.edit(PYTHON_A, 'blocked')
    let releaseSave!: () => void
    const blocked = new Promise<void>((resolve) => {
      releaseSave = resolve
    })

    const result = await queue.flush(PYTHON_A, () => blocked, {
      maxAttempts: 3,
      timeoutMs: 20,
    })
    assert.equal(result.status, 'timeout')
    assert.equal(queue.isDirty(PYTHON_A), true)

    releaseSave()
    await blocked
    assert.equal(queue.isDirty(PYTHON_A), true)
  })

  it('serializes saves for one slot so a late old request cannot overwrite newer code', async () => {
    const queue = new DraftSaveQueue()
    let releaseOld!: () => void
    const oldBlocked = new Promise<void>((resolve) => {
      releaseOld = resolve
    })
    let serverCode = 'initial'
    const save = async (snapshot: DraftSnapshot) => {
      if (snapshot.revision === 1) await oldBlocked
      serverCode = snapshot.code
    }

    queue.edit(PYTHON_A, 'old')
    const first = await queue.flush(PYTHON_A, save, { maxAttempts: 1, timeoutMs: 20 })
    assert.equal(first.status, 'timeout')

    queue.edit(PYTHON_A, 'new')
    const second = queue.flush(PYTHON_A, save, { maxAttempts: 1, timeoutMs: 200 })
    releaseOld()

    assert.equal((await second).status, 'saved')
    assert.equal(serverCode, 'new')
    assert.equal(queue.isDirty(PYTHON_A), false)
  })

  it('prefers a failed local snapshot over an older server draft when returning to a slot', () => {
    const queue = new DraftSaveQueue()
    queue.edit(PYTHON_A, 'local unsaved')

    const restored = queue.recordLoaded(PYTHON_A, 'server old')

    assert.deepEqual(restored, { code: 'local unsaved', dirty: true })
    assert.equal(queue.snapshot(PYTHON_A)?.code, 'local unsaved')
  })

  it('keeps dirty snapshots isolated by slug', () => {
    const queue = new DraftSaveQueue()
    queue.edit(PYTHON_A, 'code A')
    queue.edit(PYTHON_B, 'code B')

    assert.equal(queue.snapshot(PYTHON_A)?.code, 'code A')
    assert.equal(queue.snapshot(PYTHON_B)?.code, 'code B')
  })
})

describe('generation gate', () => {
  it('invalidates older loads and polls when a newer transition starts', () => {
    const gate = createGenerationGate()
    const first = gate.next()
    assert.equal(gate.isCurrent(first), true)

    const second = gate.next()
    assert.equal(gate.isCurrent(first), false)
    assert.equal(gate.isCurrent(second), true)

    gate.invalidate()
    assert.equal(gate.isCurrent(second), false)
  })
})
