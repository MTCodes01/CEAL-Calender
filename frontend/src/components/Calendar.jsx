import { useRef, forwardRef, useImperativeHandle } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';

const Calendar = forwardRef(({ events, onEventClick, onDateSelect, onDatesSet, onEventDrop, onEventResize }, ref) => {
  const calendarRef = useRef(null);

  useImperativeHandle(ref, () => ({
    getApi: () => calendarRef.current.getApi(),
  }));

  const calendarEvents = events.map((event) => ({
    id: event.id,
    title: event.title,
    start: event.start,
    end: event.end,
    backgroundColor: event.club.color,
    borderColor: event.club.color,
    editable: event.editable,
    startEditable: event.startEditable,
    durationEditable: event.durationEditable,
    resourceEditable: event.resourceEditable,
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
      dayMaxEvents={4}
      selectable={true}
      selectMirror={true}
      unselectAuto={false}
      selectOverlap={true}
      slotEventOverlap={false}
      editable={true}
      eventDrop={(info) => {
        if (onEventDrop) onEventDrop(info);
      }}
      eventResize={(info) => {
        if (onEventResize) onEventResize(info);
      }}
      select={(info) => {
        if (onDateSelect && (info.view.type === 'timeGridWeek' || info.view.type === 'timeGridDay')) {
          onDateSelect(info.start, info.end);
        }
        // Selection is now persisted until manually cleared
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
      eventContent={(eventInfo) => {
        if (eventInfo.view.type === 'dayGridMonth') {
          return (
            <div 
              className="px-2 py-0.5 rounded text-xs font-medium truncate text-white w-full text-center"
              style={{ backgroundColor: eventInfo.event.backgroundColor }}
            >
              {eventInfo.event.title}
            </div>
          );
        }
        return (
          <div className="p-1 cursor-pointer h-full flex flex-col overflow-hidden">
            <div className="flex justify-between items-start mb-0.5">
              <div className="text-xs font-bold text-white">{eventInfo.timeText}</div>
              {eventInfo.event.extendedProps.club && (
                <div className="text-[10px] bg-white/20 px-1 rounded text-white truncate max-w-[50%]">
                  {eventInfo.event.extendedProps.club.name}
                </div>
              )}
            </div>
            <div className="font-semibold text-xs truncate text-white mb-0.5">{eventInfo.event.title}</div>
            {eventInfo.event.extendedProps.location && (
              <div className="text-xs opacity-90 text-white truncate mb-0.5">
                📍 {eventInfo.event.extendedProps.location}
              </div>
            )}
            {eventInfo.event.extendedProps.description && (
              <div className="text-[10px] opacity-80 text-white truncate">
                {eventInfo.event.extendedProps.description}
              </div>
            )}
          </div>
        );
      }}
      height="auto"
      slotMinTime="00:00:00"
      slotMaxTime="24:00:00"
      slotDuration="00:30:00"
      snapDuration="00:15:00"
      dragScroll={true}
      dragRevertDuration={500}
      expandRows={true}
      stickyHeaderDates={true}
      nowIndicator={true}
    />
  );
});

export default Calendar;
