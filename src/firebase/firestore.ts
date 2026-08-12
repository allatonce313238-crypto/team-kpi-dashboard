import {
  collection,
  doc,
  getDocs,
  addDoc,
  updateDoc,
  deleteDoc,
  query,
  where,
  setDoc,
} from 'firebase/firestore'
import { db } from './config'
import type { Member, KPIEntry } from '../types'

// ── Members ──────────────────────────────────────────────

export async function getMembers(): Promise<Member[]> {
  const snap = await getDocs(collection(db, 'members'))
  return snap.docs.map(d => ({ id: d.id, ...d.data() } as Member))
}

export async function setMember(member: Omit<Member, 'id'> & { id?: string }): Promise<string> {
  if (member.id) {
    const { id, ...data } = member
    await setDoc(doc(db, 'members', id), data)
    return id
  }
  const ref = await addDoc(collection(db, 'members'), member)
  return ref.id
}

export async function deleteMember(id: string): Promise<void> {
  await deleteDoc(doc(db, 'members', id))
}

// ── KPI Entries ───────────────────────────────────────────

export async function getKPIEntries(memberId?: string): Promise<KPIEntry[]> {
  const q = memberId
    ? query(collection(db, 'kpi_entries'), where('memberId', '==', memberId))
    : query(collection(db, 'kpi_entries'))

  const snap = await getDocs(q)
  const docs = snap.docs.map(d => ({ id: d.id, ...d.data() } as KPIEntry))
  return docs.sort((a, b) => b.period.localeCompare(a.period))
}

export async function addKPIEntry(entry: Omit<KPIEntry, 'id' | 'createdAt'>): Promise<string> {
  const ref = await addDoc(collection(db, 'kpi_entries'), {
    ...entry,
    createdAt: new Date().toISOString(),
  })
  return ref.id
}

export async function updateKPIEntry(id: string, entry: Partial<Omit<KPIEntry, 'id'>>): Promise<void> {
  await updateDoc(doc(db, 'kpi_entries', id), entry)
}

export async function deleteKPIEntry(id: string): Promise<void> {
  await deleteDoc(doc(db, 'kpi_entries', id))
}
