import { useState, useEffect, useCallback } from 'react'
import type { KPIEntry } from '../types'
import { getKPIEntries, addKPIEntry, updateKPIEntry, deleteKPIEntry } from '../firebase/firestore'

export function useKPIEntries(memberId?: string) {
  const [entries, setEntries] = useState<KPIEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetch = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await getKPIEntries(memberId)
      setEntries(data)
    } catch (e) {
      setError('Failed to load KPI data')
    } finally {
      setLoading(false)
    }
  }, [memberId])

  useEffect(() => { fetch() }, [fetch])

  const addEntry = async (entry: Omit<KPIEntry, 'id' | 'createdAt'>) => {
    await addKPIEntry(entry)
    await fetch()
  }

  const editEntry = async (id: string, entry: Partial<Omit<KPIEntry, 'id'>>) => {
    await updateKPIEntry(id, entry)
    await fetch()
  }

  const removeEntry = async (id: string) => {
    await deleteKPIEntry(id)
    await fetch()
  }

  return { entries, loading, error, addEntry, editEntry, removeEntry, refetch: fetch }
}
