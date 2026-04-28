import { Pill } from "lucide-react";

function MedicineCard({ medicine, explanation }) {
  return (
    <div className="medicine-card">
      <div className="medicine-title">
        <Pill size={22} />
        <h3>{medicine.medicine_name || "Unknown"}</h3>
        <span className={`confidence ${medicine.confidence || "medium"}`}>
          {medicine.confidence || "medium"}
        </span>
      </div>

      <div className="medicine-grid">
        <p>
          <strong>Type:</strong> {medicine.medicine_type || "Not mentioned"}
        </p>
        <p>
          <strong>Strength:</strong> {medicine.strength || "Not mentioned"}
        </p>
        <p>
          <strong>Dosage:</strong> {medicine.dosage || "Not mentioned"}
        </p>
        <p>
          <strong>Frequency:</strong> {medicine.frequency || "Not mentioned"}
        </p>
        <p>
          <strong>Duration:</strong> {medicine.duration || "Not mentioned"}
        </p>
        <p>
          <strong>Route:</strong> {medicine.route || "Not mentioned"}
        </p>
        <p>
          <strong>Timing:</strong> {medicine.timing || "Not mentioned"}
        </p>
        <p>
          <strong>Refills:</strong> {medicine.refills || "Not mentioned"}
        </p>
        <p>
          <strong>Instructions:</strong>{" "}
          {medicine.instructions ||
            medicine.special_instructions ||
            "Not mentioned"}
        </p>
      </div>

      {medicine.original_text && (
        <div className="original-text-box">
          <strong>Original Prescription Line:</strong>
          <p>{medicine.original_text}</p>
        </div>
      )}

      {explanation && (
        <div className="explanation-box">
          <h4>Simple Explanation</h4>
          <p>{explanation.simple_explanation}</p>
          <small>{explanation.safety_note}</small>
        </div>
      )}
    </div>
  );
}

export default MedicineCard;
