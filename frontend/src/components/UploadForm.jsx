import { useState } from "react";

export default function UploadForm({ onSubmit, isSubmitting }) {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    if (!resumeFile || !jobDescription.trim()) return;
    onSubmit(resumeFile, jobDescription);
  }

  return (
    <form className="upload-form" onSubmit={handleSubmit}>
      <label className="field-label">
        Resume (PDF)
        <input
          type="file"
          accept="application/pdf"
          onChange={(event) => setResumeFile(event.target.files[0])}
        />
      </label>

      <label className="field-label">
        Job Description
        <textarea
          rows={8}
          value={jobDescription}
          onChange={(event) => setJobDescription(event.target.value)}
          placeholder="Paste the job description here..."
        />
      </label>

      <button type="submit" disabled={isSubmitting || !resumeFile}>
        {isSubmitting ? "Analyzing..." : "Screen Resume"}
      </button>
    </form>
  );
}
