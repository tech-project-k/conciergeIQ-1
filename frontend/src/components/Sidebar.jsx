import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, MessageSquarePlus, BookmarkCheck } from 'lucide-react';

export default function Sidebar() {
  const linkClass = ({ isActive }) =>
    `flex items-center gap-3 px-4 py-3.5 rounded-xl text-sm font-semibold transition-all duration-200 ${
      isActive
        ? 'bg-violet-600/10 text-violet-400 border border-violet-500/25 shadow-md shadow-violet-500/5'
        : 'text-gray-400 hover:bg-slate-900 hover:text-gray-200 border border-transparent'
    }`;

  return (
    <aside className="w-64 bg-[#0a0d16] border-r border-gray-900 min-h-[calc(screen-80px)] hidden md:flex flex-col p-4 gap-2.5">
      <div className="px-4 py-2 mb-4 text-xs font-bold uppercase tracking-wider text-gray-600">
        Workspace
      </div>
      
      <NavLink to="/dashboard" className={linkClass}>
        <LayoutDashboard className="w-5 h-5" />
        Dashboard
      </NavLink>
      
      <NavLink to="/chat" className={linkClass}>
        <MessageSquarePlus className="w-5 h-5" />
        AI Concierge Planner
      </NavLink>
      
      <NavLink to="/saved-trips" className={linkClass}>
        <BookmarkCheck className="w-5 h-5" />
        Saved Trips
      </NavLink>
    </aside>
  );
}
