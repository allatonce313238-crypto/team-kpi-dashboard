import { User, Crown } from 'lucide-react'
import type { Member, KPIEntry } from '../types'

interface MemberCardProps {
  member: Member
  entries: KPIEntry[]
  onClick: () => void
}

function getInitials(name: string) {
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
}

function getLatestEntry(entries: KPIEntry[]) {
  return entries.sort((a, b) => b.period.localeCompare(a.period))[0]
}

const AVATAR_COLORS = [
  'bg-blue-500', 'bg-purple-500', 'bg-green-500',
  'bg-orange-500', 'bg-pink-500', 'bg-teal-500',
]

export default function MemberCard({ member, entries, onClick }: MemberCardProps) {
  const latest = getLatestEntry(entries)
  const colorIdx = member.name.charCodeAt(0) % AVATAR_COLORS.length

  return (
    <div
      onClick={onClick}
      className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 cursor-pointer hover:shadow-md hover:border-blue-200 transition-all group"
    >
      <div className="flex items-center gap-3 mb-4">
        <div className={`${AVATAR_COLORS[colorIdx]} w-11 h-11 rounded-full flex items-center justify-center text-white font-bold text-sm flex-shrink-0`}>
          {getInitials(member.name)}
        </div>
        <div className="min-w-0">
          <p className="font-semibold text-gray-800 truncate">{member.name}</p>
          <div className="flex items-center gap-1">
            {member.role === 'team_lead'
              ? <Crown size={12} className="text-amber-500" />
              : <User size={12} className="text-gray-400" />}
            <p className="text-xs text-gray-500 capitalize">
              {member.role === 'team_lead' ? 'Team Lead' : 'Developer'}
            </p>
          </div>
        </div>
      </div>

      {latest ? (
        <div className="grid grid-cols-2 gap-2">
          <div className="bg-blue-50 rounded-xl p-3">
            <p className="text-xs text-blue-600 font-medium">Tasks</p>
            <p className="text-xl font-bold text-blue-700">{latest.tasksCompleted}</p>
          </div>
          <div className="bg-purple-50 rounded-xl p-3">
            <p className="text-xs text-purple-600 font-medium">Points</p>
            <p className="text-xl font-bold text-purple-700">{latest.storyPoints}</p>
          </div>
          <div className="bg-red-50 rounded-xl p-3">
            <p className="text-xs text-red-600 font-medium">Bugs Fixed</p>
            <p className="text-xl font-bold text-red-700">{latest.bugsFixed}</p>
          </div>
          <div className="bg-green-50 rounded-xl p-3">
            <p className="text-xs text-green-600 font-medium">Quality</p>
            <p className="text-xl font-bold text-green-700">{latest.codeQuality}%</p>
          </div>
        </div>
      ) : (
        <div className="bg-gray-50 rounded-xl p-4 text-center">
          <p className="text-sm text-gray-400">No KPI data yet</p>
          <p className="text-xs text-gray-300 mt-1">Click to add entry</p>
        </div>
      )}

      {latest && (
        <p className="text-xs text-gray-400 mt-3 text-right">
          Latest: {latest.period}
        </p>
      )}
    </div>
  )
}
