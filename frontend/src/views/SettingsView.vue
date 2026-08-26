<template>
  <div class="container settings-page">
    <div class="page-head">
      <div>
        <div class="kicker">Account</div>
        <h1 class="display">账号设置</h1>
        <p class="muted">修改密码、上传自定义头像。头像会出现在顶栏和排行榜。</p>
      </div>
    </div>

    <div class="settings-grid">
      <section class="card settings-card">
        <h2>头像</h2>
        <div class="avatar-editor">
          <UserAvatar :username="auth.me?.username || ''" :avatar-url="auth.me?.avatar_url" size="md" />
          <div class="avatar-editor-copy">
            <p>支持 JPG / PNG / WebP / GIF，最大 1.5MB。上传后会裁成正方形。</p>
            <div class="settings-actions">
              <label class="btn btn-primary btn-sm">
                {{ avatarBusy ? '上传中…' : '选择图片' }}
                <input
                  type="file"
                  accept="image/jpeg,image/png,image/webp,image/gif"
                  hidden
                  :disabled="avatarBusy"
                  @change="onPickAvatar"
                />
              </label>
              <button
                v-if="auth.me?.avatar_url"
                class="btn btn-sm"
                type="button"
                :disabled="avatarBusy"
                @click="onRemoveAvatar"
              >
                恢复默认
              </button>
            </div>
            <p v-if="avatarError" class="form-err">{{ avatarError }}</p>
          </div>
        </div>
      </section>

      <section class="card settings-card">
        <h2>修改密码</h2>
        <form class="settings-form" @submit.prevent="onChangePassword">
          <div class="form-group">
            <label>当前密码</label>
            <input v-model="oldPassword" class="input" type="password" autocomplete="current-password" required />
          </div>
          <div class="form-group">
            <label>新密码（至少 8 位）</label>
            <input
              v-model="newPassword"
              class="input"
              type="password"
              autocomplete="new-password"
              required
              minlength="8"
            />
          </div>
          <div class="form-group">
            <label>确认新密码</label>
            <input
              v-model="confirmPassword"
              class="input"
              type="password"
              autocomplete="new-password"
              required
              minlength="8"
            />
          </div>
          <p v-if="passwordError" class="form-err">{{ passwordError }}</p>
          <button class="btn btn-primary" type="submit" :disabled="passwordBusy">
            {{ passwordBusy ? '保存中…' : '更新密码' }}
          </button>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import UserAvatar from '../components/UserAvatar.vue'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../stores/toast'

const auth = useAuthStore()
const toast = useToast()

const avatarBusy = ref(false)
const avatarError = ref('')
const passwordBusy = ref(false)
const passwordError = ref('')
const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

async function onPickAvatar(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  input.value = ''
  if (!file) return
  avatarError.value = ''
  if (file.size > 1.5 * 1024 * 1024) {
    avatarError.value = '图片不能超过 1.5MB'
    return
  }
  avatarBusy.value = true
  try {
    await auth.uploadAvatar(file)
    toast.success('头像已更新')
  } catch (err) {
    avatarError.value = err instanceof Error ? err.message : '上传失败'
  } finally {
    avatarBusy.value = false
  }
}

async function onRemoveAvatar() {
  avatarBusy.value = true
  avatarError.value = ''
  try {
    await auth.deleteAvatar()
    toast.success('已恢复默认头像')
  } catch (err) {
    avatarError.value = err instanceof Error ? err.message : '操作失败'
  } finally {
    avatarBusy.value = false
  }
}

async function onChangePassword() {
  passwordError.value = ''
  if (newPassword.value !== confirmPassword.value) {
    passwordError.value = '两次输入的新密码不一致'
    return
  }
  if (newPassword.value.length < 8) {
    passwordError.value = '新密码至少 8 位'
    return
  }
  passwordBusy.value = true
  try {
    await auth.changePassword(oldPassword.value, newPassword.value)
    oldPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
    toast.success('密码已更新')
  } catch (err) {
    passwordError.value = err instanceof Error ? err.message : '修改失败'
  } finally {
    passwordBusy.value = false
  }
}
</script>
