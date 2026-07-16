import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import api from '../services/api';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import CustomMapContainer from '../components/MapContainer';
import Timeline from '../components/Timeline';
import { Sparkles, Send, Loader, AlertTriangle, Compass, Map, CalendarRange } from 'lucide-react';

export default function AIChatPage() {
  const routerLocation = useLocation();
  const [tripId, setTripId] = useState(routerLocation.state?.tripId || null);
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [trip, setTrip] = useState(null);
  const [warnings, setWarnings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('map'); // 'map' or 'timeline'
  
  const chatBottomRef = useRef(null);

  // Suggested quick prompts
  const suggestionChips = [
    { label: "Plan 3 days in Paris", text: "I want to plan a 3-day trip to Paris for 2 adults. Keep the budget moderate." },
    { label: "Plan 2 days in Tokyo", text: "Plan a 2-day family vacation in Tokyo with kids." },
    { label: "Suggest cheaper hotel", text: "Suggest a cheaper hotel and update the itinerary budget." },
    { label: "Plan rainy-day activities", text: "It is raining today, shift the outdoor walking activities to indoor options." },
    { label: "Emergency contacts", text: "What are the nearest emergency hospitals and emergency numbers in Paris?" }
  ];

  // Fetch initial history if tripId exists
  useEffect(() => {
    const initPage = async () => {
      if (tripId) {
        try {
          const tripRes = await api.get(`/trips/${tripId}`);
          setTrip(tripRes.data);
          
          const chatRes = await api.get(`/chat/history/${tripId}`);
          setMessages(chatRes.data);
        } catch (err) {
          console.error("Error loading trip/chat details:", err);
        }
      } else {
        // Welcome message
        setMessages([
          {
            id: 'welcome',
            role: 'assistant',
            content: "Hello! I am your AI Travel Concierge. Tell me where you want to travel, your budget, how many days, and any accessibility or food requirements (e.g. 'Plan 3 days in Paris with kid-friendly activities'). I'll build a complete itinerary, map out coordinates, and check for weather shifts!"
          }
        ]);
      }
    };
    initPage();
  }, [tripId]);

  // Scroll chat list to bottom
  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (textToSend) => {
    const msgText = textToSend || query;
    if (!msgText.trim()) return;

    setQuery('');
    setLoading(true);
    
    // Add user message to UI instantly
    const userTempMsg = {
      id: Date.now().toString(),
      role: 'user',
      content: msgText,
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, userTempMsg]);

    try {
      const res = await api.post('/chat', {
        query: msgText,
        trip_id: tripId
      });

      // Update state
      setMessages(res.data.messages || []);
      setWarnings(res.data.warnings || []);
      
      if (res.data.trip) {
        setTrip(res.data.trip);
        setTripId(res.data.trip.id);
      }
    } catch (err) {
      console.error("AI Chat failed:", err);
      setMessages(prev => [
        ...prev,
        {
          id: Date.now().toString(),
          role: 'assistant',
          content: "Sorry, I encountered an issue updating your itinerary. Please check the backend connection."
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const activeActivities = trip?.activities || [];

  return (
    <div className="min-h-screen bg-darkBg flex flex-col h-screen overflow-hidden">
      <Navbar />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        
        {/* Main interactive panel */}
        <main className="flex-1 flex flex-col lg:flex-row overflow-hidden w-full">
          
          {/* Left: Chat Stream Pane */}
          <section className="flex-1 flex flex-col bg-[#0b0e17] border-r border-gray-900 overflow-hidden h-1/2 lg:h-full lg:w-1/2">
            
            {/* Active Header */}
            <div className="px-6 py-4.5 border-b border-gray-900 bg-[#090b12] flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-violet-400" />
                <span className="font-bold text-sm text-gray-200">
                  {trip ? `Planning: ${trip.destination}` : 'Autonomous Concierge Agent'}
                </span>
              </div>
              {trip && (
                <div className="text-xs text-violet-400 font-bold bg-violet-600/10 border border-violet-500/20 px-3 py-1 rounded-full">
                  Budget: ${trip.budget}
                </div>
              )}
            </div>

            {/* Messages Feed */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {messages.map(msg => (
                <div
                  key={msg.id}
                  className={`flex gap-3 max-w-[85%] ${
                    msg.role === 'user' ? 'ml-auto flex-row-reverse' : 'mr-auto'
                  }`}
                >
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center text-xs border flex-shrink-0 ${
                      msg.role === 'user'
                        ? 'bg-indigo-600/20 border-indigo-500/30 text-indigo-400'
                        : 'bg-violet-600/20 border-violet-500/30 text-violet-400'
                    }`}
                  >
                    {msg.role === 'user' ? 'ME' : 'AI'}
                  </div>
                  
                  <div
                    className={`p-4 rounded-2xl text-sm leading-relaxed border select-text ${
                      msg.role === 'user'
                        ? 'bg-indigo-600/10 border-indigo-500/25 text-indigo-100 rounded-tr-none'
                        : 'bg-slate-900/60 border-slate-900 text-gray-200 rounded-tl-none'
                    }`}
                  >
                    {msg.content}
                  </div>
                </div>
              ))}
              
              {loading && (
                <div className="flex gap-3 mr-auto items-center text-xs text-gray-500">
                  <div className="w-8 h-8 rounded-full bg-violet-600/15 flex items-center justify-center">
                    <Loader className="w-4 h-4 animate-spin text-violet-400" />
                  </div>
                  Thinking, searching, and structuring route coordinates...
                </div>
              )}
              
              <div ref={chatBottomRef} />
            </div>

            {/* Suggestion Chips */}
            <div className="px-6 py-2 border-t border-gray-900 bg-[#090b12]/50 flex gap-2 overflow-x-auto select-none">
              {suggestionChips.map((chip, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSendMessage(chip.text)}
                  className="px-3.5 py-1.5 bg-slate-950/70 border border-slate-900 rounded-full text-xs font-semibold text-gray-400 hover:text-white hover:border-violet-500/35 hover:bg-violet-500/5 transition whitespace-nowrap"
                >
                  {chip.label}
                </button>
              ))}
            </div>

            {/* Input area */}
            <div className="p-4 border-t border-gray-900 bg-[#090b12]">
              <div className="relative flex items-center bg-slate-950 rounded-2xl border border-slate-800 focus-within:border-violet-500 focus-within:ring-1 focus-within:ring-violet-500 transition px-2">
                <input
                  type="text"
                  placeholder="Ask me: 'Move dinner to tomorrow', 'Avoid walking', 'Suggest cheaper hotel'..."
                  className="flex-1 bg-transparent border-0 ring-0 focus:ring-0 focus:outline-none text-sm text-gray-200 py-4.5 px-4 placeholder-gray-600"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                  disabled={loading}
                />
                <button
                  onClick={() => handleSendMessage()}
                  disabled={loading || !query.trim()}
                  className="w-11 h-11 rounded-xl bg-gradient-to-tr from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 disabled:from-violet-800 disabled:to-indigo-800 text-white flex items-center justify-center transition shadow-lg shadow-violet-500/10 cursor-pointer"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </div>

          </section>

          {/* Right: Visual Tab View (Map & Timeline) */}
          <section className="flex-1 flex flex-col overflow-hidden h-1/2 lg:h-full lg:w-1/2 bg-[#090b12]/30 p-6 space-y-6">
            
            {/* Tabs Header */}
            <div className="flex bg-slate-950 p-1.5 rounded-2xl border border-slate-900 w-fit select-none">
              <button
                onClick={() => setActiveTab('map')}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-bold transition-all duration-200 ${
                  activeTab === 'map'
                    ? 'bg-violet-600 text-white shadow shadow-violet-500/10'
                    : 'text-gray-400 hover:text-gray-200'
                }`}
              >
                <Map className="w-4 h-4" />
                Interactive Map Route
              </button>
              <button
                onClick={() => setActiveTab('timeline')}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-bold transition-all duration-200 ${
                  activeTab === 'timeline'
                    ? 'bg-violet-600 text-white shadow shadow-violet-500/10'
                    : 'text-gray-400 hover:text-gray-200'
                }`}
              >
                <CalendarRange className="w-4 h-4" />
                Daily Timeline Itinerary
              </button>
            </div>

            {/* Tab Contents */}
            <div className="flex-grow overflow-y-auto min-h-0 relative">
              {activeTab === 'map' ? (
                <CustomMapContainer activities={activeActivities} />
              ) : (
                <div className="h-full">
                  <Timeline activities={activeActivities} warnings={warnings} tripId={tripId} />
                </div>
              )}
            </div>

          </section>

        </main>
      </div>
    </div>
  );
}
