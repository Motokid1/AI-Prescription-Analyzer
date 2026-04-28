import { AlertTriangle } from "lucide-react";

function MissingInfoCard({ missingInfo }) {
  if (!missingInfo || missingInfo.length === 0) {
    return (
      <div className="success-box">
        No major missing prescription details detected.
      </div>
    );
  }

  return (
    <div className="card warning-card">
      <div className="section-title">
        <AlertTriangle size={22} />
        <h2>Missing or Unclear Information</h2>
      </div>

      {missingInfo.map((item, index) => (
        <div className="missing-item" key={index}>
          <h3>{item.medicine_name}</h3>

          <p>
            <strong>Missing Fields:</strong> {item.missing_fields.join(", ")}
          </p>

          <small>{item.warning}</small>
        </div>
      ))}
    </div>
  );
}

export default MissingInfoCard;
