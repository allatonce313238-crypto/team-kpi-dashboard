import { useState } from 'react'
import { X } from 'lucide-react'
import type { Member } from '../types'

interface MemberFormProps {
  initialData?: Member
  onSubmit: (data: Omit<Member, 'id'> & { id?: string }) => Promise<void>
  onClose: () => void
}

export default function MemberForm({ initialData, onSubmit, onClose }: MemberFormProps) {
  const [name, setName] = useState(initialData?.name ?? '')
  const [role, setRole] = useState<Member['role']>(initialData?.role ?? 'developer')
  const [saving, setSaving] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim()) return
    setSaving(true)
    try {
      await onSubmit({ name: name.trim(), role, ...(initialData?.id ? { id: initialData.id } : {}) })
      onClose()
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-sm">
        <div className="flex items-center justify-between p-6 border-b border-gray-100">
          <h2 className="text-lg font-bold text-gray-800">
            {initialData ? 'Edit Member' : 'Add Member'}
          </h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
            <input
              required
              type="text"
              value={name}
              onChange={e => setName(e.target.value)}
              placeholder="e.g. John Smith"
              className="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
            <div className="grid grid-cols-2 gap-2">
              {(['developer', 'team_lead'] as const).map(r => (
                <button
                  key={r}
                  type="button"
                  onClick={() => setRole(r)}
                  className={`py-2.5 rounded-xl text-sm font-medium border transition-colors ${
                    role === r
                      ? 'bg-blue-500 text-white border-blue-500'
                      : 'bg-white text-gray-600 border-gray-200 hover:border-blue-300'
                  }`}
                >
                  {r === 'team_lead' ? 'Team Lead' : 'Developer'}
                </button>
              ))}
            </div>
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
              className="flex-1 bg-blue-500 hover:bg-blue-600 disabled:opacity-60 rounded-xl py-2.5 text-sm font-medium text-white"
            >
              {saving ? 'Saving...' : initialData ? 'Update' : 'Add Member'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
