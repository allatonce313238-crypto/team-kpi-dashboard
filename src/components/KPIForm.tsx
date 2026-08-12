import { useState } from 'react'
import { X, Plus, Trash2 } from 'lucide-react'
import type { KPIEntry, Member } from '../types'

interface KPIFormProps {
  members: Member[]
  initialData?: KPIEntry
  defaultMemberId?: string
  onSubmit: (data: Omit<KPIEntry, 'id' | 'createdAt'>) => Promise<void>
  onClose: () => void
}

const empty: Omit<KPIEntry, 'id' | 'createdAt'> = {
  memberId: '',
  period: '',
  periodType: 'monthly',
  tasksCompleted: 0,
  storyPoints: 0,
  bugsFixed: 0,
  prReviews: 0,
  codeQuality: 80,
  customMetrics: [],
  notes: '',
}

export default function KPIForm({ members, initialData, defaultMemberId, onSubmit, onClose }: KPIFormProps) {
  const [form, setForm] = useState<Omit<KPIEntry, 'id' | 'createdAt'>>(() => ({
    ...empty,
    ...(initialData ? { ...initialData } : {}),
    memberId: initialData?.memberId ?? defaultMemberId ?? '',
  }))
  const [saving, setSaving] = useState(false)
  const [customName, setCustomName] = useState('')
  const [customValue, setCustomValue] = useState('')

  const set = <K extends keyof typeof form>(k: K, v: typeof form[K]) =>
    setForm(f => ({ ...f, [k]: v }))

  const addCustomMetric = () => {
    if (!customName.trim()) return
    set('customMetrics', [...form.customMetrics, { name: customName.trim(), value: Number(customValue) || 0 }])
    setCustomName('')
    setCustomValue('')
  }

  const removeCustomMetric = (i: number) =>
    set('customMetrics', form.customMetrics.filter((_, idx) => idx !== i))

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!form.memberId || !form.period) return
    setSaving(true)
    try {
      await onSubmit(form)
      onClose()
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-gray-100">
          <h2 className="text-lg font-bold text-gray-800">
            {initialData ? 'Edit KPI Entry' : 'Add KPI Entry'}
          </h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {/* Member */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Member</label>
            <select
              required
              value={form.memberId}
              onChange={e => set('memberId', e.target.value)}
              className="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
            >
              <option value="">Select member...</option>
              {members.map(m => (
                <option key={m.id} value={m.id}>{m.name}</option>
              ))}
            </select>
          </div>

          {/* Period */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Period Type</label>
              <select
                value={form.periodType}
                onChange={e => set('periodType', e.target.value as 'monthly' | 'sprint')}
                className="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
              >
                <option value="monthly">Monthly</option>
                <option value="sprint">Sprint</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {form.periodType === 'monthly' ? 'Month (YYYY-MM)' : 'Sprint'}
              </label>
              <input
                required
                type={form.periodType === 'monthly' ? 'month' : 'text'}
                placeholder={form.periodType === 'sprint' ? 'e.g. Sprint 12' : ''}
                value={form.period}
                onChange={e => set('period', e.target.value)}
                className="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
            </div>
          </div>

          {/* Core KPIs */}
          <div className="grid grid-cols-2 gap-3">
            {([
              ['tasksCompleted', 'Tasks Completed'],
              ['storyPoints', 'Story Points'],
              ['bugsFixed', 'Bugs Fixed'],
              ['prReviews', 'PR Reviews'],
            ] as const).map(([key, label]) => (
              <div key={key}>
                <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
                <input
                  type="number"
                  min={0}
                  value={form[key]}
                  onChange={e => set(key, Number(e.target.value))}
                  className="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
                />
              </div>
            ))}
          </div>

          {/* Code Quality */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Code Quality: <span className="text-blue-600 font-bold">{form.codeQuality}%</span>
            </label>
            <input
              type="range"
              min={0}
              max={100}
              value={form.codeQuality}
              onChange={e => set('codeQuality', Number(e.target.value))}
              className="w-full accent-blue-500"
            />
          </div>

          {/* Custom Metrics */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Custom Metrics</label>
            {form.customMetrics.map((m, i) => (
              <div key={i} className="flex items-center gap-2 mb-2">
                <span className="flex-1 bg-gray-50 rounded-lg px-3 py-1.5 text-sm text-gray-700">
                  {m.name}: <strong>{m.value}</strong>
                </span>
                <button type="button" onClick={() => removeCustomMetric(i)} className="text-red-400 hover:text-red-600">
                  <Trash2 size={14} />
                </button>
              </div>
            ))}
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Metric name"
                value={customName}
                onChange={e => setCustomName(e.target.value)}
                className="flex-1 border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
              <input
                type="number"
                placeholder="Value"
                value={customValue}
                onChange={e => setCustomValue(e.target.value)}
                className="w-24 border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
              <button
                type="button"
                onClick={addCustomMetric}
                className="bg-gray-100 hover:bg-gray-200 rounded-xl px-3 py-2 text-gray-600"
              >
                <Plus size={16} />
              </button>
            </div>
          </div>

          {/* Notes */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Notes (optional)</label>
            <textarea
              rows={2}
              value={form.notes}
              onChange={e => set('notes', e.target.value)}
              placeholder="Any additional notes..."
              className="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 resize-none"
            />
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 border border-gray-200 rounded-xl py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={saving}
              className="flex-1 bg-blue-500 hover:bg-blue-600 disabled:opacity-60 rounded-xl py-2.5 text-sm font-medium text-white transition-colors"
            >
              {saving ? 'Saving...' : initialData ? 'Update' : 'Add Entry'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
