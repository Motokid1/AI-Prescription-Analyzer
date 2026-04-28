import { Pill, ShieldCheck } from "lucide-react";

function Header() {
  return (
    <header className="header">
      <div className="header-icon">
        <Pill size={32} />
      </div>

      <div>
        <h1>AI Prescription Analyzer</h1>
        <p>
          Upload a prescription and get a patient-friendly medicine explanation,
          dosage schedule, and safety warnings.
        </p>
      </div>

      <div className="safe-badge">
        <ShieldCheck size={18} />
        Medical Safety Mode
      </div>
    </header>
  );
}

export default Header;
