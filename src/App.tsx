import { useState } from 'react'
import './index.css'
import Dashboard from './pages/Dashboard'
import MemberDetail from './pages/MemberDetail'
import OverviewPage from './pages/OverviewPage'
import type { Member } from './types'

type Page = 'team' | 'overview' | 'member'

export default function App() {
  const [page, setPage] = useState<Page>('team')
  const [selectedMember, setSelectedMember] = useState<Member | null>(null)

  const handleSelectMember = (member: Member) => {
    setSelectedMember(member)
    setPage('member')
  }

  const handleBack = () => {
    setSelectedMember(null)
    setPage('team')
  }

  if (page === 'member' && selectedMember) {
    return <MemberDetail member={selectedMember} onBack={handleBack} />
  }

  if (page === 'overview') {
    return <OverviewPage onNavigate={() => setPage('team')} />
  }

  return <Dashboard onSelectMember={handleSelectMember} onNavigate={() => setPage('overview')} />
}
