export type MemberRole = 'developer' | 'team_lead'

export interface Member {
  id: string
  name: string
  role: MemberRole
  avatar?: string
}

export interface CustomMetric {
  name: string
  value: number
  unit?: string
}

export interface KPIEntry {
  id: string
  memberId: string
  period: string // "2024-01" or "Sprint 1"
  periodType: 'monthly' | 'sprint'
  tasksCompleted: number
  storyPoints: number
  bugsFixed: number
  prReviews: number
  codeQuality: number // 0-100
  customMetrics: CustomMetric[]
  notes?: string
  createdAt: string
}

export interface TeamStats {
  totalTasks: number
  totalStoryPoints: number
  totalBugsFixed: number
  avgCodeQuality: number
  totalPRReviews: number
}
