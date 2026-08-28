export default function ResultCard({ result }) {
  const ringColor =
    result.match_score >= 80
      ? "var(--seal-high)"
      : result.match_score >= 50
      ? "var(--seal-mid)"
      : "var(--seal-low)";

  return (
    <div className="result-card">
      <div className="result-header">
        <h2>{result.candidate_name || "Candidate"}</h2>
        <div
          className="score-ring"
          style={{ "--pct": result.match_score, "--ring-color": ringColor }}
        >
          <div className="score-ring-inner">
            <span className="num">{result.match_score}</span>
            <span className="denom">/ 100</span>
          </div>
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
