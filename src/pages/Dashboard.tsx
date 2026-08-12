import { useState, useMemo } from 'react'
import { CheckSquare, Zap, Bug, Star, Plus, Users, BarChart2 } from 'lucide-react'
import { useMembers } from '../hooks/useMembers'
import { useKPIEntries } from '../hooks/useKPIEntries'
import StatCard from '../components/StatCard'
import MemberCard from '../components/MemberCard'
import MemberForm from '../components/MemberForm'
import KPIForm from '../components/KPIForm'
import MonthRangeFilter from '../components/MonthRangeFilter'
import type { Member } from '../types'

interface DashboardProps {
  onSelectMember: (member: Member) => void
  onNavigate: (page: 'overview') => void
}

export default function Dashboard({ onSelectMember, onNavigate }: DashboardProps) {
  const { members, loading: loadingMembers, error: membersError, saveMember } = useMembers()
  const { entries, loading: loadingEntries, addEntry } = useKPIEntries()
  const [showMemberForm, setShowMemberForm] = useState(false)
  const [showKPIForm, setShowKPIForm] = useState(false)
  const [fromMonth, setFromMonth] = useState('')
  const [toMonth, setToMonth] = useState('')

  const filteredEntries = useMemo(() => entries.filter(e => {
    if (fromMonth && e.period < fromMonth) return false
    if (toMonth && e.period > toMonth) return false
    return true
  }), [entries, fromMonth, toMonth])

  const teamStats = useMemo(() => ({
    totalTasks: filteredEntries.reduce((s, e) => s + e.tasksCompleted, 0),
    totalStoryPoints: filteredEntries.reduce((s, e) => s + e.storyPoints, 0),
    totalBugs: filteredEntries.reduce((s, e) => s + e.bugsFixed, 0),
    avgQuality: filteredEntries.length
      ? Math.round(filteredEntries.reduce((s, e) => s + e.codeQuality, 0) / filteredEntries.length)
      : 0,
  }), [filteredEntries])

  const loading = loadingMembers || loadingEntries
  const isFiltered = !!(fromMonth || toMonth)

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-100 px-6 py-4">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <div className="bg-blue-500 rounded-xl p-2">
                <BarChart2 size={22} className="text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-800">Team KPI Dashboard</h1>
                <p className="text-xs text-gray-400">{members.length} members</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {/* Nav Tabs */}
              <div className="flex gap-1 bg-gray-100 rounded-xl p-1 mr-2">
                <button className="px-4 py-1.5 rounded-lg text-sm font-medium bg-white text-gray-800 shadow-sm">
                  Team
                </button>
                <button
                  onClick={() => onNavigate('overview')}
                  className="px-4 py-1.5 rounded-lg text-sm font-medium text-gray-500 hover:text-gray-700 transition-colors"
                >
                  Overview
                </button>
              </div>
              <button
                onClick={() => setShowKPIForm(true)}
                className="flex items-center gap-2 bg-blue-500 hover:bg-blue-600 text-white rounded-xl px-4 py-2 text-sm font-medium transition-colors"
              >
                <Plus size={16} /> Add KPI
              </button>
              <button
                onClick={() => setShowMemberForm(true)}
                className="flex items-center gap-2 border border-gray-200 hover:bg-gray-50 text-gray-700 rounded-xl px-4 py-2 text-sm font-medium transition-colors"
              >
                <Users size={16} /> Add Member
              </button>
            </div>
          </div>

          {/* Filter */}
          <MonthRangeFilter
            fromMonth={fromMonth}
            toMonth={toMonth}
            onChange={(f, t) => { setFromMonth(f); setToMonth(t) }}
          />
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-6">
        {/* Team Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <StatCard
            label="Total Tasks"
            value={teamStats.totalTasks}
            icon={<CheckSquare size={20} />}
            color="text-blue-500"
            sub={isFiltered ? 'ช่วงที่เลือก' : 'ทั้งหมด'}
          />
          <StatCard
            label="Story Points"
            value={teamStats.totalStoryPoints}
            icon={<Zap size={20} />}
            color="text-purple-500"
            sub="Velocity"
          />
          <StatCard
            label="Bugs Fixed"
            value={teamStats.totalBugs}
            icon={<Bug size={20} />}
            color="text-red-500"
            sub={isFiltered ? 'ช่วงที่เลือก' : 'ทั้งหมด'}
          />
          <StatCard
            label="Avg Quality"
            value={`${teamStats.avgQuality}%`}
            icon={<Star size={20} />}
            color="text-green-500"
            sub="Code quality"
          />
        </div>

        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Team Members</h2>
          {isFiltered && (
            <span className="text-xs text-gray-400">
              แสดง KPI ล่าสุดในช่วง {fromMonth || '…'} — {toMonth || '…'}
            </span>
          )}
        </div>

        {membersError && (
          <div className="bg-red-50 border border-red-200 rounded-xl px-4 py-3 text-sm text-red-700 mb-4">
            Error loading members. Check browser console (F12) for details.
          </div>
        )}

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="bg-white rounded-2xl h-48 animate-pulse border border-gray-100" />
            ))}
          </div>
        ) : members.length === 0 ? (
          <div className="bg-white rounded-2xl border border-dashed border-gray-200 p-12 text-center">
            <Users size={40} className="text-gray-300 mx-auto mb-3" />
            <p className="text-gray-500 font-medium">No team members yet</p>
            <p className="text-sm text-gray-400 mt-1">Click "Add Member" to get started</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {members.map(member => (
              <MemberCard
                key={member.id}
                member={member}
                entries={filteredEntries.filter(e => e.memberId === member.id)}
                onClick={() => onSelectMember(member)}
              />
            ))}
          </div>
        )}
      </div>

      {showMemberForm && (
        <MemberForm onSubmit={saveMember} onClose={() => setShowMemberForm(false)} />
      )}
      {showKPIForm && (
        <KPIForm members={members} onSubmit={addEntry} onClose={() => setShowKPIForm(false)} />
      )}
    </div>
  )
}
