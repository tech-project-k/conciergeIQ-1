import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import { Sliders, CheckSquare, Sparkles, MapPin, Calendar, Heart, ShieldAlert, ArrowRight, Loader } from 'lucide-react';

export default function Dashboard() {
  const { user, updatePreferences } = useAuth();
  const navigate = useNavigate();
  const [trips, setTrips] = useState([]);
  const [loadingTrips, setLoadingTrips] = useState(true);
  
  // Preference States
  const [budgetTier, setBudgetTier] = useState('moderate');
  const [styles, setStyles] = useState({ adventure: 3, nature: 3, luxury: 3, family: 3 });
  const [dietary, setDietary] = useState([]);
  const [accessibility, setAccessibility] = useState([]);
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    // Sync context preferences with state
    if (user?.preferences) {
      setBudgetTier(user.preferences.budget_tier || 'moderate');
      setStyles(prev => ({
        ...prev,
        ...user.preferences.travel_style
      }));
      setDietary(user.preferences.dietary_restrictions || []);
      setAccessibility(user.preferences.accessibility_needs || []);
    }
  }, [user]);

  useEffect(() => {
    const fetchTrips = async () => {
      try {
        const res = await api.get('/trips');
        setTrips(res.data);
      } catch (err) {
        console.error("Error fetching trips:", err);
      } finally {
        setLoadingTrips(false);
      }
    };
    fetchTrips();
  }, []);

  const handleStyleChange = (key, val) => {
    setStyles(prev => ({ ...prev, [key]: parseInt(val) }));
  };

  const handleDietToggle = (diet) => {
    setDietary(prev =>
      prev.includes(diet) ? prev.filter(d => d !== diet) : [...prev, diet]
    );
  };

  const handleAccessToggle = (need) => {
    setAccessibility(prev =>
      prev.includes(need) ? prev.filter(a => a !== need) : [...prev, need]
    );
  };

  const handleSavePreferences = async () => {
    setSaveSuccess(false);
    try {
      await updatePreferences({
        travel_style: styles,
        dietary_restrictions: dietary,
        accessibility_needs: accessibility,
        budget_tier: budgetTier
      });
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err) {
      alert("Failed to update preferences.");
    }
  };

  const activeTrip = trips.find(t => t.status === "planning" || t.status === "active") || trips[0];

  return (
    <div className="min-h-screen bg-darkBg flex flex-col">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 max-w-7xl mx-auto px-6 py-8 w-full space-y-8 overflow-y-auto">
          
          {/* Welcome Panel */}
          <div className="relative rounded-3xl overflow-hidden glass-panel p-8 md:p-10 flex flex-col md:flex-row md:items-center justify-between gap-6 shadow-xl">
            <div className="absolute top-0 right-0 w-[30%] h-full bg-gradient-to-l from-violet-600/10 to-transparent blur-xl pointer-events-none" />
            <div>
              <h1 className="text-3xl font-extrabold text-white">Welcome back, {user?.full_name || 'Traveler'}</h1>
              <p className="text-gray-400 mt-2 text-sm md:text-base max-w-xl">
                Ready for your next adventure? Let ConciergeIQ compile a custom travel itinerary based on your preferences.
              </p>
            </div>
            <button
              onClick={() => navigate('/chat')}
              className="px-6 py-3.5 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white font-semibold rounded-xl transition flex items-center justify-center gap-2 group shadow-lg shadow-violet-500/10 hover:shadow-violet-500/20 w-fit"
            >
              Start AI Trip Planner
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {/* Preferences Column */}
            <div className="lg:col-span-2 space-y-6">
              <div className="glass-panel rounded-3xl p-6 shadow-md space-y-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <Sliders className="w-5 h-5 text-violet-400" />
                    <h2 className="text-xl font-bold text-white">AI Travel Profile Preferences</h2>
                  </div>
                  {saveSuccess && (
                    <span className="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2.5 py-1 rounded-full font-semibold">
                      Profile Saved
                    </span>
                  )}
                </div>

                {/* Travel styles sliders */}
                <div className="space-y-4">
                  <h3 className="text-sm font-bold text-gray-300">Interest Scores</h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {Object.keys(styles).map(style => (
                      <div key={style} className="bg-slate-950 p-4 rounded-xl border border-slate-900 space-y-2">
                        <div className="flex justify-between text-xs font-semibold capitalize text-gray-400">
                          <span>{style}</span>
                          <span>{styles[style]} / 5</span>
                        </div>
                        <input
                          type="range"
                          min="0"
                          max="5"
                          className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-violet-500"
                          value={styles[style]}
                          onChange={(e) => handleStyleChange(style, e.target.value)}
                        />
                      </div>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-2">
                  {/* Dietary constraints */}
                  <div className="space-y-3">
                    <h3 className="text-sm font-bold text-gray-300">Dietary Needs</h3>
                    <div className="space-y-2">
                      {['vegetarian', 'vegan', 'gluten-free', 'halal', 'kosher'].map(diet => (
                        <label key={diet} className="flex items-center gap-3 cursor-pointer select-none text-sm text-gray-400">
                          <input
                            type="checkbox"
                            checked={dietary.includes(diet)}
                            onChange={() => handleDietToggle(diet)}
                            className="w-4.5 h-4.5 rounded border-gray-800 text-violet-600 focus:ring-violet-500 bg-slate-950"
                          />
                          <span className="capitalize">{diet}</span>
                        </label>
                      ))}
                    </div>
                  </div>

                  {/* Accessibility options */}
                  <div className="space-y-3">
                    <h3 className="text-sm font-bold text-gray-300">Accessibility Needs</h3>
                    <div className="space-y-2">
                      {['wheelchair access', 'no stairs / elevator access', 'minimal walking required', 'service dog friendly'].map(need => (
                        <label key={need} className="flex items-center gap-3 cursor-pointer select-none text-sm text-gray-400">
                          <input
                            type="checkbox"
                            checked={accessibility.includes(need)}
                            onChange={() => handleAccessToggle(need)}
                            className="w-4.5 h-4.5 rounded border-gray-800 text-violet-600 focus:ring-violet-500 bg-slate-950"
                          />
                          <span className="capitalize">{need}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Budget selection */}
                <div className="space-y-3">
                  <h3 className="text-sm font-bold text-gray-300">Preferred Budget Class</h3>
                  <div className="grid grid-cols-3 gap-3">
                    {['budget', 'moderate', 'luxury'].map(tier => (
                      <button
                        key={tier}
                        onClick={() => setBudgetTier(tier)}
                        className={`py-3 rounded-xl border text-sm font-semibold capitalize transition ${
                          budgetTier === tier
                            ? 'bg-violet-600/10 border-violet-500 text-violet-400 shadow-md shadow-violet-500/5'
                            : 'bg-slate-950 border-slate-900 text-gray-500 hover:text-gray-300'
                        }`}
                      >
                        {tier}
                      </button>
                    ))}
                  </div>
                </div>

                <button
                  onClick={handleSavePreferences}
                  className="w-full py-3.5 bg-violet-600 hover:bg-violet-500 transition text-white font-semibold rounded-xl shadow-lg shadow-violet-500/10 mt-4"
                >
                  Save Profile Preferences
                </button>
              </div>
            </div>

            {/* Active Trip Info Column */}
            <div className="space-y-6">
              <div className="glass-panel rounded-3xl p-6 shadow-md space-y-6 h-full flex flex-col justify-between">
                <div>
                  <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                    <Heart className="w-5 h-5 text-fuchsia-400" />
                    Active Journey
                  </h2>
                  
                  {loadingTrips ? (
                    <div className="flex justify-center items-center py-12 text-gray-500">
                      <Loader className="w-6 h-6 animate-spin" />
                    </div>
                  ) : activeTrip ? (
                    <div className="space-y-4">
                      <div className="p-4 bg-slate-950 border border-slate-900 rounded-2xl space-y-3">
                        <div className="flex items-center gap-2 text-violet-400">
                          <MapPin className="w-5 h-5" />
                          <span className="font-bold text-lg text-white">{activeTrip.destination}</span>
                        </div>
                        <div className="flex items-center gap-2 text-sm text-gray-400">
                          <Calendar className="w-4 h-4 text-gray-500" />
                          <span>{activeTrip.start_date} &rarr; {activeTrip.end_date}</span>
                        </div>
                        <div className="flex justify-between text-xs text-gray-400 pt-2 border-t border-slate-900">
                          <span>Budget: <strong className="text-white">${activeTrip.budget}</strong></span>
                          <span>Travelers: <strong className="text-white">{activeTrip.num_travelers}</strong></span>
                        </div>
                      </div>
                      
                      {activeTrip.activities && activeTrip.activities.length > 0 ? (
                        <div className="space-y-2">
                          <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider">Itinerary Highlights</h3>
                          {activeTrip.activities.slice(0, 3).map((act, i) => (
                            <div key={i} className="flex justify-between items-center text-xs p-2.5 bg-slate-950/45 rounded-lg border border-slate-900">
                              <span className="text-gray-300 font-medium">{act.name}</span>
                              <span className="text-gray-500">{act.start_time}</span>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="p-4 rounded-xl bg-violet-500/5 border border-violet-500/10 text-xs text-gray-400 leading-relaxed flex items-center gap-2">
                          <Sparkles className="w-5 h-5 text-violet-400 flex-shrink-0" />
                          <span>Ask the AI Planner to fill out activities for this trip!</span>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="py-12 text-center text-gray-500 text-sm">
                      No active trips. Type "plan a trip to Paris" in the AI Concierge to get started!
                    </div>
                  )}
                </div>
                
                {activeTrip && (
                  <button
                    onClick={() => navigate(`/chat`, { state: { tripId: activeTrip.id } })}
                    className="w-full py-3.5 bg-slate-900 border border-slate-800 hover:bg-slate-800 transition text-gray-200 font-semibold rounded-xl flex items-center justify-center gap-2"
                  >
                    Open Active Trip Timeline
                  </button>
                )}
              </div>
            </div>

          </div>
        </main>
      </div>
    </div>
  );
}
