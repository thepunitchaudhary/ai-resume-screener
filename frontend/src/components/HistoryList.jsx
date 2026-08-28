export default function HistoryList({ history }) {
  if (history.length === 0) {
    return <p className="empty-state">No screenings yet.</p>;
  }

  return (
    <ul className="history-list">
      {history.map((item) => (
        <li key={item.id}>
          <span>{item.candidate_name || item.resume_filename}</span>
          <span className="history-score">{item.match_score}/100</span>
        </li>
      ))}
    </ul>
  );
}
