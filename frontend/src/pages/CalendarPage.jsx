import { useState, useEffect, useRef } from 'react';
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
  const calendarRef = useRef(null);

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
      // Select all clubs and their sub-clubs by default
      const allIds = [];
      finalClubs.forEach(c => {
        allIds.push(c.id);
        if (c.sub_clubs) {
          c.sub_clubs.forEach(sub => allIds.push(sub.id));
        }
      });
      setSelectedClubs(allIds);
    } catch (error) {
      console.error('Failed to load clubs:', error);
    }
  };

  const loadEvents = async (start, end) => {
    try {
      setLoading(true);

      // If clubs are loaded but none are selected (e.g., "None" filter), show no events
      if (clubs.length > 0 && selectedClubs.length === 0) {
        setEvents([]);
        setLoading(false);
        return;
      }

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
      
      const processedEvents = (Array.isArray(eventsArray) ? eventsArray : []).map(event => {
        // Check if user has permission to edit this event
        const isEditable = user && (
          user.is_superuser || 
          (user.club && event.club && user.club.id === event.club.id) ||
          (user.sub_club && event.club && user.sub_club.id === event.club.id)
        );
        
        return {
          ...event,
          editable: isEditable,
          startEditable: isEditable,
          durationEditable: isEditable,
          resourceEditable: isEditable,
        };
      });

      setEvents(processedEvents);
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
      setShowEventModal(true);
    }
  };

  const handleEventSaved = () => {
    loadEvents();
    setShowEventModal(false);
    setSelectedEvent(null);
    if (calendarRef.current) {
      calendarRef.current.getApi().unselect();
    }
  };

  const handleEventDeleted = () => {
    loadEvents();
    setShowEventModal(false);
    setSelectedEvent(null);
    if (calendarRef.current) {
      calendarRef.current.getApi().unselect();
    }
  };

  const handleEventDrop = async (info) => {
    const { event, oldEvent, revert, view } = info;
    
    // Check permission
    if (!canEditEvent(event)) {
      revert();
      return;
    }

    let start = event.start;
    let end = event.end;

    // Preserve time when dragging in Month View
    if (view.type === 'dayGridMonth' && oldEvent.start) {
      const newDate = new Date(start);
      const oldDate = new Date(oldEvent.start);
      
      newDate.setHours(oldDate.getHours(), oldDate.getMinutes(), oldDate.getSeconds());
      start = newDate;

      if (oldEvent.end) {
        const duration = oldEvent.end.getTime() - oldEvent.start.getTime();
        end = new Date(start.getTime() + duration);
      } else {
        end = null;
      }
    }

    try {
      await api.patch(`/api/events/${event.id}/`, {
        start: start.toISOString(),
        end: end ? end.toISOString() : null,
      });
      
      // Reload events to reflect the correct time in the UI if we modified it
      if (view.type === 'dayGridMonth') {
        loadEvents();
      }
    } catch (error) {
      console.error('Failed to update event:', error);
      revert();
    }
  };

  const handleEventResize = async (info) => {
    const { event, revert } = info;

    // Check permission
    if (!canEditEvent(event)) {
      revert();
      return;
    }

    try {
      await api.patch(`/api/events/${event.id}/`, {
        start: event.start.toISOString(),
        end: event.end.toISOString(),
      });
    } catch (error) {
      console.error('Failed to update event:', error);
      revert();
    }
  };

  const handleModalClose = () => {
    setShowEventModal(false);
    setSelectedEvent(null);
    if (calendarRef.current) {
      calendarRef.current.getApi().unselect();
    }
  };

  const canEditEvent = (event) => {
    if (!user) return false;
    if (user.is_superuser) return true;

    // Get club from event (API object) or extendedProps (FC object)
    const eventClub = event.club || (event.extendedProps && event.extendedProps.club);
    
    if (!eventClub) return false;
    
    // Strict check matching backend:
    // If user has a sub_club, they can ONLY edit sub_club events.
    // If user has NO sub_club, they can edit main club events.
    if (user.sub_club) {
      return eventClub.id === user.sub_club.id;
    } else if (user.club) {
      return eventClub.id === user.club.id;
    }
    
    return false;
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      <Navbar />
      
      <div className="flex h-[calc(100vh-64px)] overflow-hidden">
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
          onSelectAll={() => {
            const allIds = [];
            clubs.forEach(c => {
              allIds.push(c.id);
              if (c.sub_clubs) {
                c.sub_clubs.forEach(sub => allIds.push(sub.id));
              }
            });
            setSelectedClubs(allIds);
          }}
          onDeselectAll={() => setSelectedClubs([])}
        />

        <div className="flex-1 p-4 sm:p-6 lg:p-8 overflow-y-auto bg-gray-50/50 dark:bg-[#0f172a]/50">
          <div className="bg-white/90 dark:bg-gray-900/80 backdrop-blur-xl rounded-2xl shadow-xl p-6 transition-all duration-300 border border-white/20 dark:border-gray-700/50 min-h-full flex flex-col">
            <div className="flex justify-between items-center mb-6">
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white tracking-tight">Event Calendar</h1>
              {user?.club && (
                <button
                  onClick={() => {
                    setSelectedEvent({ start: new Date(), end: new Date() });
                    setShowEventModal(true);
                  }}
                  className="bg-primary-600 text-white px-5 py-2.5 rounded-xl font-semibold hover:bg-primary-700 shadow-md hover:shadow-lg transition-all duration-200 flex items-center gap-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
                  </svg>
                  Create Event
                </button>
              )}
            </div>

            <div className="flex-1 min-h-0 bg-white/50 dark:bg-gray-800/30 rounded-xl overflow-hidden p-2 shadow-inner border border-gray-100 dark:border-gray-800/50">
              <Calendar
                ref={calendarRef}
                events={events}
                onEventClick={handleEventClick}
                onDateSelect={handleDateSelect}
                onDatesSet={loadEvents}
                onEventDrop={handleEventDrop}
                onEventResize={handleEventResize}
              />
            </div>
          </div>
        </div>
      </div>

      {showEventModal && (
        <EventModal
          event={selectedEvent}
          canEdit={selectedEvent?.id ? canEditEvent(selectedEvent) : true}
          onClose={handleModalClose}
          onSave={handleEventSaved}
          onDelete={handleEventDeleted}
        />
      )}
    </div>
  );
}
