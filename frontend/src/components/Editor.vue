<template>
  <div ref="host" class="editor-wrap"></div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { EditorState, Compartment } from '@codemirror/state'
import { EditorView, basicSetup } from 'codemirror'
import { python } from '@codemirror/lang-python'
import { cpp } from '@codemirror/lang-cpp'
import { oneDark } from '@codemirror/theme-one-dark'
import { HighlightStyle, syntaxHighlighting } from '@codemirror/language'
import { tags } from '@lezer/highlight'
import { isDarkTheme } from '../theme'
import type { Language } from '../types'

const props = defineProps<{
  modelValue: string
  language: Language
  readonly?: boolean
}>()
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

const host = ref<HTMLElement>()
let view: EditorView | null = null

const langConf = new Compartment()
const themeConf = new Compartment()
// 跟随站点手动主题（<html data-theme>），而非系统偏好
const themeObserver = new MutationObserver(() => onThemeChange())

// 浅色/护眼主题的语法高亮：全部引用站点 CSS 变量，随主题联动
const lightHighlight = syntaxHighlighting(
  HighlightStyle.define([
    { tag: tags.keyword, color: 'var(--accent)' },
    { tag: [tags.string, tags.special(tags.string)], color: 'var(--green)' },
    { tag: [tags.number, tags.bool, tags.null], color: 'var(--amber)' },
    { tag: tags.comment, color: 'var(--text-faint)', fontStyle: 'italic' },
    { tag: [tags.function(tags.variableName), tags.function(tags.propertyName)], color: 'var(--purple)' },
    { tag: [tags.typeName, tags.className], color: 'var(--accent-2)' },
    { tag: [tags.operator, tags.punctuation], color: 'var(--text-dim)' },
    { tag: tags.propertyName, color: 'var(--purple)' },
  ]),
)

function langExt(lang: Language) {
  return lang === 'cpp' ? cpp() : python()
}

function themeExt() {
  return isDarkTheme() ? [oneDark, baseTheme()] : [baseTheme(), lightHighlight]
}

function baseTheme() {
  return EditorView.theme({
    '&': { backgroundColor: 'var(--surface)', color: 'var(--text)', fontSize: 'var(--font-editor)' },
    '.cm-content': { fontSize: 'var(--font-editor)' },
    '.cm-gutters': {
      backgroundColor: 'var(--surface)',
      color: 'var(--text-faint)',
      border: 'none',
      borderRight: '1px solid var(--border)',
    },
    '.cm-activeLine': { backgroundColor: 'var(--surface-2)' },
    '.cm-activeLineGutter': { backgroundColor: 'var(--surface-2)', color: 'var(--text-dim)' },
    '&.cm-focused': { outline: 'none' },
    '.cm-cursor': { borderLeftColor: 'var(--text)' },
    '.cm-selectionBackground, &.cm-focused .cm-selectionBackground': {
      backgroundColor: 'var(--accent-soft)',
    },
  })
}

function createView() {
  view = new EditorView({
    parent: host.value!,
    state: EditorState.create({
      doc: props.modelValue,
      extensions: [
        basicSetup,
        langConf.of(langExt(props.language)),
        themeConf.of(themeExt()),
        EditorView.updateListener.of((u) => {
          if (u.docChanged) emit('update:modelValue', u.state.doc.toString())
        }),
        EditorState.readOnly.of(props.readonly ?? false),
        EditorView.lineWrapping,
      ],
    }),
  })
}

function onThemeChange() {
  view?.dispatch({
    effects: themeConf.reconfigure(themeExt()),
  })
}

onMounted(() => {
  createView()
  themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme', 'data-font-size'] })
})

onBeforeUnmount(() => {
  themeObserver.disconnect()
  view?.destroy()
  view = null
})

watch(
  () => props.language,
  (lang) => {
    view?.dispatch({ effects: langConf.reconfigure(langExt(lang)) })
  },
)

watch(
  () => props.modelValue,
  (val) => {
    if (view && val !== view.state.doc.toString()) {
      view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: val } })
    }
  },
)
</script>
