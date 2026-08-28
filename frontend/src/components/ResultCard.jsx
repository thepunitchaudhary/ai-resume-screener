export default function ResultCard({ result }) {
  const scoreColor =
    result.match_score >= 80 ? "#2e7d32" : result.match_score >= 50 ? "#ed6c02" : "#c62828";

  return (
    <div className="result-card">
      <div className="result-header">
        <h2>{result.candidate_name || "Candidate"}</h2>
        <div className="score-badge" style={{ backgroundColor: scoreColor }}>
          {result.match_score}/100
        </div>
      </div>

      <p className="reasoning">{result.reasoning_summary}</p>

      <div className="result-columns">
        <div>
          <h3>Strengths</h3>
          <ul>
            {result.strengths.map((point, index) => (
              <li key={index}>{point}</li>
            ))}
          </ul>
        </div>

        <div>
          <h3>Skill Gaps</h3>
          <ul>
            {result.skill_gaps.map((point, index) => (
              <li key={index}>{point}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
