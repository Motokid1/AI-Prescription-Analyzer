import MedicineCard from "./MedicineCard";
import ScheduleTable from "./ScheduleTable";
import MissingInfoCard from "./MissingInfoCard";
import {
  FileText,
  ShieldCheck,
  UserRound,
  AlertTriangle,
  Sparkles,
} from "lucide-react";

function ResultSection({ result }) {
  if (!result) return null;

  const findExplanation = (medicineName) => {
    return result.explanations?.find(
      (item) =>
        item.medicine_name?.toLowerCase() === medicineName?.toLowerCase(),
    );
  };

  return (
    <div className="results">
      {result.prescription_summary && (
        <div className="card">
          <div className="section-title">
            <Sparkles size={22} />
            <h2>Prescription Summary</h2>
          </div>
          <p>{result.prescription_summary}</p>
        </div>
      )}

      {result.patient_details && (
        <div className="card">
          <div className="section-title">
            <UserRound size={22} />
            <h2>Patient Details</h2>
          </div>

          <div className="medicine-grid">
            <p>
              <strong>Name:</strong>{" "}
              {result.patient_details.name || "Not mentioned"}
            </p>
            <p>
              <strong>Age:</strong>{" "}
              {result.patient_details.age || "Not mentioned"}
            </p>
            <p>
              <strong>Gender:</strong>{" "}
              {result.patient_details.gender || "Not mentioned"}
            </p>
            <p>
              <strong>Date:</strong>{" "}
              {result.patient_details.date || "Not mentioned"}
            </p>
            <p>
              <strong>Doctor:</strong>{" "}
              {result.patient_details.doctor_name || "Not mentioned"}
            </p>
          </div>
        </div>
      )}

      {result.cleaned_text && (
        <div className="card cleaned-card">
          <div className="section-title">
            <Sparkles size={22} />
            <h2>Cleaned Prescription Context</h2>
          </div>

          <p className="muted">
            This is the cleaned OCR text passed to the AI extraction agent.
          </p>

          <pre className="cleaned-text">{result.cleaned_text}</pre>
        </div>
      )}

      <div className="card">
        <div className="section-title">
          <FileText size={22} />
          <h2>Raw OCR Text</h2>
        </div>

        <p className="muted">
          This is the direct text extracted from PDF/image before AI cleanup.
        </p>

        <pre className="raw-text">{result.raw_text}</pre>
      </div>

      <div className="card">
        <h2>Medicine Details</h2>

        <div className="medicine-list">
          {result.medicines?.map((medicine, index) => (
            <MedicineCard
              key={index}
              medicine={medicine}
              explanation={findExplanation(medicine.medicine_name)}
            />
          ))}
        </div>
      </div>

      {result.tests_or_advice?.length > 0 && (
        <div className="card">
          <h2>Tests / Advice</h2>
          <ul>
            {result.tests_or_advice.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {result.follow_up && (
        <div className="card">
          <h2>Follow Up</h2>
          <p>{result.follow_up}</p>
        </div>
      )}

      {result.warnings_or_unclear_parts?.length > 0 && (
        <div className="card warning-card">
          <div className="section-title">
            <AlertTriangle size={22} />
            <h2>Warnings / Unclear Parts</h2>
          </div>

          <ul>
            {result.warnings_or_unclear_parts.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      <ScheduleTable schedule={result.daily_schedule} />

      <MissingInfoCard missingInfo={result.missing_information} />

      <div className="disclaimer">
        <ShieldCheck size={20} />
        <p>{result.safety_disclaimer}</p>
      </div>
    </div>
  );
}

export default ResultSection;
