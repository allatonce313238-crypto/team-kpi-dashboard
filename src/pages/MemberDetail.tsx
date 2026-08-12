import { useState } from 'react'
import { ArrowLeft, Plus, Edit2, Trash2, Crown, User } from 'lucide-react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, LineChart, Line, RadarChart, Radar,
  PolarGrid, PolarAngleAxis, PolarRadiusAxis,
} from 'recharts'
import { useKPIEntries } from '../hooks/useKPIEntries'
import { useMembers } from '../hooks/useMembers'
import KPIForm from '../components/KPIForm'
import type { Member, KPIEntry } from '../types'

interface MemberDetailProps {
  member: Member
  onBack: () => void
}

const AVATAR_COLORS = [
  'bg-blue-500', 'bg-purple-500', 'bg-green-500',
  'bg-orange-500', 'bg-pink-500', 'bg-teal-500',
]

function getInitials(name: string) {
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
}

export default function MemberDetail({ member, onBack }: MemberDetailProps) {
  const { members } = useMembers()
  const { entries, loading, addEntry, editEntry, removeEntry } = useKPIEntries(member.id)
  const [showForm, setShowForm] = useState(false)
  const [editingEntry, setEditingEntry] = useState<KPIEntry | undefined>()

  const sorted = [...entries].sort((a, b) => a.period.localeCompare(b.period))
  const colorIdx = member.name.charCodeAt(0) % AVATAR_COLORS.length

  const latest = sorted[sorted.length - 1]

  const radarData = latest
    ? [
        { subject: 'Tasks', value: Math.min(latest.tasksCompleted, 30) },
        { subject: 'Points', value: Math.min(latest.storyPoints, 50) },
        { subject: 'Bug Fix', value: Math.min(latest.bugsFixed * 5, 50) },
        { subject: 'PR Reviews', value: Math.min(latest.prReviews * 5, 50) },
        { subject: 'Quality', value: latest.codeQuality / 2 },
      ]
    : []

  const handleEdit = (entry: KPIEntry) => {
    setEditingEntry(entry)
    setShowForm(true)
  }

  const handleFormClose = () => {
    setShowForm(false)
    setEditingEntry(undefined)
  }

  const handleSubmit = async (data: Omit<KPIEntry, 'id' | 'createdAt'>) => {
    if (editingEntry) {
      await editEntry(editingEntry.id, data)
    } else {
      await addEntry(data)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-100 px-6 py-4">
        <div className="max-w-5xl mx-auto flex items-center gap-4">
          <button
            onClick={onBack}
            className="text-gray-400 hover:text-gray-700 flex items-center gap-1 text-sm"
          >
            <ArrowLeft size={18} /> Back
          </button>
          <div className="flex items-center gap-3 flex-1">
            <div className={`${AVATAR_COLORS[colorIdx]} w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm`}>
              {getInitials(member.name)}
            </div>
            <div>
              <h1 className="text-lg font-bold text-gray-800">{member.name}</h1>
              <div className="flex items-center gap-1">
                {member.role === 'team_lead'
                  ? <Crown size={12} className="text-amber-500" />
                  : <User size={12} className="text-gray-400" />}
                <p className="text-xs text-gray-500">
                  {member.role === 'team_lead' ? 'Team Lead' : 'Developer'}
                </p>
              </div>
            </div>
          </div>
          <button
            onClick={() => setShowForm(true)}
            className="flex items-center gap-2 bg-blue-500 hover:bg-blue-600 text-white rounded-xl px-4 py-2 text-sm font-medium"
          >
            <Plus size={16} /> Add Entry
          </button>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-6 py-6 space-y-6">
        {loading ? (
          <div className="text-center py-16 text-gray-400">Loading...</div>
        ) : entries.length === 0 ? (
          <div className="bg-white rounded-2xl border border-dashed border-gray-200 p-12 text-center">
            <p className="text-gray-500 font-medium">No KPI entries yet</p>
            <p className="text-sm text-gray-400 mt-1 mb-4">Add the first KPI entry for {member.name}</p>
            <button
              onClick={() => setShowForm(true)}
              className="bg-blue-500 hover:bg-blue-600 text-white rounded-xl px-5 py-2 text-sm font-medium"
            >
              Add First Entry
            </button>
          </div>
        ) : (
          <>
            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
              {/* Tasks & Points trend */}
              <div className="lg:col-span-2 bg-white rounded-2xl border border-gray-100 p-5">
                <h3 className="text-sm font-semibold text-gray-700 mb-4">Tasks & Story Points</h3>
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={sorted} barGap={4}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="period" tick={{ fontSize: 11 }} />
                    <YAxis tick={{ fontSize: 11 }} />
                    <Tooltip />
                    <Bar dataKey="tasksCompleted" name="Tasks" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="storyPoints" name="Story Points" fill="#a855f7" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Radar */}
              {radarData.length > 0 && (
                <div className="bg-white rounded-2xl border border-gray-100 p-5">
                  <h3 className="text-sm font-semibold text-gray-700 mb-4">Latest Performance</h3>
                  <ResponsiveContainer width="100%" height={200}>
                    <RadarChart data={radarData}>
                      <PolarGrid />
                      <PolarAngleAxis dataKey="subject" tick={{ fontSize: 10 }} />
                      <PolarRadiusAxis tick={false} />
                      <Radar dataKey="value" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.2} />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
              )}
            </div>

            {/* Code Quality trend */}
            <div className="bg-white rounded-2xl border border-gray-100 p-5">
              <h3 className="text-sm font-semibold text-gray-700 mb-4">Code Quality Trend</h3>
              <ResponsiveContainer width="100%" height={140}>
                <LineChart data={sorted}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="period" tick={{ fontSize: 11 }} />
                  <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
                  <Tooltip formatter={(v) => `${v}%`} />
                  <Line type="monotone" dataKey="codeQuality" name="Quality" stroke="#10b981" strokeWidth={2} dot={{ r: 4 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Entries Table */}
            <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden">
              <div className="px-5 py-4 border-b border-gray-50">
                <h3 className="text-sm font-semibold text-gray-700">KPI History</h3>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="bg-gray-50">
                      {['Period', 'Tasks', 'Story Pts', 'Bugs Fixed', 'PR Reviews', 'Quality', 'Notes', ''].map(h => (
                        <th key={h} className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide whitespace-nowrap">
                          {h}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {[...sorted].reverse().map(entry => (
                      <tr key={entry.id} className="hover:bg-gray-50 transition-colors">
                        <td className="px-4 py-3 font-medium text-gray-700">{entry.period}</td>
                        <td className="px-4 py-3 text-blue-600 font-semibold">{entry.tasksCompleted}</td>
                        <td className="px-4 py-3 text-purple-600 font-semibold">{entry.storyPoints}</td>
                        <td className="px-4 py-3 text-red-600 font-semibold">{entry.bugsFixed}</td>
                        <td className="px-4 py-3 text-gray-600">{entry.prReviews}</td>
                        <td className="px-4 py-3">
                          <span className={`font-semibold ${entry.codeQuality >= 80 ? 'text-green-600' : entry.codeQuality >= 60 ? 'text-yellow-600' : 'text-red-600'}`}>
                            {entry.codeQuality}%
                          </span>
                        </td>
                        <td className="px-4 py-3 text-gray-400 max-w-[140px] truncate">{entry.notes || '—'}</td>
                        <td className="px-4 py-3">
                          <div className="flex gap-2">
                            <button
                              onClick={() => handleEdit(entry)}
                              className="text-gray-400 hover:text-blue-500"
                            >
                              <Edit2 size={14} />
                            </button>
                            <button
                              onClick={() => removeEntry(entry.id)}
                              className="text-gray-400 hover:text-red-500"
                            >
                              <Trash2 size={14} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </div>

      {showForm && (
        <KPIForm
          members={members}
          initialData={editingEntry}
          defaultMemberId={member.id}
          onSubmit={handleSubmit}
          onClose={handleFormClose}
        />
      )}
    </div>
  )
}
