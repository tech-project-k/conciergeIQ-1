import React from 'react';
import { Link } from 'react-router-dom';
import { Compass, Sparkles, Map, CloudRain, ShieldCheck, PhoneCall } from 'lucide-react';

export default function Landing() {
  return (
    <div className="relative min-h-screen bg-darkBg text-gray-100 overflow-hidden flex flex-col justify-between">
      
      {/* Background Neon Glows */}
      <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] rounded-full bg-violet-900/20 blur-[120px]" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] rounded-full bg-indigo-900/20 blur-[120px]" />

      {/* Navigation */}
      <header className="relative w-full max-w-7xl mx-auto px-6 py-6 flex items-center justify-between z-10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-violet-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-violet-500/20">
            <Compass className="w-6 h-6 text-white" />
          </div>
          <span className="text-xl font-extrabold tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-violet-400 to-indigo-300">
            ConciergeIQ
          </span>
        </div>
        <div className="flex items-center gap-4">
          <Link to="/dashboard" className="px-5 py-2.5 text-sm font-semibold rounded-xl bg-gradient-to-tr from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 transition shadow-lg shadow-violet-500/10">
            Enter App &rarr;
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <main className="relative max-w-7xl mx-auto px-6 py-16 text-center z-10 flex-grow flex flex-col justify-center items-center">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-violet-500/10 border border-violet-500/20 text-violet-300 text-xs font-semibold tracking-wide uppercase mb-6 animate-pulse">
          <Sparkles className="w-4 h-4" /> Next-Generation AI Agent
        </div>
        
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight leading-none mb-6">
          Your Autonomous <br/>
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-violet-400 via-fuchsia-400 to-indigo-400">
            AI Travel Concierge
          </span>
        </h1>
        
        <p className="max-w-2xl text-gray-400 text-base md:text-xl leading-relaxed mb-10">
          Not a basic CRUD website or search aggregator. ConciergeIQ is a stateful travel agent that reasons, live-searches, maps distances, optimizes schedules, and dynamically shifts itineraries to handle weather and traffic.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 mb-16 justify-center w-full">
          <Link to="/dashboard" className="px-8 py-4 text-base font-semibold rounded-2xl bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 transition shadow-xl shadow-violet-500/20 transform hover:-translate-y-0.5 duration-200">
            Launch AI Planner
          </Link>
        </div>

        {/* Feature Highlights */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mt-10">
          
          <div className="glass-panel rounded-2xl p-8 text-left glass-panel-hover">
            <div className="w-12 h-12 rounded-xl bg-violet-500/10 border border-violet-500/20 flex items-center justify-center text-violet-400 mb-6">
              <Map className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold mb-2">Live Map & ETA Route Optimization</h3>
            <p className="text-gray-400 text-sm leading-relaxed">
              Computes spatial coordinate travel paths (cab, walking, transit) with distance and traffic-aware travel durations.
            </p>
          </div>

          <div className="glass-panel rounded-2xl p-8 text-left glass-panel-hover">
            <div className="w-12 h-12 rounded-xl bg-fuchsia-500/10 border border-fuchsia-500/20 flex items-center justify-center text-fuchsia-400 mb-6">
              <CloudRain className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold mb-2">Weather-Aware Adaptations</h3>
            <p className="text-gray-400 text-sm leading-relaxed">
              If rain is forecast, the LangGraph engine detects the conflict and updates outdoor walking tours to indoor activities.
            </p>
          </div>

          <div className="glass-panel rounded-2xl p-8 text-left glass-panel-hover">
            <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-6">
              <PhoneCall className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold mb-2">Instant Contact Assistance</h3>
            <p className="text-gray-400 text-sm leading-relaxed">
              Retrieve direct phone numbers, official websites, coordinate details, and navigation links of all itinerary destinations.
            </p>
          </div>

        </div>
      </main>

      {/* Footer */}
      <footer className="relative w-full max-w-7xl mx-auto px-6 py-8 border-t border-gray-900 text-center text-gray-500 text-xs z-10">
        &copy; {new Date().getFullYear()} ConciergeIQ AI. Engineered for premium, autonomous trip planning.
      </footer>
    </div>
  );
}
