import { useEffect, useState } from "react";
import UploadForm from "./components/UploadForm.jsx";
import ResultCard from "./components/ResultCard.jsx";
import HistoryList from "./components/HistoryList.jsx";
import { screenResume, fetchScreeningHistory } from "./api.js";

export default function App() {
  const [latestResult, setLatestResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    loadHistory();
  }, []);

  async function loadHistory() {
    try {
      const items = await fetchScreeningHistory();
      setHistory(items);
    } catch {
      // History is a nice-to-have; a failed load shouldn't block the main flow.
    }
  }

  async function handleSubmit(resumeFile, jobDescription) {
    setIsSubmitting(true);
    setErrorMessage("");
    try {
      const result = await screenResume(resumeFile, jobDescription);
      setLatestResult(result);
      loadHistory();
    } catch (error) {
      const detail = error.response?.data?.detail || "Something went wrong. Please try again.";
      setErrorMessage(detail);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="app-shell">
      <header>
        <p className="eyebrow">Screening Desk / Automated Review</p>
        <h1>AI Resume Screener</h1>
        <p>Upload a resume and paste a job description to get an instant AI match score.</p>
      </header>

      <main>
        <section className="upload-section">
          <UploadForm onSubmit={handleSubmit} isSubmitting={isSubmitting} />
          {errorMessage && <p className="error-message">{errorMessage}</p>}
          {latestResult && <ResultCard result={latestResult} />}
        </section>

        <aside className="history-section">
          <h2>Recent Screenings</h2>
          <HistoryList history={history} />
        </aside>
      </main>
    </div>
  );
}
