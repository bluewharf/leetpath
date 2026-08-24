// 与后端契约对齐的类型定义

export type Language = 'python3' | 'cpp'
export type Difficulty = 'easy' | 'medium' | 'hard'
export type SubmissionStatus =
  | 'pending'
  | 'judging'
  | 'AC'
  | 'WA'
  | 'TLE'
  | 'MLE'
  | 'CE'
  | 'RE'
  | 'IE'

export interface User {
  id: number
  username: string
  email: string | null
  is_admin: boolean
}

export interface InviteSummary {
  id: number
  expires_at: string
  used_at: string | null
  revoked_at: string | null
  created_at: string
}

export interface InviteCreated extends InviteSummary {
  code: string
}

export interface ProblemListItem {
  id: number
  slug: string
  title: string
  difficulty: Difficulty
  source: 'hot100' | 'mianjing'
  tags: string[]
  my_status: 'solved' | 'attempted' | null
  has_solution: boolean
  memory: 'remembered' | 'unremembered' | null
}

export interface SampleTest {
  ordinal: number
  input: string
  expected_output: string
}

export interface ProblemDetail extends Omit<ProblemListItem, 'my_status'> {
  statement_md: string
  time_limit_ms: number
  memory_limit_mb: number
  samples: SampleTest[]
}

export interface TestResult {
  ordinal: number
  is_sample: boolean
  status: SubmissionStatus
  runtime_ms?: number | null
  input?: string
  expected?: string
  output?: string
  stderr?: string
}

export interface Submission {
  id: number
  problem_slug: string
  problem_title?: string
  language: Language
  code?: string
  status: SubmissionStatus
  runtime_ms: number | null
  compile_output: string | null
  detail: TestResult[] | null
  created_at: string
}

export interface Draft {
  code: string
  updated_at: string | null
  is_default?: boolean
}

export interface Job {
  id: number
  company: string
  position: string
  tier: 'big' | 'mid' | 'small'
  batch: string | null
  open_at: string | null
  deadline_at: string | null
  jd_text: string | null
  apply_url: string | null
  status: string
  days_left: number | null
  created_at?: string
}

export interface LinkItem {
  category: string
  title: string
  url: string
  note?: string
}

export const FINAL_STATUSES: SubmissionStatus[] = ['AC', 'WA', 'TLE', 'MLE', 'CE', 'RE', 'IE']

export function isFinal(s: SubmissionStatus): boolean {
  return FINAL_STATUSES.includes(s)
}
