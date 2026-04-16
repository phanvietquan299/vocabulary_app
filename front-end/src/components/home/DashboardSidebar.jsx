import { useLocation, useNavigate } from 'react-router-dom'

const NAV_ITEMS = [
  {
    key: 'dashboard',
    label: 'Dashboard',
    to: '/home',
    icon: DashboardIcon,
  },
  {
    key: 'flashcards',
    label: 'Flashcards',
    to: '/review',
    icon: FlashcardsIcon,
  },
  {
    key: 'topics',
    label: 'Topics',
    action: 'scroll-topics',
    icon: TopicsIcon,
  },
]

export default function DashboardSidebar() {
  const location = useLocation()
  const navigate = useNavigate()

  function handleSidebarAction(item) {
    if (item.to) {
      navigate(item.to)
      return
    }

    if (item.action === 'scroll-topics') {
      document.getElementById('topics-hub')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }

  return (
    <aside className="dashboard-sidebar" aria-label="Dashboard navigation">
      <nav className="dashboard-nav">
        {NAV_ITEMS.map((item) => {
          const active = item.to ? location.pathname === item.to : false
          const className = `dashboard-nav-item${active ? ' is-active' : ''}${item.disabled ? ' is-disabled' : ''}`
          const Icon = item.icon

          return (
            <button
              key={item.key}
              type="button"
              className={className}
              disabled={item.disabled}
              onClick={() => handleSidebarAction(item)}
              aria-label={item.label}
              title={item.label}
            >
              <Icon />
              <span>{item.label}</span>
            </button>
          )
        })}
      </nav>
    </aside>
  )
}

function DashboardIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M4 11.5 12 4l8 7.5" />
      <path d="M6 10.5V20h12v-9.5" />
    </svg>
  )
}

function FlashcardsIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="5" y="4.5" width="12" height="15" rx="2" />
      <path d="M9 8.5h4" />
      <path d="M8 12h6" />
    </svg>
  )
}

function TopicsIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M4.5 7h15" />
      <path d="M4.5 12h15" />
      <path d="M4.5 17h15" />
      <circle cx="7" cy="7" r="1.1" />
      <circle cx="13" cy="12" r="1.1" />
      <circle cx="9" cy="17" r="1.1" />
    </svg>
  )
}
