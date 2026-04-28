import { CalendarClock } from "lucide-react";

function ScheduleTable({ schedule }) {
  if (!schedule || schedule.length === 0) {
    return null;
  }

  return (
    <div className="card">
      <div className="section-title">
        <CalendarClock size={22} />
        <h2>Daily Medicine Schedule</h2>
      </div>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Time</th>
              <th>Medicine</th>
              <th>Dosage</th>
              <th>Instructions</th>
            </tr>
          </thead>

          <tbody>
            {schedule.map((item, index) => (
              <tr key={index}>
                <td>{item.time}</td>
                <td>{item.medicine_name}</td>
                <td>{item.dosage || "Not mentioned"}</td>
                <td>{item.instructions || "Not mentioned"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ScheduleTable;
