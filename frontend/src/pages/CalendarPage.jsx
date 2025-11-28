import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Calendar from '../components/Calendar';
import EventModal from '../components/EventModal';
import ClubFilterSidebar from '../components/ClubFilterSidebar';
import Navbar from '../components/Navbar';
import api from '../api/client';

export default function CalendarPage() {
  const [events, setEvents] = useState([]);
  const [clubs, setClubs] = useState([]);
  const [selectedClubs, setSelectedClubs] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [showEventModal, setShowEventModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    } else {
      loadClubs();
    }
  }, [isAuthenticated]);

  useEffect(() => {
    if (isAuthenticated) {
      loadEvents();
    }
  }, [selectedClubs, isAuthenticated]);

  const loadClubs = async () => {
    try {
      const response = await api.get('/api/clubs/');
      const data = response.data;
      const clubsArray = Array.isArray(data) ? data : (data.results || []);
      const finalClubs = Array.isArray(clubsArray) ? clubsArray : [];
      setClubs(finalClubs);
      // Select all clubs by default
      setSelectedClubs(finalClubs.map((c) => c.id));
    } catch (error) {
      console.error('Failed to load clubs:', error);
    }
  };

  const loadEvents = async (start, end) => {
    try {
      setLoading(true);
      const params = {};
      
      if (start && end) {
        params.start = start.toISOString();
        params.end = end.toISOString();
      }
      
      if (selectedClubs.length > 0 && selectedClubs.length < clubs.length) {
        params.clubs = selectedClubs.join(',');
      }

      const response = await api.get('/api/events/', { params });
      const data = response.data;
      const eventsArray = Array.isArray(data) ? data : (data.results || []);
      setEvents(Array.isArray(eventsArray) ? eventsArray : []);
    } catch (error) {
      console.error('Failed to load events:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEventClick = (event) => {
    setSelectedEvent(event);
    setShowEventModal(true);
  };

  const handleDateSelect = (start, end) => {
    if (user?.club) {
      setSelectedEvent({ start, end });
      // setShowEventModal(true);
    }
  };

  const handleEventSaved = () => {
    loadEvents();
    setShowEventModal(false);
    setSelectedEvent(null);
  };

  const handleEventDeleted = () => {
    loadEvents();
    setShowEventModal(false);
    setSelectedEvent(null);
  };

  const canEditEvent = (event) => {
    if (!user || !user.club) return false;
    return event.club.id === user.club.id;
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      <Navbar />
      
      <div className="flex">
        <ClubFilterSidebar
          clubs={clubs}
          selectedClubs={selectedClubs}
          onToggleClub={(clubId) => {
            setSelectedClubs((prev) =>
              prev.includes(clubId)
                ? prev.filter((id) => id !== clubId)
                : [...prev, clubId]
            );
          }}
          onSelectAll={() => setSelectedClubs(clubs.map((c) => c.id))}
          onDeselectAll={() => setSelectedClubs([])}
        />

        <div className="flex-1 p-6">
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-colors duration-200 border border-gray-100 dark:border-gray-700">
            <div className="flex justify-between items-center mb-6">
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Event Calendar</h1>
              {user?.club && (
                <button
                  onClick={() => {
                    setSelectedEvent({ start: new Date(), end: new Date() });
                    setShowEventModal(true);
                  }}
                  className="bg-primary-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-primary-700 shadow-md hover:shadow-lg transition-all duration-200"
                >
                  + Create Event
                </button>
              )}
            </div>

            <Calendar
              events={events}
              onEventClick={handleEventClick}
              onDateSelect={handleDateSelect}
              onDatesSet={loadEvents}
            />
          </div>
        </div>
      </div>

      {showEventModal && (
        <EventModal
          event={selectedEvent}
          canEdit={selectedEvent?.id ? canEditEvent(selectedEvent) : true}
          onClose={() => {
            setShowEventModal(false);
            setSelectedEvent(null);
          }}
          onSave={handleEventSaved}
          onDelete={handleEventDeleted}
        />
      )}
    </div>
  );
}
