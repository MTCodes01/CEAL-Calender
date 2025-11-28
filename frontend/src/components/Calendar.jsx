import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';

export default function Calendar({ events, onEventClick, onDateClick, onDatesSet }) {
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
      plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
      initialView="dayGridMonth"
      headerToolbar={{
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay',
      }}
      events={calendarEvents}
      eventClick={(info) => {
        const event = events.find((e) => e.id === parseInt(info.event.id));
        if (event) onEventClick(event);
      }}
      dateClick={(info) => {
        if (onDateClick) onDateClick(new Date(info.date));
      }}
      datesSet={(dateInfo) => {
        if (onDatesSet) {
          onDatesSet(dateInfo.start, dateInfo.end);
        }
      }}
      eventContent={(eventInfo) => (
        <div className="p-1 cursor-pointer">
          <div className="font-semibold text-xs truncate">{eventInfo.event.title}</div>
          <div className="text-xs opacity-90">
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
