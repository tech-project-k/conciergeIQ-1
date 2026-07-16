import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import { Calendar, DollarSign, Users, Trash2, ArrowRight, Loader } from 'lucide-react';

export default function SavedTrips() {
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchTrips = async () => {
    try {
      const res = await api.get('/trips');
      setTrips(res.data);
    } catch (err) {
      console.error("Error fetching trips:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTrips();
  }, []);

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (!confirm("Are you sure you want to delete this trip and its itinerary?")) return;
    try {
      await api.delete(`/trips/${id}`);
      setTrips(prev => prev.filter(t => t.id !== id));
    } catch (err) {
      alert("Failed to delete trip.");
    }
  };

  return (
    <div className="min-h-screen bg-darkBg flex flex-col">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 max-w-7xl mx-auto px-6 py-8 w-full space-y-8 overflow-y-auto">
          
          <div>
            <h1 className="text-3xl font-extrabold text-white">Your Saved Trips</h1>
            <p className="text-gray-400 mt-2 text-sm">
              Review and manage your previously planned AI journeys.
            </p>
          </div>

          {loading ? (
            <div className="flex justify-center items-center py-20 text-gray-500">
              <Loader className="w-8 h-8 animate-spin" />
            </div>
          ) : trips.length === 0 ? (
            <div className="glass-panel rounded-3xl p-12 text-center text-gray-500 max-w-xl mx-auto">
              You haven't planned any trips yet!
              <button
                onClick={() => navigate('/chat')}
                className="mt-6 px-5 py-2.5 bg-violet-600 hover:bg-violet-500 text-white font-semibold rounded-xl transition flex items-center gap-2 mx-auto"
              >
                Plan a Trip Now <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {trips.map(trip => (
                <div
                  key={trip.id}
                  onClick={() => navigate('/chat', { state: { tripId: trip.id } })}
                  className="glass-panel rounded-3xl p-6 glass-panel-hover cursor-pointer flex flex-col justify-between h-56 group"
                >
                  <div className="space-y-4">
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="text-xl font-bold text-white group-hover:text-violet-400 transition">
                          {trip.destination}
                        </h3>
                        <span className="inline-block mt-1 text-xs px-2.5 py-0.5 rounded-full font-semibold bg-violet-500/10 text-violet-400 border border-violet-500/15 uppercase">
                          {trip.status}
                        </span>
                      </div>
                      <button
                        onClick={(e) => handleDelete(trip.id, e)}
                        className="text-gray-600 hover:text-red-400 p-1.5 hover:bg-slate-900 rounded-lg transition"
                        title="Delete Trip"
                      >
                        <Trash2 className="w-5 h-5" />
                      </button>
                    </div>

                    <div className="space-y-2.5 text-sm text-gray-400">
                      <div className="flex items-center gap-2.5">
                        <Calendar className="w-4 h-4 text-gray-500" />
                        <span>{trip.start_date} &rarr; {trip.end_date}</span>
                      </div>
                      <div className="flex items-center gap-6">
                        <div className="flex items-center gap-1.5">
                          <DollarSign className="w-4 h-4 text-gray-500" />
                          <span>Budget: <strong className="text-white">${trip.budget}</strong></span>
                        </div>
                        <div className="flex items-center gap-1.5">
                          <Users className="w-4 h-4 text-gray-500" />
                          <span>Travelers: <strong className="text-white">{trip.num_travelers}</strong></span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-1 text-xs font-semibold text-violet-400 group-hover:underline pt-4 border-t border-slate-900">
                    Open AI Chat Planner
                    <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
                  </div>
                </div>
              ))}
            </div>
          )}

        </main>
      </div>
    </div>
  );
}
