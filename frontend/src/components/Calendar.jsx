import { useRef } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';

export default function Calendar({ events, onEventClick, onDateSelect, onDatesSet }) {
  const calendarRef = useRef(null);

  const calendarEvents = events.map((event) => ({
    id: event.id,
    title: event.title,
    start: event.start,
    end: event.end,
    backgroundColor: event.club.color,
    borderColor: event.club.color,
    extendedProps: {
      description: event.description,
      location: event.location,
      club: event.club,
      created_by: event.created_by,
      created_by_name: event.created_by_name,
    },
  }));

  return (
    <FullCalendar
      ref={calendarRef}
      plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
      initialView="dayGridMonth"
      headerToolbar={{
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay',
      }}
      events={calendarEvents}
      selectable={true}
      selectMirror={true}
      select={(info) => {
        if (onDateSelect && (info.view.type === 'timeGridWeek' || info.view.type === 'timeGridDay')) {
          onDateSelect(info.start, info.end);
        }
        const calendarApi = calendarRef.current.getApi();
        calendarApi.unselect();
      }}
      eventClick={(info) => {
        const event = events.find((e) => e.id === parseInt(info.event.id));
        if (event) onEventClick(event);
      }}
      dateClick={(info) => {
        const calendarApi = calendarRef.current.getApi();
        if (calendarApi.view.type === 'dayGridMonth') {
          calendarApi.changeView('timeGridDay', info.dateStr);
        }
      }}
      datesSet={(dateInfo) => {
        if (onDatesSet) {
          onDatesSet(dateInfo.start, dateInfo.end);
        }
      }}
      eventContent={(eventInfo) => (
        <div className="p-1 cursor-pointer">
          <div className="font-semibold text-xs truncate text-white">{eventInfo.event.title}</div>
          <div className="text-xs opacity-90 text-white">
            📍 {eventInfo.event.extendedProps.location}
          </div>
        </div>
      )}
      height="auto"
      slotMinTime="06:00:00"
      slotMaxTime="22:00:00"
      expandRows={true}
      stickyHeaderDates={true}
      nowIndicator={true}
    />
  );
}
