import { useState, useEffect, useCallback } from 'react'
import type { Member } from '../types'
import { getMembers, setMember, deleteMember } from '../firebase/firestore'

export function useMembers() {
  const [members, setMembers] = useState<Member[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetch = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await getMembers()
      setMembers(data)
    } catch (e) {
      console.error('[useMembers] fetch error:', e)
      setError('Failed to load members')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { fetch() }, [fetch])

  const saveMember = async (member: Omit<Member, 'id'> & { id?: string }) => {
    await setMember(member)
    await fetch()
  }

  const removeMember = async (id: string) => {
    await deleteMember(id)
    await fetch()
  }

  return { members, loading, error, saveMember, removeMember, refetch: fetch }
}
