import { useState } from "react";
import Header from "../components/Header";
import UploadBox from "../components/UploadBox";
import TextInputBox from "../components/TextInputBox";
import LoadingSpinner from "../components/LoadingSpinner";
import ResultSection from "../components/ResultSection";
import { analyzePrescription } from "../api/prescriptionApi";

function PrescriptionAnalyzer() {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setError("");
    setResult(null);

    if (!file && !text.trim()) {
      setError("Please upload a prescription file or paste prescription text.");
      return;
    }

    try {
      setLoading(true);

      const data = await analyzePrescription({
        file,
        text: text.trim(),
      });

      setResult(data);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Something went wrong while analyzing the prescription.",
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setText("");
    setResult(null);
    setError("");
  };

  return (
    <main className="app-container">
      <Header />

      <section className="input-grid">
        <UploadBox file={file} setFile={setFile} />
        <TextInputBox text={text} setText={setText} />
      </section>

      {error && <div className="error-box">{error}</div>}

      <div className="action-row">
        <button onClick={handleAnalyze} disabled={loading}>
          Analyze Prescription
        </button>

        <button className="secondary-btn" onClick={handleReset}>
          Reset
        </button>
      </div>

      {loading && <LoadingSpinner />}

      <ResultSection result={result} />
    </main>
  );
}

export default PrescriptionAnalyzer;
