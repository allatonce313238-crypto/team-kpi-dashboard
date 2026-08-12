import { Calendar, X } from 'lucide-react'

interface MonthRangeFilterProps {
  fromMonth: string
  toMonth: string
  onChange: (from: string, to: string) => void
}

export default function MonthRangeFilter({ fromMonth, toMonth, onChange }: MonthRangeFilterProps) {
  const hasFilter = fromMonth || toMonth

  return (
    <div className="flex items-center gap-2 flex-wrap">
      <div className="flex items-center gap-1.5 text-sm text-gray-500">
        <Calendar size={15} />
        <span className="font-medium">ช่วงเวลา:</span>
      </div>
      <div className="flex items-center gap-2">
        <input
          type="month"
          value={fromMonth}
          onChange={e => onChange(e.target.value, toMonth)}
          className="border border-gray-200 rounded-xl px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 bg-white"
        />
        <span className="text-gray-400 text-sm">—</span>
        <input
          type="month"
          value={toMonth}
          onChange={e => onChange(fromMonth, e.target.value)}
          className="border border-gray-200 rounded-xl px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 bg-white"
        />
        {hasFilter && (
          <button
            onClick={() => onChange('', '')}
            className="flex items-center gap-1 text-xs text-gray-400 hover:text-red-500 border border-gray-200 rounded-lg px-2 py-1.5 transition-colors"
          >
            <X size={12} /> ล้าง
          </button>
        )}
      </div>
      {hasFilter && (
        <span className="text-xs bg-blue-50 text-blue-600 rounded-full px-2.5 py-1 font-medium">
          {fromMonth || '…'} → {toMonth || '…'}
        </span>
      )}
    </div>
  )
}
