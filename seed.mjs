import { initializeApp } from 'firebase/app'
import { getFirestore, collection, doc, setDoc, addDoc } from 'firebase/firestore'
import { readFileSync } from 'fs'

// load .env manually
const env = readFileSync('.env', 'utf-8')
const get = (k) => env.match(new RegExp(`^${k}=(.+)$`, 'm'))?.[1]?.trim()

const app = initializeApp({
  apiKey: get('VITE_FIREBASE_API_KEY'),
  authDomain: get('VITE_FIREBASE_AUTH_DOMAIN'),
  projectId: get('VITE_FIREBASE_PROJECT_ID'),
  storageBucket: get('VITE_FIREBASE_STORAGE_BUCKET'),
  messagingSenderId: get('VITE_FIREBASE_MESSAGING_SENDER_ID'),
  appId: get('VITE_FIREBASE_APP_ID'),
})
const db = getFirestore(app)

const members = [
  { id: 'member-1', name: 'สมชาย ใจดี',    role: 'team_lead' },
  { id: 'member-2', name: 'วิชัย รักงาน',   role: 'developer' },
  { id: 'member-3', name: 'นภา สดใส',      role: 'developer' },
  { id: 'member-4', name: 'ธนากร มั่นคง',  role: 'developer' },
  { id: 'member-5', name: 'พิมพ์ใจ เก่งมาก', role: 'developer' },
  { id: 'member-6', name: 'กิตติ์ ตั้งใจ',  role: 'developer' },
]

const periods = ['2025-05', '2025-06', '2025-07', '2025-08']

function rand(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min }

const entries = []

for (const m of members) {
  for (const period of periods) {
    const isLead = m.role === 'team_lead'
    entries.push({
      memberId: m.id,
      period,
      periodType: 'monthly',
      tasksCompleted: isLead ? rand(8, 15)  : rand(12, 25),
      storyPoints:    isLead ? rand(15, 30) : rand(20, 45),
      bugsFixed:      isLead ? rand(2, 6)   : rand(4, 12),
      prReviews:      isLead ? rand(10, 20) : rand(3, 10),
      codeQuality:    rand(72, 98),
      customMetrics:  [
        { name: 'On-time delivery (%)', value: rand(80, 100) },
        { name: 'Blocked days', value: rand(0, 3) },
      ],
      notes: '',
      createdAt: new Date().toISOString(),
    })
  }
}

async function seed() {
  console.log('Seeding members...')
  for (const { id, ...data } of members) {
    await setDoc(doc(db, 'members', id), data)
    console.log(`  ✓ ${data.name} (${data.role})`)
  }

  console.log('\nSeeding KPI entries...')
  for (const entry of entries) {
    await addDoc(collection(db, 'kpi_entries'), entry)
  }
  console.log(`  ✓ ${entries.length} entries added`)

  console.log('\nDone! 🎉')
  process.exit(0)
}

seed().catch(e => { console.error(e); process.exit(1) })
