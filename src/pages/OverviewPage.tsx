import { useMemo, useState } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  LineChart, Line, ResponsiveContainer,
} from 'recharts'
import { BarChart2, CheckSquare, Zap, Bug, Star, GitPullRequest, Crown, User } from 'lucide-react'
import { useMembers } from '../hooks/useMembers'
import { useKPIEntries } from '../hooks/useKPIEntries'
import MonthRangeFilter from '../components/MonthRangeFilter'

// ─── Palette (consistent with rest of app) ───────────────
const COLOR = {
  tasks:   '#3b82f6', // blue-500
  points:  '#a855f7', // purple-500
  bugs:    '#ef4444', // red-500
  quality: '#10b981', // emerald-500
  prs:     '#f97316', // orange-500
}

interface OverviewPageProps {
  onNavigate: (page: 'team') => void
}

function shortName(name: string) {
  const parts = name.split(' ')
  return parts.length > 1 ? parts[0] : name
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null
  return (
    <div className="bg-white border border-gray-100 rounded-xl shadow-md px-3 py-2 text-xs">
      <p className="font-semibold text-gray-700 mb-1">{label}</p>
      {payload.map((p: any) => (
        <div key={p.dataKey} className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full inline-block" style={{ background: p.color }} />
          <span className="text-gray-500">{p.name}:</span>
          <span className="font-medium text-gray-800">
            {p.dataKey === 'quality' ? `${p.value}%` : p.value}
          </span>
        </div>
      ))}
    </div>
  )
}

export default function OverviewPage({ onNavigate }: OverviewPageProps) {
  const { members, loading: loadingMembers } = useMembers()
  const { entries, loading: loadingEntries } = useKPIEntries()
  const [fromMonth, setFromMonth] = useState('')
  const [toMonth, setToMonth] = useState('')

  const filteredEntries = useMemo(() => entries.filter(e => {
    if (fromMonth && e.period < fromMonth) return false
    if (toMonth && e.period > toMonth) return false
    return true
  }), [entries, fromMonth, toMonth])

  // ─── Summary Stats ────────────────────────────────────
  const stats = useMemo(() => ({
    totalTasks:  filteredEntries.reduce((s, e) => s + e.tasksCompleted, 0),
    totalPoints: filteredEntries.reduce((s, e) => s + e.storyPoints, 0),
    totalBugs:   filteredEntries.reduce((s, e) => s + e.bugsFixed, 0),
    totalPRs:    filteredEntries.reduce((s, e) => s + e.prReviews, 0),
    avgQuality:  filteredEntries.length
      ? Math.round(filteredEntries.reduce((s, e) => s + e.codeQuality, 0) / filteredEntries.length)
      : 0,
  }), [filteredEntries])

  // ─── Monthly Trend ────────────────────────────────────
  const monthlyData = useMemo(() => {
    const periods = [...new Set(filteredEntries.map(e => e.period))].sort()
    return periods.map(period => {
      const pe = filteredEntries.filter(e => e.period === period)
      return {
        period,
        tasks:   pe.reduce((s, e) => s + e.tasksCompleted, 0),
        points:  pe.reduce((s, e) => s + e.storyPoints, 0),
        bugs:    pe.reduce((s, e) => s + e.bugsFixed, 0),
        quality: pe.length ? Math.round(pe.reduce((s, e) => s + e.codeQuality, 0) / pe.length) : 0,
        prs:     pe.reduce((s, e) => s + e.prReviews, 0),
      }
    })
  }, [filteredEntries])

  // ─── Member Comparison ────────────────────────────────
  const memberData = useMemo(() =>
    members.map(m => {
      const me = filteredEntries.filter(e => e.memberId === m.id)
      return {
        name:    shortName(m.name),
        fullName: m.name,
        role:    m.role,
        tasks:   me.reduce((s, e) => s + e.tasksCompleted, 0),
        points:  me.reduce((s, e) => s + e.storyPoints, 0),
        bugs:    me.reduce((s, e) => s + e.bugsFixed, 0),
        quality: me.length ? Math.round(me.reduce((s, e) => s + e.codeQuality, 0) / me.length) : 0,
        prs:     me.reduce((s, e) => s + e.prReviews, 0),
        periods: me.length,
      }
    }).sort((a, b) => b.tasks - a.tasks),
  [members, filteredEntries])

  const loading = loadingMembers || loadingEntries

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-400 text-sm">Loading...</div>
      </div>
    )
  }

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
            {/* Nav Tabs */}
            <div className="flex gap-1 bg-gray-100 rounded-xl p-1">
              <button
                onClick={() => onNavigate('team')}
                className="px-4 py-1.5 rounded-lg text-sm font-medium text-gray-500 hover:text-gray-700 transition-colors"
              >
                Team
              </button>
              <button className="px-4 py-1.5 rounded-lg text-sm font-medium bg-white text-gray-800 shadow-sm">
                Overview
              </button>
            </div>
          </div>
          <MonthRangeFilter
            fromMonth={fromMonth}
            toMonth={toMonth}
            onChange={(f, t) => { setFromMonth(f); setToMonth(t) }}
          />
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-6 space-y-6">

        {/* ─── Summary Stat Tiles ─────────────────────────── */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {[
            { label: 'Tasks Done',     value: stats.totalTasks,          icon: <CheckSquare size={18}/>, color: 'text-blue-500',   bg: 'bg-blue-50'   },
            { label: 'Story Points',   value: stats.totalPoints,         icon: <Zap size={18}/>,        color: 'text-purple-500', bg: 'bg-purple-50' },
            { label: 'Bugs Fixed',     value: stats.totalBugs,           icon: <Bug size={18}/>,        color: 'text-red-500',    bg: 'bg-red-50'    },
            { label: 'PR Reviews',     value: stats.totalPRs,            icon: <GitPullRequest size={18}/>, color: 'text-orange-500', bg: 'bg-orange-50' },
            { label: 'Avg Quality',    value: `${stats.avgQuality}%`,    icon: <Star size={18}/>,       color: 'text-green-500',  bg: 'bg-green-50'  },
          ].map(s => (
            <div key={s.label} className={`${s.bg} rounded-2xl p-4 flex items-center gap-3`}>
              <span className={s.color}>{s.icon}</span>
              <div>
                <p className="text-xs text-gray-500 font-medium">{s.label}</p>
                <p className="text-xl font-bold text-gray-800">{s.value}</p>
              </div>
            </div>
          ))}
        </div>

        {/* ─── Monthly Trend + Quality ────────────────────── */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">

          {/* Tasks & Story Points per Month */}
          <div className="lg:col-span-2 bg-white rounded-2xl border border-gray-100 p-5">
            <p className="text-sm font-semibold text-gray-700 mb-4">Velocity รายเดือน (Tasks + Story Points)</p>
            {monthlyData.length === 0 ? (
              <div className="h-48 flex items-center justify-center text-gray-300 text-sm">ไม่มีข้อมูลในช่วงนี้</div>
            ) : (
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={monthlyData} barCategoryGap="30%">
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
                  <XAxis dataKey="period" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fontSize: 11 }} axisLine={false} tickLine={false} />
                  <Tooltip content={<CustomTooltip />} cursor={{ fill: '#f9fafb' }} />
                  <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize: 12 }} />
                  <Bar dataKey="tasks"  name="Tasks"        fill={COLOR.tasks}  radius={[4,4,0,0]} />
                  <Bar dataKey="points" name="Story Points" fill={COLOR.points} radius={[4,4,0,0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>

          {/* Code Quality Trend */}
          <div className="bg-white rounded-2xl border border-gray-100 p-5">
            <p className="text-sm font-semibold text-gray-700 mb-4">Code Quality เฉลี่ย (%)</p>
            {monthlyData.length === 0 ? (
              <div className="h-48 flex items-center justify-center text-gray-300 text-sm">ไม่มีข้อมูล</div>
            ) : (
              <ResponsiveContainer width="100%" height={220}>
                <LineChart data={monthlyData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
                  <XAxis dataKey="period" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis domain={[60, 100]} tick={{ fontSize: 11 }} axisLine={false} tickLine={false} />
                  <Tooltip content={<CustomTooltip />} />
                  <Line
                    type="monotone" dataKey="quality" name="Quality"
                    stroke={COLOR.quality} strokeWidth={2.5}
                    dot={{ r: 5, fill: COLOR.quality, strokeWidth: 2, stroke: '#fff' }}
                    activeDot={{ r: 7 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {/* ─── Member Comparison ─────────────────────────── */}
        <div className="bg-white rounded-2xl border border-gray-100 p-5">
          <p className="text-sm font-semibold text-gray-700 mb-4">เปรียบเทียบ Tasks ต่อคน</p>
          {memberData.length === 0 ? (
            <div className="h-48 flex items-center justify-center text-gray-300 text-sm">ไม่มีข้อมูล</div>
          ) : (
            <ResponsiveContainer width="100%" height={Math.max(200, memberData.length * 52)}>
              <BarChart data={memberData} layout="vertical" barCategoryGap="25%">
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" horizontal={false} />
                <XAxis type="number" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis type="category" dataKey="name" tick={{ fontSize: 12 }} width={80} axisLine={false} tickLine={false} />
                <Tooltip content={<CustomTooltip />} cursor={{ fill: '#f9fafb' }} />
                <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="tasks"  name="Tasks"        fill={COLOR.tasks}  radius={[0,4,4,0]} />
                <Bar dataKey="points" name="Story Points" fill={COLOR.points} radius={[0,4,4,0]} />
                <Bar dataKey="bugs"   name="Bugs Fixed"   fill={COLOR.bugs}   radius={[0,4,4,0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* ─── Leaderboard + Quality per Member ──────────── */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">

          {/* Leaderboard */}
          <div className="bg-white rounded-2xl border border-gray-100 p-5">
            <p className="text-sm font-semibold text-gray-700 mb-4">Leaderboard (Tasks)</p>
            <div className="space-y-2">
              {memberData.map((m, i) => (
                <div key={m.name} className="flex items-center gap-3">
                  <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 ${
                    i === 0 ? 'bg-yellow-100 text-yellow-700' :
                    i === 1 ? 'bg-gray-100 text-gray-600' :
                    i === 2 ? 'bg-orange-100 text-orange-700' :
                    'bg-gray-50 text-gray-400'
                  }`}>{i + 1}</span>
                  <div className="flex items-center gap-1.5 w-28 flex-shrink-0">
                    {m.role === 'team_lead'
                      ? <Crown size={12} className="text-amber-500 flex-shrink-0" />
                      : <User size={12} className="text-gray-400 flex-shrink-0" />}
                    <span className="text-sm text-gray-700 truncate">{m.fullName}</span>
                  </div>
                  <div className="flex-1 bg-gray-100 rounded-full h-2 overflow-hidden">
                    <div
                      className="h-2 rounded-full"
                      style={{
                        width: `${memberData[0].tasks ? (m.tasks / memberData[0].tasks) * 100 : 0}%`,
                        background: COLOR.tasks,
                      }}
                    />
                  </div>
                  <span className="text-sm font-bold text-blue-600 w-8 text-right flex-shrink-0">{m.tasks}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Code Quality per Member */}
          <div className="bg-white rounded-2xl border border-gray-100 p-5">
            <p className="text-sm font-semibold text-gray-700 mb-4">Code Quality เฉลี่ยต่อคน (%)</p>
            <div className="space-y-2">
              {[...memberData].sort((a, b) => b.quality - a.quality).map(m => (
                <div key={m.name} className="flex items-center gap-3">
                  <div className="flex items-center gap-1.5 w-28 flex-shrink-0">
                    {m.role === 'team_lead'
                      ? <Crown size={12} className="text-amber-500 flex-shrink-0" />
                      : <User size={12} className="text-gray-400 flex-shrink-0" />}
                    <span className="text-sm text-gray-700 truncate">{m.fullName}</span>
                  </div>
                  <div className="flex-1 bg-gray-100 rounded-full h-2 overflow-hidden">
                    <div
                      className="h-2 rounded-full transition-all"
                      style={{
                        width: `${m.quality}%`,
                        background: m.quality >= 85 ? COLOR.quality : m.quality >= 70 ? '#f59e0b' : COLOR.bugs,
                      }}
                    />
                  </div>
                  <span className={`text-sm font-bold w-10 text-right flex-shrink-0 ${
                    m.quality >= 85 ? 'text-green-600' : m.quality >= 70 ? 'text-yellow-600' : 'text-red-600'
                  }`}>{m.quality}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ─── Summary Table ──────────────────────────────── */}
        <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden">
          <div className="px-5 py-4 border-b border-gray-50">
            <p className="text-sm font-semibold text-gray-700">สรุป KPI ทั้งทีม</p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50">
                  {['ชื่อ', 'Role', 'Tasks', 'Story Points', 'Bugs Fixed', 'PR Reviews', 'Avg Quality'].map(h => (
                    <th key={h} className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide whitespace-nowrap">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {memberData.map(m => (
                  <tr key={m.name} className="hover:bg-gray-50 transition-colors">
                    <td className="px-4 py-3 font-medium text-gray-800">{m.fullName}</td>
                    <td className="px-4 py-3">
                      <span className={`inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full font-medium ${
                        m.role === 'team_lead' ? 'bg-amber-50 text-amber-700' : 'bg-gray-100 text-gray-600'
                      }`}>
                        {m.role === 'team_lead' ? <Crown size={10}/> : <User size={10}/>}
                        {m.role === 'team_lead' ? 'Team Lead' : 'Developer'}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-semibold text-blue-600">{m.tasks}</td>
                    <td className="px-4 py-3 font-semibold text-purple-600">{m.points}</td>
                    <td className="px-4 py-3 font-semibold text-red-600">{m.bugs}</td>
                    <td className="px-4 py-3 text-gray-600">{m.prs}</td>
                    <td className="px-4 py-3">
                      <span className={`font-semibold ${
                        m.quality >= 85 ? 'text-green-600' : m.quality >= 70 ? 'text-yellow-600' : 'text-red-600'
                      }`}>{m.quality}%</span>
                    </td>
                  </tr>
                ))}
                {/* Total Row */}
                <tr className="bg-blue-50 font-semibold">
                  <td className="px-4 py-3 text-gray-800">รวม / เฉลี่ย</td>
                  <td className="px-4 py-3 text-gray-400 text-xs">ทั้งทีม</td>
                  <td className="px-4 py-3 text-blue-700">{stats.totalTasks}</td>
                  <td className="px-4 py-3 text-purple-700">{stats.totalPoints}</td>
                  <td className="px-4 py-3 text-red-700">{stats.totalBugs}</td>
                  <td className="px-4 py-3 text-orange-700">{stats.totalPRs}</td>
                  <td className="px-4 py-3 text-green-700">{stats.avgQuality}%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  )
}
